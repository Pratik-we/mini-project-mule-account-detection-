package com.upi.fraud;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.upi.fraud.model.MuleAlert;
import com.upi.fraud.model.TransactionEvent;
import com.upi.fraud.operators.MultiHopChainDetector;
import com.upi.fraud.operators.RapidPassThroughDetector;
import org.apache.flink.api.common.eventtime.WatermarkStrategy;
import org.apache.flink.api.common.serialization.SimpleStringSchema;
import org.apache.flink.cep.CEP;
import org.apache.flink.cep.PatternSelectFunction;
import org.apache.flink.cep.PatternStream;
import org.apache.flink.cep.pattern.Pattern;
import org.apache.flink.connector.kafka.sink.KafkaRecordSerializationSchema;
import org.apache.flink.connector.kafka.sink.KafkaSink;
import org.apache.flink.connector.kafka.source.KafkaSource;
import org.apache.flink.connector.kafka.source.enumerator.initializer.OffsetsInitializer;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.datastream.SingleOutputStreamOperator;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;

import java.time.Duration;
import java.time.Instant;
import java.util.List;
import java.util.Map;
import java.util.UUID;

/**
 * Production-Grade Apache Flink 1.17 Real-Time Fraud & Mule Detection Pipeline
 * ============================================================================
 * Consumes raw UPI transactions from Kafka topic 'upi.transactions.raw',
 * assigns bounded out-of-orderness watermarks, evaluates stateful CEP rules
 * (Rapid Pass-Through and Multi-Hop Layering Chains), and streams alerts to 'upi.fraud.alerts'.
 */
public class FraudDetectionJob {

    private static final String DEFAULT_KAFKA_BROKER = "kafka:29092";
    private static final String DEFAULT_RAW_TOPIC = "upi.transactions.raw";
    private static final String DEFAULT_ALERTS_TOPIC = "upi.fraud.alerts";

    public static void main(String[] args) throws Exception {
        final StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

        // 1. Fault Tolerance & Checkpointing
        env.enableCheckpointing(5000);
        env.getCheckpointConfig().setMinPauseBetweenCheckpoints(2000);
        env.getCheckpointConfig().setCheckpointTimeout(60000);

        String kafkaBroker = System.getenv().getOrDefault("KAFKA_BROKER", DEFAULT_KAFKA_BROKER);
        String rawTopic = System.getenv().getOrDefault("KAFKA_RAW_TOPIC", DEFAULT_RAW_TOPIC);
        String alertsTopic = System.getenv().getOrDefault("KAFKA_ALERTS_TOPIC", DEFAULT_ALERTS_TOPIC);

        System.out.println("=========================================================");
        System.out.println("🛡️  INITIALIZING APACHE FLINK FRAUD & MULE DETECTOR");
        System.out.println("   Kafka Broker : " + kafkaBroker);
        System.out.println("   Source Topic : " + rawTopic);
        System.out.println("   Alerts Topic : " + alertsTopic);
        System.out.println("=========================================================");

        // 2. Kafka Source Configuration
        KafkaSource<String> kafkaSource = KafkaSource.<String>builder()
                .setBootstrapServers(kafkaBroker)
                .setTopics(rawTopic)
                .setGroupId("flink-upi-fraud-detector-group")
                .setStartingOffsets(OffsetsInitializer.latest())
                .setValueOnlyDeserializer(new SimpleStringSchema())
                .build();

        // 3. Watermark Strategy (Bounded Out-Of-Orderness of 5 seconds)
        WatermarkStrategy<TransactionEvent> watermarkStrategy = WatermarkStrategy
                .<TransactionEvent>forBoundedOutOfOrderness(Duration.ofSeconds(5))
                .withTimestampAssigner((event, timestamp) -> event.eventTimeEpochMs);

        // 4. Ingest and Parse JSON Stream
        ObjectMapper objectMapper = new ObjectMapper();
        DataStream<TransactionEvent> txStream = env.fromSource(kafkaSource, WatermarkStrategy.noWatermarks(), "KafkaRawTxSource")
                .map(jsonStr -> {
                    try {
                        return objectMapper.readValue(jsonStr, TransactionEvent.class);
                    } catch (Exception e) {
                        return null;
                    }
                })
                .filter(tx -> tx != null && "SUCCESS".equalsIgnoreCase(tx.status))
                .assignTimestampsAndWatermarks(watermarkStrategy);

        // 5. Detection Rule 1: Rapid In-to-Out Pass-Through Mule
        SingleOutputStreamOperator<MuleAlert> passThroughAlerts = txStream
                .keyBy(tx -> tx.beneficiaryAccount != null ? tx.beneficiaryAccount : tx.beneficiaryVpa)
                .process(new RapidPassThroughDetector())
                .name("RapidPassThroughOperator");

        // 6. Detection Rule 2: Multi-Hop Layering CEP Pattern Matching
        Pattern<TransactionEvent, ?> multiHopPattern = MultiHopChainDetector.getMultiHopPattern();
        PatternStream<TransactionEvent> patternStream = CEP.pattern(txStream, multiHopPattern);

        SingleOutputStreamOperator<MuleAlert> multiHopAlerts = patternStream.select(
                (PatternSelectFunction<TransactionEvent, MuleAlert>) (Map<String, List<TransactionEvent>> pattern) -> {
                    TransactionEvent hop1 = pattern.get("hop1").get(0);
                    TransactionEvent hop2 = pattern.get("hop2").get(0);

                    double deltaSec = Math.max(0.1, (hop2.eventTimeEpochMs - hop1.eventTimeEpochMs) / 1000.0);
                    double ratio = (hop2.amount / hop1.amount) * 100.0;

                    return new MuleAlert(
                            "ALT-CEP-" + UUID.randomUUID().toString().substring(0, 8).toUpperCase(),
                            Instant.ofEpochMilli(hop2.eventTimeEpochMs).toString(),
                            "MULTI_HOP_LAYERING",
                            deltaSec <= 15 ? "CRITICAL" : "HIGH",
                            Math.min(99.0, 75.0 + (30.0 - Math.min(30.0, deltaSec))),
                            hop1.beneficiaryAccount,
                            hop1.beneficiaryVpa,
                            hop1.remitterVpa,
                            hop2.beneficiaryVpa,
                            2,
                            deltaSec,
                            ratio,
                            String.format("Multi-Hop Layering: %s transferred ₹%.2f to %s within %.1fs",
                                    hop1.remitterVpa, hop2.amount, hop2.beneficiaryVpa, deltaSec)
                    );
                }
        ).name("MultiHopCEPOperator");

        // 7. Merge Alerts
        DataStream<MuleAlert> unifiedAlerts = passThroughAlerts.union(multiHopAlerts);

        // 8. Kafka Sink Configuration for Emitting Alerts
        KafkaSink<String> kafkaAlertSink = KafkaSink.<String>builder()
                .setBootstrapServers(kafkaBroker)
                .setRecordSerializer(
                        KafkaRecordSerializationSchema.builder()
                                .setTopic(alertsTopic)
                                .setValueSerializationSchema(new SimpleStringSchema())
                                .build()
                )
                .build();

        unifiedAlerts
                .map(objectMapper::writeValueAsString)
                .sinkTo(kafkaAlertSink)
                .name("KafkaAlertSink");

        env.execute("Sentinel Real-Time UPI Fraud & Mule Stream Sentinel");
    }
}
