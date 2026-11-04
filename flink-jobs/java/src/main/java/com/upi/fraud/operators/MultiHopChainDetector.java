package com.upi.fraud.operators;

import com.upi.fraud.model.TransactionEvent;
import org.apache.flink.cep.pattern.Pattern;
import org.apache.flink.cep.pattern.conditions.IterativeCondition;
import org.apache.flink.cep.pattern.conditions.SimpleCondition;
import org.apache.flink.streaming.api.windowing.time.Time;

/**
 * Flink CEP Pattern: Multi-Hop Money Mule Chain Tracking (Hop 1 -> Hop 2 within 30s)
 */
public class MultiHopChainDetector {

    public static Pattern<TransactionEvent, ?> getMultiHopPattern() {
        return Pattern.<TransactionEvent>begin("hop1")
            .where(new SimpleCondition<TransactionEvent>() {
                @Override
                public boolean filter(TransactionEvent tx) {
                    return tx.amount >= 10000.0;
                }
            })
            .followedBy("hop2")
            .where(new IterativeCondition<TransactionEvent>() {
                @Override
                public boolean filter(TransactionEvent hop2, Context<TransactionEvent> ctx) throws Exception {
                    TransactionEvent hop1 = ctx.getEventsForPattern("hop1").iterator().next();
                    // Check if Hop 2's remitter is Hop 1's beneficiary and transfers >= 80%
                    return hop2.remitterAccount.equals(hop1.beneficiaryAccount)
                        && hop2.amount >= (hop1.amount * 0.80);
                }
            })
            .within(Time.seconds(30));
    }
}

