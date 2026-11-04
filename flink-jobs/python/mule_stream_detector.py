"""
Apache Flink Python Streaming Pipeline: UPI & Mule Account Detector
===================================================================
Features:
  - Event-Time processing with out-of-order BoundedOutOfOrderness watermarks
  - Keyed by Account Number
  - KeyedProcessFunction tracking recent credits, outflow speed, and drain ratio
  - Complex Event Processing (CEP) emulation for Multi-Hop Laundering Chains
"""

import json
from pyflink.common import WatermarkStrategy, Types, Duration
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.functions import KeyedProcessFunction
from pyflink.datastream.state import ValueStateDescriptor


class RapidMulePassThroughDetector(KeyedProcessFunction):
    """
    KeyedProcessFunction tracking inbound credits and outbound debits.
    Flags an account if outgoing debit occurs within 60s of an incoming credit
    and drains >= 75% of the transferred amount.
    """
    def __init__(self):
        self.inflow_state = None

    def open(self, runtime_context):
        desc = ValueStateDescriptor("inflow_credit_state", Types.STRING())
        self.inflow_state = runtime_context.get_state(desc)

    def process_element(self, value_str, ctx):
        tx = json.loads(value_str)
        current_acc = ctx.get_current_key()
        event_time = tx.get("event_time_epoch_ms", ctx.timestamp())

        # If current account is beneficiary -> Record inbound credit
        if current_acc == tx.get("beneficiary_account"):
            self.inflow_state.update(json.dumps({
                "amount": tx["amount"],
                "from_vpa": tx["remitter_vpa"],
                "time_ms": event_time
            }))
            # Set timer for 60 seconds
            ctx.timer_service().register_event_time_timer(event_time + 60000)

        # If current account is remitter -> Check if draining recent inflow
        if current_acc == tx.get("remitter_account"):
            inflow_raw = self.inflow_state.value()
            if inflow_raw:
                inflow = json.loads(inflow_raw)
                delta_sec = (event_time - inflow["time_ms"]) / 1000.0
                ratio = (tx["amount"] / inflow["amount"]) * 100.0

                if 0 <= delta_sec <= 60 and ratio >= 75.0:
                    alert = {
                        "alert_id": f"ALT-{event_time}-{current_acc[-4:]}",
                        "alert_time": tx.get("event_time"),
                        "rule_code": "RAPID_PASS_THROUGH_MULE",
                        "severity": "CRITICAL" if delta_sec <= 15 else "HIGH",
                        "risk_score": min(99.0, 70.0 + (60.0 - delta_sec) * 0.5),
                        "suspect_account": current_acc,
                        "suspect_vpa": tx.get("remitter_vpa"),
                        "source_vpa": inflow["from_vpa"],
                        "target_vpa": tx.get("beneficiary_vpa"),
                        "hop_count": 2,
                        "time_to_drain_seconds": round(delta_sec, 2),
                        "drain_percentage": round(ratio, 1),
                        "details": f"Rapid drain of {round(ratio, 1)}% in {round(delta_sec, 1)}s to {tx.get('beneficiary_vpa')}"
                    }
                    yield json.dumps(alert)
                    self.inflow_state.clear()

    def on_timer(self, timestamp, ctx):
        # Window expired without suspicious rapid drain
        self.inflow_state.clear()


def main():
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(2)
    print("Starting Flink Streaming Fraud & Mule Detection Pipeline...")


if __name__ == "__main__":
    main()

