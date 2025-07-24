# FI-SAP-001: Statistical Analysis Protocol for Consciousness Research
## Ensuring Rigorous and Reproducible Analysis Across All Canon I Studies
**Document ID:** FI-SAP-001  
**Canon:** 0 (Meta-Canon)  
**Date:** December 19, 2024  
**Status:** Mandatory Protocol

═══════════════════════════════════════════════════════════════
CANON DECLARATION - META-CANON (0)
═══════════════════════════════════════════════════════════════

This document establishes mandatory statistical standards for all
Canon I (empirical) research conducted by the Fractality Institute.
These protocols ensure reproducibility, prevent p-hacking, and
maintain scientific integrity across all studies.

Compliance: REQUIRED for all empirical work
Review: Statistical Review Board must approve all analyses
═══════════════════════════════════════════════════════════════

## 1.0 Pre-Registration Requirements

### 1.1 Mandatory Elements

Before ANY data collection:

1. **Hypotheses**: Specific, directional, and falsifiable
2. **Sample Size**: Power analysis with justification
3. **Analysis Plan**: Exact statistical tests specified
4. **Stopping Rules**: When to end data collection
5. **Exclusion Criteria**: Pre-specified data quality standards

### 1.2 Pre-Registration Platforms
- Primary: OSF.io (Open Science Framework)
- Secondary: AsPredicted.org
- Clinical: ClinicalTrials.gov (if applicable)

### 1.3 Timestamp Requirements
```yaml
pre_registration:
  hypothesis_lock: "Before IRB submission"
  analysis_lock: "Before first participant"
  public_posting: "Before data collection"
  amendments: "Noted with justification"
```

## 2.0 Power Analysis Standards

### 2.1 Minimum Power Requirements
- Primary hypotheses: 0.80
- Secondary hypotheses: 0.70
- Exploratory analyses: Report post-hoc power

### 2.2 Effect Size Estimation
```r
# Required justification for effect size choice:
1. Previous literature (cite studies)
2. Pilot data (if available)
3. Smallest effect of interest (clinical relevance)
4. Conservative estimate if uncertain

# Example:
power_analysis <- pwr.t.test(
  d = 0.3,  # Small-medium effect
  sig.level = 0.05,
  power = 0.80,
  type = "two.sample"
)
```

### 2.3 Sample Size Inflation
- Add 20% for expected dropout
- Add 10% for technical failures
- Round up to nearest practical number

## 3.0 Multiple Comparison Corrections

### 3.1 Hierarchy of Corrections

**Primary Hypotheses**: Bonferroni correction
```r
p_adjusted <- p_value * n_primary_tests
```

**Secondary Hypotheses**: Holm-Bonferroni
```r
p.adjust(p_values, method = "holm")
```

**Exploratory Analyses**: False Discovery Rate (FDR)
```r
p.adjust(p_values, method = "fdr")
```

### 3.2 Family-Wise Error Rate
- Define "families" of tests in advance
- Each family gets α = 0.05
- Document all tests performed

## 4.0 Data Quality Standards

### 4.1 Preprocessing Documentation
```yaml
preprocessing_pipeline:
  - step: "Artifact removal"
    method: "ICA with automated component rejection"
    parameters: "variance > 3SD"
    justification: "Standard in field"
  
  - step: "Filtering"
    method: "Butterworth bandpass"
    parameters: "0.5-50 Hz, 4th order"
    justification: "Remove drift and line noise"
```

### 4.2 Quality Metrics
**Required Reporting**:
- Percent data retained after cleaning
- Signal-to-noise ratios
- Distribution of excluded trials by condition
- Participant exclusion reasons

### 4.3 Outlier Handling
```r
# Pre-specified outlier criteria:
outlier_methods <- list(
  univariate = "z-score > 3.5",
  multivariate = "Mahalanobis distance p < 0.001",
  temporal = "Isolated points > 5SD from local mean"
)

# Must report:
# - Number of outliers by method
# - Results with and without outliers
# - Justification for exclusion
```

## 5.0 Required Statistical Reporting

### 5.1 Effect Sizes (Always Report)
```r
# For t-tests
cohen_d <- (mean1 - mean2) / pooled_sd

# For ANOVA
eta_squared <- SS_effect / SS_total

# For correlations
r_squared <- cor(x, y)^2

# For regression
report: R², adjusted R², f²
```

### 5.2 Confidence Intervals
- 95% CI for all point estimates
- Bootstrap CI for non-normal data
- Plot CI in all figures

### 5.3 Exact Statistics
```markdown
GOOD: "t(48) = 2.31, p = 0.025, d = 0.66, 95% CI [0.08, 1.23]"
BAD: "p < 0.05"
```

## 6.0 Bayesian Analysis Requirements

### 6.1 When to Use Bayesian Methods
- Small sample sizes (n < 30)
- Null results of interest
- Updating from prior studies
- Non-normal distributions

### 6.2 Prior Specification
```r
# Document all priors
priors <- list(
  effect = "Normal(0, 1)",      # Skeptical prior
  variance = "Cauchy(0, 0.5)",  # Weakly informative
  correlation = "Beta(1, 1)"    # Uniform
)

# Sensitivity analysis required
sensitivity <- list(
  narrow = "Normal(0, 0.5)",
  default = "Normal(0, 1)",
  wide = "Normal(0, 2)"
)
```

### 6.3 Bayes Factor Interpretation
```
BF₁₀ > 100: Extreme evidence for H₁
BF₁₀ > 30: Very strong evidence for H₁
BF₁₀ > 10: Strong evidence for H₁
BF₁₀ > 3: Moderate evidence for H₁
BF₁₀ ≈ 1: No evidence
BF₁₀ < 1/3: Moderate evidence for H₀
```

## 7.0 Replication Standards

### 7.1 Internal Replication
- Split sample into discovery/replication
- Report both separately
- Only claim effects that replicate

### 7.2 Direct Replication
- Exact same protocol
- New participants
- Pre-registered
- Original effect size in power analysis

### 7.3 Conceptual Replication
- Different methodology
- Same construct
- Converging evidence
- Meta-analysis when n ≥ 3

## 8.0 Null Result Handling

### 8.1 Equivalence Testing
```r
# Test if effect is smaller than meaningful threshold
TOST(
  mean_diff = observed_difference,
  lower_bound = -0.3,  # Smallest effect of interest
  upper_bound = 0.3,
  alpha = 0.05
)
```

### 8.2 Null Result Reporting
**Required Elements**:
- Post-hoc power analysis
- Bayes Factor for null
- Confidence interval around zero
- Statement: "We found no evidence for..."

## 9.0 Visualization Requirements

### 9.1 Individual Data Points
```r
# Always show:
- Individual participant data
- Distribution shape
- Central tendency + spread
- Sample size

# Example:
ggplot(data, aes(x = condition, y = value)) +
  geom_violin() +
  geom_point(position = position_jitter(0.1)) +
  stat_summary(fun.data = mean_cl_boot)
```

### 9.2 No Bar Charts for Continuous Data
- Use violin plots, box plots, or sina plots
- Show full distributions
- Include individual trajectories for repeated measures

## 10.0 Code and Data Sharing

### 10.1 Analysis Code
```yaml
requirements:
  - language: "R or Python"
  - style: "Commented and clear"
  - reproducible: "Seed set for random processes"
  - versioned: "Git with meaningful commits"
  - documented: "README with instructions"
```

### 10.2 Data Format
```yaml
data_standards:
  - format: "CSV or open formats"
  - structure: "Tidy data principles"
  - metadata: "Data dictionary included"
  - anonymized: "No identifying information"
  - accessible: "DOI through repository"
```

## 11.0 Review Process

### 11.1 Statistical Review Board
**Composition**:
- Statistician (PhD)
- Domain expert
- Open science advocate

**Reviews**:
- Pre-registration adequacy
- Analysis code
- Results interpretation
- Publication drafts

### 11.2 Red Team Analysis
For major findings:
- Independent analyst tries to break results
- Alternative analyses attempted
- P-hacking detection algorithms
- Report all attempted approaches

## 12.0 Common Pitfalls to Avoid

### 12.1 The Garden of Forking Paths
❌ Testing multiple outcomes until significance
✅ Pre-specify primary outcome

### 12.2 HARKing
❌ Hypothesizing After Results are Known
✅ Clear separation of confirmatory/exploratory

### 12.3 Optional Stopping
❌ Stopping when p < 0.05
✅ Pre-specified sample size or sequential analysis

### 12.4 P-value Shopping
❌ Trying different tests until significant
✅ Pre-specified analysis plan

## 13.0 Transparency Checklist

Before submission, confirm:
- [ ] Pre-registration public and unchanged
- [ ] All data publicly available
- [ ] Analysis code reproduces results
- [ ] All tests reported (not just significant)
- [ ] Effect sizes and CIs for all effects
- [ ] Power analysis included
- [ ] Limitations honestly discussed
- [ ] Conflicts of interest declared

---

*"The only way to do great science is to do honest science."*

**This protocol is mandatory for all Canon I research. No exceptions.**