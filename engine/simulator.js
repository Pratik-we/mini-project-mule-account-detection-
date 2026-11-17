/**
 * Advanced Attack Scenario Simulator & Replay Engine
 * ==================================================
 * Generates synthetic and dataset-driven financial fraud scenarios:
 *  1. Normal UPI activity bursts
 *  2. Rapid pass-through draining attacks
 *  3. Fan-in smurfing aggregation
 *  4. Fan-out distribution dispersal
 *  5. Multi-hop laundering chains (4-5 hops)
 *  6. Circular loop laundering (A -> B -> C -> D -> A)
 *  7. Structuring / splitting attacks (sub-threshold bursts)
 */

class AttackSimulator {
  constructor(onTxGenerated) {
    this.onTxGenerated = onTxGenerated;
    this.scenarioSeq = 0;
  }

  setCallback(fn) {
    this.onTxGenerated = fn;
  }

  emit(tx) {
    if (typeof this.onTxGenerated === 'function') {
      this.onTxGenerated(tx);
    }
  }

  /**
   * Scenario 1: Rapid In-to-Out Fund Draining
   * Victim sends ₹75,000 to Mule Tier-1; Mule drains ₹72,000 (96%) in 4 seconds to Cashout off-ramp
   */
  injectRapidPassThrough() {
    this.scenarioSeq++;
    const now = Date.now();
    const tag = `SCEN_RAPID_${this.scenarioSeq}_${now.toString().slice(-4)}`;

    const victimVpa = `victim_ramesh_${now.toString().slice(-4)}@oksbi`;
    const muleVpa = `mule_t1_${now.toString().slice(-4)}@okaxis`;
    const cashoutVpa = `crypto_desk_${now.toString().slice(-4)}@paytm`;

    console.log(`[Simulator] Injecting Rapid Pass-Through Attack: ${tag}`);

    // Inflow: Victim -> Mule Tier-1
    this.emit({
      transaction_id: `${tag}_INFLOW`,
      timestamp: new Date(now).toISOString(),
      time_ms: now,
      stream_time_ms: now,
      sender_name: 'Ramesh Sharma (Victim)',
      sender_vpa: victimVpa,
      receiver_name: 'Aditya Verma (Mule Tier-1)',
      receiver_vpa: muleVpa,
      amount: 75000.00,
      status: 'SUCCESS',
      bank_code: 'SBI',
      location: 'Delhi',
      scenario_tag: 'RAPID_PASS_THROUGH'
    });

    // Outflow: Mule Tier-1 -> Cashout within 3.5s
    setTimeout(() => {
      const tOut = Date.now();
      this.emit({
        transaction_id: `${tag}_OUTFLOW`,
        timestamp: new Date(tOut).toISOString(),
        time_ms: tOut,
        stream_time_ms: tOut,
        sender_name: 'Aditya Verma (Mule Tier-1)',
        sender_vpa: muleVpa,
        receiver_name: 'P2P Crypto Cashout Settlement',
        receiver_vpa: cashoutVpa,
        amount: 72000.00, // 96% drain ratio
        status: 'SUCCESS',
        bank_code: 'AXIS',
        location: 'Mumbai',
        scenario_tag: 'RAPID_PASS_THROUGH'
      });
    }, 3500);

    return { tag, scenario: 'RAPID_PASS_THROUGH', suspect: muleVpa, amount: 72000 };
  }

  /**
   * Scenario 2: Fan-In Smurfing Aggregator
   * 4 distinct victim accounts transfer amounts into 1 mule aggregator
   */
  injectFanInSmurfing() {
    this.scenarioSeq++;
    const now = Date.now();
    const tag = `SCEN_SMURF_${this.scenarioSeq}_${now.toString().slice(-4)}`;
    const aggVpa = `mule_agg_${now.toString().slice(-4)}@okhdfcbank`;

    console.log(`[Simulator] Injecting Fan-In Smurfing Scenario: ${tag}`);

    const victims = [
      { name: 'Kavita Sen (Victim)', vpa: `kavita_${now.toString().slice(-4)}@okaxis`, amt: 35000, bank: 'AXIS', city: 'Kolkata' },
      { name: 'Pranav Joshi (Victim)', vpa: `pranav_${now.toString().slice(-4)}@okybl`, amt: 40000, bank: 'YBL', city: 'Pune' },
      { name: 'Sunita Rao (Victim)', vpa: `sunita_${now.toString().slice(-4)}@okicici`, amt: 32000, bank: 'ICICI', city: 'Hyderabad' },
      { name: 'Girish Menon (Victim)', vpa: `girish_${now.toString().slice(-4)}@oksbi`, amt: 45000, bank: 'SBI', city: 'Bangalore' }
    ];

    victims.forEach((v, idx) => {
      setTimeout(() => {
        const t = Date.now();
        this.emit({
          transaction_id: `${tag}_V${idx + 1}`,
          timestamp: new Date(t).toISOString(),
          time_ms: t,
          stream_time_ms: t,
          sender_name: v.name,
          sender_vpa: v.vpa,
          receiver_name: 'Suresh Singhania (Mule Aggregator)',
          receiver_vpa: aggVpa,
          amount: v.amt,
          status: 'SUCCESS',
          bank_code: v.bank,
          location: v.city,
          scenario_tag: 'FAN_IN_SMURFING'
        });
      }, idx * 1000);
    });

    // Followed by bulk drain
    setTimeout(() => {
      const tDrain = Date.now();
      this.emit({
        transaction_id: `${tag}_AGG_DRAIN`,
        timestamp: new Date(tDrain).toISOString(),
        time_ms: tDrain,
        stream_time_ms: tDrain,
        sender_name: 'Suresh Singhania (Mule Aggregator)',
        sender_vpa: aggVpa,
        receiver_name: 'Offshore Hawala Syndicate',
        receiver_vpa: `hawala_hub_${now.toString().slice(-4)}@ybl`,
        amount: 148000.00,
        status: 'SUCCESS',
        bank_code: 'HDFCBANK',
        location: 'Mumbai',
        scenario_tag: 'FAN_IN_SMURFING'
      });
    }, victims.length * 1000 + 1500);

    return { tag, scenario: 'FAN_IN_SMURFING', suspect: aggVpa, sendersCount: victims.length };
  }

  /**
   * Scenario 3: Fan-Out Distribution Dispersal
   * Mule distributor receives ₹1,80,000 and disperses it to 4 distinct runner accounts within seconds
   */
  injectFanOutDistribution() {
    this.scenarioSeq++;
    const now = Date.now();
    const tag = `SCEN_FANOUT_${this.scenarioSeq}_${now.toString().slice(-4)}`;
    const distVpa = `mule_distributor_${now.toString().slice(-4)}@okicici`;

    console.log(`[Simulator] Injecting Fan-Out Distribution Scenario: ${tag}`);

    // Inflow
    this.emit({
      transaction_id: `${tag}_IN`,
      timestamp: new Date(now).toISOString(),
      time_ms: now,
      stream_time_ms: now,
      sender_name: 'Compromised Corporate Account',
      sender_vpa: `corp_payroll_${now.toString().slice(-4)}@okaxis`,
      receiver_name: 'Karan Mehra (Mule Distributor)',
      receiver_vpa: distVpa,
      amount: 180000.00,
      status: 'SUCCESS',
      bank_code: 'AXIS',
      location: 'Delhi',
      scenario_tag: 'FAN_OUT_DISTRIBUTION'
    });

    const runners = [
      { name: 'Runner 1 (ATM Mule)', vpa: `runner_1_${now.toString().slice(-4)}@paytm`, amt: 45000, bank: 'PAYTM', city: 'Delhi' },
      { name: 'Runner 2 (ATM Mule)', vpa: `runner_2_${now.toString().slice(-4)}@oksbi`, amt: 44000, bank: 'SBI', city: 'Jaipur' },
      { name: 'Runner 3 (P2P Merchant)', vpa: `runner_3_${now.toString().slice(-4)}@okaxis`, amt: 43000, bank: 'AXIS', city: 'Gurgaon' },
      { name: 'Runner 4 (Crypto OTC)', vpa: `runner_4_${now.toString().slice(-4)}@okybl`, amt: 46000, bank: 'YBL', city: 'Chandigarh' }
    ];

    runners.forEach((r, idx) => {
      setTimeout(() => {
        const t = Date.now();
        this.emit({
          transaction_id: `${tag}_OUT_${idx + 1}`,
          timestamp: new Date(t).toISOString(),
          time_ms: t,
          stream_time_ms: t,
          sender_name: 'Karan Mehra (Mule Distributor)',
          sender_vpa: distVpa,
          receiver_name: r.name,
          receiver_vpa: r.vpa,
          amount: r.amt,
          status: 'SUCCESS',
          bank_code: r.bank,
          location: r.city,
          scenario_tag: 'FAN_OUT_DISTRIBUTION'
        });
      }, 1200 + idx * 800);
    });

    return { tag, scenario: 'FAN_OUT_DISTRIBUTION', suspect: distVpa, runnersCount: runners.length };
  }

  /**
   * Scenario 4: Multi-Hop Layering Chain (4 Hops)
   * Victim -> Mule Tier-1 -> Mule Tier-2 -> Mule Tier-3 -> Cashout
   */
  injectMultiHopChain() {
    this.scenarioSeq++;
    const now = Date.now();
    const tag = `SCEN_CHAIN_${this.scenarioSeq}_${now.toString().slice(-4)}`;

    console.log(`[Simulator] Injecting Multi-Hop Chain Scenario: ${tag}`);

    const hopNodes = [
      { role: 'Victim', name: 'Alok Gupta (Victim)', vpa: `alok_victim_${now.toString().slice(-4)}@oksbi`, bank: 'SBI', city: 'Varanasi', amt: 90000 },
      { role: 'Mule Tier-1', name: 'Rohit Saxena (Mule Tier-1)', vpa: `mule_t1_${now.toString().slice(-4)}@okaxis`, bank: 'AXIS', city: 'Lucknow', amt: 87000 },
      { role: 'Mule Tier-2', name: 'Nikhil Bansal (Mule Tier-2)', vpa: `mule_t2_${now.toString().slice(-4)}@okhdfcbank`, bank: 'HDFCBANK', city: 'Kanpur', amt: 84000 },
      { role: 'Mule Tier-3', name: 'Vinay Poddar (Mule Tier-3)', vpa: `mule_t3_${now.toString().slice(-4)}@okicici`, bank: 'ICICI', city: 'Delhi', amt: 81000 },
      { role: 'Cashout', name: 'Gold Bullion Terminal Offramp', vpa: `gold_vault_${now.toString().slice(-4)}@paytm`, bank: 'PAYTM', city: 'Delhi', amt: 81000 }
    ];

    for (let i = 0; i < hopNodes.length - 1; i++) {
      setTimeout(() => {
        const t = Date.now();
        const sender = hopNodes[i];
        const receiver = hopNodes[i + 1];

        this.emit({
          transaction_id: `${tag}_HOP_${i + 1}`,
          timestamp: new Date(t).toISOString(),
          time_ms: t,
          stream_time_ms: t,
          sender_name: sender.name,
          sender_vpa: sender.vpa,
          receiver_name: receiver.name,
          receiver_vpa: receiver.vpa,
          amount: receiver.amt,
          status: 'SUCCESS',
          bank_code: sender.bank,
          location: sender.city,
          scenario_tag: 'MULTI_HOP_CHAIN'
        });
      }, i * 2000);
    }

    return { tag, scenario: 'MULTI_HOP_CHAIN', hops: hopNodes.length - 1 };
  }

  /**
   * Scenario 5: Circular Transaction Loop (Cycle)
   * Entity A -> Entity B -> Entity C -> Entity A
   */
  injectCircularLoop() {
    this.scenarioSeq++;
    const now = Date.now();
    const tag = `SCEN_LOOP_${this.scenarioSeq}_${now.toString().slice(-4)}`;

    console.log(`[Simulator] Injecting Circular Transaction Loop: ${tag}`);

    const nodeA = { name: 'Manish Traders', vpa: `node_a_${now.toString().slice(-4)}@okaxis`, bank: 'AXIS', city: 'Ahmedabad' };
    const nodeB = { name: 'Shree Logistics', vpa: `node_b_${now.toString().slice(-4)}@okhdfcbank`, bank: 'HDFCBANK', city: 'Surat' };
    const nodeC = { name: 'Apex Financial Services', vpa: `node_c_${now.toString().slice(-4)}@okicici`, bank: 'ICICI', city: 'Mumbai' };

    const cycleSteps = [
      { sender: nodeA, receiver: nodeB, amt: 60000, step: 1 },
      { sender: nodeB, receiver: nodeC, amt: 58500, step: 2 },
      { sender: nodeC, receiver: nodeA, amt: 57000, step: 3 } // Closes the circle back to A!
    ];

    cycleSteps.forEach((s, idx) => {
      setTimeout(() => {
        const t = Date.now();
        this.emit({
          transaction_id: `${tag}_STEP_${s.step}`,
          timestamp: new Date(t).toISOString(),
          time_ms: t,
          stream_time_ms: t,
          sender_name: s.sender.name,
          sender_vpa: s.sender.vpa,
          receiver_name: s.receiver.name,
          receiver_vpa: s.receiver.vpa,
          amount: s.amt,
          status: 'SUCCESS',
          bank_code: s.sender.bank,
          location: s.sender.city,
          scenario_tag: 'CIRCULAR_LOOP'
        });
      }, idx * 1800);
    });

    return { tag, scenario: 'CIRCULAR_LOOP', entities: [nodeA.vpa, nodeB.vpa, nodeC.vpa] };
  }

  /**
   * Scenario 6: Structuring / Splitting (Sub-threshold Bursts)
   * 4 rapid transactions between ₹46,000 and ₹49,500 within 40 seconds to evade ₹50,000 reporting threshold
   */
  injectStructuringSplit() {
    this.scenarioSeq++;
    const now = Date.now();
    const tag = `SCEN_STRUCT_${this.scenarioSeq}_${now.toString().slice(-4)}`;

    console.log(`[Simulator] Injecting Structuring Split Scenario: ${tag}`);

    const senderVpa = `struct_sender_${now.toString().slice(-4)}@okaxis`;
    const receiverVpa = `mule_drop_${now.toString().slice(-4)}@okhdfcbank`;

    const splits = [48500, 49200, 47800, 49000];

    splits.forEach((amt, idx) => {
      setTimeout(() => {
        const t = Date.now();
        this.emit({
          transaction_id: `${tag}_SPLIT_${idx + 1}`,
          timestamp: new Date(t).toISOString(),
          time_ms: t,
          stream_time_ms: t,
          sender_name: 'Rajesh Chawla',
          sender_vpa: senderVpa,
          receiver_name: 'Deepak Mhatre',
          receiver_vpa: receiverVpa,
          amount: amt,
          status: 'SUCCESS',
          bank_code: 'AXIS',
          location: 'Delhi',
          scenario_tag: 'STRUCTURING_SPLIT'
        });
      }, idx * 1500);
    });

    return { tag, scenario: 'STRUCTURING_SPLIT', totalSplits: splits.length };
  }
}

module.exports = AttackSimulator;
