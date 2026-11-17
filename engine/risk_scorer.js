/**
 * Explainable Multi-Signal Risk Scoring Engine
 * ============================================
 * Calculates a normalized risk score between 0 and 100 with clear,
 * transparent, and mathematically justified signal contributions.
 */

class ExplainableRiskScorer {
  /**
   * Evaluates composite risk score and produces human-readable evidence.
   * @param {Object} params
   * @param {string} params.ruleCode
   * @param {number} [params.timeToDrainSec]
   * @param {number} [params.drainPercentage]
   * @param {number} [params.inDegree]
   * @param {number} [params.outDegree]
   * @param {number} [params.amount]
   * @param {number} [params.hopCount]
   * @param {boolean} [params.isCycle]
   * @param {boolean} [params.isQuarantined]
   * @param {number} [params.previousAlertCount]
   * @returns {{ score: number, severity: string, breakdown: Array<{ signal: string, points: number, weight: string, description: string }> }}
   */
  static calculateScore(params) {
    const breakdown = [];
    let baseScore = 40; // Base threshold for an triggered rule

    breakdown.push({
      signal: 'RULE_TRIGGER_BASE',
      points: baseScore,
      weight: 'Base',
      description: `Baseline rule invocation for ${params.ruleCode}`
    });

    // 1. Velocity Signal (Weight: up to +25 points)
    if (params.timeToDrainSec !== undefined && params.timeToDrainSec >= 0) {
      let velocityPoints = 0;
      let desc = '';
      if (params.timeToDrainSec <= 10) {
        velocityPoints = 25;
        desc = `Ultra-rapid velocity: funds drained in ${params.timeToDrainSec.toFixed(1)}s (≤ 10s)`;
      } else if (params.timeToDrainSec <= 30) {
        velocityPoints = 20;
        desc = `High velocity: funds drained in ${params.timeToDrainSec.toFixed(1)}s (≤ 30s)`;
      } else if (params.timeToDrainSec <= 60) {
        velocityPoints = 15;
        desc = `Elevated velocity: funds drained in ${params.timeToDrainSec.toFixed(1)}s (≤ 60s)`;
      } else if (params.timeToDrainSec <= 120) {
        velocityPoints = 10;
        desc = `Moderate velocity: funds drained in ${params.timeToDrainSec.toFixed(1)}s (≤ 120s)`;
      }

      if (velocityPoints > 0) {
        breakdown.push({
          signal: 'VELOCITY_PENALTY',
          points: velocityPoints,
          weight: '25%',
          description: desc
        });
      }
    }

    // 2. Drain Percentage Signal (Weight: up to +20 points)
    if (params.drainPercentage !== undefined && params.drainPercentage > 0) {
      let drainPoints = 0;
      let desc = '';
      if (params.drainPercentage >= 95) {
        drainPoints = 20;
        desc = `Complete liquidation: ${params.drainPercentage.toFixed(1)}% drained (≥ 95%)`;
      } else if (params.drainPercentage >= 85) {
        drainPoints = 15;
        desc = `Severe liquidation: ${params.drainPercentage.toFixed(1)}% drained (≥ 85%)`;
      } else if (params.drainPercentage >= 70) {
        drainPoints = 10;
        desc = `Substantial liquidation: ${params.drainPercentage.toFixed(1)}% drained (≥ 70%)`;
      }

      if (drainPoints > 0) {
        breakdown.push({
          signal: 'DRAIN_RATIO_WEIGHT',
          points: drainPoints,
          weight: '20%',
          description: desc
        });
      }
    }

    // 3. Network Degree & Smurfing/Dispersal Signal (Weight: up to +20 points)
    const fanDegree = Math.max(params.inDegree || 0, params.outDegree || 0);
    if (fanDegree >= 3) {
      let degreePoints = 0;
      let desc = '';
      if (fanDegree >= 6) {
        degreePoints = 20;
        desc = `High network cardinality: ${fanDegree} counter-parties connected`;
      } else if (fanDegree >= 4) {
        degreePoints = 15;
        desc = `Elevated network cardinality: ${fanDegree} counter-parties connected`;
      } else {
        degreePoints = 10;
        desc = `Multi-party fan pattern: ${fanDegree} counter-parties connected`;
      }

      breakdown.push({
        signal: 'NETWORK_CENTRALITY',
        points: degreePoints,
        weight: '20%',
        description: desc
      });
    }

    // 4. Multi-Hop Layering / Cycle Topology Signal (Weight: up to +15 points)
    if (params.hopCount && params.hopCount >= 3) {
      const hopPoints = Math.min(15, (params.hopCount - 1) * 5);
      breakdown.push({
        signal: 'MULTI_HOP_LAYERING',
        points: hopPoints,
        weight: '15%',
        description: `Deep layering detected across ${params.hopCount} successive hops`
      });
    }

    if (params.isCycle) {
      breakdown.push({
        signal: 'CIRCULAR_LOOP_DETECTED',
        points: 15,
        weight: '15%',
        description: 'Circular money flow detected: funds looped back to originating entity'
      });
    }

    // 5. Value Anomaly Signal (Weight: up to +10 points)
    if (params.amount && params.amount >= 50000) {
      let valPoints = 5;
      if (params.amount >= 100000) valPoints = 10;
      breakdown.push({
        signal: 'HIGH_VALUE_EXPOSURE',
        points: valPoints,
        weight: '10%',
        description: `High financial volume: ₹${params.amount.toLocaleString('en-IN')}`
      });
    }

    // 6. Historical Repeat / Quarantine Multiplier
    if (params.previousAlertCount && params.previousAlertCount > 0) {
      const histPoints = Math.min(10, params.previousAlertCount * 3);
      breakdown.push({
        signal: 'RECIDIVISM_HISTORY',
        points: histPoints,
        weight: '10%',
        description: `Account has ${params.previousAlertCount} previous fraud alert(s)`
      });
    }

    if (params.isQuarantined) {
      breakdown.push({
        signal: 'QUARANTINE_OVERRIDE',
        points: 10,
        weight: 'Critical',
        description: 'Account is actively quarantined under analyst surveillance'
      });
    }

    // Aggregate score
    let totalScore = breakdown.reduce((sum, item) => sum + item.points, 0);
    totalScore = Math.min(99, Math.max(1, Math.round(totalScore)));

    // Categorize Severity
    let severity = 'LOW';
    if (totalScore >= 85) {
      severity = 'CRITICAL';
    } else if (totalScore >= 70) {
      severity = 'HIGH';
    } else if (totalScore >= 50) {
      severity = 'MEDIUM';
    }

    return {
      score: totalScore,
      severity,
      breakdown
    };
  }
}

module.exports = ExplainableRiskScorer;
