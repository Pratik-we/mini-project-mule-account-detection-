package com.upi.fraud;

import com.upi.fraud.model.MuleAlert;
import com.upi.fraud.model.TransactionEvent;
import com.upi.fraud.operators.RapidPassThroughDetector;
import org.apache.flink.api.common.eventtime.WatermarkStrategy;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;

import java.time.Duration;

/**
 * Main Apache Flink Streaming Fraud Detection Pipeline Entry Point
 */
public class FraudDetectionJob {

    public static void main(String[] args) throws Exception {
        final StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

        // Checkpointing configuration for fault tolerance
        env.enableCheckpointing(5000);
        env.getCheckpointConfig().setMinPauseBetweenCheckpoints(2000);

        // Watermark Strategy: Handles up to 5 seconds of out-of-order UPI transactions
        WatermarkStrategy<TransactionEvent> watermarkStrategy = WatermarkStrategy
            .<TransactionEvent>forBoundedOutOfOrderness(Duration.ofSeconds(5))
            .withTimestampAssigner((event, timestamp) -> event.eventTimeEpochMs);

        System.out.println("Flink Fraud Detection Job Initialized.");
        // DataStream<TransactionEvent> txStream = env.fromSource(kafkaSource, watermarkStrategy, "KafkaRawSource");
        // txStream.keyBy(tx -> tx.beneficiaryAccount).process(new RapidPassThroughDetector()).sinkTo(kafkaAlertSink);

        env.execute("UPI Real-Time Mule Stream Detector");
    }
}

