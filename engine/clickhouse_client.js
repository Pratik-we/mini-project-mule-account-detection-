/**
 * ClickHouse Client Integration (HTTP Interface)
 * ===============================================
 * Sub-second ingestion client pushing transactions and alerts
 * into ClickHouse OLAP tables when available. Fails gracefully
 * without disrupting standalone mode if ClickHouse is offline.
 */

const http = require('http');

class ClickHouseClient {
  constructor(options = {}) {
    this.host = options.host || process.env.CLICKHOUSE_HOST || 'localhost';
    this.port = parseInt(options.port || process.env.CLICKHOUSE_HTTP_PORT || '8123', 10);
    this.database = options.database || process.env.CLICKHOUSE_DB || 'fraud_stream';
    this.isAvailable = false;
    this.checkHealth();
  }

  async checkHealth() {
    return new Promise((resolve) => {
      const req = http.get(`http://${this.host}:${this.port}/ping`, (res) => {
        this.isAvailable = res.statusCode === 200;
        resolve(this.isAvailable);
      });
      req.on('error', () => {
        this.isAvailable = false;
        resolve(false);
      });
      req.setTimeout(1000, () => {
        req.destroy();
        this.isAvailable = false;
        resolve(false);
      });
    });
  }

  insertTransaction(tx) {
    if (!this.isAvailable) return;
    // Format for ClickHouse JSONEachRow
    const record = {
      transaction_id: tx.transaction_id,
      event_time: new Date(tx.time_ms || Date.now()).toISOString().replace('T', ' ').replace('Z', ''),
      remitter_vpa: tx.sender_vpa,
      remitter_account: tx.sender_name || tx.sender_vpa,
      beneficiary_vpa: tx.receiver_vpa,
      beneficiary_account: tx.receiver_name || tx.receiver_vpa,
      amount: tx.amount,
      currency: 'INR',
      txn_type: 'P2P',
      device_id: 'DEV-SIM',
      ip_address: '127.0.0.1',
      status: tx.status
    };

    this.executeInsert('upi_transactions', [record]);
  }

  insertAlert(alert) {
    if (!this.isAvailable) return;
    const record = {
      alert_id: alert.alert_id,
      alert_time: new Date(alert.alert_timestamp || Date.now()).toISOString().replace('T', ' ').replace('Z', ''),
      rule_code: alert.rule_code,
      severity: alert.severity,
      risk_score: alert.risk_score,
      suspect_account: alert.suspect_vpa,
      suspect_vpa: alert.suspect_vpa,
      source_vpa: alert.source_vpa || '',
      target_vpa: alert.target_vpa || '',
      hop_count: alert.hop_count || 1,
      time_to_drain_seconds: alert.time_to_drain_seconds || 0,
      drain_percentage: alert.drain_percentage || 0,
      details: alert.details || ''
    };

    this.executeInsert('mule_alerts', [record]);
  }

  executeInsert(table, rows) {
    if (!this.isAvailable || rows.length === 0) return;
    const body = rows.map(r => JSON.stringify(r)).join('\n');
    const query = `INSERT INTO ${this.database}.${table} FORMAT JSONEachRow`;

    const req = http.request({
      hostname: this.host,
      port: this.port,
      path: `/?query=${encodeURIComponent(query)}`,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(body)
      }
    }, (res) => {
      // Consume response
      res.resume();
    });

    req.on('error', () => {});
    req.write(body);
    req.end();
  }
}

module.exports = ClickHouseClient;
