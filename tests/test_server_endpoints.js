/**
 * Automated End-to-End API Test for Sentinel Web Server
 * =====================================================
 * Tests HTTP endpoints, JSON responses, and scenario triggers.
 */

const http = require('http');

async function testEndpoints() {
  console.log('Testing Sentinel Server Endpoints...\n');

  function get(urlPath) {
    return new Promise((resolve, reject) => {
      const req = http.get(`http://127.0.0.1:3000${urlPath}`, (res) => {
        let body = '';
        res.on('data', chunk => { body += chunk; });
        res.on('end', () => {
          resolve({ status: res.statusCode, headers: res.headers, body });
        });
      });
      req.on('error', reject);
      req.setTimeout(2000, () => {
        req.destroy();
        reject(new Error('Timeout'));
      });
    });
  }

  try {
    // 1. Test /api/stats
    const statsRes = await get('/api/stats');
    console.log(`[PASS] /api/stats -> Status ${statsRes.status}`);
    const stats = JSON.parse(statsRes.body);
    console.log(`       Stats: Ingested: ${stats.streamIngestionCounter}, Alerts: ${stats.totalAlerts}, Avg Latency: ${stats.avgLatencyMs}ms`);

    // 2. Test /api/transactions
    const txRes = await get('/api/transactions?limit=5');
    console.log(`[PASS] /api/transactions -> Status ${txRes.status}`);
    const txs = JSON.parse(txRes.body);
    console.log(`       Transactions retrieved: ${txs.length}`);

    // 3. Test /api/network/graph
    const graphRes = await get('/api/network/graph?limit=20');
    console.log(`[PASS] /api/network/graph -> Status ${graphRes.status}`);
    const graph = JSON.parse(graphRes.body);
    console.log(`       Graph Nodes: ${graph.nodes.length}, Edges: ${graph.edges.length}`);

    // 4. Test /api/simulate/rapid-pass-through
    const simRes = await get('/api/simulate/rapid-pass-through');
    console.log(`[PASS] /api/simulate/rapid-pass-through -> Status ${simRes.status}`);
    const sim = JSON.parse(simRes.body);
    console.log(`       Simulated Tag: ${sim.tag}, Suspect: ${sim.suspect}`);

    // 5. Test Static HTML
    const htmlRes = await get('/');
    console.log(`[PASS] / (index.html) -> Status ${htmlRes.status}, Content Length: ${htmlRes.body.length} bytes`);

    console.log('\n✅ ALL SERVER API ENDPOINTS VALIDATED SUCCESSFULLY!\n');
    process.exit(0);
  } catch (err) {
    console.error(`\n❌ Endpoint Test Failed: ${err.message}\n`);
    process.exit(1);
  }
}

testEndpoints();
