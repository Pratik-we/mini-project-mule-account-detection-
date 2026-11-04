/**
 * Ingestion: Dataset-Driven Stream Simulator
 * ==========================================
 * Reads the actual transactions dataset (data/transactions.csv)
 * and streams it in real-time to the processing engine & dashboard.
 */

const fs = require('fs');
const path = require('path');

const CSV_PATH = path.join(__dirname, '..', 'data', 'transactions.csv');

let cachedTransactions = [];
let currentIndex = 0;

function parseCSVLine(line) {
  return line.split(/,(?=(?:(?:[^"]*"){2})*[^"]*$)/).map(v => v.replace(/^"|"$/g, '').trim());
}

function loadDataset() {
  if (!fs.existsSync(CSV_PATH)) {
    console.error(`[Stream Simulator] transactions.csv not found at: ${CSV_PATH}`);
    return [];
  }

  const content = fs.readFileSync(CSV_PATH, 'utf8');
  const lines = content.split(/\r?\n/).filter(l => l.trim().length > 0);

  if (lines.length < 2) return [];

  const headers = parseCSVLine(lines[0]);
  const txList = [];

  for (let i = 1; i < lines.length; i++) {
    const values = parseCSVLine(lines[i]);
    if (values.length < 7) continue;

    const row = {};
    headers.forEach((h, idx) => {
      row[h] = values[idx] !== undefined ? values[idx] : '';
    });

    const amount = parseFloat(String(row.amount || '0').replace(/[^0-9.-]+/g, '')) || 0;
    const timeRaw = row.timestamp || new Date().toISOString();
    let timeMs = Date.now();
    const parsedDate = Date.parse(timeRaw.includes('T') ? timeRaw : timeRaw.replace(' ', 'T') + 'Z');
    if (!isNaN(parsedDate)) {
      timeMs = parsedDate;
    }

    txList.push({
      transaction_id: row.transaction_id || `TXN-${i}`,
      timestamp: timeRaw,
      time_ms: timeMs,
      sender_name: row.sender_name || 'Sender',
      sender_vpa: (row.sender_vpa || 'sender@upi').toLowerCase(),
      receiver_name: row.receiver_name || 'Receiver',
      receiver_vpa: (row.receiver_vpa || 'receiver@upi').toLowerCase(),
      amount: amount,
      status: (row.status || 'SUCCESS').toUpperCase(),
      bank_code: row.bank_code || 'UPI_NET',
      location: row.location || 'India'
    });
  }

  console.log(`[Stream Simulator] Loaded ${txList.length} transactions from ${path.basename(CSV_PATH)}`);
  return txList;
}

function init() {
  if (cachedTransactions.length === 0) {
    cachedTransactions = loadDataset();
  }
}

function getNextTransaction() {
  init();
  if (cachedTransactions.length === 0) return null;

  const tx = cachedTransactions[currentIndex];
  currentIndex = (currentIndex + 1) % cachedTransactions.length;
  
  // Clone and assign fresh live timestamp for active streaming
  return {
    ...tx,
    stream_time_ms: Date.now()
  };
}

function injectMuleAttack(onTxGenerated) {
  console.log(`\n======================================================`);
  console.log(`⚡ [INJECTOR] TRIGGERING RAPID MULE LAUNDERING CHAIN ⚡`);
  console.log(`======================================================`);

  // Hop 1: Victim -> Mule Tier-1 (Inflow of ₹65,000)
  const tx1 = {
    transaction_id: 'LIVE_MULE_' + Date.now().toString().slice(-6) + '_H1',
    timestamp: new Date().toISOString(),
    time_ms: Date.now(),
    stream_time_ms: Date.now(),
    sender_name: 'Mohanlal Bakshi (Victim)',
    sender_vpa: '8908837379@okaxis',
    receiver_name: 'Mehul Sankaran (Mule Tier-1)',
    receiver_vpa: '7683454560@okaxis',
    amount: 65000.00,
    status: 'SUCCESS',
    bank_code: 'AXIS',
    location: 'Delhi'
  };
  onTxGenerated(tx1);

  // Hop 2: Mule Tier-1 -> Mule Tier-2 (Drained 95% in 2.5s)
  setTimeout(() => {
    const tx2 = {
      transaction_id: 'LIVE_MULE_' + Date.now().toString().slice(-6) + '_H2',
      timestamp: new Date().toISOString(),
      time_ms: Date.now(),
      stream_time_ms: Date.now(),
      sender_name: 'Mehul Sankaran (Mule Tier-1)',
      sender_vpa: '7683454560@okaxis',
      receiver_name: 'Rhea Kothari (Mule Tier-2)',
      receiver_vpa: '2246623650@okaxis',
      amount: 62000.00,
      status: 'SUCCESS',
      bank_code: 'AXIS',
      location: 'Delhi'
    };
    onTxGenerated(tx2);

    // Hop 3: Mule Tier-2 -> Cashout Off-Ramp (Drained 96% in 2s)
    setTimeout(() => {
      const tx3 = {
        transaction_id: 'LIVE_MULE_' + Date.now().toString().slice(-6) + '_H3',
        timestamp: new Date().toISOString(),
        time_ms: Date.now(),
        stream_time_ms: Date.now(),
        sender_name: 'Rhea Kothari (Mule Tier-2)',
        sender_vpa: '2246623650@okaxis',
        receiver_name: 'Crypto Offramp Settlement',
        receiver_vpa: 'crypto_cashout@paytm',
        amount: 59500.00,
        status: 'SUCCESS',
        bank_code: 'PAYTM',
        location: 'Mumbai'
      };
      onTxGenerated(tx3);
    }, 2000);

  }, 2500);
}

module.exports = {
  loadDataset,
  getNextTransaction,
  injectMuleAttack
};
