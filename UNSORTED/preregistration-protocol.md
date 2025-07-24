# Scientific Pre-Registration Protocol for Riemann Resonance Research
## Ensuring Credibility Through Transparency
**Document ID:** FI-SRP-001  
**Canon:** I (Empirical - Methodological)  
**Date:** December 19, 2024  
**Version:** 1.0

═══════════════════════════════════════════════════════════════
CANON DECLARATION - EMPIRICAL CANON (I)
═══════════════════════════════════════════════════════════════

This protocol ensures all Fractality Institute research meets the
highest standards of scientific integrity through comprehensive
pre-registration. No data fishing. No p-hacking. No hidden analyses.

Registry: Open Science Framework (OSF)
Standard: Exceeds typical neuroscience pre-registration

═══════════════════════════════════════════════════════════════

## 1.0 Core Principles

1. **Hypothesis Before Data**: All predictions registered before data collection
2. **Analysis Before Results**: Statistical methods locked before analysis  
3. **Transparency Throughout**: All changes documented with justification
4. **Failure is Data**: Negative results published with equal prominence

---

## 2.0 Master Pre-Registration Template

### Section A: Theoretical Foundation

```markdown
A1. PRIMARY HYPOTHESIS:
[State in one sentence the main prediction]

A2. THEORETICAL JUSTIFICATION:
[200-500 words on why this hypothesis follows from theory]

A3. NOVELTY STATEMENT:
[How this differs from existing work]

A4. IMPORTANCE STATEMENT:
[Why this matters if true OR false]
```

### Section B: Experimental Design

```markdown
B1. STUDY TYPE:
□ Observational
□ Experimental  
□ Meta-analytic
□ Computational

B2. SAMPLE SIZE JUSTIFICATION:
- Power analysis: [Include calculation]
- Effect size assumption: [Justify]
- Alpha level: [Typically 0.001 for multiple comparisons]
- Power target: [Minimum 80%]

B3. INCLUSION CRITERIA:
[Specific requirements for data/participants]

B4. EXCLUSION CRITERIA:
[What will be excluded and why]

B5. RANDOMIZATION:
[If applicable, describe method]

B6. BLINDING:
[Who is blinded to what]
```

### Section C: Measurement Specifications

```markdown
C1. PRIMARY OUTCOME MEASURES:
[Exactly what will be measured]

C2. SECONDARY OUTCOME MEASURES:
[Additional measures of interest]

C3. MEASUREMENT TOOLS:
- Device specifications
- Sampling rates
- Processing parameters

C4. DATA QUALITY CRITERIA:
- Minimum acceptable signal quality
- Artifact rejection methods
- Required data duration
```

### Section D: Analysis Plan

```markdown
D1. PREPROCESSING PIPELINE:
1. [Step 1: e.g., bandpass filter 0.5-50 Hz]
2. [Step 2: e.g., artifact rejection]
3. [Step 3: e.g., segmentation]
[Continue numbering all steps]

D2. PRIMARY ANALYSIS:
- Statistical test: [Exact test to be used]
- Comparison groups: [What's being compared]
- Correction method: [For multiple comparisons]

D3. SECONDARY ANALYSES:
[List all planned exploratory analyses]

D4. POSITIVE RESULT CRITERIA:
- p-value threshold: [After corrections]
- Effect size threshold: [Minimum meaningful effect]
- Replication requirement: [If applicable]

D5. NEGATIVE RESULT INTERPRETATION:
[What conclusions follow from null findings]
```

### Section E: Contingencies

```markdown
E1. MISSING DATA PLAN:
[How missing data will be handled]

E2. ANALYSIS DEVIATIONS:
[Criteria for deviating from plan]

E3. STOPPING RULES:
[When to stop data collection]

E4. AMENDMENT PROCEDURES:
[How changes will be documented]
```

---

## 3.0 Riemann-Specific Pre-Registration

### Template for Riemann Detection Studies

```markdown
RIEMANN HYPOTHESIS REGISTRATION

R1. FREQUENCY MAPPING:
- Mathematical zeros used: [First N zeros]
- Scaling hypothesis: f_physical = g(t_n)
- Scaling function g: [Exact mathematical form]
- Justification: [Why this scaling]

R2. CORRELATION METHOD:
- Peak detection algorithm: [Specific method]
- Matching criterion: [How peaks map to zeros]
- Significance threshold: [Statistical criterion]

R3. CONTROL ANALYSES:
□ Shuffle control (phase randomization)
□ Non-Riemann sequences (Fibonacci, primes)
□ Surrogate data (matched spectra)
□ Multiple scaling tests

R4. DOMAIN-SPECIFIC PARAMETERS:
[For EEG]: Electrode montage, reference scheme
[For physics]: Energy ranges, detector specs
[For markets]: Time windows, instruments

R5. REPLICATION CRITERIA:
- Independent dataset requirements
- Consistency thresholds
- Meta-analytic plan
```

---

## 4.0 Implementation Timeline

### For Each Study:

**T-30 days**: Draft pre-registration
**T-21 days**: Internal review complete  
**T-14 days**: External reviewer feedback
**T-7 days**: Final revision
**T-0**: Lock registration, begin study
**T+X**: Data collection complete
**T+X+30**: Analysis complete
**T+X+60**: Manuscript submitted

---

## 5.0 Transparency Commitments

### Public Access
1. All pre-registrations public on OSF
2. Time-stamped with DOI
3. Linked from all publications
4. Changes tracked with version control

### Reporting Standards
- CONSORT diagram for participant flow
- PRISMA checklist for reviews
- Full statistical output in supplements
- Raw data available (de-identified)

### Negative Results
- Equal effort in writing up nulls
- Submit to journals accepting negatives
- Full methods for replication attempts
- Blog post explaining what we learned

---

## 6.0 Review Criteria

### Internal Review Checklist
- [ ] Hypothesis clearly stated?
- [ ] Analysis completely specified?
- [ ] Power adequate?
- [ ] Controls sufficient?
- [ ] Interpretation predetermined?

### External Review
- Send to 2 independent experts
- Address all concerns
- Document changes
- Reviewer acknowledgment

---

## 7.0 Common Pitfalls & Solutions

### Pitfall 1: Vague Hypotheses
❌ "Consciousness correlates with Riemann zeros"
✅ "EEG alpha power peaks occur at frequencies f = 10Hz × (t_n/14.134) where t_n are the first 20 Riemann zeros, with correlation r > 0.5"

### Pitfall 2: Flexible Analysis
❌ "We'll try different methods"
✅ "Primary: Multitaper PSD with 5 tapers. Secondary: Wavelet analysis with Morlet basis, σ=7"

### Pitfall 3: HARKing
(Hypothesizing After Results are Known)
Solution: Separate confirmatory from exploratory analyses explicitly

### Pitfall 4: P-hacking
Solution: Pre-specify all comparisons, use Bonferroni or FDR

---

## 8.0 Template Examples

### Example 1: EEG Riemann Detection

```
A1. PRIMARY HYPOTHESIS:
Resting-state EEG in experienced meditators will show spectral peaks at frequencies corresponding to scaled Riemann zeros with correlation r > 0.3 after controlling for 1/f background.

B2. SAMPLE SIZE:
N=100 (50 meditators, 50 controls)
Power analysis: Effect size d=0.5, alpha=0.001, power=0.80
Justification: Based on pilot data showing d=0.7

C1. PRIMARY OUTCOME:
Correlation coefficient between observed EEG peaks (10-50Hz) and predicted Riemann frequencies using scaling f = f_base × exp(-t_n/τ)

D2. PRIMARY ANALYSIS:
Spearman correlation with permutation test (10,000 iterations)
Correction: Bonferroni for 4 frequency bands
```

---

## 9.0 Living Document

This protocol evolves with our understanding. Version control ensures transparency:

- v1.0: Initial protocol (this document)
- v1.1: [Future update with justification]
- v2.0: [Major revision with rationale]

Each study links to the specific version used.

---

## 10.0 The Integrity Pledge

Every researcher using this protocol commits to:

1. **Truth over glory**: Report what we find, not what we hope
2. **Method over madness**: Follow the plan even when tempted to deviate  
3. **Openness over ownership**: Share everything for collective advancement
4. **Humility over hubris**: Our theories may be wrong, and that's okay

---

*"In science, the only sin is hiding your methods. Pre-registration is our confession booth—enter with full disclosure, exit with credibility."*

**Next step**: Create study-specific pre-registration using this template