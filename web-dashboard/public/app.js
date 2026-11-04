/**
 * UPI Sentinel - Enterprise SOC Dashboard Controller
 * Real-Time CEP Stream Consumer, Threat Ledger & Theme Controller
 */

// Global State
let totalTx = 0;
let totalAlerts = 0;
let totalCrit = 0;
let totalVolume = 0;
const trackedMules = new Set();
const allAlerts = [];
const allTransactions = [];
const seenAlertIds = new Set();

let isStreamPaused = false;
let activeFilter = 'all';
let currentSearchQuery = '';

// ========================================================
// 1. Theme Controller (Light / Dark Mode)
// ========================================================

function initTheme() {
  const savedTheme = localStorage.getItem('sentinel_theme') || 'light';
  applyTheme(savedTheme);
}

function applyTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  localStorage.setItem('sentinel_theme', theme);

  const themeLabel = document.getElementById('theme-label');
  if (themeLabel) {
    themeLabel.innerText = theme === 'dark' ? 'Light' : 'Dark';
  }
}

function toggleTheme() {
  const current = document.documentElement.getAttribute('data-theme') || 'light';
  const target = current === 'dark' ? 'light' : 'dark';
  applyTheme(target);
  showToast(`Switched to ${target.toUpperCase()} theme`);
}

// ========================================================
// 2. Live System Clock & Metrics
// ========================================================

function updateClock() {
  const clockEl = document.getElementById('live-clock');
  if (!clockEl) return;
  const now = new Date();
  const istStr = now.toLocaleTimeString('en-IN', { hour12: false });
  clockEl.innerText = `${istStr} IST`;
}
setInterval(updateClock, 1000);

// Throughput Calculator (TPS)
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
  if (badge) badge.innerText = `${totalAlerts} Alerts`;
}

// ========================================================
// 3. Data Fetching & Stream Intake
// ========================================================

window.addEventListener('DOMContentLoaded', () => {
  initTheme();
  updateClock();

  // Bootstrap with existing alerts from REST API
  fetch('/api/alerts')
    .then(r => r.json())
    .then(alerts => {
      if (!Array.isArray(alerts) || alerts.length === 0) return;
      alerts.forEach(alert => {
        if (seenAlertIds.has(alert.alert_id)) return;
        seenAlertIds.add(alert.alert_id);
        allAlerts.push(alert);
        totalAlerts++;
        if (alert.severity === 'CRITICAL') totalCrit++;
        trackedMules.add(alert.suspect_vpa);
      });
      allAlerts.sort((a, b) => (b.alert_id > a.alert_id ? 1 : -1));
      updateMetrics();
      renderAlerts();
    })
    .catch(() => {});
});

// Server-Sent Events Listener
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

  if (seenAlertIds.has(alert.alert_id)) return;
  seenAlertIds.add(alert.alert_id);

  totalAlerts++;
  if (alert.severity === 'CRITICAL') totalCrit++;
  trackedMules.add(alert.suspect_vpa);

  allAlerts.unshift(alert);
  if (allAlerts.length > 200) allAlerts.pop();

  updateMetrics();
  renderAlerts();

  // Subtle header highlight on new detection
  const panelHeader = document.querySelector('.alerts-section .panel-header');
  if (panelHeader) {
    panelHeader.classList.add('alert-flash');
    setTimeout(() => panelHeader.classList.remove('alert-flash'), 1500);
  }
});

// ========================================================
// 4. Rendering Engine
// ========================================================

function renderTransaction(tx) {
  const feed = document.getElementById('tx-feed');
  if (!feed) return;

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
  if (feed.children.length > 60) feed.lastChild.remove();
}

function renderAlerts() {
  const feed = document.getElementById('alerts-feed');
  if (!feed) return;

  const placeholder = document.getElementById('alerts-placeholder');
  if (placeholder && allAlerts.length > 0) {
    placeholder.remove();
  }

  const filtered = allAlerts.filter(a => {
    if (activeFilter === 'all') return true;
    if (activeFilter === 'CRITICAL') return a.severity === 'CRITICAL';
    return a.rule_code === activeFilter;
  });

  feed.innerHTML = '';

  if (filtered.length === 0) {
    feed.innerHTML = `
      <div class="empty-placeholder">
        <div class="placeholder-icon">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
        </div>
        <div class="placeholder-title">No Incidents in Filter "${activeFilter}"</div>
        <p class="placeholder-text">Evaluating live transactions for matching pattern signatures...</p>
      </div>
    `;
    return;
  }

  filtered.forEach(alert => {
    const card = document.createElement('div');
    const isCritical = alert.severity === 'CRITICAL';
    card.className = `alert-card ${isCritical ? 'critical-threat' : 'high-threat'}`;

    const sevPill = isCritical
      ? '<span class="severity-pill critical">CRITICAL</span>'
      : '<span class="severity-pill high">HIGH</span>';

    const riskScore = alert.risk_score || 85;
    const isSmurfing = alert.rule_code === 'FAN_IN_SMURFING_AGGREGATOR';

    let flowHtml = '';
    if (isSmurfing) {
      flowHtml = `
        <div class="laundering-flow-box">
          <div class="flow-node-row">
            <div class="node-entity">
              <span class="node-role-badge victim">VICTIMS</span>
              <div class="node-name-vpa">
                <span class="node-name">${alert.distinct_senders_count || 3} Remitters</span>
                <span class="node-vpa">Multiple Compromised Accounts</span>
              </div>
            </div>
            <span class="meta-pill">Window &le; 120s</span>
          </div>

          <div class="flow-hop-connector">
            <div class="hop-line"></div>
            <div class="hop-telemetry critical-speed">
              &darr; Smurfing Inflow Aggregation: ₹${(alert.amount_drained || 0).toLocaleString('en-IN')}
            </div>
            <div class="hop-line"></div>
          </div>

          <div class="flow-node-row">
            <div class="node-entity">
              <span class="node-role-badge mule">MULE AGGREGATOR</span>
              <div class="node-name-vpa">
                <span class="node-name">${escapeHtml(alert.suspect_name)}</span>
                <span class="node-vpa">&lt;${escapeHtml(alert.suspect_vpa)}&gt;</span>
              </div>
            </div>
            <span class="meta-pill amount">₹${(alert.amount_drained || 0).toLocaleString('en-IN')}</span>
          </div>
        </div>
      `;
    } else {
      flowHtml = `
        <div class="laundering-flow-box">
          <!-- Step 1: Inflow Remitter -->
          <div class="flow-node-row">
            <div class="node-entity">
              <span class="node-role-badge victim">REMITTER</span>
              <div class="node-name-vpa">
                <span class="node-name">${escapeHtml(alert.source_vpa || 'Compromised Remitter')}</span>
              </div>
            </div>
            <span class="meta-pill">Source</span>
          </div>

          <!-- Hop 1 -> 2: Rapid In-to-Out Velocity -->
          <div class="flow-hop-connector">
            <div class="hop-line"></div>
            <div class="hop-telemetry ${isCritical ? 'critical-speed' : ''}">
              &darr; Drained ${alert.drain_percentage}% in ${alert.time_to_drain_seconds}s
            </div>
            <div class="hop-line"></div>
          </div>

          <!-- Step 2: Intermediate Mule -->
          <div class="flow-node-row">
            <div class="node-entity">
              <span class="node-role-badge mule">SUSPECT MULE</span>
              <div class="node-name-vpa">
                <span class="node-name">${escapeHtml(alert.suspect_name)}</span>
                <span class="node-vpa">&lt;${escapeHtml(alert.suspect_vpa)}&gt;</span>
              </div>
            </div>
            <span class="meta-pill amount">₹${(alert.amount_drained || 0).toLocaleString('en-IN')}</span>
          </div>

          <!-- Hop 2 -> 3 -->
          <div class="flow-hop-connector">
            <div class="hop-line"></div>
            <div class="hop-telemetry">
              &darr; Immediate Transfer Out
            </div>
            <div class="hop-line"></div>
          </div>

          <!-- Step 3: Off-Ramp Target -->
          <div class="flow-node-row">
            <div class="node-entity">
              <span class="node-role-badge destination">DESTINATION</span>
              <div class="node-name-vpa">
                <span class="node-name">${escapeHtml(alert.target_vpa || 'Cashout Account')}</span>
              </div>
            </div>
            <span class="meta-pill">Exit Channel</span>
          </div>
        </div>
      `;
    }

    card.innerHTML = `
      <div class="alert-card-top">
        <div class="rule-meta-group">
          ${sevPill}
          <span class="rule-code-name">${escapeHtml(alert.rule_code)}</span>
        </div>
        <div class="risk-meter">
          <div class="risk-bar">
            <div class="risk-bar-fill ${isCritical ? 'critical' : 'high'}" style="width: ${riskScore}%;"></div>
          </div>
          <span class="risk-score-badge">Risk ${riskScore}/100</span>
        </div>
      </div>

      ${flowHtml}

      <div class="alert-footer-row">
        <div class="alert-metadata-pills">
          <span class="meta-pill">${alert.bank ? `🏛️ ${escapeHtml(alert.bank)}` : '🏛️ UPI'}</span>
          <span class="meta-pill">${alert.location ? `📍 ${escapeHtml(alert.location)}` : '📍 India'}</span>
          ${alert.time_to_drain_seconds > 0 ? `<span class="meta-pill">⏱️ ${alert.time_to_drain_seconds}s Velocity</span>` : ''}
          <span class="meta-pill">🕒 ${escapeHtml(alert.alert_time || new Date().toLocaleTimeString())}</span>
        </div>
        <button class="btn-quarantine-action" onclick="quarantineMule('${escapeHtml(alert.suspect_vpa)}')">
          Quarantine Account
        </button>
      </div>
    `;

    feed.appendChild(card);
  });
}

// ========================================================
// 5. User Controls & Actions
// ========================================================

function setAlertFilter(filter, btnEl) {
  activeFilter = filter;
  document.querySelectorAll('.seg-btn').forEach(btn => btn.classList.remove('active'));
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

  if (isStreamPaused) {
    if (icon) icon.innerText = '▶️';
    if (label) label.innerText = 'Resume';
    showToast('Live stream rendering paused');
  } else {
    if (icon) icon.innerText = '⏸';
    if (label) label.innerText = 'Pause';
    showToast('Live stream resumed');
  }
}

async function injectMuleAttack() {
  try {
    showToast('⚡ Injected coordinated 3-hop mule attack sequence');
    const res = await fetch('/api/inject-mule');
    if (!res.ok) console.warn('Mule attack trigger HTTP status:', res.status);
  } catch (err) {
    console.error('Failed to trigger mule ring attack:', err);
  }
}

function quarantineMule(vpa) {
  showToast(`Quarantined account: ${vpa}`);
}

function showToast(msg) {
  const container = document.getElementById('toast-container');
  if (!container) return;
  const toast = document.createElement('div');
  toast.className = 'toast';
  toast.innerHTML = `<span>🛡️</span> <span>${escapeHtml(msg)}</span>`;
  container.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(10px)';
    setTimeout(() => toast.remove(), 250);
  }, 3200);
}

function escapeHtml(str) {
  if (typeof str !== 'string') return String(str || '');
  return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}
