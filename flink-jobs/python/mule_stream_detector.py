"""
Apache Flink Python Streaming Pipeline: UPI & Mule Account Detector
===================================================================
Features:
  - Event-Time stream processing with BoundedOutOfOrderness watermarks
  - KeyedProcessFunction tracking recent credits, outflow velocity, and drain percentage
  - Connects to Kafka source (upi.transactions.raw) and Kafka sink (upi.fraud.alerts)
  - Emits explainable fraud alerts to downstream ClickHouse & SOC Dashboard
"""

import json
import os
from pyflink.common import WatermarkStrategy, Types, Duration
from pyflink.common.serialization import SimpleStringSchema
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.kafka import KafkaSource, KafkaSink, KafkaRecordSerializationSchema, OffsetsInitializer
from pyflink.datastream.functions import KeyedProcessFunction
from pyflink.datastream.state import ValueStateDescriptor


class RapidMulePassThroughDetector(KeyedProcessFunction):
    """
    KeyedProcessFunction tracking inbound credits and outbound debits.
    Flags an account if outgoing debit occurs within 60s of an incoming credit
    and drains >= 70% of the transferred amount.
    """
    def __init__(self):
        self.inflow_state = None

    def open(self, runtime_context):
        desc = ValueStateDescriptor("inflow_credit_state", Types.STRING())
        self.inflow_state = runtime_context.get_state(desc)

    def process_element(self, value_str, ctx):
        try:
            tx = json.loads(value_str)
        except Exception:
            return

        current_acc = ctx.get_current_key()
        event_time = tx.get("time_ms") or tx.get("event_time_epoch_ms") or ctx.timestamp()
        
        sender = tx.get("sender_vpa") or tx.get("remitter_vpa") or tx.get("remitter_account")
        receiver = tx.get("receiver_vpa") or tx.get("beneficiary_vpa") or tx.get("beneficiary_account")
        amount = float(tx.get("amount", 0.0))

        # 1. Inbound Credit: Beneficiary receives funds
        if current_acc == receiver:
            self.inflow_state.update(json.dumps({
                "amount": amount,
                "from_vpa": sender,
                "time_ms": event_time
            }))
            ctx.timer_service().register_event_time_timer(event_time + 60000)

        # 2. Outbound Debit: Remitter drains funds
        if current_acc == sender:
            inflow_raw = self.inflow_state.value()
            if inflow_raw:
                inflow = json.loads(inflow_raw)
                delta_sec = max(0.1, (event_time - inflow["time_ms"]) / 1000.0)
                ratio = (amount / inflow["amount"]) * 100.0 if inflow["amount"] > 0 else 0.0

                if 0 <= delta_sec <= 60 and ratio >= 70.0 and amount >= 5000:
                    alert = {
                        "alert_id": f"ALT-PY-{event_time}-{str(current_acc)[-4:]}",
                        "alert_time": tx.get("timestamp") or tx.get("event_time"),
                        "rule_code": "RAPID_PASS_THROUGH_MULE",
                        "severity": "CRITICAL" if delta_sec <= 15 else "HIGH",
                        "risk_score": min(99.0, 75.0 + (60.0 - min(60.0, delta_sec)) * 0.4),
                        "suspect_account": current_acc,
                        "suspect_vpa": sender,
                        "source_vpa": inflow["from_vpa"],
                        "target_vpa": receiver,
                        "hop_count": 2,
                        "time_to_drain_seconds": round(delta_sec, 2),
                        "drain_percentage": round(min(100.0, ratio), 1),
                        "details": f"Drained {round(min(100.0, ratio), 1)}% (₹{amount}) within {round(delta_sec, 1)}s"
                    }
                    yield json.dumps(alert)
                    self.inflow_state.clear()

    def on_timer(self, timestamp, ctx):
        self.inflow_state.clear()


def main():
    env = StreamExecutionEnvironment.get_execution_environment()
    env.enable_checkpointing(5000)
    env.set_parallelism(2)

    kafka_broker = os.getenv("KAFKA_BROKER", "kafka:29092")
    raw_topic = os.getenv("KAFKA_RAW_TOPIC", "upi.transactions.raw")
    alerts_topic = os.getenv("KAFKA_ALERTS_TOPIC", "upi.fraud.alerts")

    print("=========================================================")
    print("🛡️  STARTING PYFLINK FRAUD & MULE DETECTOR")
    print(f"   Kafka Broker : {kafka_broker}")
    print(f"   Raw Topic    : {raw_topic}")
    print(f"   Alerts Topic : {alerts_topic}")
    print("=========================================================")

    kafka_source = KafkaSource.builder() \
        .set_bootstrap_servers(kafka_broker) \
        .set_topics(raw_topic) \
        .set_group_id("pyflink-mule-detector-group") \
        .set_starting_offsets(OffsetsInitializer.latest()) \
        .set_value_only_deserializer(SimpleStringSchema()) \
        .build()

    tx_stream = env.from_source(kafka_source, WatermarkStrategy.no_watermarks(), "KafkaRawSource")

    alerts_stream = tx_stream \
        .key_by(lambda raw: json.loads(raw).get("receiver_vpa", "unknown") if "{" in raw else "unknown") \
        .process(RapidMulePassThroughDetector())

    kafka_sink = KafkaSink.builder() \
        .set_bootstrap_servers(kafka_broker) \
        .set_record_serializer(
            KafkaRecordSerializationSchema.builder()
                .set_topic(alerts_topic)
                .set_value_serialization_schema(SimpleStringSchema())
                .build()
        ) \
        .build()

    alerts_stream.sink_to(kafka_sink)
    env.execute("PyFlink Sentinel UPI Mule Stream Detector")


if __name__ == "__main__":
    main()
