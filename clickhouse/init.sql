-- ========================================================
-- Database: fraud_stream
-- ClickHouse Initialization for Real-Time Fraud & Mule Detection
-- ========================================================

CREATE DATABASE IF NOT EXISTS fraud_stream;

USE fraud_stream;

-- 1. Main Storage Table for Raw UPI Transactions
CREATE TABLE IF NOT EXISTS fraud_stream.upi_transactions (
    transaction_id String,
    event_time DateTime64(3, 'UTC'),
    remitter_vpa LowCardinality(String),
    remitter_account String,
    beneficiary_vpa LowCardinality(String),
    beneficiary_account String,
    amount Float64,
    currency LowCardinality(String),
    txn_type LowCardinality(String),
    device_id String,
    ip_address String,
    status LowCardinality(String)
)
ENGINE = MergeTree()
PARTITION BY toYYYYMMDD(event_time)
ORDER BY (beneficiary_account, remitter_account, event_time);

-- 2. Main Storage Table for Fraud & Mule Alerts
CREATE TABLE IF NOT EXISTS fraud_stream.mule_alerts (
    alert_id String,
    alert_time DateTime64(3, 'UTC'),
    rule_code LowCardinality(String),
    severity LowCardinality(String),
    risk_score Float32,
    suspect_account String,
    suspect_vpa String,
    source_vpa String,
    target_vpa String,
    hop_count UInt8,
    time_to_drain_seconds Float32,
    drain_percentage Float32,
    details String
)
ENGINE = ReplacingMergeTree()
PARTITION BY toYYYYMMDD(alert_time)
ORDER BY (suspect_account, alert_time, alert_id);

-- 3. Kafka Engine Table for Ingesting Raw Transactions
CREATE TABLE IF NOT EXISTS fraud_stream.kafka_upi_transactions (
    transaction_id String,
    event_time DateTime64(3, 'UTC'),
    remitter_vpa String,
    remitter_account String,
    beneficiary_vpa String,
    beneficiary_account String,
    amount Float64,
    currency String,
    txn_type String,
    device_id String,
    ip_address String,
    status String
)
ENGINE = Kafka
SETTINGS kafka_broker_list = 'kafka:29092',
         kafka_topic_list = 'upi.transactions.raw',
         kafka_group_name = 'clickhouse-tx-consumer-group',
         kafka_format = 'JSONEachRow';

-- Pipe Kafka transactions into upi_transactions
CREATE MATERIALIZED VIEW IF NOT EXISTS fraud_stream.mv_upi_transactions TO fraud_stream.upi_transactions AS
SELECT * FROM fraud_stream.kafka_upi_transactions;

-- 4. Kafka Engine Table for Ingesting Mule Alerts
CREATE TABLE IF NOT EXISTS fraud_stream.kafka_mule_alerts (
    alert_id String,
    alert_time DateTime64(3, 'UTC'),
    rule_code String,
    severity String,
    risk_score Float32,
    suspect_account String,
    suspect_vpa String,
    source_vpa String,
    target_vpa String,
    hop_count UInt8,
    time_to_drain_seconds Float32,
    drain_percentage Float32,
    details String
)
ENGINE = Kafka
SETTINGS kafka_broker_list = 'kafka:29092',
         kafka_topic_list = 'upi.fraud.alerts',
         kafka_group_name = 'clickhouse-alerts-consumer-group',
         kafka_format = 'JSONEachRow';

-- Pipe Kafka alerts into mule_alerts
CREATE MATERIALIZED VIEW IF NOT EXISTS fraud_stream.mv_mule_alerts TO fraud_stream.mule_alerts AS
SELECT * FROM fraud_stream.kafka_mule_alerts;

