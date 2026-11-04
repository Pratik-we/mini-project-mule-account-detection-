-- ========================================================
-- ClickHouse Sub-Second Analytical Queries for SOC Analysts
-- ========================================================

-- 1. Real-Time Fan-In Aggregator Detection (Last 5 minutes)
-- Finds accounts receiving funds from >= 3 distinct senders with rapid velocity
SELECT 
    beneficiary_account,
    beneficiary_vpa,
    count(DISTINCT remitter_account) AS distinct_senders,
    count() AS total_tx_count,
    sum(amount) AS total_inflow_inr,
    min(event_time) AS first_seen,
    max(event_time) AS last_seen,
    dateDiff('second', min(event_time), max(event_time)) AS window_seconds
FROM fraud_stream.upi_transactions
WHERE event_time >= now() - INTERVAL 5 MINUTE
GROUP BY beneficiary_account, beneficiary_vpa
HAVING distinct_senders >= 3
ORDER BY total_inflow_inr DESC;

-- 2. Most Critical Mule Accounts by Frequency of Drain Alerts
SELECT 
    suspect_account,
    suspect_vpa,
    count() AS alert_frequency,
    avg(risk_score) AS avg_risk_score,
    avg(time_to_drain_seconds) AS avg_drain_velocity_sec,
    avg(drain_percentage) AS avg_drain_ratio,
    groupArray(target_vpa) AS money_hops_destinations
FROM fraud_stream.mule_alerts
WHERE alert_time >= now() - INTERVAL 1 HOUR
GROUP BY suspect_account, suspect_vpa
ORDER BY alert_frequency DESC, avg_risk_score DESC
LIMIT 20;

-- 3. Live Transactions per Second (TPS) & Throughput Gauge
SELECT 
    toStartOfInterval(event_time, INTERVAL 5 SECOND) AS time_window,
    count() / 5.0 AS transactions_per_sec,
    sum(amount) AS volume_inr,
    countIf(amount >= 40000) AS high_value_count
FROM fraud_stream.upi_transactions
WHERE event_time >= now() - INTERVAL 5 MINUTE
GROUP BY time_window
ORDER BY time_window DESC
LIMIT 12;

