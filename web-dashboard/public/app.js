/**
 * Client-Side Stream Event Broker & Dashboard Controller
 * ======================================================
 * Renders real-time transactions from data/transactions.csv
 * and dynamically surfaces stateful money mule alerts.
 */

let totalTx = 0;
let totalAlerts = 0;
let totalCrit = 0;
const trackedMules = new Set();

const evtSource = new EventSource('/api/stream');

evtSource.addEventListener('transaction', (event) => {
  const tx = JSON.parse(event.data);
  totalTx++;
  document.getElementById('stat-tx').innerText = totalTx.toLocaleString();

  const feed = document.getElementById('tx-feed');
  const row = document.createElement('div');
  row.className = 'tx-row';

  const senderDisplay = tx.sender_name && tx.sender_name !== tx.sender_vpa 
    ? `<strong>${tx.sender_name}</strong> <span class="vpa-dim">(${tx.sender_vpa})</span>`
    : `<strong>${tx.sender_vpa}</strong>`;

  const receiverDisplay = tx.receiver_name && tx.receiver_name !== tx.receiver_vpa
    ? `<strong>${tx.receiver_name}</strong> <span class="vpa-dim">(${tx.receiver_vpa})</span>`
    : `<strong>${tx.receiver_vpa}</strong>`;

  const bankBadge = tx.bank_code ? `<span class="badge-bank">${tx.bank_code}</span>` : '';
  const locBadge = tx.location ? `<span class="badge-loc">📍 ${tx.location}</span>` : '';

  row.innerHTML = `
    <div class="tx-main">
      <div class="tx-flow">${senderDisplay} &rarr; ${receiverDisplay}</div>
      <div class="tx-meta">${bankBadge} ${locBadge} <span class="tx-id">${tx.transaction_id}</span></div>
    </div>
    <div class="tx-amount">₹${tx.amount.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</div>
  `;
  feed.prepend(row);
  if (feed.children.length > 50) feed.lastChild.remove();
});

evtSource.addEventListener('alert', (event) => {
  const alert = JSON.parse(event.data);
  totalAlerts++;
  if (alert.severity === 'CRITICAL') totalCrit++;
  trackedMules.add(alert.suspect_vpa);

  document.getElementById('stat-alerts').innerText = totalAlerts;
  document.getElementById('stat-crit').innerText = totalCrit;
  document.getElementById('stat-mules').innerText = trackedMules.size;

  const feed = document.getElementById('alerts-feed');
  const card = document.createElement('div');
  card.className = 'alert-card';

  const badge = alert.severity === 'CRITICAL' 
    ? '<span class="badge-crit">CRITICAL</span>' 
    : '<span class="badge-high">HIGH</span>';

  card.innerHTML = `
    <div class="alert-top">
      <span>${badge} <strong>${alert.rule_code}</strong></span>
      <span class="alert-risk">Risk: ${alert.risk_score}/100</span>
    </div>
    <div class="alert-desc">
      <div class="mule-highlight">🚨 Suspect: <strong>${alert.suspect_name}</strong> &lt;${alert.suspect_vpa}&gt;</div>
      ${alert.source_vpa ? `<div><strong>Source Victim:</strong> ${alert.source_vpa}</div>` : ''}
      ${alert.target_vpa ? `<div><strong>Destination:</strong> ${alert.target_vpa}</div>` : ''}
      ${alert.time_to_drain_seconds > 0 ? `<div><strong>Velocity:</strong> Drained in <strong>${alert.time_to_drain_seconds}s</strong> (${alert.drain_percentage}%)</div>` : ''}
      <div class="alert-details-text">${alert.details}</div>
      <div class="alert-footer">${alert.bank ? `Bank: ${alert.bank} | ` : ''}${alert.location ? `City: ${alert.location} | ` : ''}Time: ${alert.alert_time}</div>
    </div>
  `;
  feed.prepend(card);
  if (feed.children.length > 30) feed.lastChild.remove();
});

async function injectMuleAttack() {
  try {
    await fetch('/api/inject-mule');
  } catch (err) {
    console.error('Failed to trigger mule ring attack:', err);
  }
}
