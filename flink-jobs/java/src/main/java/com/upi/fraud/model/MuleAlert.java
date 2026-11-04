package com.upi.fraud.model;

import java.io.Serializable;

/**
 * Fraud & Mule Alert Event Model
 */
public class MuleAlert implements Serializable {
    private static final long serialVersionUID = 1L;

    public String alertId;
    public String alertTime;
    public String ruleCode;
    public String severity; // CRITICAL, HIGH, MEDIUM
    public double riskScore; // 0.0 to 100.0
    public String suspectAccount;
    public String suspectVpa;
    public String sourceVpa;
    public String targetVpa;
    public int hopCount;
    public double timeToDrainSeconds;
    public double drainPercentage;
    public String details;

    public MuleAlert() {}

    public MuleAlert(String alertId, String alertTime, String ruleCode, String severity,
                     double riskScore, String suspectAccount, String suspectVpa,
                     String sourceVpa, String targetVpa, int hopCount,
                     double timeToDrainSeconds, double drainPercentage, String details) {
        this.alertId = alertId;
        this.alertTime = alertTime;
        this.ruleCode = ruleCode;
        this.severity = severity;
        this.riskScore = riskScore;
        this.suspectAccount = suspectAccount;
        this.suspectVpa = suspectVpa;
        this.sourceVpa = sourceVpa;
        this.targetVpa = targetVpa;
        this.hopCount = hopCount;
        this.timeToDrainSeconds = timeToDrainSeconds;
        this.drainPercentage = drainPercentage;
        this.details = details;
    }
}

