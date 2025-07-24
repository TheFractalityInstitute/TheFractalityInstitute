# FI-RM-001v3: The Riemann Signature Project - Rigorous Methodology Update
## Pre-Registered Experimental Protocol with Falsification Criteria
**Document ID:** FI-RM-001v3  
**Canon:** I - Empirical  
**Date:** December 19, 2024  
**Status:** Pre-Registration Ready  
**Replaces:** FI-RM-001v2

═══════════════════════════════════════════════════════════════
CANON DECLARATION - EMPIRICAL CANON (I)
Document ID: FI-RM-001v3
Canon: I - Empirical
Epistemological Status: Testable/Falsifiable Claims
Evidence Level: ☐ Theoretical ☑ Preliminary ☐ Validated
Peer Review Status: ☐ Internal ☐ External ☐ Published

This document contains only empirically testable hypotheses with
pre-specified statistical criteria. All analyses will be conducted
regardless of outcome and published in accordance with open science
principles.

Cross-Canon Dependencies: None (pure empirical protocol)
Related Documents: FI-CSP-001 (Citizen Science Implementation)
═══════════════════════════════════════════════════════════════

## 1.0 Refined Research Question

Do human EEG recordings contain periodic frequency components that correlate with the known distribution of Riemann zeta function zeros beyond what would be expected by chance?

**Note**: This is a pattern-detection study. Finding or not finding such patterns does not validate any particular theory of consciousness—it simply documents whether this mathematical structure appears in neural data.

## 2.0 Pre-Registered Hypotheses

### Primary Hypothesis (H1)
The spacing between peak frequencies in human EEG spectra will show statistically significant correlation with the spacing between Riemann zeros (first 50 zeros) compared to:
- Random number sequences
- Other mathematical sequences (Fibonacci, primes)
- Phase-scrambled versions of the same EEG data

**Falsification Criteria**: 
- p > 0.05 after Bonferroni correction
- Effect size (Cohen's d) < 0.3
- Failure to replicate in independent dataset

### Secondary Hypothesis (H2)
If H1 is supported, the correlation strength will vary with consciousness state:
- Meditation > Resting > Task-focused
- REM sleep > Deep sleep > Waking

**Falsification Criteria**:
- No significant difference between states (ANOVA p > 0.05)
- Effect not monotonic as predicted

### Null Hypothesis (H0)
EEG frequency patterns show no relationship to Riemann zeros beyond chance expectations.

## 3.0 Methodology

### 3.1 Sample Size Calculation

**Power Analysis** (G*Power 3.1):
- Expected effect size: d = 0.3 (small-medium)
- Alpha: 0.05 (Bonferroni adjusted: 0.0125)
- Power: 0.80
- **Required N**: 139 per group × 4 groups = 556 total

**Groups**:
1. Experienced meditators (>5 years practice)
2. Controls (no meditation experience)
3. Musicians (>10 years, for rhythm control)
4. Mathematicians (for familiarity bias control)

### 3.2 EEG Data Collection

**Equipment**: 
- 64-channel system (10-20 placement)
- Sampling rate: 1000 Hz
- Reference: Linked mastoids
- Impedance: <5 kΩ

**Conditions** (randomized order):
1. Resting state (eyes closed, 10 min)
2. Meditation (20 min)
3. Mathematical task (15 min)
4. Music listening (15 min)

### 3.3 Analysis Pipeline

**Step 1: Preprocessing**
```python
# Standardized pipeline
1. Bandpass filter: 0.5-100 Hz
2. ICA artifact removal (automated)
3. Epoch rejection (±100 μV threshold)
4. Minimum 80% data retention required
```

**Step 2: Frequency Analysis**
```python
# Welch's method parameters (pre-specified)
- Window: 4 seconds
- Overlap: 50%
- Frequency resolution: 0.25 Hz
- Range of interest: 1-50 Hz
```

**Step 3: Peak Detection**
```python
# Automated peak finding
- Prominence threshold: 2 SD above mean
- Minimum distance: 0.5 Hz
- Maximum 30 peaks per participant
```

**Step 4: Riemann Correlation**
```python
def calculate_riemann_correlation(peak_frequencies):
    """
    Pre-registered analysis code
    """
    # Scale Riemann zeros to EEG frequency range
    riemann_zeros = get_first_n_zeros(50)
    scaled_zeros = scale_to_range(riemann_zeros, 1, 50)
    
    # Compare spacings, not absolute values
    eeg_spacings = np.diff(peak_frequencies)
    riemann_spacings = np.diff(scaled_zeros)
    
    # Multiple correlation methods
    pearson_r = stats.pearsonr(eeg_spacings, riemann_spacings[:len(eeg_spacings)])
    spearman_r = stats.spearmanr(eeg_spacings, riemann_spacings[:len(eeg_spacings)])
    dtw_distance = dynamic_time_warping(eeg_spacings, riemann_spacings)
    
    return {
        'pearson': pearson_r,
        'spearman': spearman_r,
        'dtw': dtw_distance
    }
```

### 3.4 Control Analyses

**Control 1: Surrogate Data**
- Generate 1000 phase-scrambled versions of each EEG
- Calculate same correlations
- Establish chance distribution

**Control 2: Alternative Sequences**
- Fibonacci numbers (first 50)
- Prime numbers (first 50)
- Random uniform distribution
- AR(1) process matched to EEG autocorrelation

**Control 3: Multiple Scaling Attempts**
- Test 100 different scaling factors
- Bonferroni correct for multiple comparisons
- Report if ANY scaling produces correlation

## 4.0 Statistical Analysis Plan

### 4.1 Primary Analysis
```r
# Mixed effects model
model <- lmer(correlation ~ sequence_type + state + (1|participant), data=results)

# Planned contrasts
contrast1: Riemann vs. All_Other_Sequences
contrast2: Meditation vs. Resting (if contrast1 significant)
```

### 4.2 Robustness Checks
1. Bootstrap confidence intervals (10,000 iterations)
2. Permutation testing for non-parametric validation
3. Leave-one-out cross-validation
4. Bayesian analysis for evidence strength

### 4.3 Correction for Multiple Comparisons
- Primary hypotheses: Bonferroni correction
- Exploratory analyses: False Discovery Rate (FDR)
- Report all tests performed, not just significant ones

## 5.0 Quality Controls

### 5.1 Blinding
- Analysts blind to group membership
- Automated pipeline reduces subjective decisions
- Code locked before data collection

### 5.2 Data Quality Metrics
- Signal-to-noise ratio must exceed 10 dB
- Less than 20% data rejected
- Stable impedances throughout recording

### 5.3 Positive Controls
- Alpha peak detection (8-12 Hz) as sanity check
- Sleep spindle detection in sleep data
- P300 response in oddball task

## 6.0 Results Interpretation Framework

### If H1 Supported:
- Report exact p-values and effect sizes
- Acknowledge pattern correlation ≠ consciousness theory validation
- Call for independent replication
- Make all data publicly available

### If H1 Not Supported:
- Publish null results prominently
- Analyze whether power was sufficient
- Consider alternative frequency ranges
- Do NOT engage in post-hoc fishing

## 7.0 Open Science Commitments

1. **Pre-registration**: OSF.io before data collection
2. **Open Data**: All raw EEG on OpenNeuro
3. **Open Code**: Analysis pipeline on GitHub
4. **Open Access**: Preprint on bioRxiv regardless of outcome
5. **Registered Report**: Seeking journal commitment before data collection

## 8.0 Ethical Considerations

- IRB approval required
- Informed consent emphasizing uncertainty
- No claims about consciousness or healing
- Incidental findings protocol in place

## 9.0 Budget and Timeline

**Budget**: $125,000
- EEG technician: $50,000
- Participant compensation: $30,000
- Equipment access: $20,000
- Analysis/publication: $25,000

**Timeline**:
- Months 1-2: IRB and pre-registration
- Months 3-8: Data collection
- Months 9-10: Analysis
- Month 11: Manuscript preparation
- Month 12: Submission

## 10.0 Potential Outcomes and Their Meanings

**Positive Result**: 
"We found a statistical correlation between EEG frequency patterns and Riemann zero spacings. This is an interesting mathematical curiosity that warrants replication. No consciousness theories are validated by this finding."

**Negative Result**: 
"We found no evidence for Riemann patterns in EEG data using our pre-specified methods. This suggests that if such patterns exist, they are not detectable using standard frequency analysis."

**Either Way**: 
"This study demonstrates the feasibility of citizen science approaches to consciousness research and the importance of pre-registered, open science methods."

---

*This protocol is designed to be bulletproof against criticism while still allowing for genuine discovery. By pre-specifying everything and committing to publish regardless of outcome, we ensure scientific integrity while exploring an unconventional hypothesis.*