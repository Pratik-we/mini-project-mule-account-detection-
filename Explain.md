# 📖 Detailed Project Documentation: Real-Time UPI & Mule Account Stream Detector

---

## 📌 1. Project Overview & Objective

### What is this project?
This project is an **enterprise-grade, real-time streaming fraud detection system** specifically designed to detect **Money Mule Networks, Rapid In-to-Out Fund Draining, Smurfing, and Multi-Hop Layering Attacks** across UPI (Unified Payments Interface) and instant banking rails.

### What problem does it solve?
In modern digital banking and UPI scams:
1. Fraudsters trick victims into transferring money into a compromised bank account (**Mule Account Tier-1**).
2. Within seconds (often $< 15$ to $60$ seconds), the mule forwards the money to another intermediary account (**Mule Tier-2** or **Tier-3**) or off-ramps it into cryptocurrency / ATM withdrawals.
3. Traditional batch fraud detection systems (which run overnight SQL queries or hourly jobs) detect the fraud **hours too late**, after the funds have already left the banking system.
4. **This system detects the mule in sub-second latency** the moment the outflow transaction occurs, calculating the **Time-to-Drain** velocity and **Drain Percentage** in real time.

---

## 📊 2. Dataset Specification (`data/transactions.csv`)

The system directly ingests and processes `data/transactions.csv`. It contains 9,000+ real-world and synthetic UPI transactions adhering to the following schema:

| Column | Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `transaction_id` | String | Unique transaction reference identifier | `099ee548-2fc1-4811-bf92-559c467ca792` |
| `timestamp` | String/DateTime | Transaction occurrence time (`YYYY-MM-DD HH:mm:ss`) | `2024-06-19 06:04:49` |
| `sender_name` | String | Name of the remitter / payer | `Mohanlal Bakshi` |
| `sender_vpa` | String | Virtual Payment Address of sender | `8908837379@okaxis` |
| `receiver_name` | String | Name of the beneficiary / payee | `Mehul Sankaran` |
| `receiver_vpa` | String | Virtual Payment Address of receiver | `7683454560@okaxis` |
| `amount` | Float | Transferred amount in Indian Rupees (₹) | `8404.55` |
| `status` | String | Transfer status (`SUCCESS` or `FAILED`) | `SUCCESS` |
| `bank_code` | String | Participating bank code | `AXIS`, `HDFCBANK`, `ICICI`, `SBI`, `YBL` |
| `location` | String | Transaction origination city / region | `Delhi`, `Mumbai`, `Ahmedabad`, `Pune` |

> **Note**: Failed transactions (`status === 'FAILED'`) are filtered out during evaluation because no funds are settled.

---

## 🔄 3. Dual-Engine Architecture (How It Runs)

The system is architected with dual operating modes for maximum flexibility:

| Feature | Mode 1: Zero-Dependency Standalone Mode | Mode 2: Distributed Production Mode |
| :--- | :--- | :--- |
| **Requirements** | Node.js only (v16+) | Docker Desktop (Docker Compose) |
| **Pipeline Stack** | Pure Node.js in-memory stream processor | Apache Kafka (KRaft) + Apache Flink + ClickHouse |
| **State Storage** | JavaScript `Map` with 2-minute sliding window | RocksDB state backend with checkpointing |
| **Data Delivery** | Server-Sent Events (SSE) directly to browser | Kafka topics + ClickHouse Materialized Views |
| **Primary Use Case**| Rapid prototyping, team collaboration without Docker, UI design | High-throughput distributed benchmark, production deployment |

---

## 🗂️ 4. Comprehensive File-by-File Breakdown

```
MP/
├── config/                                 # Configuration & cluster tuning
│   ├── default.env                         # Environment variables (ports, brokers)
│   └── flink-conf.yaml                     # Apache Flink cluster & state backend config
├── docker/                                 # Production container definitions
│   └── docker-compose.yml                  # Kafka (KRaft), Flink, ClickHouse stack
├── data/                                   # Datasets and generated reports
│   ├── transactions.csv                    # Ingested UPI transaction dataset (9,000+ rows)
│   └── alerts_output.json                  # Output analysis report from dataset streamer
├── clickhouse/                             # Columnar database schemas & analytics
│   ├── init.sql                            # Tables, Kafka engines & Materialized Views
│   └── queries.sql                         # Sub-second SOC analyst analytical queries
├── flink-jobs/                             # Distributed stream processing code
│   ├── python/                             # PyFlink implementation
│   │   ├── requirements.txt                # Python dependencies (apache-flink)
│   │   └── mule_stream_detector.py         # PyFlink KeyedProcessFunction pipeline
│   └── java/                               # Production Java Flink implementation
│       ├── pom.xml                         # Maven dependencies & build packaging
│       └── src/main/java/com/upi/fraud/
│           ├── FraudDetectionJob.java      # Main Flink pipeline topology
│           ├── model/
│           │   ├── TransactionEvent.java   # UPI transaction POJO / Data model
│           │   └── MuleAlert.java          # Fraud alert POJO / Data model
│           └── operators/
│               ├── RapidPassThroughDetector.java # Keyed stateful pass-through detector
│               └── MultiHopChainDetector.java    # Multi-hop layering chain correlator
├── ingestion/                              # Data generators and dataset ingestors
│   ├── stream_simulator.js                 # Dataset stream reader & live attack injector
│   └── dataset_streamer.js                 # Batch dataset scanner for transactions.csv
├── web-dashboard/                          # Web UI & Real-Time Alert Broker
│   ├── server.js                           # Zero-dependency HTTP & SSE server
│   └── public/
│       ├── index.html                      # Real-time SOC analyst dashboard
│       ├── styles.css                      # Cyber-security dark theme styling
│       └── app.js                          # Client-side SSE listener & event renderer
└── Explain.md                              # (This file) Complete technical documentation
```

---

## 🔬 5. Detailed Component Explanations

### 5.1 Ingestion Layer (`ingestion/`)

#### 📄 `ingestion/dataset_streamer.js`
* **What it does**: Reads `data/transactions.csv`, normalizes all 10 columns, tracks account inflow/outflow states, and detects money mule patterns.
* **Key Features**:
  * **Intelligent Normalization (`normalizeRecord`)**: Maps names, VPAs, amounts, status, bank codes, and locations cleanly.
  * **Status Filtering**: Ignores `FAILED` transactions and only evaluates settled money movements.
  * **Pattern Detection**:
    1. `RAPID_PASS_THROUGH_MULE`: Catches accounts where money enters and drains out ($\ge 70\%$ drain ratio) within $<120$ seconds (or $<20$ seconds for CRITICAL).
    2. `FAN_IN_SMURFING_AGGREGATOR`: Catches accounts receiving transfers from $\ge 3$ distinct remitter victims within the time window.
  * **Output**: Produces formatted console output and writes `data/alerts_output.json`.

#### 📄 `ingestion/stream_simulator.js`
* **What it does**: Connects `data/transactions.csv` to the real-time server.
* **Key Functions**:
  * `loadDataset()`: Loads and parses `data/transactions.csv`.
  * `getNextTransaction()`: Fetches the next sequential transaction from the dataset and timestamps it for real-time streaming.
  * `injectMuleAttack(callback)`: Fires a coordinated multi-hop attack across dataset accounts (Victim $\to$ Mule 1 $\to$ Mule 2 $\to$ Crypto Cashout) with sub-3-second latency per hop to trigger instant alerts on the dashboard.

---

### 5.2 Web Dashboard & Real-Time Broker (`web-dashboard/`)

#### 📄 `web-dashboard/server.js`
* **What it does**: Zero-dependency Node.js server powering the live Security Operations Center (SOC) dashboard.
* **How it works**:
  1. **HTTP Server**: Serves static assets (`index.html`, `styles.css`, `app.js`) on port `3000`.
  2. **SSE Gateway (`/api/stream`)**: Pushes live transactions and alerts over Server-Sent Events to connected browsers.
  3. **Stateful In-Memory CEP Engine**:
     * Tracks account balance delta, recent credits, debits, and unique remitter sets.
     * Evaluates incoming transactions against sliding-window rules.
  4. **Continuous Dataset Streaming**: Emits a transaction from `data/transactions.csv` every 450 ms.
  5. **REST Endpoints**:
     * `GET /api/stats`: Sub-second KPI metrics (total volume, alert counts, active mules).
     * `GET /api/alerts`: JSON list of all detected alerts.
     * `GET /api/inject-mule`: Triggers the live coordinated attack.

#### 📄 `web-dashboard/public/index.html`, `styles.css`, `app.js`
* **What it does**: The frontend SOC dashboard.
* **Features**:
  * Live KPI Counters: Total Transactions, Flagged Mule Alerts, Critical Velocity Drains ($<15$s), Active Mules under watch.
  * Real-Time Mule Ring Alerts Feed (displaying suspect name & VPA, severity badge, risk score / 100, flow path, drain speed, bank, and city).
  * Live Keyed Transaction Feed showing sender $\to$ receiver, amount, bank badge, city, and transaction ID.
  * 1-Click Button: **🚨 Inject Mule Ring Attack**.

---

### 5.3 Production Stream Processing Layer (`flink-jobs/`)

#### 📄 `flink-jobs/python/mule_stream_detector.py`
* **What it does**: The PyFlink (Apache Flink Python API) implementation of the detection pipeline.
* **How it works**:
  * Uses `KeyedProcessFunction` keyed by account VPA.
  * Maintains state of recent credits and sets event-time timers for velocity evaluation.

#### 📄 `flink-jobs/java/src/main/java/com/upi/fraud/`
* **`FraudDetectionJob.java`**: The main Java Flink entry point with checkpointing and bounded out-of-orderness watermarks.
* **`operators/RapidPassThroughDetector.java`**: Java implementation of the sliding state machine.
* **`operators/MultiHopChainDetector.java`**: Flink CEP (Complex Event Processing) pattern matcher detecting chained sequence transitions ($A \to B \to C \to D$).

---

### 5.4 Storage & Containerization (`clickhouse/` & `docker/`)

* **`clickhouse/init.sql`**: Schema for `fraud_stream.upi_transactions` and `fraud_stream.mule_alerts`, integrated with Kafka via Materialized Views.
* **`clickhouse/queries.sql`**: Fast analytical queries for mule ring identification.
* **`docker/docker-compose.yml`**: Spawns Kafka (KRaft), Flink, and ClickHouse.

---

## 🧠 6. Fraud Detection Algorithms & Formulas

### 1. Rapid In-to-Out Pass-Through (Time-to-Drain)
* **Concept**: A mule account rarely holds illicit funds for long; money is immediately moved out.
* **Formulas**:
  $$\text{Time to Drain} = t_{\text{debit}} - t_{\text{credit}}$$
  $$\text{Drain Ratio} = \left(\frac{\text{Debit Amount}}{\text{Credit Inflow Amount}}\right) \times 100$$
* **Thresholds**:
  * Flagged if: $\text{Time to Drain} \le 60\text{ seconds}$ AND $\text{Drain Ratio} \ge 70\%$.
  * Severity:
    * $\text{CRITICAL}$ if $\text{Time to Drain} \le 15\text{ seconds}$.
    * $\text{HIGH}$ if $15\text{ seconds} < \text{Time to Drain} \le 60\text{ seconds}$.
  * Risk Score:
    $$\text{Risk Score} = \min\left(99, 75 + (60 - \text{Time to Drain}) \times 0.4\right)$$

### 2. Fan-In Smurfing Aggregator
* **Concept**: A central fraud account collects small transfers from multiple compromised victims to evade single-transaction threshold limits.
* **Condition**: $\ge 3$ distinct remitter accounts transferring money to the same beneficiary account within a 120-second sliding window.

### 3. Multi-Hop Layering Chain
* **Concept**: Funds move along an $A \to B \to C \to D$ path across multiple banks within minutes to obfuscate tracking.
* **Condition**: $\text{Beneficiary}(T_x) = \text{Remitter}(T_{x+1})$ within a 30-second correlation window.

---

## 🚀 7. How to Run the Project (Step-by-Step)

### Option A: Run the Live Web Dashboard
```powershell
node web-dashboard/server.js
```
Then open **`http://localhost:3000`** in your browser. You will see:
* **Enterprise Banking & SOC Design**: Executive layout with clean financial risk cards, zero visual clutter, and high data density.
* **Light / Dark Theme Toggle**: Click the theme button in the top right to switch between **Clean Light Mode** (default) and **Enterprise Dark Mode** with instant local persistence.
* **Live Ingestion**: Transactions from `data/transactions.csv` streaming live in the transaction ledger.
* **Automated Mule Detection**: Real-time money mule alerts appearing automatically in the left surveillance panel.
* **Audit Trail Flow**: Step-by-step visual money routing ($Remitter \to Suspect Mule \to Destination$) with exact velocity metrics ($\text{Time to Drain}$ and $\text{Drain Ratio}$).
* **Attack Simulation**: Click **"Simulate Attack"** to inject a live multi-hop laundering attack into the stream.

### Option B: Run the Dataset Scanner Directly
```powershell
node ingestion/dataset_streamer.js data/transactions.csv
```
This processes all 9,000+ transactions, identifies the mule networks, and outputs a complete report to `data/alerts_output.json`.
