/**
 * Directed Transaction Graph Store & Network Analyzer
 * ====================================================
 * In-memory directed graph representing accounts as nodes and
 * transactions as weighted directed edges. Provides topological
 * analysis including cycle detection, multi-hop path tracing,
 * and neighborhood subgraph extraction.
 */

class GraphStore {
  constructor(maxTransactions = 10000) {
    this.nodes = new Map(); // vpa -> { vpa, name, bank, location, inDegree, outDegree, totalInflow, totalOutflow, isMule, isQuarantined, riskScore, firstSeen, lastSeen }
    this.edges = []; // Array of { id, source, target, amount, timestamp, timeMs, txId, bank, location }
    this.adjList = new Map(); // vpa -> Array<{ target, amount, timeMs, txId }>
    this.reverseAdjList = new Map(); // vpa -> Array<{ source, amount, timeMs, txId }>
    this.maxTransactions = maxTransactions;
  }

  addNodeIfMissing(vpa, name = '', bank = '', location = '') {
    const key = String(vpa || '').toLowerCase().trim();
    if (!key) return null;

    if (!this.nodes.has(key)) {
      this.nodes.set(key, {
        vpa: key,
        name: name || key,
        bank: bank || 'UPI',
        location: location || 'India',
        inDegree: 0,
        outDegree: 0,
        totalInflow: 0,
        totalOutflow: 0,
        isMule: false,
        isQuarantined: false,
        riskScore: 0,
        firstSeen: Date.now(),
        lastSeen: Date.now()
      });
      this.adjList.set(key, []);
      this.reverseAdjList.set(key, []);
    } else {
      const node = this.nodes.get(key);
      if (name && (!node.name || node.name === key)) node.name = name;
      if (bank && node.bank === 'UPI') node.bank = bank;
      if (location && node.location === 'India') node.location = location;
      node.lastSeen = Date.now();
    }
    return this.nodes.get(key);
  }

  addTransaction(tx) {
    if (tx.status !== 'SUCCESS') return null;

    const sourceKey = String(tx.sender_vpa || '').toLowerCase().trim();
    const targetKey = String(tx.receiver_vpa || '').toLowerCase().trim();

    if (!sourceKey || !targetKey) return null;

    const sourceNode = this.addNodeIfMissing(sourceKey, tx.sender_name, tx.bank_code, tx.location);
    const targetNode = this.addNodeIfMissing(targetKey, tx.receiver_name, tx.bank_code, tx.location);

    const timeMs = tx.time_ms || tx.stream_time_ms || Date.now();
    const amount = Number(tx.amount || 0);

    // Update node aggregates
    sourceNode.outDegree++;
    sourceNode.totalOutflow += amount;
    targetNode.inDegree++;
    targetNode.totalInflow += amount;

    const edge = {
      id: `edge-${tx.transaction_id || Math.random().toString(36).substring(2, 9)}`,
      source: sourceKey,
      target: targetKey,
      amount: amount,
      timestamp: tx.timestamp || new Date(timeMs).toISOString(),
      timeMs: timeMs,
      txId: tx.transaction_id,
      bank: tx.bank_code,
      location: tx.location
    };

    this.edges.push(edge);
    this.adjList.get(sourceKey).push({ target: targetKey, amount, timeMs, txId: tx.transaction_id });
    this.reverseAdjList.get(targetKey).push({ source: sourceKey, amount, timeMs, txId: tx.transaction_id });

    // Evict oldest edges if cap exceeded
    if (this.edges.length > this.maxTransactions) {
      const removed = this.edges.shift();
      // Keep nodes and degrees representative
    }

    return edge;
  }

  updateNodeRisk(vpa, riskScore, isMule = true) {
    const key = String(vpa || '').toLowerCase().trim();
    if (this.nodes.has(key)) {
      const node = this.nodes.get(key);
      node.riskScore = Math.max(node.riskScore, riskScore);
      if (isMule) node.isMule = true;
    }
  }

  setQuarantine(vpa, isQuarantined) {
    const key = String(vpa || '').toLowerCase().trim();
    if (!key) return false;
    const node = this.addNodeIfMissing(key);
    if (node) {
      node.isQuarantined = isQuarantined;
      return true;
    }
    return false;
  }

  getNode(vpa) {
    const key = String(vpa || '').toLowerCase().trim();
    return this.nodes.get(key) || null;
  }

  /**
   * Detects simple cycles involving a given node within maxDepth hops (e.g. A -> B -> C -> A)
   * @param {string} startVpa
   * @param {number} maxDepth
   * @returns {Array<string>|null} The cycle path or null
   */
  findCycle(startVpa, maxDepth = 4) {
    const start = String(startVpa || '').toLowerCase().trim();
    if (!this.adjList.has(start)) return null;

    const visited = new Set();
    const path = [start];

    const dfs = (current, depth) => {
      if (depth > maxDepth) return null;

      const neighbors = this.adjList.get(current) || [];
      for (const edge of neighbors) {
        if (edge.target === start && depth >= 2) {
          // Cycle found!
          return [...path, start];
        }
        if (!visited.has(edge.target)) {
          visited.add(edge.target);
          path.push(edge.target);
          const found = dfs(edge.target, depth + 1);
          if (found) return found;
          path.pop();
          visited.delete(edge.target);
        }
      }
      return null;
    };

    visited.add(start);
    return dfs(start, 1);
  }

  /**
   * Traces multi-hop forward layering chains starting from an account
   * @param {string} startVpa
   * @param {number} maxHops
   * @param {number} maxTimeDeltaMs
   * @returns {Array<{ chain: Array<string>, totalAmount: number, hopCount: number }>}
   */
  traceLayeringChains(startVpa, maxHops = 4, maxTimeDeltaMs = 180000) {
    const start = String(startVpa || '').toLowerCase().trim();
    if (!this.adjList.has(start)) return [];

    const results = [];

    const traverse = (current, path, lastTimeMs, minAmount, hop) => {
      if (hop >= maxHops) return;

      const outgoing = (this.adjList.get(current) || []).filter(e => e.timeMs >= lastTimeMs && (e.timeMs - lastTimeMs) <= maxTimeDeltaMs);
      for (const e of outgoing) {
        if (path.includes(e.target)) continue; // Avoid loops in chain tracing
        const nextPath = [...path, e.target];
        if (nextPath.length >= 3) {
          results.push({
            chain: nextPath,
            totalAmount: e.amount,
            hopCount: nextPath.length - 1
          });
        }
        traverse(e.target, nextPath, e.timeMs, e.amount, hop + 1);
      }
    };

    const firstHops = this.adjList.get(start) || [];
    for (const e of firstHops) {
      traverse(e.target, [start, e.target], e.timeMs, e.amount, 1);
    }

    return results;
  }

  /**
   * Extracts a Cytoscape-compatible subgraph centered on a specific account, or top risk nodes
   * @param {string} [focusVpa]
   * @param {number} [limit=100]
   */
  getGraphVisualizationData(focusVpa = null, limit = 80) {
    const cyNodes = [];
    const cyEdges = [];
    const includedNodeKeys = new Set();

    if (focusVpa) {
      const key = String(focusVpa).toLowerCase().trim();
      const centerNode = this.nodes.get(key);
      if (centerNode) {
        includedNodeKeys.add(key);
        // Include immediate neighbors (1-hop in & out)
        const outEdges = this.adjList.get(key) || [];
        outEdges.slice(-15).forEach(e => includedNodeKeys.add(e.target));
        const inEdges = this.reverseAdjList.get(key) || [];
        inEdges.slice(-15).forEach(e => includedNodeKeys.add(e.source));
      }
    } else {
      // Pick top suspicious nodes + active recent transaction participants
      const sortedNodes = Array.from(this.nodes.values())
        .sort((a, b) => (b.riskScore * 2 + (b.inDegree + b.outDegree)) - (a.riskScore * 2 + (a.inDegree + a.outDegree)));

      sortedNodes.slice(0, limit).forEach(n => includedNodeKeys.add(n.vpa));
    }

    // Build Cytoscape nodes
    includedNodeKeys.forEach(vpa => {
      const node = this.nodes.get(vpa);
      if (!node) return;

      let role = 'NORMAL';
      if (node.isQuarantined) role = 'QUARANTINED';
      else if (node.riskScore >= 85) role = 'CRITICAL_MULE';
      else if (node.riskScore >= 70) role = 'HIGH_MULE';
      else if (node.inDegree >= 3 && node.outDegree >= 1) role = 'AGGREGATOR';
      else if (node.outDegree >= 3) role = 'DISPERSAL';

      cyNodes.push({
        data: {
          id: node.vpa,
          label: node.name ? `${node.name.split(' ')[0]} (${node.vpa.split('@')[0]})` : node.vpa,
          fullName: node.name,
          vpa: node.vpa,
          bank: node.bank,
          location: node.location,
          inDegree: node.inDegree,
          outDegree: node.outDegree,
          totalInflow: node.totalInflow,
          totalOutflow: node.totalOutflow,
          riskScore: node.riskScore,
          role: role,
          isQuarantined: node.isQuarantined
        }
      });
    });

    // Build Cytoscape edges between included nodes
    const edgeLimit = limit * 2;
    let edgeCount = 0;
    for (let i = this.edges.length - 1; i >= 0 && edgeCount < edgeLimit; i--) {
      const edge = this.edges[i];
      if (includedNodeKeys.has(edge.source) && includedNodeKeys.has(edge.target)) {
        cyEdges.push({
          data: {
            id: edge.id,
            source: edge.source,
            target: edge.target,
            amount: edge.amount,
            label: `₹${(edge.amount >= 1000 ? (edge.amount / 1000).toFixed(1) + 'k' : edge.amount)}`,
            timestamp: edge.timestamp,
            bank: edge.bank,
            txId: edge.txId
          }
        });
        edgeCount++;
      }
    }

    return {
      nodes: cyNodes,
      edges: cyEdges,
      stats: {
        totalNodes: this.nodes.size,
        totalEdges: this.edges.length,
        visualizedNodes: cyNodes.length,
        visualizedEdges: cyEdges.length
      }
    };
  }

  getTopSuspiciousAccounts(limit = 10) {
    return Array.from(this.nodes.values())
      .filter(n => n.riskScore > 0 || n.isMule)
      .sort((a, b) => b.riskScore - a.riskScore || (b.inDegree + b.outDegree) - (a.inDegree + a.outDegree))
      .slice(0, limit);
  }

  reset() {
    this.nodes.clear();
    this.edges = [];
    this.adjList.clear();
    this.reverseAdjList.clear();
  }
}

module.exports = GraphStore;
