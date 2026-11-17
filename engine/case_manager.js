/**
 * SOC Case Management & Quarantine Workflow Engine
 * =================================================
 * Manages alert investigations, case lifecycles, analyst notes,
 * quarantine actions, and compliance audit logs.
 */

const fs = require('fs');
const path = require('path');

const CASES_FILE = path.join(__dirname, '..', 'data', 'cases.json');
const QUARANTINE_FILE = path.join(__dirname, '..', 'data', 'quarantined_accounts.json');

class CaseManager {
  constructor(graphStore, options = {}) {
    this.graphStore = graphStore;
    this.inMemory = options.inMemory || false;
    this.cases = new Map(); // caseId -> Case Object
    this.quarantinedAccounts = new Map(); // vpa -> { vpa, quarantinedAt, reason, analyst, notes }
    if (!this.inMemory) {
      this.loadState();
    }
  }

  loadState() {
    if (this.inMemory) return;
    try {
      if (fs.existsSync(CASES_FILE)) {
        const raw = fs.readFileSync(CASES_FILE, 'utf8');
        const list = JSON.parse(raw);
        list.forEach(c => this.cases.set(c.caseId, c));
      }
    } catch (err) {
      console.warn('[CaseManager] Could not load cases.json:', err.message);
    }

    try {
      if (fs.existsSync(QUARANTINE_FILE)) {
        const raw = fs.readFileSync(QUARANTINE_FILE, 'utf8');
        const list = JSON.parse(raw);
        list.forEach(q => {
          this.quarantinedAccounts.set(q.vpa, q);
          if (this.graphStore) this.graphStore.setQuarantine(q.vpa, true);
        });
      }
    } catch (err) {
      console.warn('[CaseManager] Could not load quarantined_accounts.json:', err.message);
    }
  }

  saveState() {
    if (this.inMemory) return;
    try {
      fs.writeFileSync(CASES_FILE, JSON.stringify(Array.from(this.cases.values()), null, 2));
      fs.writeFileSync(QUARANTINE_FILE, JSON.stringify(Array.from(this.quarantinedAccounts.values()), null, 2));
    } catch (err) {
      console.error('[CaseManager] Error saving case state:', err.message);
    }
  }

  createCaseFromAlert(alert, analystName = 'SOC Analyst') {
    const caseId = `CASE-${alert.alert_id.replace('ALT-', '')}`;
    if (this.cases.has(caseId)) {
      return this.cases.get(caseId);
    }

    const newCase = {
      caseId,
      alertId: alert.alert_id,
      suspectVpa: alert.suspect_vpa,
      suspectName: alert.suspect_name,
      ruleCode: alert.rule_code,
      severity: alert.severity,
      riskScore: alert.risk_score,
      riskBreakdown: alert.risk_breakdown || [],
      amountDrained: alert.amount_drained || 0,
      bank: alert.bank || 'UPI',
      location: alert.location || 'India',
      status: 'NEW', // NEW -> INVESTIGATING -> ESCALATED -> RESOLVED
      assignedAnalyst: analystName,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      timeline: [
        {
          timestamp: new Date().toISOString(),
          type: 'ALERT_TRIGGERED',
          message: `Alert ${alert.alert_id} triggered rule ${alert.rule_code} with risk score ${alert.risk_score}/100`
        }
      ],
      notes: []
    };

    this.cases.set(caseId, newCase);
    this.saveState();
    return newCase;
  }

  updateCaseStatus(caseId, newStatus, analyst = 'SOC Analyst', comment = '') {
    const c = this.cases.get(caseId);
    if (!c) return null;

    const allowed = ['NEW', 'INVESTIGATING', 'ESCALATED', 'RESOLVED'];
    if (!allowed.includes(newStatus)) {
      throw new Error(`Invalid status: ${newStatus}`);
    }

    const oldStatus = c.status;
    c.status = newStatus;
    c.updatedAt = new Date().toISOString();
    c.timeline.push({
      timestamp: new Date().toISOString(),
      type: 'STATUS_CHANGE',
      message: `Status changed from ${oldStatus} to ${newStatus} by ${analyst}${comment ? `: ${comment}` : ''}`
    });

    this.saveState();
    return c;
  }

  addNote(caseId, author, text) {
    const c = this.cases.get(caseId);
    if (!c) return null;

    const note = {
      id: `note-${Date.now()}`,
      author: author || 'SOC Analyst',
      text,
      timestamp: new Date().toISOString()
    };

    c.notes.push(note);
    c.updatedAt = new Date().toISOString();
    c.timeline.push({
      timestamp: new Date().toISOString(),
      type: 'NOTE_ADDED',
      message: `Note added by ${author}: "${text.substring(0, 40)}..."`
    });

    this.saveState();
    return note;
  }

  quarantineAccount(vpa, reason = 'Automated Fraud Detection Threshold Exceeded', analyst = 'SOC Analyst') {
    const key = String(vpa || '').toLowerCase().trim();
    if (!key) return null;

    const record = {
      vpa: key,
      quarantinedAt: new Date().toISOString(),
      reason,
      analyst,
      active: true
    };

    this.quarantinedAccounts.set(key, record);
    if (this.graphStore) this.graphStore.setQuarantine(key, true);

    // Update any matching cases
    for (const c of this.cases.values()) {
      if (c.suspectVpa.toLowerCase() === key) {
        c.timeline.push({
          timestamp: new Date().toISOString(),
          type: 'ACCOUNT_QUARANTINED',
          message: `Account ${key} quarantined by ${analyst}. Reason: ${reason}`
        });
      }
    }

    this.saveState();
    return record;
  }

  unquarantineAccount(vpa, analyst = 'SOC Analyst') {
    const key = String(vpa || '').toLowerCase().trim();
    if (this.quarantinedAccounts.has(key)) {
      this.quarantinedAccounts.delete(key);
      if (this.graphStore) this.graphStore.setQuarantine(key, false);

      for (const c of this.cases.values()) {
        if (c.suspectVpa.toLowerCase() === key) {
          c.timeline.push({
            timestamp: new Date().toISOString(),
            type: 'ACCOUNT_UNQUARANTINED',
            message: `Account ${key} released from quarantine by ${analyst}.`
          });
        }
      }

      this.saveState();
      return true;
    }
    return false;
  }

  isQuarantined(vpa) {
    const key = String(vpa || '').toLowerCase().trim();
    return this.quarantinedAccounts.has(key);
  }

  getAllCases() {
    return Array.from(this.cases.values()).sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
  }

  getCase(caseId) {
    return this.cases.get(caseId) || null;
  }

  getQuarantinedAccounts() {
    return Array.from(this.quarantinedAccounts.values());
  }
}

module.exports = CaseManager;
