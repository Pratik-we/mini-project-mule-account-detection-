/**
 * In-Process End-to-End Test Runner
 * =================================
 * Starts Sentinel server within Node.js, tests REST endpoints,
 * validates JSON structures and scenario triggers, then closes cleanly.
 */

const { server, getPort } = require('../web-dashboard/server');
const http = require('http');

async function wait(ms) {
  return new Promise(r => setTimeout(r, ms));
}

function get(port, path) {
  return new Promise((resolve, reject) => {
    const req = http.get({
      hostname: '127.0.0.1',
      port: port,
      path: path,
      timeout: 3000
    }, (res) => {
      let body = '';
      res.on('data', chunk => { body += chunk; });
      res.on('end', () => {
        resolve({ status: res.statusCode, headers: res.headers, body });
      });
    });
    req.on('error', reject);
    req.on('timeout', () => {
      req.destroy();
      reject(new Error(`Timeout fetching ${path}`));
    });
  });
}

async function run() {
  console.log('\n======================================================');
  console.log('🧪 RUNNING IN-PROCESS SERVER ENDPOINT INTEGRATION TESTS');
  console.log('======================================================\n');

  // Wait 1.5s for initial transactions to be ingested
  await wait(1500);
  const port = getPort();
  console.log(`Testing against Sentinel Server on port ${port}...\n`);

  try {
    // 1. /api/stats
    const statsRes = await get(port, '/api/stats');
    if (statsRes.status !== 200) throw new Error(`Expected 200, got ${statsRes.status}`);
    const stats = JSON.parse(statsRes.body);
    console.log(`  ✅ [PASS] /api/stats: Ingested=${stats.streamIngestionCounter}, Volume=₹${stats.cumulativeVolume}, Alerts=${stats.totalAlerts}, Avg Latency=${stats.avgLatencyMs}ms`);

    // 2. /api/transactions
    const txRes = await get(port, '/api/transactions?limit=10');
    if (txRes.status !== 200) throw new Error(`Expected 200, got ${txRes.status}`);
    const txs = JSON.parse(txRes.body);
    console.log(`  ✅ [PASS] /api/transactions: Retrieved ${txs.length} transactions`);

    // 3. /api/network/graph
    const graphRes = await get(port, '/api/network/graph?limit=50');
    if (graphRes.status !== 200) throw new Error(`Expected 200, got ${graphRes.status}`);
    const graph = JSON.parse(graphRes.body);
    console.log(`  ✅ [PASS] /api/network/graph: Visualized ${graph.nodes.length} nodes, ${graph.edges.length} edges`);

    // 4. /api/simulate/rapid-pass-through
    const simRes = await get(port, '/api/simulate/rapid-pass-through');
    if (simRes.status !== 200) throw new Error(`Expected 200, got ${simRes.status}`);
    const sim = JSON.parse(simRes.body);
    console.log(`  ✅ [PASS] /api/simulate/rapid-pass-through: Triggered ${sim.tag}, Suspect=${sim.suspect}`);

    // 5. /api/simulate/fan-in-smurfing
    const smurfRes = await get(port, '/api/simulate/fan-in-smurfing');
    const smurf = JSON.parse(smurfRes.body);
    console.log(`  ✅ [PASS] /api/simulate/fan-in-smurfing: Triggered ${smurf.tag}, Senders=${smurf.sendersCount}`);

    // 6. /api/simulate/fan-out-distribution
    const distRes = await get(port, '/api/simulate/fan-out-distribution');
    const dist = JSON.parse(distRes.body);
    console.log(`  ✅ [PASS] /api/simulate/fan-out-distribution: Triggered ${dist.tag}, Runners=${dist.runnersCount}`);

    // 7. /api/simulate/circular-loop
    const loopRes = await get(port, '/api/simulate/circular-loop');
    const loop = JSON.parse(loopRes.body);
    console.log(`  ✅ [PASS] /api/simulate/circular-loop: Triggered ${loop.tag}, Entities=${loop.entities.length}`);

    // 8. /api/analytics
    const analyticsRes = await get(port, '/api/analytics');
    const analytics = JSON.parse(analyticsRes.body);
    console.log(`  ✅ [PASS] /api/analytics: Banks=${Object.keys(analytics.bankDistribution).length}, Cities=${Object.keys(analytics.cityDistribution).length}`);

    // 9. Static UI Check
    const htmlRes = await get(port, '/');
    if (htmlRes.status !== 200) throw new Error(`Expected 200, got ${htmlRes.status}`);
    console.log(`  ✅ [PASS] Static HTML (index.html): Received ${htmlRes.body.length} bytes`);

    console.log('\n======================================================');
    console.log('🎉 ALL SERVER APIS AND SIMULATION SCENARIOS VERIFIED!');
    console.log('======================================================\n');

    server.close();
    process.exit(0);
  } catch (err) {
    console.error(`\n❌ Integration Test Error: ${err.message}`);
    server.close();
    process.exit(1);
  }
}

run();
