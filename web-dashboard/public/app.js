/**
 * SENTINEL SOC - Client-Side Intelligence & Visualization Controller
 * =================================================================
 * High-performance state management, real-time SSE intake,
 * interactive Canvas Network Graph, and SOC investigation workflow.
 */

// Global Application State
const appState = {
  transactions: [],
  alerts: [],
  cases: [],
  quarantinedVpas: new Set(),
  stats: {
    streamIngestionCounter: 0,
    cumulativeVolume: 0,
    datasetTotalRows: 9077,
    datasetTotalVolume: 17495336,
    avgLatencyMs: 0.4
  },
  activeTab: 'tab-command-center',
  isPaused: false,
  streamSpeed: '1x',
  currentTxFilter: 'ALL',
  currentTxSearch: '',
  currentAlertFilter: 'ALL',
  selectedAccountVpa: null,
  tpsCounter: 0,
  lastTxCount: 0,
  volumeHistory: [], // Rolling { time, volume }
  networkGraph: {
    nodes: [],
    edges: [],
    transform: { x: 0, y: 0, scale: 1 },
    draggedNode: null,
    hoveredNode: null,
    selectedNode: null,
    isDraggingViewport: false,
    dragStart: { x: 0, y: 0 }
  }
};

// ========================================================
// 1. INITIALIZATION & SSE CONNECTION
// ========================================================
window.addEventListener('DOMContentLoaded', () => {
  initTheme();
  initClock();
  initNavigation();
  initCanvasNetwork();
  initTpsCalculator();

  // Load initial state from backend APIs
  loadInitialStats();
  loadInitialAlerts();
  loadInitialCases();
  loadInitialTransactions();
  refreshGraphData();

  // Connect Server-Sent Events (SSE)
  connectEventSource();
});

function connectEventSource() {
  const evtSource = new EventSource('/api/stream');

  evtSource.addEventListener('transaction', (e) => {
    if (appState.isPaused) return;
    const tx = JSON.parse(e.data);
    handleLiveTransaction(tx);
  });

  evtSource.addEventListener('alert', (e) => {
    const alert = JSON.parse(e.data);
    handleLiveAlert(alert);
  });

  evtSource.addEventListener('case', (e) => {
    const newCase = JSON.parse(e.data);
    appState.cases.unshift(newCase);
    if (appState.cases.length > 300) appState.cases.pop();
  });

  evtSource.addEventListener('case_update', (e) => {
    const updated = JSON.parse(e.data);
    const idx = appState.cases.findIndex(c => c.caseId === updated.caseId);
    if (idx !== -1) {
      appState.cases[idx] = updated;
      if (appState.selectedAccountVpa && appState.selectedAccountVpa.toLowerCase() === updated.suspectVpa.toLowerCase()) {
        renderAccountInvestigation(updated.suspectVpa);
      }
    }
  });

  evtSource.onerror = () => {
    document.getElementById('telemetry-dot').style.backgroundColor = 'var(--accent-warning)';
    document.getElementById('telemetry-status').innerText = 'RECONNECTING';
  };

  evtSource.onopen = () => {
    document.getElementById('telemetry-dot').style.backgroundColor = 'var(--accent-success)';
    document.getElementById('telemetry-status').innerText = 'STREAM LIVE';
  };
}

function handleLiveTransaction(tx) {
  appState.stats.streamIngestionCounter = tx.stream_counter || (appState.stats.streamIngestionCounter + 1);
  if (tx.cumulative_volume !== undefined) {
    appState.stats.cumulativeVolume = tx.cumulative_volume;
  } else if (tx.status === 'SUCCESS') {
    appState.stats.cumulativeVolume += (tx.amount || 0);
  }

  if (tx.avg_latency_ms !== undefined) {
    appState.stats.avgLatencyMs = tx.avg_latency_ms;
  }

  appState.transactions.unshift(tx);
  if (appState.transactions.length > 500) appState.transactions.pop();

  // Record volume sample
  appState.volumeHistory.push({
    time: Date.now(),
    volume: tx.amount || 0
  });
  if (appState.volumeHistory.length > 30) appState.volumeHistory.shift();

  // Update UI Elements
  updateCommandKPIs();
  renderLiveTxItem(tx);
  if (appState.activeTab === 'tab-live-transactions') {
    renderTxTableRow(tx, true);
  }
}

function handleLiveAlert(alert) {
  appState.alerts.unshift(alert);
  if (appState.alerts.length > 300) appState.alerts.pop();

  updateCommandKPIs();
  renderAlertItem(alert, true);

  showToast(`🚨 [ALERT] ${alert.rule_code} (Risk ${alert.risk_score}/100) on ${alert.suspect_vpa}`);
}

// ========================================================
// 2. NAVIGATION & TABS
// ========================================================
function initNavigation() {
  document.querySelectorAll('.nav-tab').forEach(tab => {
    tab.addEventListener('click', () => {
      const tabId = tab.getAttribute('data-tab');
      switchTab(tabId, tab);
    });
  });
}

function switchTab(tabId, btnEl) {
  appState.activeTab = tabId;

  document.querySelectorAll('.nav-tab').forEach(b => b.classList.remove('active'));
  if (btnEl) btnEl.classList.add('active');
  else {
    const target = document.querySelector(`.nav-tab[data-tab="${tabId}"]`);
    if (target) target.classList.add('active');
  }

  document.querySelectorAll('.tab-view').forEach(view => view.classList.remove('active'));
  const activeView = document.getElementById(tabId);
  if (activeView) activeView.classList.add('active');

  // Specific tab initializations
  if (tabId === 'tab-network-intelligence') {
    resizeNetworkCanvas();
    refreshGraphData();
  } else if (tabId === 'tab-analytics') {
    loadAnalyticsData();
  } else if (tabId === 'tab-live-transactions') {
    renderAllTransactionsTable();
  } else if (tabId === 'tab-fraud-alerts') {
    renderAllAlertsFeed();
  }
}

function handleGlobalSearch(e) {
  if (e.key === 'Enter') {
    const val = e.target.value.trim();
    if (!val) return;
    if (val.includes('@')) {
      switchTab('tab-account-investigation');
      document.getElementById('investigate-vpa-input').value = val;
      investigateAccount(val);
    } else {
      switchTab('tab-live-transactions');
      document.getElementById('tx-search-input').value = val;
      onTxTableFilter();
    }
  }
}

// ========================================================
// 3. THEME & CLOCK CONTROLLERS
// ========================================================
function initTheme() {
  const saved = localStorage.getItem('sentinel_theme') || 'dark';
  applyTheme(saved);
}

function applyTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  localStorage.setItem('sentinel_theme', theme);
  const label = document.getElementById('theme-label');
  if (label) label.innerText = theme === 'dark' ? 'Dark' : 'Light';
}

function toggleTheme() {
  const current = document.documentElement.getAttribute('data-theme') || 'dark';
  applyTheme(current === 'dark' ? 'light' : 'dark');
}

function initClock() {
  const clockEl = document.getElementById('live-clock');
  const update = () => {
    if (clockEl) {
      clockEl.innerText = `${new Date().toLocaleTimeString('en-IN', { hour12: false })} IST`;
    }
  };
  setInterval(update, 1000);
  update();
}

function initTpsCalculator() {
  setInterval(() => {
    const current = appState.stats.streamIngestionCounter;
    const delta = current - appState.lastTxCount;
    appState.lastTxCount = current;
    const tps = (delta / 2).toFixed(1);
    const el = document.getElementById('kpi-tps');
    if (el) el.innerText = `${tps} /s`;
  }, 2000);
}

// ========================================================
// 4. API LOADERS & STATS
// ========================================================
async function loadInitialStats() {
  try {
    const res = await fetch('/api/stats');
    const data = await res.json();
    appState.stats = { ...appState.stats, ...data };
    updateCommandKPIs();
  } catch (_) {}
}

async function loadInitialAlerts() {
  try {
    const res = await fetch('/api/alerts?limit=50');
    const alerts = await res.json();
    appState.alerts = alerts;
    updateCommandKPIs();
    renderAllAlertsFeed();
  } catch (_) {}
}

async function loadInitialCases() {
  try {
    const res = await fetch('/api/cases');
    appState.cases = await res.json();
  } catch (_) {}
}

async function loadInitialTransactions() {
  try {
    const res = await fetch('/api/transactions?limit=30');
    appState.transactions = await res.json();
    renderAllTransactionsTable();
  } catch (_) {}
}

function updateCommandKPIs() {
  const txEl = document.getElementById('kpi-tx');
  const txSub = document.getElementById('kpi-tx-sub');
  const volEl = document.getElementById('kpi-vol');
  const volSub = document.getElementById('kpi-vol-sub');
  const alertsEl = document.getElementById('kpi-alerts');
  const alertsSub = document.getElementById('kpi-alerts-sub');
  const critEl = document.getElementById('kpi-critical');
  const mulesEl = document.getElementById('kpi-mules');
  const latencyEl = document.getElementById('kpi-latency');
  const headerLatency = document.getElementById('header-latency');
  const navTxBadge = document.getElementById('nav-tx-badge');
  const navAlertsBadge = document.getElementById('nav-alerts-badge');

  if (txEl) txEl.innerText = appState.stats.streamIngestionCounter.toLocaleString('en-IN');
  if (navTxBadge) navTxBadge.innerText = appState.stats.streamIngestionCounter.toLocaleString('en-IN');

  if (txSub && appState.stats.datasetTotalRows) {
    const pct = ((appState.stats.streamIngestionCounter / appState.stats.datasetTotalRows) * 100).toFixed(1);
    txSub.innerText = `of ${appState.stats.datasetTotalRows.toLocaleString('en-IN')} Dataset Events (${pct}%)`;
  }

  if (volEl) {
    const v = appState.stats.cumulativeVolume;
    if (v >= 10000000) volEl.innerText = `₹${(v / 10000000).toFixed(2)} Cr`;
    else if (v >= 100000) volEl.innerText = `₹${(v / 100000).toFixed(2)} L`;
    else volEl.innerText = `₹${Math.round(v).toLocaleString('en-IN')}`;
  }

  const alertCount = appState.alerts.length;
  if (alertsEl) alertsEl.innerText = alertCount.toLocaleString('en-IN');
  if (navAlertsBadge) navAlertsBadge.innerText = alertCount.toLocaleString('en-IN');

  if (alertsSub && appState.stats.streamIngestionCounter > 0) {
    const rate = ((alertCount / appState.stats.streamIngestionCounter) * 100).toFixed(2);
    alertsSub.innerText = `Detection Rate: ${rate}%`;
  }

  const criticalCount = appState.alerts.filter(a => a.severity === 'CRITICAL').length;
  if (critEl) critEl.innerText = criticalCount.toLocaleString('en-IN');

  const uniqueMules = new Set(appState.alerts.map(a => a.suspect_vpa));
  if (mulesEl) mulesEl.innerText = uniqueMules.size.toLocaleString('en-IN');

  const lat = `${appState.stats.avgLatencyMs || 0.4} ms`;
  if (latencyEl) latencyEl.innerText = lat;
  if (headerLatency) headerLatency.innerText = lat;

  // Render Volume and Severity Canvas charts
  renderVolumeChart();
  renderSeverityChart();
}

// ========================================================
// 5. INTERACTIVE CANVAS NETWORK GRAPH ENGINE
// ========================================================
let networkCanvas, networkCtx;

function initCanvasNetwork() {
  networkCanvas = document.getElementById('network-canvas');
  if (!networkCanvas) return;
  networkCtx = networkCanvas.getContext('2d');

  resizeNetworkCanvas();
  window.addEventListener('resize', resizeNetworkCanvas);

  // Mouse Interactivity
  networkCanvas.addEventListener('mousedown', onGraphMouseDown);
  window.addEventListener('mousemove', onGraphMouseMove);
  window.addEventListener('mouseup', onGraphMouseUp);
  networkCanvas.addEventListener('wheel', onGraphWheel, { passive: false });
}

function resizeNetworkCanvas() {
  const container = document.getElementById('graph-viewport-container');
  if (!container || !networkCanvas) return;
  networkCanvas.width = container.clientWidth;
  networkCanvas.height = container.clientHeight;
  drawNetworkGraph();
}

async function refreshGraphData(focusVpa = null) {
  try {
    const url = focusVpa ? `/api/network/graph?focus=${encodeURIComponent(focusVpa)}` : '/api/network/graph?limit=70';
    const res = await fetch(url);
    const data = await res.json();

    // Map Cytoscape-format to local layout coordinates
    const width = networkCanvas ? networkCanvas.width : 800;
    const height = networkCanvas ? networkCanvas.height : 600;

    const existingMap = new Map();
    appState.networkGraph.nodes.forEach(n => existingMap.set(n.id, { x: n.x, y: n.y }));

    appState.networkGraph.nodes = (data.nodes || []).map((cn, i) => {
      const id = cn.data.id;
      const prev = existingMap.get(id);
      const angle = (i / data.nodes.length) * Math.PI * 2;
      const radius = 160 + (i % 3) * 60;
      return {
        id: id,
        label: cn.data.label || id,
        vpa: cn.data.vpa,
        name: cn.data.fullName,
        role: cn.data.role,
        riskScore: cn.data.riskScore || 0,
        inDegree: cn.data.inDegree || 0,
        outDegree: cn.data.outDegree || 0,
        totalInflow: cn.data.totalInflow || 0,
        totalOutflow: cn.data.totalOutflow || 0,
        x: prev ? prev.x : (width / 2 + Math.cos(angle) * radius),
        y: prev ? prev.y : (height / 2 + Math.sin(angle) * radius),
        radius: 12 + Math.min(16, (cn.data.inDegree + cn.data.outDegree) * 2)
      };
    });

    appState.networkGraph.edges = (data.edges || []).map(ce => ({
      id: ce.data.id,
      source: ce.data.source,
      target: ce.data.target,
      amount: ce.data.amount,
      label: ce.data.label
    }));

    const statsPill = document.getElementById('graph-stats-pill');
    if (statsPill) {
      statsPill.innerText = `${appState.networkGraph.nodes.length} Nodes | ${appState.networkGraph.edges.length} Edges`;
    }

    drawNetworkGraph();
  } catch (err) {
    console.error('Error refreshing graph data:', err);
  }
}

function drawNetworkGraph() {
  if (!networkCtx || !networkCanvas) return;
  const ctx = networkCtx;
  const { width, height } = networkCanvas;

  ctx.clearRect(0, 0, width, height);
  ctx.save();

  // Apply zoom and pan transform
  const t = appState.networkGraph.transform;
  ctx.translate(t.x, t.y);
  ctx.scale(t.scale, t.scale);

  const nodeMap = new Map();
  appState.networkGraph.nodes.forEach(n => nodeMap.set(n.id, n));

  // Draw Edges with directed arrows
  appState.networkGraph.edges.forEach(edge => {
    const sNode = nodeMap.get(edge.source);
    const tNode = nodeMap.get(edge.target);
    if (!sNode || !tNode) return;

    ctx.beginPath();
    ctx.moveTo(sNode.x, sNode.y);
    ctx.lineTo(tNode.x, tNode.y);
    ctx.strokeStyle = 'rgba(56, 189, 248, 0.25)';
    ctx.lineWidth = Math.max(1, Math.min(5, (edge.amount / 30000)));
    ctx.stroke();

    // Draw Arrowhead
    const angle = Math.atan2(tNode.y - sNode.y, tNode.x - sNode.x);
    const arrowDist = tNode.radius + 6;
    const ax = tNode.x - Math.cos(angle) * arrowDist;
    const ay = tNode.y - Math.sin(angle) * arrowDist;

    ctx.beginPath();
    ctx.fillStyle = '#00e5ff';
    ctx.moveTo(ax, ay);
    ctx.lineTo(ax - 8 * Math.cos(angle - Math.PI / 6), ay - 8 * Math.sin(angle - Math.PI / 6));
    ctx.lineTo(ax - 8 * Math.cos(angle + Math.PI / 6), ay - 8 * Math.sin(angle + Math.PI / 6));
    ctx.fill();

    // Edge Amount Label
    if (t.scale > 0.7) {
      const midX = (sNode.x + tNode.x) / 2;
      const midY = (sNode.y + tNode.y) / 2;
      ctx.fillStyle = 'rgba(148, 163, 184, 0.85)';
      ctx.font = '9px JetBrains Mono';
      ctx.fillText(edge.label || `₹${edge.amount}`, midX + 4, midY - 4);
    }
  });

  // Draw Nodes
  appState.networkGraph.nodes.forEach(node => {
    ctx.beginPath();
    ctx.arc(node.x, node.y, node.radius, 0, Math.PI * 2);

    // Node Coloring based on Role & Risk
    let fill = '#38bdf8'; // Normal
    if (node.role === 'QUARANTINED') fill = '#a855f7';
    else if (node.role === 'CRITICAL_MULE') fill = '#ff1744';
    else if (node.role === 'HIGH_MULE') fill = '#ef4444';
    else if (node.role === 'AGGREGATOR') fill = '#f59e0b';
    else if (node.role === 'DISPERSAL') fill = '#06b6d4';

    ctx.fillStyle = fill;
    ctx.fill();

    // Border
    ctx.lineWidth = appState.networkGraph.selectedNode === node ? 3 : 1.5;
    ctx.strokeStyle = appState.networkGraph.selectedNode === node ? '#ffffff' : 'rgba(255, 255, 255, 0.4)';
    ctx.stroke();

    // Node Label
    ctx.fillStyle = '#ffffff';
    ctx.font = '10px Inter';
    ctx.textAlign = 'center';
    ctx.fillText(node.label, node.x, node.y + node.radius + 12);

    if (node.riskScore > 0) {
      ctx.fillStyle = '#ff1744';
      ctx.font = '9px JetBrains Mono';
      ctx.fillText(`Risk ${node.riskScore}`, node.x, node.y - node.radius - 4);
    }
  });

  ctx.restore();
}

function onGraphMouseDown(e) {
  const rect = networkCanvas.getBoundingClientRect();
  const mouseX = e.clientX - rect.left;
  const mouseY = e.clientY - rect.top;

  const t = appState.networkGraph.transform;
  const worldX = (mouseX - t.x) / t.scale;
  const worldY = (mouseY - t.y) / t.scale;

  // Check if clicked a node
  const clicked = appState.networkGraph.nodes.find(n => {
    const dx = n.x - worldX;
    const dy = n.y - worldY;
    return Math.sqrt(dx * dx + dy * dy) <= n.radius + 4;
  });

  if (clicked) {
    appState.networkGraph.draggedNode = clicked;
    appState.networkGraph.selectedNode = clicked;
    inspectNodeInSidebar(clicked);
    drawNetworkGraph();
  } else {
    appState.networkGraph.isDraggingViewport = true;
    appState.networkGraph.dragStart = { x: mouseX - t.x, y: mouseY - t.y };
  }
}

function onGraphMouseMove(e) {
  if (!networkCanvas) return;
  const rect = networkCanvas.getBoundingClientRect();
  const mouseX = e.clientX - rect.left;
  const mouseY = e.clientY - rect.top;
  const t = appState.networkGraph.transform;

  if (appState.networkGraph.draggedNode) {
    appState.networkGraph.draggedNode.x = (mouseX - t.x) / t.scale;
    appState.networkGraph.draggedNode.y = (mouseY - t.y) / t.scale;
    drawNetworkGraph();
  } else if (appState.networkGraph.isDraggingViewport) {
    t.x = mouseX - appState.networkGraph.dragStart.x;
    t.y = mouseY - appState.networkGraph.dragStart.y;
    drawNetworkGraph();
  }
}

function onGraphMouseUp() {
  appState.networkGraph.draggedNode = null;
  appState.networkGraph.isDraggingViewport = false;
}

function onGraphWheel(e) {
  e.preventDefault();
  const zoomFactor = e.deltaY < 0 ? 1.15 : 0.85;
  const t = appState.networkGraph.transform;
  t.scale = Math.max(0.2, Math.min(4, t.scale * zoomFactor));
  drawNetworkGraph();
}

function resetGraphView() {
  appState.networkGraph.transform = { x: 0, y: 0, scale: 1 };
  appState.networkGraph.selectedNode = null;
  drawNetworkGraph();
}

function inspectNodeInSidebar(node) {
  const container = document.getElementById('graph-inspector-body');
  const badge = document.getElementById('inspector-status-badge');
  if (!container) return;

  if (badge) {
    badge.innerText = node.role || 'INSPECTING';
    badge.className = `badge-status ${node.riskScore >= 85 ? 'status-failed' : 'status-success'}`;
  }

  container.innerHTML = `
    <div class="flow-routing-box" style="margin-bottom: 12px;">
      <div style="font-weight: 700; font-size: 13px; color: var(--text-main); margin-bottom: 4px;">
        ${escapeHtml(node.name || node.label)}
      </div>
      <div style="font-family: var(--font-mono); font-size: 11px; color: var(--accent-cyan);">
        ${escapeHtml(node.vpa)}
      </div>
    </div>

    <div class="signals-breakdown" style="margin-bottom: 12px;">
      <div class="signal-row">
        <span>Risk Score:</span>
        <span class="signal-pts" style="color: ${node.riskScore >= 85 ? 'var(--accent-critical)' : 'var(--accent-cyan)'}; font-weight: 700;">
          ${node.riskScore}/100
        </span>
      </div>
      <div class="signal-row">
        <span>Inbound Connections (In-Degree):</span>
        <span class="signal-pts">${node.inDegree}</span>
      </div>
      <div class="signal-row">
        <span>Outbound Connections (Out-Degree):</span>
        <span class="signal-pts">${node.outDegree}</span>
      </div>
      <div class="signal-row">
        <span>Total Inflow Settled:</span>
        <span class="signal-pts">₹${Math.round(node.totalInflow).toLocaleString('en-IN')}</span>
      </div>
      <div class="signal-row">
        <span>Total Outflow Drained:</span>
        <span class="signal-pts">₹${Math.round(node.totalOutflow).toLocaleString('en-IN')}</span>
      </div>
    </div>

    <div style="display: flex; gap: 8px;">
      <button class="btn btn-primary btn-sm" style="flex: 1;" onclick="openInvestigationFor('${escapeHtml(node.vpa)}')">
        Audit Dossier
      </button>
      <button class="btn btn-secondary btn-sm" onclick="focusNetworkVpa('${escapeHtml(node.vpa)}')">
        Focus
      </button>
    </div>
  `;
}

function openInvestigationFor(vpa) {
  switchTab('tab-account-investigation');
  document.getElementById('investigate-vpa-input').value = vpa;
  investigateAccount(vpa);
}

function focusNetworkVpa(vpa) {
  refreshGraphData(vpa);
}

function onGraphSearchKey(e) {
  if (e.key === 'Enter') {
    const vpa = e.target.value.trim();
    if (vpa) refreshGraphData(vpa);
  }
}

function highlightMultiHopChains() {
  showToast('Highlighting multi-hop layering paths across accounts...');
  const suspicious = appState.networkGraph.nodes.filter(n => n.riskScore >= 70);
  if (suspicious.length > 0) {
    appState.networkGraph.selectedNode = suspicious[0];
    inspectNodeInSidebar(suspicious[0]);
    drawNetworkGraph();
  }
}

function highlightCycles() {
  showToast('Scanning in-memory graph for circular money flow loops...');
  const loopNode = appState.networkGraph.nodes.find(n => n.role === 'CRITICAL_MULE' || n.riskScore >= 80);
  if (loopNode) {
    appState.networkGraph.selectedNode = loopNode;
    inspectNodeInSidebar(loopNode);
    drawNetworkGraph();
  }
}

// ========================================================
// 6. ACCOUNT 360 INVESTIGATION DOSSIER
// ========================================================
function onInvestigateKey(e) {
  if (e.key === 'Enter') investigateAccount();
}

async function investigateAccount(targetVpa = null) {
  const input = document.getElementById('investigate-vpa-input');
  const vpa = targetVpa || (input ? input.value.trim() : '');
  if (!vpa) return;

  appState.selectedAccountVpa = vpa;
  const container = document.getElementById('investigation-content-area');
  if (!container) return;

  container.innerHTML = `
    <div class="empty-placeholder">
      <div class="placeholder-icon">⏳</div>
      <div class="placeholder-title">Querying Forensic Dossier...</div>
    </div>
  `;

  try {
    const res = await fetch(`/api/account/${encodeURIComponent(vpa)}`);
    const dossier = await res.json();
    renderDossierView(dossier);
  } catch (err) {
    container.innerHTML = `<div class="empty-placeholder"><div class="placeholder-icon">⚠️</div><div>Error loading account: ${err.message}</div></div>`;
  }
}

function renderDossierView(dossier) {
  const container = document.getElementById('investigation-content-area');
  if (!container) return;

  const node = dossier.node || {};
  const isQuarantined = dossier.isQuarantined;
  const riskScore = node.riskScore || 0;
  const netDelta = (node.totalInflow || 0) - (node.totalOutflow || 0);

  const matchedCase = (dossier.cases && dossier.cases.length > 0) ? dossier.cases[0] : null;
  const caseStatus = matchedCase ? matchedCase.status : 'NEW';

  container.innerHTML = `
    <div class="dossier-grid">
      <!-- Card 1: Identity & Surveillance Summary -->
      <div class="dossier-card">
        <div class="metric-header">
          <span class="metric-title">SUBJECT ACCOUNT IDENTITY</span>
          <span class="metric-badge ${isQuarantined ? 'danger' : 'neutral'}">
            ${isQuarantined ? 'QUARANTINED' : 'ACTIVE'}
          </span>
        </div>
        <div style="font-size: 18px; font-weight: 700; color: var(--text-main); margin-bottom: 2px;">
          ${escapeHtml(node.fullName || node.name || dossier.vpa)}
        </div>
        <div style="font-family: var(--font-mono); font-size: 13px; color: var(--accent-cyan); margin-bottom: 12px;">
          ${escapeHtml(dossier.vpa)}
        </div>

        <div class="signals-breakdown">
          <div class="signal-row">
            <span>Associated Bank:</span>
            <span class="signal-pts">${escapeHtml(node.bank || 'UPI')}</span>
          </div>
          <div class="signal-row">
            <span>Primary Location:</span>
            <span class="signal-pts">📍 ${escapeHtml(node.location || 'India')}</span>
          </div>
          <div class="signal-row">
            <span>Net Financial Balance Delta:</span>
            <span class="signal-pts" style="color: ${netDelta >= 0 ? 'var(--accent-success)' : 'var(--accent-danger)'}">
              ₹${Math.round(netDelta).toLocaleString('en-IN')}
            </span>
          </div>
          <div class="signal-row">
            <span>Total Inflow (Settled):</span>
            <span class="signal-pts">₹${Math.round(node.totalInflow || 0).toLocaleString('en-IN')}</span>
          </div>
          <div class="signal-row">
            <span>Total Outflow (Drained):</span>
            <span class="signal-pts">₹${Math.round(node.totalOutflow || 0).toLocaleString('en-IN')}</span>
          </div>
        </div>

        <div style="margin-top: 14px; display: flex; gap: 8px;">
          <button class="btn ${isQuarantined ? 'btn-secondary' : 'btn-danger'} btn-sm" onclick="toggleAccountQuarantine('${escapeHtml(dossier.vpa)}')">
            ${isQuarantined ? '🔓 Lift Quarantine' : '🚨 Quarantine Account'}
          </button>
          <button class="btn btn-secondary btn-sm" onclick="focusNetworkVpa('${escapeHtml(dossier.vpa)}'); switchTab('tab-network-intelligence');">
            🕸️ View on Graph
          </button>
        </div>
      </div>

      <!-- Card 2: Risk Scoring & Contributing Signals -->
      <div class="dossier-card">
        <div class="metric-header">
          <span class="metric-title">COMPOSITE RISK MODEL EVALUATION</span>
          <span class="severity-pill ${riskScore >= 85 ? 'critical' : riskScore >= 70 ? 'high' : 'medium'}">
            Score ${riskScore}/100
          </span>
        </div>

        <div class="risk-bar" style="width: 100%; height: 8px; margin: 10px 0 14px 0;">
          <div class="risk-bar-fill ${riskScore >= 85 ? 'critical' : 'high'}" style="width: ${riskScore}%;"></div>
        </div>

        <div style="font-size: 11px; font-weight: 600; color: var(--text-secondary); margin-bottom: 6px;">
          Contributing Explainable Signals:
        </div>
        <div class="signals-breakdown">
          ${(matchedCase && matchedCase.riskBreakdown && matchedCase.riskBreakdown.length > 0)
            ? matchedCase.riskBreakdown.map(b => `
                <div class="signal-row">
                  <span>${escapeHtml(b.description)}</span>
                  <span class="signal-pts">+${b.points} pts</span>
                </div>
              `).join('')
            : `<div class="signal-row"><span>Baseline Risk Evaluation</span><span class="signal-pts">${riskScore} pts</span></div>`
          }
        </div>

        <!-- Case Status Transition -->
        <div style="margin-top: 14px; padding-top: 12px; border-top: 1px solid var(--border-subtle);">
          <div style="font-size: 11px; font-weight: 600; color: var(--text-secondary); margin-bottom: 6px;">
            Investigation Lifecycle Status:
          </div>
          <div class="segmented-control">
            <button class="seg-btn ${caseStatus === 'NEW' ? 'active' : ''}" onclick="updateInvestigationStatus('${matchedCase ? matchedCase.caseId : ''}', 'NEW')">New</button>
            <button class="seg-btn ${caseStatus === 'INVESTIGATING' ? 'active' : ''}" onclick="updateInvestigationStatus('${matchedCase ? matchedCase.caseId : ''}', 'INVESTIGATING')">Investigating</button>
            <button class="seg-btn ${caseStatus === 'ESCALATED' ? 'active' : ''}" onclick="updateInvestigationStatus('${matchedCase ? matchedCase.caseId : ''}', 'ESCALATED')">Escalated</button>
            <button class="seg-btn ${caseStatus === 'RESOLVED' ? 'active' : ''}" onclick="updateInvestigationStatus('${matchedCase ? matchedCase.caseId : ''}', 'RESOLVED')">Resolved</button>
          </div>
        </div>
      </div>

      <!-- Card 3: Counter-Party Graph Connections -->
      <div class="dossier-card full-width">
        <div class="panel-header" style="padding: 0 0 10px 0;">
          <h3>Immediate Counter-Party Transaction Flows</h3>
        </div>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px;">
          <div>
            <div style="font-size: 11px; font-weight: 600; color: var(--accent-blue); margin-bottom: 6px;">
              &darr; Received Funds From (Inbound Remitters):
            </div>
            <div class="signals-breakdown">
              ${(dossier.counterparties.receivedFrom || []).length > 0
                ? dossier.counterparties.receivedFrom.map(e => `
                    <div class="signal-row">
                      <span>${escapeHtml(e.source)}</span>
                      <span class="signal-pts">₹${e.amount.toLocaleString('en-IN')}</span>
                    </div>
                  `).join('')
                : '<div>No recent recorded inbound inflows</div>'
              }
            </div>
          </div>

          <div>
            <div style="font-size: 11px; font-weight: 600; color: var(--accent-danger); margin-bottom: 6px;">
              &uarr; Drained Funds To (Outbound Beneficiaries):
            </div>
            <div class="signals-breakdown">
              ${(dossier.counterparties.sentTo || []).length > 0
                ? dossier.counterparties.sentTo.map(e => `
                    <div class="signal-row">
                      <span>${escapeHtml(e.target)}</span>
                      <span class="signal-pts">₹${e.amount.toLocaleString('en-IN')}</span>
                    </div>
                  `).join('')
                : '<div>No recent recorded outbound outflows</div>'
              }
            </div>
          </div>
        </div>
      </div>
    </div>
  `;
}

async function toggleAccountQuarantine(vpa) {
  try {
    const res = await fetch(`/api/account/${encodeURIComponent(vpa)}/quarantine`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ reason: 'Analyst SOC Manual Action', analyst: 'Lead Investigator' })
    });
    const data = await res.json();
    showToast(data.isQuarantined ? `Quarantined account: ${vpa}` : `Released quarantine on ${vpa}`);
    investigateAccount(vpa);
  } catch (err) {
    showToast(`Failed to update quarantine: ${err.message}`);
  }
}

async function updateInvestigationStatus(caseId, status) {
  if (!caseId) {
    showToast('No active case registered for this account yet');
    return;
  }
  try {
    await fetch('/api/cases/status', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ caseId, status, analyst: 'Lead Investigator' })
    });
    showToast(`Case ${caseId} updated to ${status}`);
    if (appState.selectedAccountVpa) investigateAccount(appState.selectedAccountVpa);
  } catch (err) {
    showToast(`Failed to update case: ${err.message}`);
  }
}

// ========================================================
// 7. SIMULATION LAB & ATTACK INJECTORS
// ========================================================
async function triggerSimulation(scenario) {
  try {
    logSim(`[SIMULATOR] Triggering scenario: ${scenario}...`);
    const res = await fetch(`/api/simulate/${scenario}`);
    const data = await res.json();
    logSim(`[SIMULATOR] Scenario ${scenario} injected! Tag: ${data.tag || 'OK'}`);
    showToast(`⚡ Injected Scenario: ${scenario.replace(/-/g, ' ').toUpperCase()}`);
  } catch (err) {
    logSim(`[ERROR] Failed to inject scenario: ${err.message}`);
  }
}

function triggerQuickScenario(scen) {
  triggerSimulation(scen);
}

function logSim(msg) {
  const terminal = document.getElementById('sim-log-terminal');
  if (!terminal) return;
  const line = document.createElement('div');
  line.className = 'log-line';
  line.innerText = `[${new Date().toLocaleTimeString()}] ${msg}`;
  terminal.appendChild(line);
  terminal.scrollTop = terminal.scrollHeight;
}

async function setStreamSpeed(speedStr, btnEl) {
  document.querySelectorAll('.speed-selector .seg-btn').forEach(b => b.classList.remove('active'));
  if (btnEl) btnEl.classList.add('active');
  try {
    await fetch(`/api/speed?val=${speedStr}`);
    appState.streamSpeed = speedStr;
    showToast(`Replay speed set to ${speedStr}`);
  } catch (_) {}
}

async function togglePauseStream() {
  appState.isPaused = !appState.isPaused;
  const url = appState.isPaused ? '/api/stream/pause' : '/api/stream/resume';
  await fetch(url, { method: 'POST' });

  const label = document.getElementById('pause-label');
  const icon = document.getElementById('pause-icon');
  const simBtn = document.getElementById('sim-pause-btn');

  if (appState.isPaused) {
    if (label) label.innerText = 'Resume';
    if (icon) icon.innerText = '▶️';
    if (simBtn) simBtn.innerText = 'Resume Stream';
    showToast('Stream paused');
  } else {
    if (label) label.innerText = 'Pause';
    if (icon) icon.innerText = '⏸';
    if (simBtn) simBtn.innerText = 'Pause Stream';
    showToast('Stream resumed');
  }
}

async function resetStreamState() {
  if (confirm('Are you sure you want to reset all transactions, alerts, and graph state?')) {
    await fetch('/api/stream/reset', { method: 'POST' });
    appState.transactions = [];
    appState.alerts = [];
    appState.cases = [];
    appState.stats.streamIngestionCounter = 0;
    appState.stats.cumulativeVolume = 0;
    updateCommandKPIs();
    renderAllTransactionsTable();
    renderAllAlertsFeed();
    refreshGraphData();
    showToast('System state reset successfully');
  }
}

// ========================================================
// 8. LIVE TRANSACTION LEDGER & TABLE
// ========================================================
function renderLiveTxItem(tx) {
  const feed = document.getElementById('command-tx-feed');
  if (!feed) return;

  const item = document.createElement('div');
  item.className = 'flow-routing-box';
  item.style.marginBottom = '6px';
  item.innerHTML = `
    <div style="display: flex; justify-content: space-between; font-size: 11px;">
      <div>
        <span style="font-weight: 600;">${escapeHtml(tx.sender_name)}</span>
        <span style="color: var(--text-muted);">&rarr;</span>
        <span style="font-weight: 600;">${escapeHtml(tx.receiver_name)}</span>
      </div>
      <div style="font-family: var(--font-mono); font-weight: 700; color: var(--accent-cyan);">
        ₹${(tx.amount || 0).toLocaleString('en-IN')}
      </div>
    </div>
    <div style="display: flex; gap: 8px; font-size: 10px; color: var(--text-muted); margin-top: 3px;">
      <span class="badge-status ${tx.status === 'SUCCESS' ? 'status-success' : 'status-failed'}">${tx.status}</span>
      <span>🏛️ ${escapeHtml(tx.bank_code || 'UPI')}</span>
      <span>📍 ${escapeHtml(tx.location || 'India')}</span>
      <span style="font-family: var(--font-mono);">${escapeHtml(tx.transaction_id)}</span>
    </div>
  `;

  feed.prepend(item);
  if (feed.children.length > 25) feed.lastChild.remove();
}

function renderAllTransactionsTable() {
  const tbody = document.getElementById('tx-table-body');
  if (!tbody) return;
  tbody.innerHTML = '';
  appState.transactions.slice(0, 100).forEach(tx => renderTxTableRow(tx, false));
}

function renderTxTableRow(tx, prepend = false) {
  const tbody = document.getElementById('tx-table-body');
  if (!tbody) return;

  // Filter check
  if (appState.currentTxFilter !== 'ALL') {
    if (appState.currentTxFilter === 'SUCCESS' && tx.status !== 'SUCCESS') return;
    if (appState.currentTxFilter === 'FAILED' && tx.status !== 'FAILED') return;
    if (appState.currentTxFilter === 'HIGH_VAL' && (tx.amount || 0) < 40000) return;
  }

  if (appState.currentTxSearch) {
    const q = appState.currentTxSearch.toLowerCase();
    const str = `${tx.sender_name} ${tx.sender_vpa} ${tx.receiver_name} ${tx.receiver_vpa} ${tx.bank_code} ${tx.location} ${tx.transaction_id}`.toLowerCase();
    if (!str.includes(q)) return;
  }

  const tr = document.createElement('tr');
  tr.innerHTML = `
    <td class="mono">${new Date().toLocaleTimeString()}</td>
    <td class="mono">${escapeHtml(tx.transaction_id)}</td>
    <td>
      <div><strong>${escapeHtml(tx.sender_name)}</strong></div>
      <div class="mono" style="font-size: 10px; color: var(--text-muted);">${escapeHtml(tx.sender_vpa)}</div>
    </td>
    <td style="color: var(--accent-cyan);">&rarr;</td>
    <td>
      <div><strong>${escapeHtml(tx.receiver_name)}</strong></div>
      <div class="mono" style="font-size: 10px; color: var(--text-muted);">${escapeHtml(tx.receiver_vpa)}</div>
    </td>
    <td class="mono" style="font-weight: 700;">₹${(tx.amount || 0).toLocaleString('en-IN', { minimumFractionDigits: 2 })}</td>
    <td><span class="badge-status ${tx.status === 'SUCCESS' ? 'status-success' : 'status-failed'}">${tx.status}</span></td>
    <td>${escapeHtml(tx.bank_code || 'UPI')}</td>
    <td>📍 ${escapeHtml(tx.location || 'India')}</td>
    <td>
      <button class="btn btn-secondary btn-xs" onclick="openInvestigationFor('${escapeHtml(tx.sender_vpa)}')">
        Audit
      </button>
    </td>
  `;

  if (prepend) {
    tbody.prepend(tr);
    if (tbody.children.length > 100) tbody.lastChild.remove();
  } else {
    tbody.appendChild(tr);
  }
}

function setTxStatusFilter(filter, btnEl) {
  appState.currentTxFilter = filter;
  document.querySelectorAll('#tab-live-transactions .seg-btn').forEach(b => b.classList.remove('active'));
  if (btnEl) btnEl.classList.add('active');
  renderAllTransactionsTable();
}

function onTxTableFilter() {
  const input = document.getElementById('tx-search-input');
  appState.currentTxSearch = input ? input.value.trim() : '';
  renderAllTransactionsTable();
}

// ========================================================
// 9. FRAUD ALERTS RENDERING & EXPORTS
// ========================================================
function renderAlertItem(alert, isLive = false) {
  // Command Center Mini Feed
  const cmdFeed = document.getElementById('command-alerts-feed');
  if (cmdFeed) {
    const placeholder = cmdFeed.querySelector('.empty-placeholder');
    if (placeholder) placeholder.remove();

    const card = buildAlertCardEl(alert);
    cmdFeed.prepend(card);
    if (cmdFeed.children.length > 20) cmdFeed.lastChild.remove();
  }

  // Full Feed
  if (appState.activeTab === 'tab-fraud-alerts') {
    renderAllAlertsFeed();
  }
}

function renderAllAlertsFeed() {
  const container = document.getElementById('full-alerts-feed');
  if (!container) return;

  const filtered = appState.alerts.filter(a => {
    if (appState.currentAlertFilter === 'ALL') return true;
    if (appState.currentAlertFilter === 'CRITICAL') return a.severity === 'CRITICAL';
    return a.rule_code === appState.currentAlertFilter;
  });

  container.innerHTML = '';
  if (filtered.length === 0) {
    container.innerHTML = `
      <div class="empty-placeholder" style="grid-column: 1 / -1;">
        <div class="placeholder-icon">🛡️</div>
        <div class="placeholder-title">No Alerts in Category "${appState.currentAlertFilter}"</div>
      </div>
    `;
    return;
  }

  filtered.forEach(alert => {
    container.appendChild(buildAlertCardEl(alert));
  });
}

function buildAlertCardEl(alert) {
  const card = document.createElement('div');
  const isCrit = alert.severity === 'CRITICAL';
  card.className = `alert-card ${isCrit ? 'critical' : alert.severity === 'HIGH' ? 'high' : 'medium'}`;

  card.innerHTML = `
    <div class="alert-card-top">
      <div>
        <span class="severity-pill ${isCrit ? 'critical' : 'high'}">${alert.severity}</span>
        <span class="rule-code-name">${escapeHtml(alert.rule_code)}</span>
      </div>
      <div class="risk-meter">
        <div class="risk-bar">
          <div class="risk-bar-fill ${isCrit ? 'critical' : 'high'}" style="width: ${alert.risk_score}%;"></div>
        </div>
        <span class="risk-score-badge">${alert.risk_score}/100</span>
      </div>
    </div>

    <div class="flow-routing-box">
      <div class="flow-step-row">
        <div class="node-entity">
          <span class="role-tag victim">SOURCE</span>
          <span style="font-weight: 600;">${escapeHtml(alert.source_vpa || 'Victim Remitter')}</span>
        </div>
      </div>
      <div class="flow-connector">
        <div class="connector-line"></div>
        <span>&darr; ${alert.details}</span>
        <div class="connector-line"></div>
      </div>
      <div class="flow-step-row">
        <div class="node-entity">
          <span class="role-tag mule">SUSPECT MULE</span>
          <span style="font-weight: 700; color: var(--accent-critical);">${escapeHtml(alert.suspect_name)} (${escapeHtml(alert.suspect_vpa)})</span>
        </div>
        <span class="mono" style="font-weight: 700;">₹${(alert.amount_drained || 0).toLocaleString('en-IN')}</span>
      </div>
    </div>

    <!-- Explainable Signal Breakdown -->
    ${alert.risk_breakdown && alert.risk_breakdown.length > 0 ? `
      <div class="signals-breakdown">
        ${alert.risk_breakdown.slice(0, 3).map(b => `
          <div class="signal-row">
            <span>${escapeHtml(b.description)}</span>
            <span class="signal-pts">+${b.points} pts</span>
          </div>
        `).join('')}
      </div>
    ` : ''}

    <div class="alert-card-footer">
      <div class="meta-tags">
        <span>🏛️ ${escapeHtml(alert.bank || 'UPI')}</span>
        <span>📍 ${escapeHtml(alert.location || 'India')}</span>
        <span>🕒 ${escapeHtml(alert.alert_time)}</span>
      </div>
      <div class="alert-actions">
        <button class="btn btn-secondary btn-xs" onclick="openInvestigationFor('${escapeHtml(alert.suspect_vpa)}')">
          Investigate
        </button>
        <button class="btn btn-danger btn-xs" onclick="toggleAccountQuarantine('${escapeHtml(alert.suspect_vpa)}')">
          Quarantine
        </button>
      </div>
    </div>
  `;
  return card;
}

function setAlertsFilter(filter, btnEl) {
  appState.currentAlertFilter = filter;
  document.querySelectorAll('#tab-fraud-alerts .seg-btn').forEach(b => b.classList.remove('active'));
  if (btnEl) btnEl.classList.add('active');
  renderAllAlertsFeed();
}

function exportAlerts(format) {
  window.open(`/api/export?format=${format}`, '_blank');
}

// ========================================================
// 10. REAL-TIME CANVAS CHART ENGINE
// ========================================================
function renderVolumeChart() {
  const canvas = document.getElementById('chart-volume');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  const { width, height } = canvas;

  ctx.clearRect(0, 0, width, height);

  const samples = appState.volumeHistory;
  if (samples.length < 2) return;

  const maxVol = Math.max(...samples.map(s => s.volume), 80000);

  ctx.beginPath();
  ctx.strokeStyle = '#00e5ff';
  ctx.lineWidth = 2.5;

  samples.forEach((s, idx) => {
    const x = (idx / (samples.length - 1)) * (width - 40) + 20;
    const y = height - 20 - (s.volume / maxVol) * (height - 40);
    if (idx === 0) ctx.moveTo(x, y);
    else ctx.lineTo(x, y);
  });
  ctx.stroke();

  // Gradient under curve
  ctx.lineTo(width - 20, height - 20);
  ctx.lineTo(20, height - 20);
  ctx.closePath();
  const grad = ctx.createLinearGradient(0, 0, 0, height);
  grad.addColorStop(0, 'rgba(0, 229, 255, 0.25)');
  grad.addColorStop(1, 'rgba(0, 229, 255, 0.0)');
  ctx.fillStyle = grad;
  ctx.fill();
}

function renderSeverityChart() {
  const canvas = document.getElementById('chart-severity');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  const { width, height } = canvas;

  ctx.clearRect(0, 0, width, height);

  const crit = appState.alerts.filter(a => a.severity === 'CRITICAL').length;
  const high = appState.alerts.filter(a => a.severity === 'HIGH').length;
  const med = appState.alerts.filter(a => a.severity === 'MEDIUM').length;
  const total = crit + high + med || 1;

  const data = [
    { label: 'Critical (≥85)', val: crit, color: '#ff1744' },
    { label: 'High (70-84)', val: high, color: '#ef4444' },
    { label: 'Medium (50-69)', val: med, color: '#f59e0b' }
  ];

  let startAngle = -Math.PI / 2;
  const cx = width / 3;
  const cy = height / 2;
  const radius = Math.min(cx, cy) - 15;

  data.forEach((d) => {
    const slice = (d.val / total) * Math.PI * 2;
    ctx.beginPath();
    ctx.arc(cx, cy, radius, startAngle, startAngle + slice);
    ctx.arc(cx, cy, radius - 16, startAngle + slice, startAngle, true);
    ctx.closePath();
    ctx.fillStyle = d.color;
    ctx.fill();
    startAngle += slice;
  });

  // Legend
  data.forEach((d, i) => {
    const lx = width * 0.58;
    const ly = 50 + i * 36;
    ctx.fillStyle = d.color;
    ctx.fillRect(lx, ly, 10, 10);
    ctx.fillStyle = '#ffffff';
    ctx.font = '11px Inter';
    ctx.fillText(`${d.label}: ${d.val}`, lx + 16, ly + 9);
  });
}

async function loadAnalyticsData() {
  try {
    const res = await fetch('/api/analytics');
    const data = await res.json();
    renderBankChart(data.bankDistribution || {});
    renderGeoChart(data.cityDistribution || {});
    renderRulesTable(data.rulePerformance || {});
  } catch (_) {}
}

function renderBankChart(bankDist) {
  const canvas = document.getElementById('chart-banks');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  const { width, height } = canvas;
  ctx.clearRect(0, 0, width, height);

  const entries = Object.entries(bankDist).sort((a, b) => b[1] - a[1]).slice(0, 6);
  if (entries.length === 0) return;

  const maxVal = Math.max(...entries.map(e => e[1]));
  const barWidth = 42;
  const gap = 24;
  const startX = 30;

  entries.forEach(([bank, count], i) => {
    const x = startX + i * (barWidth + gap);
    const barH = (count / maxVal) * (height - 60);
    const y = height - 30 - barH;

    ctx.fillStyle = '#00e5ff';
    ctx.fillRect(x, y, barWidth, barH);

    ctx.fillStyle = '#ffffff';
    ctx.font = '10px JetBrains Mono';
    ctx.textAlign = 'center';
    ctx.fillText(count, x + barWidth / 2, y - 6);
    ctx.fillText(bank, x + barWidth / 2, height - 12);
  });
}

function renderGeoChart(cityDist) {
  const canvas = document.getElementById('chart-geo');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  const { width, height } = canvas;
  ctx.clearRect(0, 0, width, height);

  const entries = Object.entries(cityDist).sort((a, b) => b[1] - a[1]).slice(0, 6);
  if (entries.length === 0) return;

  const maxVal = Math.max(...entries.map(e => e[1]));
  const barWidth = 42;
  const gap = 24;
  const startX = 30;

  entries.forEach(([city, count], i) => {
    const x = startX + i * (barWidth + gap);
    const barH = (count / maxVal) * (height - 60);
    const y = height - 30 - barH;

    ctx.fillStyle = '#a855f7';
    ctx.fillRect(x, y, barWidth, barH);

    ctx.fillStyle = '#ffffff';
    ctx.font = '10px JetBrains Mono';
    ctx.textAlign = 'center';
    ctx.fillText(count, x + barWidth / 2, y - 6);
    ctx.fillText(city, x + barWidth / 2, height - 12);
  });
}

function renderRulesTable(ruleCounts) {
  const container = document.getElementById('analytics-rules-table-container');
  if (!container) return;

  const rows = Object.entries(ruleCounts).map(([rule, cnt]) => `
    <tr>
      <td class="mono" style="font-weight: 600; color: var(--accent-cyan);">${escapeHtml(rule)}</td>
      <td class="mono" style="font-weight: 700;">${cnt} Detections</td>
      <td><span class="badge-status status-success">ACTIVE &amp; ENFORCED</span></td>
      <td>Stateful In-Memory CEP Sliding Window</td>
    </tr>
  `).join('');

  container.innerHTML = `
    <table class="soc-table">
      <thead>
        <tr>
          <th>Fraud Detection Algorithm</th>
          <th>Detections</th>
          <th>Rule Status</th>
          <th>Processing Method</th>
        </tr>
      </thead>
      <tbody>
        ${rows || '<tr><td colspan="4">No rule incidents logged yet</td></tr>'}
      </tbody>
    </table>
  `;
}

// ========================================================
// 11. GENERAL UTILITIES
// ========================================================
function showToast(msg) {
  const container = document.getElementById('toast-container');
  if (!container) return;
  const toast = document.createElement('div');
  toast.className = 'toast';
  toast.innerHTML = `<span>🛡️</span> <span>${escapeHtml(msg)}</span>`;
  container.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(12px)';
    setTimeout(() => toast.remove(), 250);
  }, 3500);
}

function escapeHtml(str) {
  if (typeof str !== 'string') return String(str || '');
  return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}
