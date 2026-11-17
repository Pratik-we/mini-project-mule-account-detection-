/**
 * Sentinel Real-Time UPI Fraud Intelligence Platform
 * ==================================================
 * High-Throughput Stream Processing Server & SOC Intelligence Gateway
 */

const http = require('http');
const fs = require('fs');
const path = require('path');

const GraphStore = require('../engine/graph_store');
const FraudDetectionEngine = require('../engine/rules');
const CaseManager = require('../engine/case_manager');
const AttackSimulator = require('../engine/simulator');
const ClickHouseClient = require('../engine/clickhouse_client');
const { getNextTransaction, getDatasetStats, loadDataset } = require('../ingestion/stream_simulator');

let PORT = parseInt(process.env.PORT || '3000', 10);
const PUBLIC_DIR = path.join(__dirname, 'public');

// Core Engines
const graphStore = new GraphStore(15000);
const detectionEngine = new FraudDetectionEngine(graphStore);
const caseManager = new CaseManager(graphStore);
const clickHouse = new ClickHouseClient();

// In-Memory Storage
const dbTransactions = [];
const dbAlerts = [];
const activeSubscribers = new Set();

let streamIngestionCounter = 0;
let cumulativeVolume = 0;
let streamIntervalMs = 400; // Default 1x: ~2.5 transactions/sec
let isEnginePaused = false;
let streamTimer = null;
const serverStartTime = Date.now();

// Processing Latency Tracking
let recentLatencies = [];

// Attack Simulator instance
const simulator = new AttackSimulator((tx) => {
  handleIngestedTx(tx);
});

function handleIngestedTx(tx) {
  const t0 = process.hrtime.bigint();

  streamIngestionCounter++;
  if (tx.status === 'SUCCESS') {
    cumulativeVolume += (tx.amount || 0);
  }

  dbTransactions.unshift(tx);
  if (dbTransactions.length > 500) dbTransactions.pop();

  // Evaluate through Detection Engine (all 6 rules)
  const newAlerts = detectionEngine.evaluateTransaction(tx);

  // Sync to ClickHouse if available
  clickHouse.insertTransaction(tx);

  // Handle new alerts
  for (const alert of newAlerts) {
    dbAlerts.unshift(alert);
    if (dbAlerts.length > 500) dbAlerts.pop();

    // Auto-create SOC case
    const autoCase = caseManager.createCaseFromAlert(alert);

    // Sync alert to ClickHouse
    clickHouse.insertAlert(alert);

    // Broadcast Alert via SSE
    broadcastEvent('alert', alert);
    broadcastEvent('case', autoCase);
  }

  const t1 = process.hrtime.bigint();
  const latencyMs = Number(t1 - t0) / 1000000;
  recentLatencies.push(latencyMs);
  if (recentLatencies.length > 100) recentLatencies.shift();

  // Broadcast Transaction via SSE
  broadcastEvent('transaction', {
    ...tx,
    stream_counter: streamIngestionCounter,
    cumulative_volume: cumulativeVolume,
    total_alerts: dbAlerts.length,
    active_mules: detectionEngine.getAllFlaggedMules().length,
    avg_latency_ms: getAverageLatency()
  });
}

function getAverageLatency() {
  if (recentLatencies.length === 0) return 0.5;
  const sum = recentLatencies.reduce((a, b) => a + b, 0);
  return parseFloat((sum / recentLatencies.length).toFixed(2));
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

function startStreamTimer() {
  if (streamTimer) clearInterval(streamTimer);
  streamTimer = setInterval(() => {
    if (isEnginePaused) return;
    const tx = getNextTransaction();
    if (tx) {
      handleIngestedTx(tx);
    }
  }, streamIntervalMs);
}

// REST Request Helper: Parse JSON Body
function parseJsonBody(req) {
  return new Promise((resolve, reject) => {
    let body = '';
    req.on('data', chunk => { body += chunk; });
    req.on('end', () => {
      try {
        resolve(body ? JSON.parse(body) : {});
      } catch (err) {
        reject(err);
      }
    });
    req.on('error', reject);
  });
}

// HTTP Server
const server = http.createServer(async (req, res) => {
  const url = new URL(req.url, `http://${req.headers.host}`);

  // CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.writeHead(204);
    res.end();
    return;
  }

  if (url.pathname === '/favicon.ico') {
    res.writeHead(204);
    res.end();
    return;
  }

  // ========================================================
  // 1. SSE Stream Gateway
  // ========================================================
  if (url.pathname === '/api/stream') {
    res.writeHead(200, {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive'
    });
    res.write('retry: 2000\n\n');

    // Replay up to 30 recent alerts
    if (dbAlerts.length > 0) {
      dbAlerts.slice(0, 30).reverse().forEach(alert => {
        try { res.write(`event: alert\ndata: ${JSON.stringify(alert)}\n\n`); } catch (_) {}
      });
    }

    // Replay up to 15 recent transactions
    if (dbTransactions.length > 0) {
      dbTransactions.slice(0, 15).reverse().forEach(tx => {
        try { res.write(`event: transaction\ndata: ${JSON.stringify(tx)}\n\n`); } catch (_) {}
      });
    }

    activeSubscribers.add(res);
    req.on('close', () => activeSubscribers.delete(res));
    return;
  }

  // ========================================================
  // 2. High-Level Metrics & Telemetry
  // ========================================================
  if (url.pathname === '/api/stats') {
    const datasetStats = getDatasetStats();
    const criticalAlerts = dbAlerts.filter(a => a.severity === 'CRITICAL').length;
    const highAlerts = dbAlerts.filter(a => a.severity === 'HIGH').length;
    const flaggedMules = detectionEngine.getAllFlaggedMules();
    const quarantined = caseManager.getQuarantinedAccounts();
    const uptimeSec = Math.round((Date.now() - serverStartTime) / 1000);

    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({
      streamIngestionCounter,
      cumulativeVolume,
      datasetTotalRows: datasetStats.totalRows,
      datasetTotalVolume: datasetStats.totalVolume,
      totalAlerts: dbAlerts.length,
      criticalAlerts,
      highAlerts,
      activeMulesCount: flaggedMules.length,
      quarantinedCount: quarantined.length,
      avgLatencyMs: getAverageLatency(),
      uptimeSeconds: uptimeSec,
      isPaused: isEnginePaused,
      currentSpeedMs: streamIntervalMs,
      clickhouseConnected: clickHouse.isAvailable,
      graphStats: {
        nodesCount: graphStore.nodes.size,
        edgesCount: graphStore.edges.length
      }
    }));
    return;
  }

  // ========================================================
  // 3. Transactions Query API
  // ========================================================
  if (url.pathname === '/api/transactions') {
    const limit = parseInt(url.searchParams.get('limit') || '50', 10);
    const query = (url.searchParams.get('q') || '').toLowerCase();
    const status = (url.searchParams.get('status') || 'ALL').toUpperCase();

    let list = dbTransactions;
    if (status !== 'ALL') {
      list = list.filter(t => t.status === status);
    }
    if (query) {
      list = list.filter(t =>
        (t.sender_name && t.sender_name.toLowerCase().includes(query)) ||
        (t.sender_vpa && t.sender_vpa.toLowerCase().includes(query)) ||
        (t.receiver_name && t.receiver_name.toLowerCase().includes(query)) ||
        (t.receiver_vpa && t.receiver_vpa.toLowerCase().includes(query)) ||
        (t.bank_code && t.bank_code.toLowerCase().includes(query)) ||
        (t.location && t.location.toLowerCase().includes(query)) ||
        (t.transaction_id && t.transaction_id.toLowerCase().includes(query))
      );
    }

    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(list.slice(0, limit)));
    return;
  }

  // ========================================================
  // 4. Alerts Query API
  // ========================================================
  if (url.pathname === '/api/alerts') {
    const limit = parseInt(url.searchParams.get('limit') || '100', 10);
    const rule = url.searchParams.get('rule');
    const severity = url.searchParams.get('severity');

    let list = dbAlerts;
    if (rule && rule !== 'ALL') list = list.filter(a => a.rule_code === rule);
    if (severity && severity !== 'ALL') list = list.filter(a => a.severity === severity);

    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(list.slice(0, limit)));
    return;
  }

  // ========================================================
  // 5. Case Management APIs
  // ========================================================
  if (url.pathname === '/api/cases') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(caseManager.getAllCases()));
    return;
  }

  if (url.pathname === '/api/cases/status' && req.method === 'POST') {
    try {
      const body = await parseJsonBody(req);
      const updated = caseManager.updateCaseStatus(body.caseId, body.status, body.analyst, body.comment);
      if (!updated) {
        res.writeHead(404, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: 'Case not found' }));
        return;
      }
      broadcastEvent('case_update', updated);
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify(updated));
    } catch (err) {
      res.writeHead(400, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ error: err.message }));
    }
    return;
  }

  if (url.pathname === '/api/cases/note' && req.method === 'POST') {
    try {
      const body = await parseJsonBody(req);
      const note = caseManager.addNote(body.caseId, body.author, body.text);
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify(note));
    } catch (err) {
      res.writeHead(400, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ error: err.message }));
    }
    return;
  }

  // ========================================================
  // 6. Account 360 Dossier & Quarantine APIs
  // ========================================================
  if (url.pathname.startsWith('/api/account/')) {
    const rawVpa = decodeURIComponent(url.pathname.replace('/api/account/', ''));

    if (url.pathname.endsWith('/quarantine') && req.method === 'POST') {
      const vpa = decodeURIComponent(rawVpa.replace('/quarantine', ''));
      const body = await parseJsonBody(req);
      const isQuarantined = caseManager.isQuarantined(vpa);

      let record = null;
      if (isQuarantined) {
        caseManager.unquarantineAccount(vpa, body.analyst || 'SOC Analyst');
      } else {
        record = caseManager.quarantineAccount(vpa, body.reason, body.analyst || 'SOC Analyst');
      }

      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ vpa, isQuarantined: !isQuarantined, record }));
      return;
    }

    const vpa = rawVpa.toLowerCase().trim();
    const node = graphStore.getNode(vpa);
    const accountState = detectionEngine.getAccountState(vpa);
    const isQuarantined = caseManager.isQuarantined(vpa);
    const accountAlerts = dbAlerts.filter(a => a.suspect_vpa.toLowerCase() === vpa);
    const accountCases = caseManager.getAllCases().filter(c => c.suspectVpa.toLowerCase() === vpa);

    // Connected counter-parties
    const outEdges = (graphStore.adjList.get(vpa) || []).slice(-10);
    const inEdges = (graphStore.reverseAdjList.get(vpa) || []).slice(-10);

    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({
      vpa,
      node: node || { vpa, name: vpa, bank: 'UPI', location: 'India' },
      state: accountState,
      isQuarantined,
      alerts: accountAlerts,
      cases: accountCases,
      counterparties: {
        sentTo: outEdges,
        receivedFrom: inEdges
      }
    }));
    return;
  }

  // ========================================================
  // 7. Network Graph Visualization API (Cytoscape JSON)
  // ========================================================
  if (url.pathname === '/api/network/graph') {
    const focusVpa = url.searchParams.get('focus');
    const limit = parseInt(url.searchParams.get('limit') || '80', 10);
    const graphData = graphStore.getGraphVisualizationData(focusVpa, limit);

    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(graphData));
    return;
  }

  if (url.pathname === '/api/network/top-suspects') {
    const limit = parseInt(url.searchParams.get('limit') || '10', 10);
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(graphStore.getTopSuspiciousAccounts(limit)));
    return;
  }

  // ========================================================
  // 8. Analytics & Reporting API
  // ========================================================
  if (url.pathname === '/api/analytics') {
    // 1. Bank Risk Breakdown
    const bankCounts = {};
    dbTransactions.forEach(t => {
      const b = t.bank_code || 'OTHER';
      bankCounts[b] = (bankCounts[b] || 0) + 1;
    });

    // 2. City / Geographic Breakdown
    const cityCounts = {};
    dbTransactions.forEach(t => {
      const c = t.location || 'India';
      cityCounts[c] = (cityCounts[c] || 0) + 1;
    });

    // 3. Rule Performance Breakdown
    const ruleCounts = {};
    dbAlerts.forEach(a => {
      ruleCounts[a.rule_code] = (ruleCounts[a.rule_code] || 0) + 1;
    });

    // 4. Severity Distribution
    const severityCounts = { CRITICAL: 0, HIGH: 0, MEDIUM: 0 };
    dbAlerts.forEach(a => {
      if (severityCounts[a.severity] !== undefined) severityCounts[a.severity]++;
    });

    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({
      bankDistribution: bankCounts,
      cityDistribution: cityCounts,
      rulePerformance: ruleCounts,
      severityDistribution: severityCounts,
      totalAlerts: dbAlerts.length,
      totalTransactions: dbTransactions.length
    }));
    return;
  }

  // ========================================================
  // 9. Attack Scenario Simulation APIs
  // ========================================================
  if (url.pathname === '/api/simulate/rapid-pass-through') {
    const result = simulator.injectRapidPassThrough();
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ status: 'Triggered', ...result }));
    return;
  }

  if (url.pathname === '/api/simulate/fan-in-smurfing') {
    const result = simulator.injectFanInSmurfing();
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ status: 'Triggered', ...result }));
    return;
  }

  if (url.pathname === '/api/simulate/fan-out-distribution') {
    const result = simulator.injectFanOutDistribution();
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ status: 'Triggered', ...result }));
    return;
  }

  if (url.pathname === '/api/simulate/multi-hop-chain') {
    const result = simulator.injectMultiHopChain();
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ status: 'Triggered', ...result }));
    return;
  }

  if (url.pathname === '/api/simulate/circular-loop') {
    const result = simulator.injectCircularLoop();
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ status: 'Triggered', ...result }));
    return;
  }

  if (url.pathname === '/api/simulate/structuring-split') {
    const result = simulator.injectStructuringSplit();
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ status: 'Triggered', ...result }));
    return;
  }

  // Legacy compatibility for simple button
  if (url.pathname === '/api/inject-mule') {
    const result = simulator.injectRapidPassThrough();
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ status: 'Triggered', ...result }));
    return;
  }

  // ========================================================
  // 10. Stream Controls (Speed, Pause, Resume, Reset)
  // ========================================================
  if (url.pathname === '/api/speed') {
    const sp = url.searchParams.get('val') || '1x';
    if (sp === '50x') streamIntervalMs = 8;
    else if (sp === '20x') streamIntervalMs = 20;
    else if (sp === '5x') streamIntervalMs = 80;
    else streamIntervalMs = 400; // 1x

    startStreamTimer();
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ speed: sp, intervalMs: streamIntervalMs }));
    return;
  }

  if (url.pathname === '/api/stream/pause') {
    isEnginePaused = true;
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ isPaused: true }));
    return;
  }

  if (url.pathname === '/api/stream/resume') {
    isEnginePaused = false;
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ isPaused: false }));
    return;
  }

  if (url.pathname === '/api/stream/reset') {
    dbTransactions.length = 0;
    dbAlerts.length = 0;
    graphStore.reset();
    detectionEngine.reset();
    streamIngestionCounter = 0;
    cumulativeVolume = 0;
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ status: 'Stream state reset' }));
    return;
  }

  // ========================================================
  // 11. Forensic Report Export (JSON / CSV)
  // ========================================================
  if (url.pathname === '/api/export') {
    const format = url.searchParams.get('format') || 'json';
    if (format === 'csv') {
      const headers = ['alert_id', 'alert_timestamp', 'rule_code', 'severity', 'risk_score', 'suspect_vpa', 'source_vpa', 'target_vpa', 'amount_drained', 'time_to_drain_seconds', 'drain_percentage'];
      let csv = headers.join(',') + '\n';
      dbAlerts.forEach(a => {
        csv += [
          `"${a.alert_id}"`,
          `"${a.alert_timestamp || ''}"`,
          `"${a.rule_code}"`,
          `"${a.severity}"`,
          a.risk_score,
          `"${a.suspect_vpa}"`,
          `"${a.source_vpa || ''}"`,
          `"${a.target_vpa || ''}"`,
          a.amount_drained || 0,
          a.time_to_drain_seconds || 0,
          a.drain_percentage || 0
        ].join(',') + '\n';
      });
      res.writeHead(200, {
        'Content-Type': 'text/csv',
        'Content-Disposition': 'attachment; filename="sentinel_fraud_report.csv"'
      });
      res.end(csv);
      return;
    }

    res.writeHead(200, {
      'Content-Type': 'application/json',
      'Content-Disposition': 'attachment; filename="sentinel_fraud_report.json"'
    });
    res.end(JSON.stringify(dbAlerts, null, 2));
    return;
  }

  // ========================================================
  // 12. Static Assets Serving
  // ========================================================
  let filePath = path.join(PUBLIC_DIR, url.pathname === '/' ? 'index.html' : url.pathname);
  if (fs.existsSync(filePath) && fs.statSync(filePath).isFile()) {
    const ext = path.extname(filePath);
    const mimeTypes = {
      '.html': 'text/html',
      '.css': 'text/css',
      '.js': 'application/javascript',
      '.json': 'application/json',
      '.svg': 'image/svg+xml',
      '.png': 'image/png'
    };
    res.writeHead(200, { 'Content-Type': mimeTypes[ext] || 'text/plain' });
    fs.createReadStream(filePath).pipe(res);
    return;
  }

  res.writeHead(404, { 'Content-Type': 'application/json' });
  res.end(JSON.stringify({ error: 'Endpoint Not Found', path: url.pathname }));
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
  const stats = getDatasetStats();
  console.log(`\n======================================================`);
  console.log(`🛡️  SENTINEL NEXT-GEN FINANCIAL FRAUD INTELLIGENCE SOC`);
  console.log(`   Interactive Platform : http://localhost:${PORT}`);
  console.log(`   Dataset Source       : data/transactions.csv (${stats.totalRows} Transactions)`);
  console.log(`   Total Dataset Volume : ₹${Math.round(stats.totalVolume).toLocaleString('en-IN')}`);
  console.log(`   Stream Status        : ACTIVE (2.5 tx/sec @ 1x)`);
  console.log(`   Detection Engine     : 6 Multi-Pattern CEP Rules Active`);
  console.log(`======================================================\n`);

  startStreamTimer();
});

module.exports = { server, getPort: () => PORT };

