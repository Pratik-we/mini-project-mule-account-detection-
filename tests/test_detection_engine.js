/**
 * Automated Verification Suite for Fraud Engine, Risk Scorer & Graph Store
 * =========================================================================
 * Tests all 6 detection rules, risk scoring explainability, graph algorithms,
 * and case management lifecycles.
 */

const assert = require('assert');
const GraphStore = require('../engine/graph_store');
const FraudDetectionEngine = require('../engine/rules');
const ExplainableRiskScorer = require('../engine/risk_scorer');
const CaseManager = require('../engine/case_manager');

let totalTests = 0;
let passedTests = 0;

function runTest(name, fn) {
  totalTests++;
  try {
    fn();
    console.log(`  ✅ PASS: ${name}`);
    passedTests++;
  } catch (err) {
    console.error(`  ❌ FAIL: ${name}`);
    console.error(`     Error: ${err.message}`);
  }
}

console.log(`\n========================================================`);
console.log(`🧪 RUNNING SENTINEL FRAUD INTELLIGENCE TEST SUITE`);
console.log(`========================================================\n`);

// ----------------------------------------------------
// Test 1: Explainable Risk Scorer
// ----------------------------------------------------
runTest('Risk Scorer: Calculates critical score with transparent breakdown', () => {
  const result = ExplainableRiskScorer.calculateScore({
    ruleCode: 'RAPID_PASS_THROUGH_MULE',
    timeToDrainSec: 8.5, // <= 10s: +25
    drainPercentage: 96.0, // >= 95%: +20
    amount: 85000, // >= 50k: +5
    inDegree: 1,
    outDegree: 1,
    hopCount: 2
  });

  assert.strictEqual(result.severity, 'CRITICAL', 'Severity should be CRITICAL');
  assert.ok(result.score >= 85, `Score should be >= 85, got ${result.score}`);
  assert.ok(result.breakdown.length >= 4, 'Breakdown should contain all contributing signals');

  const velocitySignal = result.breakdown.find(b => b.signal === 'VELOCITY_PENALTY');
  assert.ok(velocitySignal, 'Should contain VELOCITY_PENALTY signal');
  assert.strictEqual(velocitySignal.points, 25, 'Ultra-rapid velocity should give 25 points');
});

// ----------------------------------------------------
// Test 2: Rapid Pass-Through Detection
// ----------------------------------------------------
runTest('Rule: RAPID_PASS_THROUGH_MULE triggers on high drain velocity', () => {
  const graph = new GraphStore();
  const engine = new FraudDetectionEngine(graph);
  const t0 = 10000000;

  // Step 1: Inflow of ₹60,000 to Mule
  const alerts1 = engine.evaluateTransaction({
    transaction_id: 'TX-IN-1',
    time_ms: t0,
    sender_name: 'Victim User',
    sender_vpa: 'victim@okaxis',
    receiver_name: 'Suspect Mule',
    receiver_vpa: 'mule1@okaxis',
    amount: 60000,
    status: 'SUCCESS',
    bank_code: 'AXIS',
    location: 'Delhi'
  });
  assert.strictEqual(alerts1.length, 0, 'Inflow should not trigger alert immediately');

  // Step 2: Outflow of ₹57,000 (95%) after 10 seconds
  const alerts2 = engine.evaluateTransaction({
    transaction_id: 'TX-OUT-1',
    time_ms: t0 + 10000, // 10 seconds later
    sender_name: 'Suspect Mule',
    sender_vpa: 'mule1@okaxis',
    receiver_name: 'Cashout Receiver',
    receiver_vpa: 'cashout@paytm',
    amount: 57000,
    status: 'SUCCESS',
    bank_code: 'PAYTM',
    location: 'Mumbai'
  });

  assert.strictEqual(alerts2.length, 1, 'Should trigger exactly 1 alert');
  const alert = alerts2[0];
  assert.strictEqual(alert.rule_code, 'RAPID_PASS_THROUGH_MULE');
  assert.strictEqual(alert.suspect_vpa, 'mule1@okaxis');
  assert.strictEqual(alert.time_to_drain_seconds, 10);
  assert.strictEqual(alert.drain_percentage, 95);
  assert.ok(alert.risk_score >= 85, 'Rapid 10s drain should score >= 85');
});

// ----------------------------------------------------
// Test 3: Fan-In Smurfing Aggregator Detection
// ----------------------------------------------------
runTest('Rule: FAN_IN_SMURFING_AGGREGATOR triggers on >= 3 distinct senders', () => {
  const graph = new GraphStore();
  const engine = new FraudDetectionEngine(graph, { fanInMinDistinctSenders: 3 });
  const t0 = 20000000;
  const aggVpa = 'aggregator@okhdfcbank';

  // Sender 1
  engine.evaluateTransaction({
    transaction_id: 'TX-S1',
    time_ms: t0,
    sender_name: 'Sender 1',
    sender_vpa: 's1@okaxis',
    receiver_name: 'Aggregator',
    receiver_vpa: aggVpa,
    amount: 25000,
    status: 'SUCCESS',
    bank_code: 'AXIS'
  });

  // Sender 2
  engine.evaluateTransaction({
    transaction_id: 'TX-S2',
    time_ms: t0 + 2000,
    sender_name: 'Sender 2',
    sender_vpa: 's2@okybl',
    receiver_name: 'Aggregator',
    receiver_vpa: aggVpa,
    amount: 28000,
    status: 'SUCCESS',
    bank_code: 'YBL'
  });

  // Sender 3 (triggers smurfing threshold)
  const alerts3 = engine.evaluateTransaction({
    transaction_id: 'TX-S3',
    time_ms: t0 + 4000,
    sender_name: 'Sender 3',
    sender_vpa: 's3@okicici',
    receiver_name: 'Aggregator',
    receiver_vpa: aggVpa,
    amount: 30000,
    status: 'SUCCESS',
    bank_code: 'ICICI'
  });

  const smurfAlert = alerts3.find(a => a.rule_code === 'FAN_IN_SMURFING_AGGREGATOR');
  assert.ok(smurfAlert, 'Should detect FAN_IN_SMURFING_AGGREGATOR');
  assert.strictEqual(smurfAlert.suspect_vpa, aggVpa);
  assert.strictEqual(smurfAlert.amount_drained, 83000, 'Aggregated volume should match sum of 3 transfers');
});

// ----------------------------------------------------
// Test 4: Fan-Out Distribution Dispersal
// ----------------------------------------------------
runTest('Rule: FAN_OUT_DISTRIBUTION triggers on dispersing to >= 3 distinct receivers', () => {
  const graph = new GraphStore();
  const engine = new FraudDetectionEngine(graph, { fanOutMinDistinctReceivers: 3 });
  const t0 = 30000000;
  const distVpa = 'distributor@okaxis';

  // Inflow to distributor
  engine.evaluateTransaction({
    transaction_id: 'TX-DIST-IN',
    time_ms: t0,
    sender_name: 'Compromised Acct',
    sender_vpa: 'victim_corp@okaxis',
    receiver_name: 'Distributor',
    receiver_vpa: distVpa,
    amount: 150000,
    status: 'SUCCESS'
  });

  // Outflow 1
  engine.evaluateTransaction({
    transaction_id: 'TX-OUT-1',
    time_ms: t0 + 1000,
    sender_name: 'Distributor',
    sender_vpa: distVpa,
    receiver_name: 'Runner 1',
    receiver_vpa: 'runner1@paytm',
    amount: 40000,
    status: 'SUCCESS'
  });

  // Outflow 2
  engine.evaluateTransaction({
    transaction_id: 'TX-OUT-2',
    time_ms: t0 + 2000,
    sender_name: 'Distributor',
    sender_vpa: distVpa,
    receiver_name: 'Runner 2',
    receiver_vpa: 'runner2@paytm',
    amount: 40000,
    status: 'SUCCESS'
  });

  // Outflow 3 (triggers fan-out threshold)
  const alerts3 = engine.evaluateTransaction({
    transaction_id: 'TX-OUT-3',
    time_ms: t0 + 3000,
    sender_name: 'Distributor',
    sender_vpa: distVpa,
    receiver_name: 'Runner 3',
    receiver_vpa: 'runner3@paytm',
    amount: 40000,
    status: 'SUCCESS'
  });

  const fanOutAlert = alerts3.find(a => a.rule_code === 'FAN_OUT_DISTRIBUTION');
  assert.ok(fanOutAlert, 'Should detect FAN_OUT_DISTRIBUTION');
  assert.strictEqual(fanOutAlert.suspect_vpa, distVpa);
});

// ----------------------------------------------------
// Test 5: Graph Store Cycle Detection
// ----------------------------------------------------
runTest('Graph Store: Detects circular transaction loop (A -> B -> C -> A)', () => {
  const graph = new GraphStore();
  const t0 = 40000000;

  graph.addTransaction({ sender_vpa: 'node_a@upi', receiver_vpa: 'node_b@upi', amount: 50000, status: 'SUCCESS', time_ms: t0 });
  graph.addTransaction({ sender_vpa: 'node_b@upi', receiver_vpa: 'node_c@upi', amount: 48000, status: 'SUCCESS', time_ms: t0 + 1000 });
  graph.addTransaction({ sender_vpa: 'node_c@upi', receiver_vpa: 'node_a@upi', amount: 46000, status: 'SUCCESS', time_ms: t0 + 2000 });

  const cycle = graph.findCycle('node_a@upi');
  assert.ok(cycle, 'Should detect cycle');
  assert.strictEqual(cycle[0], 'node_a@upi');
  assert.strictEqual(cycle[cycle.length - 1], 'node_a@upi');
  assert.strictEqual(cycle.length, 4, 'Cycle length should be 4 (A -> B -> C -> A)');
});

// ----------------------------------------------------
// Test 6: Status Filter - Failed Transactions Ignored
// ----------------------------------------------------
runTest('Engine: Ignores FAILED transactions without generating false alerts', () => {
  const graph = new GraphStore();
  const engine = new FraudDetectionEngine(graph);

  const alerts = engine.evaluateTransaction({
    transaction_id: 'FAILED-TX',
    time_ms: Date.now(),
    sender_name: 'User 1',
    sender_vpa: 'user1@okaxis',
    receiver_name: 'User 2',
    receiver_vpa: 'user2@okaxis',
    amount: 500000,
    status: 'FAILED',
    bank_code: 'AXIS'
  });

  assert.strictEqual(alerts.length, 0, 'Failed transaction must produce 0 alerts');
});

// ----------------------------------------------------
// Test 7: Case Management Lifecycle
// ----------------------------------------------------
runTest('CaseManager: Manages lifecycle from NEW to ESCALATED and enforces quarantine', () => {
  const graph = new GraphStore();
  const caseMgr = new CaseManager(graph, { inMemory: true });

  const mockAlert = {
    alert_id: 'ALT-TEST-' + Date.now(),
    suspect_vpa: 'suspect99@okaxis',
    suspect_name: 'Suspect 99',
    rule_code: 'RAPID_PASS_THROUGH_MULE',
    severity: 'CRITICAL',
    risk_score: 95,
    amount_drained: 75000,
    bank: 'AXIS',
    location: 'Delhi'
  };

  const createdCase = caseMgr.createCaseFromAlert(mockAlert, 'Lead Investigator');
  assert.strictEqual(createdCase.status, 'NEW');
  assert.strictEqual(createdCase.suspectVpa, 'suspect99@okaxis');

  // Update status to INVESTIGATING
  const updated = caseMgr.updateCaseStatus(createdCase.caseId, 'INVESTIGATING', 'Lead Investigator', 'Initial triage started');
  assert.strictEqual(updated.status, 'INVESTIGATING');

  // Quarantine Account
  caseMgr.quarantineAccount('suspect99@okaxis', 'High risk mule network participant');
  assert.strictEqual(caseMgr.isQuarantined('suspect99@okaxis'), true);
  assert.strictEqual(graph.getNode('suspect99@okaxis').isQuarantined, true);

  // Release Quarantine
  caseMgr.unquarantineAccount('suspect99@okaxis');
  assert.strictEqual(caseMgr.isQuarantined('suspect99@okaxis'), false);
  assert.strictEqual(graph.getNode('suspect99@okaxis').isQuarantined, false);
});

console.log(`\n========================================================`);
console.log(`📊 TEST RESULTS: ${passedTests}/${totalTests} Passed (${Math.round((passedTests / totalTests) * 100)}%)`);
console.log(`========================================================\n`);

if (passedTests !== totalTests) {
  process.exit(1);
}
