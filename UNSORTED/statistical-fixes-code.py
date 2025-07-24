# Statistical Fixes for DNA Pattern Analysis
# Addresses the valid criticisms from peer review

import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.multitest import multipletests
from sklearn.model_selection import LeaveOneOut, cross_val_score
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

# %% Fix 1: GC-Content Bias Correction

def calculate_gc_content(sequence):
    """Calculate GC content of a sequence"""
    gc_count = sequence.count('G') + sequence.count('C')
    return gc_count / len(sequence)

def calculate_expected_kmer_frequency(kmer, gc_content):
    """
    Calculate expected k-mer frequency based on actual GC content
    instead of assuming uniform 25% for each base
    """
    gc_freq = gc_content / 2  # Frequency of G or C
    at_freq = (1 - gc_content) / 2  # Frequency of A or T
    
    expected_freq = 1.0
    for base in kmer:
        if base in 'GC':
            expected_freq *= gc_freq
        else:
            expected_freq *= at_freq
    
    return expected_freq

def gc_corrected_enrichment(sequence, kmer):
    """
    Calculate enrichment with GC-bias correction
    """
    gc_content = calculate_gc_content(sequence)
    
    # Observed frequency
    count = sequence.count(kmer)
    possible_positions = len(sequence) - len(kmer) + 1
    observed_freq = count / possible_positions
    
    # Expected frequency based on GC content
    expected_freq = calculate_expected_kmer_frequency(kmer, gc_content)
    
    # Corrected enrichment
    if expected_freq > 0:
        enrichment = observed_freq / expected_freq
    else:
        enrichment = 0
    
    # Calculate p-value using binomial test
    p_value = stats.binom_test(count, possible_positions, expected_freq, alternative='greater')
    
    return {
        'enrichment': enrichment,
        'p_value': p_value,
        'observed_count': count,
        'expected_count': expected_freq * possible_positions,
        'gc_content': gc_content
    }

# %% Fix 2: Multiple Testing Correction

def analyze_all_kmers_with_correction(sequences, k=6, method='fdr_bh'):
    """
    Analyze all k-mers with multiple testing correction
    """
    all_results = []
    
    for seq_name, sequence in sequences.items():
        # Get all k-mers
        kmers = [sequence[i:i+k] for i in range(len(sequence) - k + 1)]
        unique_kmers = set(kmers)
        
        # Calculate enrichment for each unique k-mer
        for kmer in unique_kmers:
            result = gc_corrected_enrichment(sequence, kmer)
            result['sequence'] = seq_name
            result['kmer'] = kmer
            all_results.append(result)
    
    # Convert to DataFrame
    results_df = pd.DataFrame(all_results)
    
    # Apply multiple testing correction
    p_values = results_df['p_value'].values
    rejected, corrected_pvals, _, _ = multipletests(p_values, method=method)
    
    results_df['p_adjusted'] = corrected_pvals
    results_df['significant'] = rejected
    
    # Filter for significant results only
    significant_df = results_df[results_df['significant']].copy()
    
    print(f"Total k-mers tested: {len(results_df)}")
    print(f"Significant after {method} correction: {len(significant_df)}")
    print(f"False Discovery Rate: {method}")
    
    return significant_df

# %% Fix 3: Proper Sample Size Check for ML

def check_ml_feasibility(X, y, min_samples_per_class=15):
    """
    Check if we have enough samples for meaningful ML
    """
    unique_classes, counts = np.unique(y, return_counts=True)
    
    print("Sample sizes per class:")
    for cls, count in zip(unique_classes, counts):
        print(f"  {cls}: {count} samples")
    
    min_count = min(counts)
    
    if min_count < min_samples_per_class:
        print(f"\nWARNING: Minimum class has only {min_count} samples.")
        print(f"Need at least {min_samples_per_class} per class for reliable ML.")
        print("Recommendations:")
        print("  1. Collect more data")
        print("  2. Use simpler statistical tests instead of ML")
        print("  3. Combine similar classes to increase sample size")
        return False
    
    return True

def safe_ml_validation(X, y):
    """
    Perform ML validation only if we have enough samples
    """
    if not check_ml_feasibility(X, y):
        print("\nSkipping ML due to insufficient samples.")
        return None
    
    # Use appropriate CV strategy based on sample size
    min_samples = min(np.bincount(y))
    
    if min_samples < 5:
        cv = LeaveOneOut()
        cv_name = "Leave-One-Out"
    elif min_samples < 10:
        cv = 3  # 3-fold
        cv_name = "3-fold"
    else:
        cv = 5  # 5-fold
        cv_name = "5-fold"
    
    print(f"\nUsing {cv_name} cross-validation")
    
    # Perform cross-validation
    from sklearn.ensemble import RandomForestClassifier
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    scores = cross_val_score(rf, X, y, cv=cv)
    
    print(f"Accuracy: {scores.mean():.2%} (+/- {scores.std() * 2:.2%})")
    
    return scores

# %% Fix 4: Proper Dose-Response Analysis

def analyze_dose_response_properly(violation_levels, quality_scores):
    """
    Analyze dose-response with proper statistics
    """
    # Remove any NaN values
    mask = ~(np.isnan(violation_levels) | np.isnan(quality_scores))
    violation_levels = violation_levels[mask]
    quality_scores = quality_scores[mask]
    
    # 1. Spearman correlation (doesn't assume linearity)
    corr, p_value = stats.spearmanr(violation_levels, quality_scores)
    print(f"Spearman correlation: r = {corr:.3f}, p = {p_value:.3e}")
    
    # 2. Linear regression for comparison
    slope, intercept, r_value, p_value_linear, std_err = stats.linregress(violation_levels, quality_scores)
    print(f"Linear regression: R² = {r_value**2:.3f}, p = {p_value_linear:.3e}")
    
    # 3. Find actual threshold (where function drops below 50% of maximum)
    max_quality = quality_scores[violation_levels == 0].mean()
    threshold_quality = max_quality * 0.5
    
    # Find violation level where quality drops below threshold
    for i, level in enumerate(np.unique(violation_levels)):
        mean_quality = quality_scores[violation_levels == level].mean()
        if mean_quality < threshold_quality:
            actual_threshold = level
            break
    else:
        actual_threshold = 1.0
    
    print(f"Actual 50% degradation threshold: {actual_threshold:.1%} violations")
    
    # 4. Report EC50 if using dose-response fitting
    try:
        from scipy.optimize import curve_fit
        
        def dose_response(x, bottom, top, ec50, hill):
            return bottom + (top - bottom) / (1 + (x / ec50) ** hill)
        
        popt, pcov = curve_fit(dose_response, violation_levels, quality_scores,
                              p0=[0.2, 0.8, 0.5, 2],
                              bounds=([0, 0, 0, 0.1], [1, 1, 1, 10]))
        
        print(f"Dose-response EC50: {popt[2]:.3f}")
        print(f"Hill coefficient: {popt[3]:.2f}")
        
        if popt[3] > 4:
            print("WARNING: Hill coefficient >4 suggests overfitting or artifacts")
    except:
        print("Dose-response fitting failed")
    
    return corr, actual_threshold

# %% Fix 5: Honest Reporting Function

def generate_honest_summary(results):
    """
    Generate an honest summary of what we can and cannot conclude
    """
    print("\n" + "="*60)
    print("HONEST STATISTICAL SUMMARY")
    print("="*60)
    
    print("\nWhat we CAN say:")
    print("1. We found k-mer patterns that correlate with biological function labels")
    print("2. GGAATG appears enriched in regeneration sequences (pending GC correction)")
    print("3. Synthetic sequences with disrupted patterns show degraded computational metrics")
    
    print("\nWhat we CANNOT say:")
    print("1. These patterns cause morphogenesis (only correlation shown)")
    print("2. The patterns represent 'grammar' (this is a metaphor)")
    print("3. We can predict cell behavior (no experimental validation)")
    
    print("\nStatistical limitations:")
    print("1. Small sample size (n=17) limits all conclusions")
    print("2. Multiple testing inflates false positive risk")
    print("3. No phylogenetic correction for evolutionary relationships")
    print("4. No epigenetic or chromatin context considered")
    
    print("\nNext steps required:")
    print("1. Experimental validation in living cells")
    print("2. Larger dataset with proper controls")
    print("3. Integration with ChIP-seq, ATAC-seq data")
    print("4. Mechanistic studies of any validated patterns")

# %% Example Usage

# Example data
sequences = {
    'regen_1': 'GGAATGGGAATGGGAATGCGTGACGTCATGACGTCAGATAGGAATGGGAATG',
    'regen_2': 'GGAATGGGAATGCGTGACGTCAGGAATGGGAATGTGACGTCATTTGGGAAAC',
    'control_1': 'GATAAGATAAGGATCCAAGGAATTGGGAATGGAATGCGTGACGTCATGACGT',
    'control_2': 'CAGCTGCAGCTGCAGCTGCGTGACGTCATGACGTCAGATACAGCTGCAGCTG'
}

print("Running improved analysis with statistical corrections...\n")

# 1. GC-corrected enrichment for GGAATG
print("1. GC-CORRECTED ENRICHMENT ANALYSIS")
print("-"*40)
for seq_name, sequence in sequences.items():
    result = gc_corrected_enrichment(sequence, 'GGAATG')
    print(f"{seq_name}:")
    print(f"  GC content: {result['gc_content']:.1%}")
    print(f"  GGAATG enrichment: {result['enrichment']:.1f}x")
    print(f"  P-value: {result['p_value']:.3e}")

# 2. Multiple testing correction example
print("\n2. MULTIPLE TESTING CORRECTION")
print("-"*40)
significant_kmers = analyze_all_kmers_with_correction(sequences, k=6)

# 3. ML feasibility check
print("\n3. MACHINE LEARNING FEASIBILITY")
print("-"*40)
# Example with too few samples
X_small = np.random.rand(8, 10)  # 8 samples, 10 features
y_small = np.array([0, 0, 1, 1, 2, 2, 3, 3])  # 4 classes, 2 samples each
safe_ml_validation(X_small, y_small)

# 4. Proper dose-response
print("\n4. DOSE-RESPONSE ANALYSIS")
print("-"*40)
# Example dose-response data
violation_levels = np.repeat([0, 0.1, 0.25, 0.5, 0.75, 0.9, 1.0], 9)
quality_scores = np.array([0.8, 0.82, 0.79] * 7) - violation_levels * 0.6 + np.random.normal(0, 0.05, 63)
analyze_dose_response_properly(violation_levels, quality_scores)

# 5. Generate honest summary
print("\n5. HONEST SUMMARY")
generate_honest_summary(None)

print("\n" + "="*60)
print("These corrections address the major statistical criticisms")
print("and provide a more rigorous foundation for the work.")
print("="*60)
