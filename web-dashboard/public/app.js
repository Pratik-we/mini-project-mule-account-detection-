/**
 * RippleGuard SOC Dashboard Controller
 * Real-Time Stream Event Broker, CEP Renderer, and Threat Management
 */

let totalTx = 0;
let totalAlerts = 0;
let totalCrit = 0;
let totalVolume = 0;
const trackedMules = new Set();
const allAlerts = [];
const allTransactions = [];
const seenAlertIds = new Set(); // Dedup guard for SSE replays

let isStreamPaused = false;
let activeFilter = 'all';
let currentSearchQuery = '';

// Live Clock
function updateClock() {
  const clockEl = document.getElementById('live-clock');
  if (!clockEl) return;
  const now = new Date();
  const istStr = now.toLocaleTimeString('en-IN', { hour12: false });
  clockEl.innerText = `${istStr} IST`;
}
setInterval(updateClock, 1000);
updateClock();

// TPS Tracker
let lastTxSnapshot = 0;
setInterval(() => {
  const delta = totalTx - lastTxSnapshot;
  lastTxSnapshot = totalTx;
  const tpsEl = document.getElementById('stat-tps');
  if (tpsEl) {
    const tps = (delta / 2).toFixed(1);
    tpsEl.innerText = `${tps} /s`;
  }
}, 2000);

// ── On page load: fetch existing alerts via REST so we never miss anything ──
window.addEventListener('DOMContentLoaded', () => {
  fetch('/api/alerts')
    .then(r => r.json())
    .then(alerts => {
      if (!Array.isArray(alerts) || alerts.length === 0) return;
      // alerts array is newest-first from server
      alerts.forEach(alert => {
        if (seenAlertIds.has(alert.alert_id)) return;
        seenAlertIds.add(alert.alert_id);
        allAlerts.push(alert);
        totalAlerts++;
        if (alert.severity === 'CRITICAL') totalCrit++;
        trackedMules.add(alert.suspect_vpa);
      });
      // Keep newest-first order
      allAlerts.sort((a, b) => (b.alert_id > a.alert_id ? 1 : -1));
      updateMetrics();
      renderAlerts();
    })
    .catch(() => {/* Fail silently — SSE will cover live events */});
});

// Server-Sent Events listener
const evtSource = new EventSource('/api/stream');

evtSource.addEventListener('transaction', (event) => {
  if (isStreamPaused) return;

  const tx = JSON.parse(event.data);
  totalTx++;
  totalVolume += (tx.amount || 0);
  allTransactions.unshift(tx);
  if (allTransactions.length > 500) allTransactions.pop();

  updateMetrics();
  renderTransaction(tx);
});

evtSource.addEventListener('alert', (event) => {
  const alert = JSON.parse(event.data);

  // Dedup: skip if we already ingested this alert via REST bootstrap or SSE replay
  if (seenAlertIds.has(alert.alert_id)) return;
  seenAlertIds.add(alert.alert_id);

  totalAlerts++;
  if (alert.severity === 'CRITICAL') totalCrit++;
  trackedMules.add(alert.suspect_vpa);

  allAlerts.unshift(alert);
  if (allAlerts.length > 200) allAlerts.pop();

  updateMetrics();
  renderAlerts();

  // Flash the alerts panel heading to draw user attention
  const panelHeading = document.querySelector('.alerts-panel .panel-header');
  if (panelHeading) {
    panelHeading.classList.add('alert-flash');
    setTimeout(() => panelHeading.classList.remove('alert-flash'), 1200);
  }
});

function updateMetrics() {
  const statTx = document.getElementById('stat-tx');
  const statVol = document.getElementById('stat-vol');
  const statAlerts = document.getElementById('stat-alerts');
  const statCrit = document.getElementById('stat-crit');
  const statMules = document.getElementById('stat-mules');
  const badge = document.getElementById('alerts-count-badge');

  if (statTx) statTx.innerText = totalTx.toLocaleString('en-IN');
  if (statVol) statVol.innerText = `Total Vol: ₹${Math.round(totalVolume).toLocaleString('en-IN')}`;
  if (statAlerts) statAlerts.innerText = totalAlerts;
  if (statCrit) statCrit.innerText = totalCrit;
  if (statMules) statMules.innerText = trackedMules.size;
  if (badge) badge.innerText = `${totalAlerts} ALERTS`;
}

function renderTransaction(tx) {
  const feed = document.getElementById('tx-feed');
  if (!feed) return;

  // Search filter
  if (currentSearchQuery) {
    const q = currentSearchQuery.toLowerCase();
    const str = `${tx.sender_name} ${tx.sender_vpa} ${tx.receiver_name} ${tx.receiver_vpa} ${tx.bank_code} ${tx.location}`.toLowerCase();
    if (!str.includes(q)) return;
  }

  const item = document.createElement('div');
  item.className = 'tx-item';

  const isSuccess = tx.status === 'SUCCESS';
  const statusBadge = isSuccess 
    ? '<span class="badge-status status-success">SUCCESS</span>' 
    : '<span class="badge-status status-failed">FAILED</span>';

  item.innerHTML = `
    <div class="tx-left">
      <div class="tx-participants">
        <span class="tx-name">${escapeHtml(tx.sender_name || 'Sender')}</span>
        <span class="tx-vpa">(${escapeHtml(tx.sender_vpa)})</span>
        <span class="tx-arrow">&rarr;</span>
        <span class="tx-name">${escapeHtml(tx.receiver_name || 'Receiver')}</span>
        <span class="tx-vpa">(${escapeHtml(tx.receiver_vpa)})</span>
      </div>
      <div class="tx-meta-row">
        ${statusBadge}
        <span class="badge-bank">${escapeHtml(tx.bank_code || 'UPI')}</span>
        <span class="badge-city">📍 ${escapeHtml(tx.location || 'India')}</span>
        <span class="tx-vpa">${escapeHtml(tx.transaction_id)}</span>
      </div>
    </div>
    <div class="tx-right">
      <div class="tx-amount">₹${tx.amount.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</div>
      <div class="tx-time">${new Date().toLocaleTimeString()}</div>
    </div>
  `;

  feed.prepend(item);
  if (feed.children.length > 50) feed.lastChild.remove();
}

function renderAlerts() {
  const feed = document.getElementById('alerts-feed');
  if (!feed) return;

  const placeholder = document.getElementById('alerts-placeholder');
  if (placeholder && allAlerts.length > 0) {
    placeholder.remove();
  }

  // Filter alerts according to active tab
  const filtered = allAlerts.filter(a => {
    if (activeFilter === 'all') return true;
    if (activeFilter === 'CRITICAL') return a.severity === 'CRITICAL';
    return a.rule_code === activeFilter;
  });

  feed.innerHTML = '';

  if (filtered.length === 0) {
    feed.innerHTML = `
      <div class="empty-state">
        <div class="scanner-ring"></div>
        <div class="empty-title">No Alerts in Selected Filter</div>
        <div class="empty-desc">Monitoring incoming stream for ${activeFilter} events...</div>
      </div>
    `;
    return;
  }

  filtered.forEach(alert => {
    const card = document.createElement('div');
    const isCritical = alert.severity === 'CRITICAL';
    card.className = `alert-card ${isCritical ? 'crit-severity' : 'high-severity'}`;

    const sevPill = isCritical 
      ? '<span class="severity-pill pill-critical">CRITICAL</span>' 
      : '<span class="severity-pill pill-high">HIGH</span>';

    const riskScore = alert.risk_score || 85;
    const isSmurfing = alert.rule_code === 'FAN_IN_SMURFING_AGGREGATOR';

    let flowHtml = '';
    if (isSmurfing) {
      flowHtml = `
        <div class="laundering-flow">
          <div class="flow-step">
            <div class="flow-node">
              <span class="node-role role-victim">MULTIPLE VICTIMS</span>
              <span class="node-name">${alert.distinct_senders_count || 3} Remitters</span>
            </div>
            <span class="flow-arrow-row">Aggregation Window &le; 120s</span>
          </div>
          <div class="flow-arrow-row">
            <span>&darr; Aggregated Total: ₹${(alert.amount_drained || alert.total_inflow || 0).toLocaleString('en-IN')}</span>
            <div class="flow-arrow-line"></div>
          </div>
          <div class="flow-step">
            <div class="flow-node">
              <span class="node-role role-mule">🚨 MULE AGGREGATOR</span>
              <span class="node-name">${escapeHtml(alert.suspect_name)}</span>
              <span class="node-vpa">&lt;${escapeHtml(alert.suspect_vpa)}&gt;</span>
            </div>
          </div>
        </div>
      `;
    } else {
      flowHtml = `
        <div class="laundering-flow">
          <div class="flow-step">
            <div class="flow-node">
              <span class="node-role role-victim">VICTIM</span>
              <span class="node-name">${escapeHtml(alert.source_victim || alert.source_vpa || 'Compromised Account')}</span>
            </div>
          </div>
          <div class="flow-arrow-row">
            <span>&darr; Layering Inflow</span>
            <div class="flow-arrow-line"></div>
          </div>
          <div class="flow-step">
            <div class="flow-node">
              <span class="node-role role-mule">🚨 MULE ACCOUNT</span>
              <span class="node-name">${escapeHtml(alert.suspect_name)}</span>
              <span class="node-vpa">&lt;${escapeHtml(alert.suspect_vpa)}&gt;</span>
            </div>
          </div>
          <div class="flow-arrow-row">
            <span>&darr; Rapid Outflow: Drained ${alert.drain_percentage}% in ${alert.time_to_drain_seconds}s</span>
            <div class="flow-arrow-line"></div>
          </div>
          <div class="flow-step">
            <div class="flow-node">
              <span class="node-role role-dest">DESTINATION</span>
              <span class="node-name">${escapeHtml(alert.target_destination || alert.target_vpa || 'Cashout Off-ramp')}</span>
            </div>
          </div>
        </div>
      `;
    }

    card.innerHTML = `
      <div class="alert-card-top">
        <div class="alert-rule-badge">
          ${sevPill}
          <span class="rule-name">${escapeHtml(alert.rule_code)}</span>
        </div>
        <div class="risk-meter">
          <div class="risk-bar-container">
            <div class="risk-bar-fill" style="width: ${riskScore}%;"></div>
          </div>
          <span class="risk-score-text">Risk: ${riskScore}/100</span>
        </div>
      </div>

      ${flowHtml}

      <div class="alert-tags-row">
        <div class="tag-list">
          <span class="info-pill">${alert.bank ? `🏛️ ${escapeHtml(alert.bank)}` : '🏛️ UPI'}</span>
          <span class="info-pill">${alert.location ? `📍 ${escapeHtml(alert.location)}` : '📍 India'}</span>
          ${alert.time_to_drain_seconds > 0 ? `<span class="info-pill">⏱️ ${alert.time_to_drain_seconds}s Drain</span>` : ''}
          <span class="info-pill">₹${(alert.amount_drained || 0).toLocaleString('en-IN')}</span>
          <span class="info-pill">🕒 ${escapeHtml(alert.alert_time || new Date().toLocaleTimeString())}</span>
        </div>
        <button class="btn-quarantine" onclick="quarantineMule('${escapeHtml(alert.suspect_vpa)}')">
          🛡️ Quarantine Account
        </button>
      </div>
    `;

    feed.appendChild(card);
  });
}

function setAlertFilter(filter, btnEl) {
  activeFilter = filter;
  document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
  if (btnEl) btnEl.classList.add('active');
  renderAlerts();
}

function onTxSearch(query) {
  currentSearchQuery = query;
}

function togglePauseStream() {
  isStreamPaused = !isStreamPaused;
  const icon = document.getElementById('pause-icon');
  const label = document.getElementById('pause-label');
  const btn = document.getElementById('btn-pause');

  if (isStreamPaused) {
    if (icon) icon.innerText = '▶️';
    if (label) label.innerText = 'Resume Stream';
    if (btn) btn.style.borderColor = 'var(--accent-amber)';
    showToast('Stream rendering paused on client.');
  } else {
    if (icon) icon.innerText = '⏸';
    if (label) label.innerText = 'Pause Stream';
    if (btn) btn.style.borderColor = '';
    showToast('Stream resumed.');
  }
}

async function injectMuleAttack() {
  try {
    showToast('⚡ Injected coordinated 3-hop mule attack into stream.');
    const res = await fetch('/api/inject-mule');
    if (!res.ok) console.warn('Mule attack trigger HTTP status:', res.status);
  } catch (err) {
    console.error('Failed to trigger mule ring attack:', err);
  }
}

function quarantineMule(vpa) {
  showToast(`🛡️ VPA ${vpa} quarantined across UPI rails and blacklisted.`);
}

function showToast(msg) {
  const container = document.getElementById('toast-container');
  if (!container) return;
  const toast = document.createElement('div');
  toast.className = 'toast';
  toast.innerText = msg;
  container.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(10px)';
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}

function escapeHtml(str) {
  if (typeof str !== 'string') return String(str || '');
  return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}
