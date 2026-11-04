package com.upi.fraud.model;

import java.io.Serializable;

/**
 * UPI Transaction Event Model
 */
public class TransactionEvent implements Serializable {
    private static final long serialVersionUID = 1L;

    public String txnId;
    public long eventTimeEpochMs;
    public String remitterVpa;
    public String remitterAccount;
    public String beneficiaryVpa;
    public String beneficiaryAccount;
    public double amount;
    public String currency;
    public String txnType;
    public String deviceId;
    public String ipAddress;
    public String status;

    public TransactionEvent() {}

    public TransactionEvent(String txnId, long eventTimeEpochMs, String remitterVpa, String remitterAccount,
                            String beneficiaryVpa, String beneficiaryAccount, double amount, String txnType) {
        this.txnId = txnId;
        this.eventTimeEpochMs = eventTimeEpochMs;
        this.remitterVpa = remitterVpa;
        this.remitterAccount = remitterAccount;
        this.beneficiaryVpa = beneficiaryVpa;
        this.beneficiaryAccount = beneficiaryAccount;
        this.amount = amount;
        this.txnType = txnType;
        this.currency = "INR";
        this.status = "SUCCESS";
    }
}

