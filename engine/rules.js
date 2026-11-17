/**
 * Comprehensive Fraud Detection Rule Suite
 * ========================================
 * Implements 6 state-of-the-art fraud and money mule detection algorithms:
 *  1. RAPID_PASS_THROUGH_MULE (Time-to-drain velocity)
 *  2. FAN_IN_SMURFING_AGGREGATOR (Aggregation from multiple victims)
 *  3. FAN_OUT_DISTRIBUTION (Rapid dispersal to multiple beneficiaries)
 *  4. MULTI_HOP_LAYERING (Chained laundering across >= 3 accounts)
 *  5. CIRCULAR_TRANSACTION_LOOP (Wash trading and loop detection)
 *  6. STRUCTURING_SPLIT (Sub-threshold transaction bursts)
 */

const ExplainableRiskScorer = require('./risk_scorer');

class FraudDetectionEngine {
  constructor(graphStore, options = {}) {
    this.graphStore = graphStore;
    this.accountStates = new Map(); // vpa -> AccountState
    this.alertHistory = [];
    this.alertSeq = 0;

    // Configurable thresholds
    this.config = {
      windowMs: options.windowMs || 120000, // 2-minute sliding window
      rapidDrainMaxSec: options.rapidDrainMaxSec || 120,
      rapidDrainMinRatio: options.rapidDrainMinRatio || 70.0,
      rapidDrainMinAmount: options.rapidDrainMinAmount || 5000,
      fanInMinDistinctSenders: options.fanInMinDistinctSenders || 3,
      fanOutMinDistinctReceivers: options.fanOutMinDistinctReceivers || 3,
      structuringMinCount: options.structuringMinCount || 3,
      structuringTimeWindowSec: options.structuringTimeWindowSec || 60,
      structuringMinAmount: options.structuringMinAmount || 25000,
      structuringMaxAmount: options.structuringMaxAmount || 49999,
      ...options
    };
  }

  getOrCreateState(vpa, name = '') {
    const key = String(vpa || '').toLowerCase().trim();
    if (!this.accountStates.has(key)) {
      this.accountStates.set(key, {
        vpa: key,
        name: name || key,
        recentCredits: [], // { txId, amount, fromVpa, fromName, timeMs }
        recentDebits: [], // { txId, amount, toVpa, toName, timeMs }
        drainedCreditIds: new Set(),
        smurfingAlertedAt: 0,
        dispersalAlertedAt: 0,
        structuringAlertedAt: 0,
        loopAlertedAt: 0,
        layeringAlertedAt: 0,
        alertCount: 0,
        riskScore: 0,
        isFlaggedMule: false
      });
    }
    const state = this.accountStates.get(key);
    if (name && (!state.name || state.name === key)) {
      state.name = name;
    }
    return state;
  }

  evictOldEvents(state, currentTimeMs) {
    const cutoff = currentTimeMs - this.config.windowMs;
    state.recentCredits = state.recentCredits.filter(c => c.timeMs >= cutoff);
    state.recentDebits = state.recentDebits.filter(d => d.timeMs >= cutoff);
  }

  /**
   * Evaluates an ingested transaction against all detection rules
   * @param {Object} tx Standardized transaction
   * @returns {Array<Object>} List of newly generated alerts
   */
  evaluateTransaction(tx) {
    if (tx.status !== 'SUCCESS') return [];

    const eventTimeMs = tx.time_ms || tx.stream_time_ms || Date.now();
    const senderState = this.getOrCreateState(tx.sender_vpa, tx.sender_name);
    const receiverState = this.getOrCreateState(tx.receiver_vpa, tx.receiver_name);

    this.evictOldEvents(senderState, eventTimeMs);
    this.evictOldEvents(receiverState, eventTimeMs);

    // Record Inflow to Receiver
    receiverState.recentCredits.push({
      txId: tx.transaction_id,
      amount: tx.amount,
      fromVpa: tx.sender_vpa,
      fromName: tx.sender_name,
      timeMs: eventTimeMs
    });

    // Record Outflow from Sender
    senderState.recentDebits.push({
      txId: tx.transaction_id,
      amount: tx.amount,
      toVpa: tx.receiver_vpa,
      toName: tx.receiver_name,
      timeMs: eventTimeMs
    });

    // Also update graph store
    this.graphStore.addTransaction(tx);

    const generatedAlerts = [];

    // ========================================================
    // RULE 1: RAPID_PASS_THROUGH_MULE (Time-to-Drain Velocity)
    // ========================================================
    const unconsumedCredits = senderState.recentCredits.filter(c => !senderState.drainedCreditIds.has(c.txId));
    if (unconsumedCredits.length > 0) {
      const totalInflow = unconsumedCredits.reduce((s, c) => s + c.amount, 0);
      const lastCredit = unconsumedCredits[unconsumedCredits.length - 1];
      const timeDeltaSec = Math.max(0.1, (eventTimeMs - lastCredit.timeMs) / 1000);
      const drainRatio = (tx.amount / totalInflow) * 100;

      if (timeDeltaSec <= this.config.rapidDrainMaxSec &&
          drainRatio >= this.config.rapidDrainMinRatio &&
          tx.amount >= this.config.rapidDrainMinAmount) {

        unconsumedCredits.forEach(c => senderState.drainedCreditIds.add(c.txId));
        senderState.isFlaggedMule = true;
        senderState.alertCount++;

        const riskEvaluation = ExplainableRiskScorer.calculateScore({
          ruleCode: 'RAPID_PASS_THROUGH_MULE',
          timeToDrainSec: timeDeltaSec,
          drainPercentage: drainRatio,
          amount: tx.amount,
          inDegree: senderState.recentCredits.length,
          outDegree: senderState.recentDebits.length,
          hopCount: 2,
          previousAlertCount: senderState.alertCount - 1
        });

        senderState.riskScore = Math.max(senderState.riskScore, riskEvaluation.score);
        this.graphStore.updateNodeRisk(tx.sender_vpa, riskEvaluation.score, true);

        generatedAlerts.push(this.buildAlert({
          rule_code: 'RAPID_PASS_THROUGH_MULE',
          severity: riskEvaluation.severity,
          risk_score: riskEvaluation.score,
          risk_breakdown: riskEvaluation.breakdown,
          suspect_vpa: tx.sender_vpa,
          suspect_name: senderState.name,
          source_vpa: `${lastCredit.fromName} (${lastCredit.fromVpa})`,
          target_vpa: `${tx.receiver_name} (${tx.receiver_vpa})`,
          hop_count: 2,
          time_to_drain_seconds: parseFloat(timeDeltaSec.toFixed(1)),
          drain_percentage: parseFloat(Math.min(100, drainRatio).toFixed(1)),
          amount_drained: tx.amount,
          bank: tx.bank_code,
          location: tx.location,
          details: `Drained ${Math.min(100, drainRatio).toFixed(1)}% (₹${tx.amount.toLocaleString('en-IN')}) of inbound funds within ${timeDeltaSec.toFixed(1)}s`
        }));
      }
    }

    // ========================================================
    // RULE 2: FAN_IN_SMURFING_AGGREGATOR (Multiple Victims)
    // ========================================================
    const activeSenders = new Set(receiverState.recentCredits.map(c => c.fromVpa));
    if (activeSenders.size >= this.config.fanInMinDistinctSenders &&
        (eventTimeMs - receiverState.smurfingAlertedAt > 90000)) {

      receiverState.smurfingAlertedAt = eventTimeMs;
      receiverState.isFlaggedMule = true;
      receiverState.alertCount++;
      const totalInflow = receiverState.recentCredits.reduce((s, c) => s + c.amount, 0);

      const riskEvaluation = ExplainableRiskScorer.calculateScore({
        ruleCode: 'FAN_IN_SMURFING_AGGREGATOR',
        inDegree: activeSenders.size,
        amount: totalInflow,
        previousAlertCount: receiverState.alertCount - 1
      });

      receiverState.riskScore = Math.max(receiverState.riskScore, riskEvaluation.score);
      this.graphStore.updateNodeRisk(tx.receiver_vpa, riskEvaluation.score, true);

      generatedAlerts.push(this.buildAlert({
        rule_code: 'FAN_IN_SMURFING_AGGREGATOR',
        severity: riskEvaluation.severity,
        risk_score: riskEvaluation.score,
        risk_breakdown: riskEvaluation.breakdown,
        suspect_vpa: tx.receiver_vpa,
        suspect_name: receiverState.name,
        source_vpa: `Multiple Remitters (${activeSenders.size} distinct victim accounts)`,
        target_vpa: tx.receiver_vpa,
        hop_count: 1,
        time_to_drain_seconds: 0,
        drain_percentage: 0,
        amount_drained: totalInflow,
        bank: tx.bank_code,
        location: tx.location,
        details: `Aggregated ₹${totalInflow.toLocaleString('en-IN')} from ${activeSenders.size} distinct senders within 2-minute window`
      }));
    }

    // ========================================================
    // RULE 3: FAN_OUT_DISTRIBUTION (Rapid Dispersal)
    // ========================================================
    const activeReceivers = new Set(senderState.recentDebits.map(d => d.toVpa));
    if (activeReceivers.size >= this.config.fanOutMinDistinctReceivers &&
        (eventTimeMs - senderState.dispersalAlertedAt > 90000)) {

      senderState.dispersalAlertedAt = eventTimeMs;
      senderState.isFlaggedMule = true;
      senderState.alertCount++;
      const totalDispersed = senderState.recentDebits.reduce((s, d) => s + d.amount, 0);

      const riskEvaluation = ExplainableRiskScorer.calculateScore({
        ruleCode: 'FAN_OUT_DISTRIBUTION',
        outDegree: activeReceivers.size,
        amount: totalDispersed,
        previousAlertCount: senderState.alertCount - 1
      });

      senderState.riskScore = Math.max(senderState.riskScore, riskEvaluation.score);
      this.graphStore.updateNodeRisk(tx.sender_vpa, riskEvaluation.score, true);

      generatedAlerts.push(this.buildAlert({
        rule_code: 'FAN_OUT_DISTRIBUTION',
        severity: riskEvaluation.severity,
        risk_score: riskEvaluation.score,
        risk_breakdown: riskEvaluation.breakdown,
        suspect_vpa: tx.sender_vpa,
        suspect_name: senderState.name,
        source_vpa: tx.sender_vpa,
        target_vpa: `Multiple Beneficiaries (${activeReceivers.size} distinct destinations)`,
        hop_count: 1,
        time_to_drain_seconds: 0,
        drain_percentage: 100,
        amount_drained: totalDispersed,
        bank: tx.bank_code,
        location: tx.location,
        details: `Rapidly dispersed ₹${totalDispersed.toLocaleString('en-IN')} across ${activeReceivers.size} distinct target accounts`
      }));
    }

    // ========================================================
    // RULE 4: MULTI_HOP_LAYERING (>= 3 Sequential Hops)
    // ========================================================
    // If the sender received money recently from another intermediate account that itself was credited
    const upstreamCredits = senderState.recentCredits.filter(c => c.fromVpa !== tx.receiver_vpa);
    if (upstreamCredits.length > 0) {
      for (const credit of upstreamCredits) {
        const upstreamSenderState = this.accountStates.get(credit.fromVpa);
        if (upstreamSenderState && upstreamSenderState.recentCredits.length > 0) {
          const firstInflow = upstreamSenderState.recentCredits[upstreamSenderState.recentCredits.length - 1];
          const totalChainTimeSec = (eventTimeMs - firstInflow.timeMs) / 1000;

          if (totalChainTimeSec <= 180 && (eventTimeMs - senderState.layeringAlertedAt > 60000)) {
            senderState.layeringAlertedAt = eventTimeMs;
            senderState.isFlaggedMule = true;
            senderState.alertCount++;

            const riskEvaluation = ExplainableRiskScorer.calculateScore({
              ruleCode: 'MULTI_HOP_LAYERING',
              hopCount: 3,
              timeToDrainSec: totalChainTimeSec,
              amount: tx.amount,
              previousAlertCount: senderState.alertCount - 1
            });

            senderState.riskScore = Math.max(senderState.riskScore, riskEvaluation.score);
            this.graphStore.updateNodeRisk(tx.sender_vpa, riskEvaluation.score, true);

            generatedAlerts.push(this.buildAlert({
              rule_code: 'MULTI_HOP_LAYERING',
              severity: riskEvaluation.severity,
              risk_score: riskEvaluation.score,
              risk_breakdown: riskEvaluation.breakdown,
              suspect_vpa: tx.sender_vpa,
              suspect_name: senderState.name,
              source_vpa: `${firstInflow.fromName} -> ${upstreamSenderState.name}`,
              target_vpa: `${tx.receiver_name} (${tx.receiver_vpa})`,
              hop_count: 3,
              time_to_drain_seconds: parseFloat(totalChainTimeSec.toFixed(1)),
              drain_percentage: 90,
              amount_drained: tx.amount,
              bank: tx.bank_code,
              location: tx.location,
              details: `3-Hop Layering Chain: ${firstInflow.fromVpa} -> ${credit.fromVpa} -> [${tx.sender_vpa}] -> ${tx.receiver_vpa} within ${totalChainTimeSec.toFixed(1)}s`
            }));
            break;
          }
        }
      }
    }

    // ========================================================
    // RULE 5: CIRCULAR_TRANSACTION_LOOP (Cycle Detection)
    // ========================================================
    if (eventTimeMs - senderState.loopAlertedAt > 60000) {
      const cycle = this.graphStore.findCycle(tx.sender_vpa, 4);
      if (cycle && cycle.length >= 3) {
        senderState.loopAlertedAt = eventTimeMs;
        senderState.isFlaggedMule = true;
        senderState.alertCount++;

        const riskEvaluation = ExplainableRiskScorer.calculateScore({
          ruleCode: 'CIRCULAR_TRANSACTION_LOOP',
          isCycle: true,
          hopCount: cycle.length - 1,
          amount: tx.amount,
          previousAlertCount: senderState.alertCount - 1
        });

        senderState.riskScore = Math.max(senderState.riskScore, riskEvaluation.score);
        this.graphStore.updateNodeRisk(tx.sender_vpa, riskEvaluation.score, true);

        generatedAlerts.push(this.buildAlert({
          rule_code: 'CIRCULAR_TRANSACTION_LOOP',
          severity: riskEvaluation.severity,
          risk_score: riskEvaluation.score,
          risk_breakdown: riskEvaluation.breakdown,
          suspect_vpa: tx.sender_vpa,
          suspect_name: senderState.name,
          source_vpa: cycle[0],
          target_vpa: cycle[cycle.length - 1],
          hop_count: cycle.length - 1,
          time_to_drain_seconds: 0,
          drain_percentage: 100,
          amount_drained: tx.amount,
          bank: tx.bank_code,
          location: tx.location,
          details: `Circular Money Loop: ${cycle.join(' -> ')}`
        }));
      }
    }

    // ========================================================
    // RULE 6: STRUCTURING_SPLIT (Sub-threshold Bursts)
    // ========================================================
    if (tx.amount >= this.config.structuringMinAmount && tx.amount <= this.config.structuringMaxAmount) {
      const recentSplits = senderState.recentDebits.filter(d =>
        d.amount >= this.config.structuringMinAmount &&
        d.amount <= this.config.structuringMaxAmount &&
        (eventTimeMs - d.timeMs) <= (this.config.structuringTimeWindowSec * 1000)
      );

      if (recentSplits.length >= this.config.structuringMinCount &&
          (eventTimeMs - senderState.structuringAlertedAt > 60000)) {

        senderState.structuringAlertedAt = eventTimeMs;
        senderState.isFlaggedMule = true;
        senderState.alertCount++;
        const totalSplitAmount = recentSplits.reduce((s, d) => s + d.amount, 0);

        const riskEvaluation = ExplainableRiskScorer.calculateScore({
          ruleCode: 'STRUCTURING_SPLIT',
          amount: totalSplitAmount,
          outDegree: recentSplits.length,
          previousAlertCount: senderState.alertCount - 1
        });

        senderState.riskScore = Math.max(senderState.riskScore, riskEvaluation.score);
        this.graphStore.updateNodeRisk(tx.sender_vpa, riskEvaluation.score, true);

        generatedAlerts.push(this.buildAlert({
          rule_code: 'STRUCTURING_SPLIT',
          severity: riskEvaluation.severity,
          risk_score: riskEvaluation.score,
          risk_breakdown: riskEvaluation.breakdown,
          suspect_vpa: tx.sender_vpa,
          suspect_name: senderState.name,
          source_vpa: tx.sender_vpa,
          target_vpa: tx.receiver_vpa,
          hop_count: 1,
          time_to_drain_seconds: 0,
          drain_percentage: 100,
          amount_drained: totalSplitAmount,
          bank: tx.bank_code,
          location: tx.location,
          details: `Detected ${recentSplits.length} structured transactions totaling ₹${totalSplitAmount.toLocaleString('en-IN')} just under reporting threshold within 60s`
        }));
      }
    }

    // Cache alerts
    generatedAlerts.forEach(a => {
      this.alertHistory.unshift(a);
      if (this.alertHistory.length > 500) this.alertHistory.pop();
    });

    return generatedAlerts;
  }

  buildAlert(payload) {
    this.alertSeq++;
    const now = new Date();
    return {
      alert_id: `ALT-${String(this.alertSeq).padStart(4, '0')}-${now.getTime().toString().slice(-5)}`,
      alert_time: now.toLocaleTimeString('en-IN', { hour12: false }),
      alert_timestamp: now.toISOString(),
      status: 'NEW',
      ...payload
    };
  }

  getAccountState(vpa) {
    const key = String(vpa || '').toLowerCase().trim();
    return this.accountStates.get(key) || null;
  }

  getAllFlaggedMules() {
    return Array.from(this.accountStates.values()).filter(s => s.isFlaggedMule);
  }

  reset() {
    this.accountStates.clear();
    this.alertHistory = [];
    this.alertSeq = 0;
  }
}

module.exports = FraudDetectionEngine;
