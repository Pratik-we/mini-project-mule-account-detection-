/**
 * Web Dashboard & Real-Time Alert Broker
 * =====================================
 * Zero-dependency server using built-in Node.js modules.
 * Connects the real UPI transactions.csv dataset, stateful
 * CEP mule detection engine, and live SSE/REST dashboard at http://localhost:3000
 */

const http = require('http');
const fs = require('fs');
const path = require('path');
const { getNextTransaction, injectMuleAttack } = require('../ingestion/stream_simulator');

let PORT = parseInt(process.env.PORT || '3000', 10);
const PUBLIC_DIR = path.join(__dirname, 'public');

// In-Memory Storage & Subscriber registry
const dbTransactions = [];
const dbAlerts = [];
const activeSubscribers = new Set();
const accountStateMap = new Map();

function getOrCreateState(vpa, name = '') {
  const key = String(vpa || '').toLowerCase().trim();
  if (!accountStateMap.has(key)) {
    accountStateMap.set(key, {
      vpa: key,
      name: name || key,
      recentCredits: [],
      recentDebits: [],
      distinctSenders: new Set(),
      upstreamSources: new Map(),
      riskScore: 0,
      isFlaggedMule: false
    });
  }
  const state = accountStateMap.get(key);
  if (name && (!state.name || state.name === key)) {
    state.name = name;
  }
  return state;
}

function evictOldState(state, currentTimeMs) {
  const cutoff = currentTimeMs - 120000; // 2-minute sliding window
  state.recentCredits = state.recentCredits.filter(c => c.timeMs >= cutoff);
  state.recentDebits = state.recentDebits.filter(d => d.timeMs >= cutoff);
}

// Stateful In-Memory CEP Mule Detection Logic
function processStreamEvent(tx) {
  if (tx.status !== 'SUCCESS') return;

  const eventTimeMs = tx.stream_time_ms || Date.now();
  const senderState = getOrCreateState(tx.sender_vpa, tx.sender_name);
  const receiverState = getOrCreateState(tx.receiver_vpa, tx.receiver_name);

  evictOldState(senderState, eventTimeMs);
  evictOldState(receiverState, eventTimeMs);

  // 1. Inflow to Receiver
  receiverState.recentCredits.push({
    txId: tx.transaction_id,
    amount: tx.amount,
    fromVpa: tx.sender_vpa,
    fromName: tx.sender_name,
    timeMs: eventTimeMs
  });
  receiverState.distinctSenders.add(tx.sender_vpa);
  receiverState.upstreamSources.set(tx.sender_vpa, { timeMs: eventTimeMs, amount: tx.amount });

  // 2. Outflow from Sender
  senderState.recentDebits.push({
    txId: tx.transaction_id,
    amount: tx.amount,
    toVpa: tx.receiver_vpa,
    toName: tx.receiver_name,
    timeMs: eventTimeMs
  });

  // --- Pattern 1: Rapid In-to-Out Pass-Through Mule (Layering) ---
  if (senderState.recentCredits.length > 0) {
    const totalInflow = senderState.recentCredits.reduce((sum, c) => sum + c.amount, 0);
    const lastCredit = senderState.recentCredits[senderState.recentCredits.length - 1];
    const timeDeltaSeconds = (eventTimeMs - lastCredit.timeMs) / 1000;
    const drainRatio = (tx.amount / totalInflow) * 100;

    // Trigger rule if drained within 60 seconds with >= 70% drain ratio
    if (timeDeltaSeconds >= 0 && timeDeltaSeconds <= 60 && drainRatio >= 70 && tx.amount >= 5000) {
      senderState.isFlaggedMule = true;
      const isCritical = timeDeltaSeconds <= 15;
      senderState.riskScore = Math.min(99, 75 + Math.round((60 - timeDeltaSeconds) * 0.4));

      emitAlert({
        alert_id: 'ALT-' + Date.now().toString().slice(-6),
        alert_time: new Date().toLocaleTimeString(),
        rule_code: 'RAPID_PASS_THROUGH_MULE',
        severity: isCritical ? 'CRITICAL' : 'HIGH',
        risk_score: senderState.riskScore,
        suspect_vpa: tx.sender_vpa,
        suspect_name: senderState.name,
        source_vpa: `${lastCredit.fromName} (${lastCredit.fromVpa})`,
        target_vpa: `${tx.receiver_name} (${tx.receiver_vpa})`,
        hop_count: 2,
        time_to_drain_seconds: parseFloat(timeDeltaSeconds.toFixed(1)),
        drain_percentage: parseFloat(drainRatio.toFixed(1)),
        amount_drained: tx.amount,
        bank: tx.bank_code,
        location: tx.location,
        details: `Drained ${drainRatio.toFixed(1)}% (₹${tx.amount.toLocaleString('en-IN')}) of received funds in ${timeDeltaSeconds.toFixed(1)}s`
      });
    }
  }

  // --- Pattern 2: Fan-in Smurfing Aggregator Mule ---
  if (receiverState.distinctSenders.size >= 3 && !receiverState.smurfingAlerted) {
    receiverState.smurfingAlerted = true;
    receiverState.isFlaggedMule = true;
    receiverState.riskScore = 94;
    const totalAggregated = receiverState.recentCredits.reduce((s, c) => s + c.amount, 0);

    emitAlert({
      alert_id: 'ALT-' + Date.now().toString().slice(-6),
      alert_time: new Date().toLocaleTimeString(),
      rule_code: 'FAN_IN_SMURFING_AGGREGATOR',
      severity: 'CRITICAL',
      risk_score: 94,
      suspect_vpa: tx.receiver_vpa,
      suspect_name: receiverState.name,
      source_vpa: `Multiple Victims (${receiverState.distinctSenders.size} remitters)`,
      target_vpa: tx.receiver_vpa,
      hop_count: 1,
      time_to_drain_seconds: 0,
      drain_percentage: 0,
      amount_drained: totalAggregated,
      bank: tx.bank_code,
      location: tx.location,
      details: `Received ₹${totalAggregated.toLocaleString('en-IN')} from ${receiverState.distinctSenders.size} distinct remitters in under 2 minutes`
    });
  }
}

function emitAlert(alert) {
  dbAlerts.unshift(alert);
  if (dbAlerts.length > 500) dbAlerts.pop();

  console.log(`\n🚨 [ALERT] ${alert.rule_code} | Severity: ${alert.severity} (Risk: ${alert.risk_score}/100)`);
  console.log(`   Suspect: ${alert.suspect_name} <${alert.suspect_vpa}>`);
  console.log(`   Speed  : ${alert.time_to_drain_seconds}s Drain | ${alert.details}`);

  broadcastEvent('alert', alert);
}

function broadcastEvent(type, data) {
  const payload = `event: ${type}\ndata: ${JSON.stringify(data)}\n\n`;
  activeSubscribers.forEach(res => {
    try {
      res.write(payload);
    } catch (e) {
      activeSubscribers.delete(res);
    }
  });
}

function handleIngestedTx(tx) {
  dbTransactions.unshift(tx);
  if (dbTransactions.length > 1000) dbTransactions.pop();

  processStreamEvent(tx);
  broadcastEvent('transaction', tx);
}

// HTTP Server
const server = http.createServer((req, res) => {
  const url = new URL(req.url, `http://${req.headers.host}`);

  // Favicon handler
  if (url.pathname === '/favicon.ico') {
    res.writeHead(204);
    res.end();
    return;
  }

  // SSE Stream Endpoint
  if (url.pathname === '/api/stream') {
    res.writeHead(200, {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive',
      'Access-Control-Allow-Origin': '*'
    });
    res.write('retry: 2000\n\n');
    activeSubscribers.add(res);
    req.on('close', () => activeSubscribers.delete(res));
    return;
  }

  // REST API: Trigger Manual Mule Ring Attack
  if (url.pathname === '/api/inject-mule') {
    injectMuleAttack(handleIngestedTx);
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ status: 'Mule ring attack triggered' }));
    return;
  }

  // REST API: Live Aggregated Metrics
  if (url.pathname === '/api/stats') {
    const totalVolume = dbTransactions.reduce((acc, t) => acc + (t.amount || 0), 0);
    const criticalAlerts = dbAlerts.filter(a => a.severity === 'CRITICAL').length;
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({
      totalTransactions: dbTransactions.length,
      totalAlerts: dbAlerts.length,
      criticalAlerts,
      totalVolumeRupees: totalVolume,
      activeMulesCount: Array.from(accountStateMap.values()).filter(s => s.isFlaggedMule).length
    }));
    return;
  }

  // REST API: Get All Alerts
  if (url.pathname === '/api/alerts') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(dbAlerts));
    return;
  }

  // Serve static UI assets
  let filePath = path.join(PUBLIC_DIR, url.pathname === '/' ? 'index.html' : url.pathname);
  if (fs.existsSync(filePath) && fs.statSync(filePath).isFile()) {
    const ext = path.extname(filePath);
    const mimeTypes = {
      '.html': 'text/html',
      '.css': 'text/css',
      '.js': 'application/javascript',
      '.json': 'application/json',
      '.svg': 'image/svg+xml'
    };
    res.writeHead(200, { 'Content-Type': mimeTypes[ext] || 'text/plain' });
    fs.createReadStream(filePath).pipe(res);
    return;
  }

  res.writeHead(404, { 'Content-Type': 'text/plain' });
  res.end('Not Found');
});

server.on('error', (err) => {
  if (err.code === 'EADDRINUSE') {
    console.warn(`[Warning] Port ${PORT} is in use. Trying port ${PORT + 1}...`);
    PORT = PORT + 1;
    server.listen(PORT);
  } else {
    console.error('[Server Error]', err);
  }
});

server.listen(PORT, () => {
  console.log(`\n======================================================`);
  console.log(`🚀 REAL-TIME UPI FRAUD & MULE STREAM SENTINEL`);
  console.log(`   Interactive Dashboard : http://localhost:${PORT}`);
  console.log(`   Dataset Source        : data/transactions.csv`);
  console.log(`   Stream Status         : ACTIVE`);
  console.log(`======================================================\n`);

  // Continuously stream transactions from data/transactions.csv every 450ms
  setInterval(() => {
    const tx = getNextTransaction();
    if (tx) {
      handleIngestedTx(tx);
    }
  }, 450);
});
