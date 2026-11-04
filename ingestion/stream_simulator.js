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

  const now = Date.now();

  // Hop 1: Victim -> Mule Tier-1 (Inflow of ₹65,000)
  const tx1 = {
    transaction_id: 'LIVE_MULE_' + now.toString().slice(-6) + '_H1',
    timestamp: new Date(now).toISOString(),
    time_ms: now,
    stream_time_ms: now,
    sender_name: 'Mohanlal Bakshi (Victim)',
    sender_vpa: 'victim_bakshi_' + now.toString().slice(-4) + '@okaxis',
    receiver_name: 'Mehul Sankaran (Mule Tier-1)',
    receiver_vpa: 'mule_tier1_' + now.toString().slice(-4) + '@okaxis',
    amount: 65000.00,
    status: 'SUCCESS',
    bank_code: 'AXIS',
    location: 'Delhi'
  };
  onTxGenerated(tx1);

  // Hop 2: Mule Tier-1 -> Mule Tier-2 (Drained 95% in 2.5s)
  setTimeout(() => {
    const t2 = Date.now();
    const tx2 = {
      transaction_id: 'LIVE_MULE_' + t2.toString().slice(-6) + '_H2',
      timestamp: new Date(t2).toISOString(),
      time_ms: t2,
      stream_time_ms: t2,
      sender_name: 'Mehul Sankaran (Mule Tier-1)',
      sender_vpa: tx1.receiver_vpa,   // same VPA — this is the mule being drained
      receiver_name: 'Rhea Kothari (Mule Tier-2)',
      receiver_vpa: 'mule_tier2_' + t2.toString().slice(-4) + '@okaxis',
      amount: 62000.00,
      status: 'SUCCESS',
      bank_code: 'AXIS',
      location: 'Delhi'
    };
    onTxGenerated(tx2);

    // Hop 3: Mule Tier-2 -> Cashout Off-Ramp (Drained 96% in 2s)
    setTimeout(() => {
      const t3 = Date.now();
      const tx3 = {
        transaction_id: 'LIVE_MULE_' + t3.toString().slice(-6) + '_H3',
        timestamp: new Date(t3).toISOString(),
        time_ms: t3,
        stream_time_ms: t3,
        sender_name: 'Rhea Kothari (Mule Tier-2)',
        sender_vpa: tx2.receiver_vpa,  // drained mule tier 2
        receiver_name: 'Crypto Offramp Settlement',
        receiver_vpa: 'crypto_cashout_' + t3.toString().slice(-4) + '@paytm',
        amount: 59500.00,
        status: 'SUCCESS',
        bank_code: 'PAYTM',
        location: 'Mumbai'
      };
      onTxGenerated(tx3);
    }, 2000);

  }, 2500);

  // --- Parallel: Fan-in Smurfing Ring (3 victims -> 1 aggregator) ---
  setTimeout(() => {
    const aggVpa = 'mule_agg_' + now.toString().slice(-4) + '@okhdfcbank';
    const victims = [
      { name: 'Tiya Mall (Victim)', vpa: 'tiya_victim_' + now.toString().slice(-4) + '@okaxis', amt: 38000, bank: 'AXIS', city: 'Ahmedabad' },
      { name: 'Jivin Batta (Victim)', vpa: 'jivin_victim_' + now.toString().slice(-4) + '@okybl', amt: 42000, bank: 'YBL', city: 'Mumbai' },
      { name: 'Kismat Rama (Victim)', vpa: 'kismat_victim_' + now.toString().slice(-4) + '@okicici', amt: 29000, bank: 'ICICI', city: 'Delhi' }
    ];

    victims.forEach((v, i) => {
      setTimeout(() => {
        const ts = Date.now();
        onTxGenerated({
          transaction_id: 'SMURF_' + ts.toString().slice(-6) + '_V' + i,
          timestamp: new Date(ts).toISOString(),
          time_ms: ts,
          stream_time_ms: ts,
          sender_name: v.name,
          sender_vpa: v.vpa,
          receiver_name: 'Vikram Roy (Mule Aggregator)',
          receiver_vpa: aggVpa,
          amount: v.amt,
          status: 'SUCCESS',
          bank_code: v.bank,
          location: v.city
        });
      }, i * 1200);
    });

    // Aggregator drains after all 3 victims have sent
    setTimeout(() => {
      const td = Date.now();
      onTxGenerated({
        transaction_id: 'SMURF_DRAIN_' + td.toString().slice(-6),
        timestamp: new Date(td).toISOString(),
        time_ms: td,
        stream_time_ms: td,
        sender_name: 'Vikram Roy (Mule Aggregator)',
        sender_vpa: aggVpa,
        receiver_name: 'Hawala Offramp Channel',
        receiver_vpa: 'hawala_node_' + td.toString().slice(-4) + '@ybl',
        amount: 150000,
        status: 'SUCCESS',
        bank_code: 'HDFCBANK',
        location: 'Mumbai'
      });
    }, victims.length * 1200 + 1500);

  }, 5000); // Start smurfing ring 5s after the first chain
}

module.exports = {
  loadDataset,
  getNextTransaction,
  injectMuleAttack
};
