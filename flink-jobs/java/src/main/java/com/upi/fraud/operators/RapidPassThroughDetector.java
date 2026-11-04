package com.upi.fraud.operators;

import com.upi.fraud.model.MuleAlert;
import com.upi.fraud.model.TransactionEvent;
import org.apache.flink.api.common.state.ValueState;
import org.apache.flink.api.common.state.ValueStateDescriptor;
import org.apache.flink.configuration.Configuration;
import org.apache.flink.streaming.api.functions.KeyedProcessFunction;
import org.apache.flink.util.Collector;

import java.io.Serializable;
import java.time.Instant;
import java.util.UUID;

/**
 * Stateful KeyedProcessFunction: Detects Rapid In-to-Out Drains (Time-to-Drain < 60s)
 */
public class RapidPassThroughDetector 
    extends KeyedProcessFunction<String, TransactionEvent, MuleAlert> {

    private static final long serialVersionUID = 1L;

    public static class InflowRecord implements Serializable {
        private static final long serialVersionUID = 1L;
        public double amount;
        public long timeMs;
        public String sourceVpa;

        public InflowRecord() {}

        public InflowRecord(double amount, long timeMs, String sourceVpa) {
            this.amount = amount;
            this.timeMs = timeMs;
            this.sourceVpa = sourceVpa;
        }
    }

    private transient ValueState<InflowRecord> lastInflowState;

    @Override
    public void open(Configuration parameters) {
        ValueStateDescriptor<InflowRecord> descriptor = 
            new ValueStateDescriptor<>("inflow-state", InflowRecord.class);
        lastInflowState = getRuntimeContext().getState(descriptor);
    }

    @Override
    public void processElement(TransactionEvent tx, Context ctx, Collector<MuleAlert> out) throws Exception {
        String currentAccount = ctx.getCurrentKey();

        // 1. Account receives funds (Inflow)
        if (currentAccount.equals(tx.beneficiaryAccount)) {
            lastInflowState.update(new InflowRecord(tx.amount, tx.eventTimeEpochMs, tx.remitterVpa));
            ctx.timerService().registerEventTimeTimer(tx.eventTimeEpochMs + 60000L); // 60-second window
        }

        // 2. Account sends funds out (Outflow)
        if (currentAccount.equals(tx.remitterAccount)) {
            InflowRecord record = lastInflowState.value();
            if (record != null) {
                double deltaSec = (tx.eventTimeEpochMs - record.timeMs) / 1000.0;
                double ratio = (tx.amount / record.amount) * 100.0;

                // Threshold: Outflow within 60s draining >= 75% of inflow
                if (deltaSec >= 0 && deltaSec <= 60 && ratio >= 75.0) {
                    double riskScore = Math.min(100.0, 70.0 + (60.0 - deltaSec) * 0.5);
                    String severity = deltaSec <= 15 ? "CRITICAL" : "HIGH";

                    MuleAlert alert = new MuleAlert(
                        "ALT-" + UUID.randomUUID().toString().substring(0, 8).toUpperCase(),
                        Instant.ofEpochMilli(tx.eventTimeEpochMs).toString(),
                        "RAPID_PASS_THROUGH_MULE",
                        severity,
                        riskScore,
                        currentAccount,
                        tx.remitterVpa,
                        record.sourceVpa,
                        tx.beneficiaryVpa,
                        2,
                        deltaSec,
                        ratio,
                        String.format("Drained %.1f%% of received funds in %.1fs to %s", ratio, deltaSec, tx.beneficiaryVpa)
                    );

                    out.collect(alert);
                    lastInflowState.clear();
                }
            }
        }
    }

    @Override
    public void onTimer(long timestamp, OnTimerContext ctx, Collector<MuleAlert> out) throws Exception {
        lastInflowState.clear();
    }
}

