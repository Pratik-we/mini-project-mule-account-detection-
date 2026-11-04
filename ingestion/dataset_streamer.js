/**
 * Ingestion: Dynamic Dataset Streamer for UPI Transaction Datasets
 * ==============================================================
 * Reads transactions.csv, maps all columns (sender/receiver names,
 * VPAs, amounts, status, bank, location), and runs stateful
 * real-time money-mule detection rules.
 */

const fs = require('fs');
const path = require('path');
const readline = require('readline');

// Stateful in-memory ledger
const accountStateMap = new Map();
const detectedAlerts = [];

function getOrCreateState(vpa, name = '') {
  const key = String(vpa || '').toLowerCase().trim();
  if (!accountStateMap.has(key)) {
    accountStateMap.set(key, {
      vpa: key,
      name: name || key,
      recentCredits: [],
      recentDebits: [],
      distinctSenders: new Set(),
      upstreamSources: new Map(), // vpa -> { timeMs, amount }
      isFlaggedMule: false
    });
  }
  const state = accountStateMap.get(key);
  if (name && (!state.name || state.name === key)) {
    state.name = name;
  }
  return state;
}

// Parses raw CSV record into standardized transaction object
function normalizeRecord(raw) {
  const get = (...candidates) => {
    for (const c of candidates) {
      if (raw[c] !== undefined && raw[c] !== null && String(raw[c]).trim() !== '') {
        return raw[c];
      }
    }
    // Case-insensitive fallback
    const lowerKeys = Object.keys(raw);
    for (const c of candidates) {
      const match = lowerKeys.find(k => k.trim().toLowerCase().replace(/[\s_-]+/g, '') === c.toLowerCase().replace(/[\s_-]+/g, ''));
      if (match && raw[match] !== undefined) return raw[match];
    }
    return '';
  };

  const txId = get('transaction_id', 'tx_id', 'txn_id', 'id') || 'TX-' + Math.random().toString(36).substring(2, 9);
  const senderVpa = get('sender_vpa', 'sender_upi', 'remitter_vpa', 'sender') || 'unknown@upi';
  const senderName = get('sender_name', 'remitter_name', 'sender') || senderVpa;
  const receiverVpa = get('receiver_vpa', 'receiver_upi', 'beneficiary_vpa', 'receiver') || 'unknown@upi';
  const receiverName = get('receiver_name', 'beneficiary_name', 'receiver') || receiverVpa;

  const rawAmt = get('amount', 'amt', 'value', 'price') || '0';
  const amount = parseFloat(String(rawAmt).replace(/[^0-9.-]+/g, '')) || 0;

  const status = (get('status', 'txn_status', 'state') || 'SUCCESS').toUpperCase().trim();
  const bank = get('bank_code', 'bank', 'bank_name') || 'UPI_NET';
  const location = get('location', 'city', 'geo') || 'India';

  const timeRaw = get('timestamp', 'time', 'datetime', 'date');
  let timeMs = Date.now();
  if (timeRaw) {
    const parsed = Date.parse(timeRaw.includes('T') ? timeRaw : timeRaw.replace(' ', 'T') + 'Z');
    if (!isNaN(parsed)) {
      timeMs = parsed;
    }
  }

  return {
    transaction_id: String(txId).trim(),
    timestamp: timeRaw || new Date().toISOString(),
    time_ms: timeMs,
    sender_vpa: String(senderVpa).toLowerCase().trim(),
    sender_name: String(senderName).trim(),
    receiver_vpa: String(receiverVpa).toLowerCase().trim(),
    receiver_name: String(receiverName).trim(),
    amount: amount,
    status: status,
    bank_code: String(bank).trim(),
    location: String(location).trim()
  };
}

function evaluateTransaction(tx) {
  // Only evaluate successful transfers; failed transactions transfer 0 funds
  if (tx.status !== 'SUCCESS') {
    return;
  }

  const senderState = getOrCreateState(tx.sender_vpa, tx.sender_name);
  const receiverState = getOrCreateState(tx.receiver_vpa, tx.receiver_name);

  // 1. Record Inflow to Receiver
  receiverState.recentCredits.push({
    txId: tx.transaction_id,
    amount: tx.amount,
    fromVpa: tx.sender_vpa,
    fromName: tx.sender_name,
    timeMs: tx.time_ms
  });
  receiverState.distinctSenders.add(tx.sender_vpa);
  receiverState.upstreamSources.set(tx.sender_vpa, { timeMs: tx.time_ms, amount: tx.amount });

  // 2. Record Outflow from Sender
  senderState.recentDebits.push({
    txId: tx.transaction_id,
    amount: tx.amount,
    toVpa: tx.receiver_vpa,
    toName: tx.receiver_name,
    timeMs: tx.time_ms
  });

  // --- Pattern 1: Rapid In-to-Out Pass-Through Mule (Layering) ---
  if (senderState.recentCredits.length > 0) {
    const totalInflow = senderState.recentCredits.reduce((s, c) => s + c.amount, 0);
    const lastCredit = senderState.recentCredits[senderState.recentCredits.length - 1];
    const timeDeltaSeconds = Math.abs(tx.time_ms - lastCredit.timeMs) / 1000;
    const drainRatio = (tx.amount / totalInflow) * 100;

    // Trigger rule if drained within 120 seconds with >= 70% drain ratio
    if (timeDeltaSeconds <= 120 && drainRatio >= 70 && tx.amount >= 5000) {
      senderState.isFlaggedMule = true;
      const isCritical = timeDeltaSeconds <= 20;
      const riskScore = Math.min(99, 75 + Math.round((120 - timeDeltaSeconds) * 0.2));

      // Determine hop chain depth
      let hopCount = 2;
      const victimSource = lastCredit.fromVpa;
      if (senderState.upstreamSources.has(victimSource)) {
        hopCount = 3;
      }

      const alert = {
        alert_id: 'ALT-' + (detectedAlerts.length + 1),
        rule: 'RAPID_PASS_THROUGH_MULE',
        severity: isCritical ? 'CRITICAL' : 'HIGH',
        risk_score: riskScore,
        suspect_vpa: tx.sender_vpa,
        suspect_name: senderState.name,
        source_victim: `${lastCredit.fromName} (${lastCredit.fromVpa})`,
        target_destination: `${tx.receiver_name} (${tx.receiver_vpa})`,
        amount_drained: tx.amount,
        time_to_drain_seconds: parseFloat(timeDeltaSeconds.toFixed(1)),
        drain_percentage: parseFloat(drainRatio.toFixed(1)),
        hop_count: hopCount,
        transaction_id: tx.transaction_id,
        timestamp: tx.timestamp,
        bank: tx.bank_code,
        location: tx.location
      };

      detectedAlerts.push(alert);
      console.log(`\n🚨 [MULE DETECTED] ${alert.rule} | Severity: ${alert.severity} (Score: ${alert.risk_score}/100)`);
      console.log(`   Suspect Mule : ${alert.suspect_name} <${alert.suspect_vpa}>`);
      console.log(`   Laundering   : ${alert.source_victim} -> [${alert.suspect_vpa}] -> ${alert.target_destination}`);
      console.log(`   Speed/Ratio  : Drained ${alert.drain_percentage}% (₹${alert.amount_drained.toLocaleString('en-IN')}) in ${alert.time_to_drain_seconds}s!`);
      console.log(`   Txn ID & Loc : ${alert.transaction_id} | ${alert.bank} | ${alert.location}`);
    }
  }

  // --- Pattern 2: Fan-in Smurfing Aggregator Mule ---
  if (receiverState.distinctSenders.size >= 3 && !receiverState.smurfingAlerted) {
    receiverState.smurfingAlerted = true;
    receiverState.isFlaggedMule = true;
    const totalInflow = receiverState.recentCredits.reduce((s, c) => s + c.amount, 0);

    const alert = {
      alert_id: 'ALT-' + (detectedAlerts.length + 1),
      rule: 'FAN_IN_SMURFING_AGGREGATOR',
      severity: 'CRITICAL',
      risk_score: 94,
      suspect_vpa: tx.receiver_vpa,
      suspect_name: receiverState.name,
      distinct_senders_count: receiverState.distinctSenders.size,
      total_inflow: totalInflow,
      senders_list: Array.from(receiverState.distinctSenders),
      transaction_id: tx.transaction_id,
      timestamp: tx.timestamp,
      bank: tx.bank_code,
      location: tx.location
    };

    detectedAlerts.push(alert);
    console.log(`\n🚨 [SMURFING DETECTED] ${alert.rule} | Severity: CRITICAL (Score: 94/100)`);
    console.log(`   Aggregator Account : ${alert.suspect_name} <${alert.suspect_vpa}>`);
    console.log(`   Aggregated Volume  : ₹${alert.total_inflow.toLocaleString('en-IN')} from ${alert.distinct_senders_count} distinct victims!`);
    console.log(`   Victim Remitters   : ${alert.senders_list.join(', ')}`);
  }
}

async function processCSV(filePath) {
  console.log(`\n======================================================`);
  console.log(`📂 [Dataset Streamer] Processing File: ${path.basename(filePath)}`);
  console.log(`   Location: ${filePath}`);
  console.log(`======================================================`);

  const fileStream = fs.createReadStream(filePath);
  const rl = readline.createInterface({ input: fileStream, crlfDelay: Infinity });

  let headers = null;
  let count = 0;
  let successCount = 0;
  let failedCount = 0;

  for await (const line of rl) {
    if (!line.trim()) continue;
    const values = line.split(/,(?=(?:(?:[^"]*"){2})*[^"]*$)/).map(v => v.replace(/^"|"$/g, '').trim());

    if (!headers) {
      headers = values;
      console.log(`[Dataset Streamer] Detected Columns (${headers.length}): ${headers.join(' | ')}`);
      continue;
    }

    const rowObj = {};
    headers.forEach((h, i) => {
      rowObj[h] = values[i] !== undefined ? values[i] : '';
    });

    const normalized = normalizeRecord(rowObj);
    if (normalized.status === 'SUCCESS') {
      successCount++;
    } else {
      failedCount++;
    }
    evaluateTransaction(normalized);
    count++;
  }

  console.log(`\n======================================================`);
  console.log(`✅ DATASET STREAM ANALYSIS COMPLETE`);
  console.log(`   Total Transactions Processed : ${count}`);
  console.log(`   Successful Transfers (Analyzed) : ${successCount}`);
  console.log(`   Failed Transactions (Ignored)  : ${failedCount}`);
  console.log(`   Fraud & Money Mule Alerts   : ${detectedAlerts.length}`);
  console.log(`   Identified Suspect Mules    : ${Array.from(accountStateMap.values()).filter(s => s.isFlaggedMule).length}`);
  console.log(`======================================================`);

  const outputPath = path.join(path.dirname(filePath), 'alerts_output.json');
  fs.writeFileSync(outputPath, JSON.stringify(detectedAlerts, null, 2));
  console.log(`[Dataset Streamer] Saved Detailed Alerts Report to: ${outputPath}\n`);
}

async function main() {
  const targetFile = process.argv[2] || path.join(__dirname, '..', 'data', 'transactions.csv');

  if (fs.existsSync(targetFile)) {
    await processCSV(targetFile);
  } else {
    console.error(`[Error] Dataset file not found: ${targetFile}`);
    process.exit(1);
  }
}

main();
