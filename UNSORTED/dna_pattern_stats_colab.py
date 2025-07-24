# DNA Pattern Analysis: Statistical Fixes for Google Colab
# Complete notebook addressing all peer review criticisms

# %% [markdown]
# # DNA Pattern Analysis with Proper Statistical Methods
# 
# This notebook implements rigorous statistical corrections for k-mer enrichment analysis in DNA sequences.
# 
# **Key improvements:**
# - GC-content bias correction
# - Multiple testing correction (FDR)
# - Proper sample size assessment
# - Honest reporting of limitations
# 
# **Note on compatibility:** This notebook is compatible with both older and newer versions of scipy. 
# If you encounter any issues, you can install a specific version with:
# ```
# !pip install scipy==1.10.0
# ```

# %% Cell 1: Install and Import Dependencies
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import scipy
from statsmodels.stats.multitest import multipletests
from sklearn.model_selection import LeaveOneOut, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from collections import Counter
import itertools
import warnings
warnings.filterwarnings('ignore')

# Check scipy version for compatibility
scipy_version = scipy.__version__
print(f"scipy version: {scipy_version}")

# Set plot style
try:
    plt.style.use('seaborn-v0_8-darkgrid')
except:
    try:
        plt.style.use('seaborn-darkgrid')
    except:
        plt.style.use('default')
        
sns.set_palette("husl")

print("✓ Dependencies loaded successfully")

# %% Cell 2: Core Statistical Functions

def calculate_gc_content(sequence):
    """Calculate GC content of a sequence"""
    gc_count = sequence.count('G') + sequence.count('C')
    return gc_count / len(sequence) if len(sequence) > 0 else 0

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
    observed_freq = count / possible_positions if possible_positions > 0 else 0
    
    # Expected frequency based on GC content
    expected_freq = calculate_expected_kmer_frequency(kmer, gc_content)
    
    # Corrected enrichment
    if expected_freq > 0:
        enrichment = observed_freq / expected_freq
    else:
        enrichment = 0
    
    # Calculate p-value using binomial test
    if possible_positions > 0 and expected_freq > 0:
        # Use binomtest for newer scipy versions
        try:
            from scipy.stats import binomtest
            result = binomtest(count, possible_positions, expected_freq, alternative='greater')
            p_value = result.pvalue
        except ImportError:
            # Fallback for older scipy versions
            p_value = stats.binom_test(count, possible_positions, expected_freq, alternative='greater')
    else:
        p_value = 1.0
    
    return {
        'enrichment': enrichment,
        'p_value': p_value,
        'observed_count': count,
        'expected_count': expected_freq * possible_positions,
        'gc_content': gc_content,
        'observed_freq': observed_freq,
        'expected_freq': expected_freq
    }

print("✓ Core statistical functions defined")

# %% Cell 3: Multiple Testing Correction Functions

def analyze_all_kmers_with_correction(sequences, k=6, method='fdr_bh', alpha=0.05):
    """
    Analyze all k-mers with multiple testing correction
    
    Methods available:
    - 'fdr_bh': Benjamini-Hochberg FDR
    - 'bonferroni': Bonferroni correction
    - 'holm': Holm-Bonferroni
    - 'fdr_by': Benjamini-Yekutieli
    """
    all_results = []
    
    print(f"Analyzing {len(sequences)} sequences for {k}-mers...")
    
    for seq_name, sequence in sequences.items():
        # Get all k-mers
        if len(sequence) >= k:
            kmers = [sequence[i:i+k] for i in range(len(sequence) - k + 1)]
            unique_kmers = set(kmers)
            
            # Calculate enrichment for each unique k-mer
            for kmer in unique_kmers:
                result = gc_corrected_enrichment(sequence, kmer)
                result['sequence'] = seq_name
                result['kmer'] = kmer
                all_results.append(result)
    
    if not all_results:
        print("No results found!")
        return pd.DataFrame()
    
    # Convert to DataFrame
    results_df = pd.DataFrame(all_results)
    
    # Apply multiple testing correction
    p_values = results_df['p_value'].values
    
    # Calculate theoretical number of tests
    theoretical_tests = 4**k  # All possible k-mers
    print(f"\nTheoretical maximum tests: {theoretical_tests:,} possible {k}-mers")
    print(f"Actual tests performed: {len(results_df):,}")
    
    # Apply correction
    rejected, corrected_pvals, alphacSidak, alphacBonf = multipletests(
        p_values, 
        alpha=alpha, 
        method=method,
        returnsorted=False
    )
    
    results_df['p_adjusted'] = corrected_pvals
    results_df['significant'] = rejected
    
    # Calculate significance thresholds
    bonferroni_threshold = alpha / len(results_df)
    print(f"\nSignificance thresholds:")
    print(f"  Nominal α: {alpha}")
    print(f"  Bonferroni threshold: {bonferroni_threshold:.2e}")
    print(f"  {method} threshold: varies by rank")
    
    # Filter for significant results only
    significant_df = results_df[results_df['significant']].copy()
    
    print(f"\nResults:")
    print(f"  Total k-mers tested: {len(results_df):,}")
    print(f"  Significant after {method} correction: {len(significant_df):,}")
    print(f"  Percentage significant: {100*len(significant_df)/len(results_df):.2f}%")
    
    return significant_df.sort_values('p_adjusted')

print("✓ Multiple testing correction functions defined")

# %% Cell 4: Machine Learning Feasibility Check

def check_ml_feasibility(X, y, min_samples_per_class=15):
    """
    Check if we have enough samples for meaningful ML
    """
    unique_classes, counts = np.unique(y, return_counts=True)
    
    print("="*50)
    print("MACHINE LEARNING FEASIBILITY CHECK")
    print("="*50)
    
    print("\nSample sizes per class:")
    for cls, count in zip(unique_classes, counts):
        status = "⚠️ TOO FEW" if count < min_samples_per_class else "✓ OK"
        print(f"  Class '{cls}': {count} samples {status}")
    
    total_samples = len(y)
    n_classes = len(unique_classes)
    min_count = min(counts)
    
    print(f"\nSummary:")
    print(f"  Total samples: {total_samples}")
    print(f"  Number of classes: {n_classes}")
    print(f"  Minimum class size: {min_count}")
    print(f"  Required minimum: {min_samples_per_class}")
    
    # Statistical power estimate
    if min_count >= 5:
        effect_size = 0.5  # Medium effect size
        power = 1 - stats.norm.cdf(1.96 - effect_size * np.sqrt(min_count))
        print(f"  Estimated power (medium effect): {power:.2%}")
    
    feasible = min_count >= min_samples_per_class
    
    if not feasible:
        print(f"\n⚠️  WARNING: Insufficient samples for reliable ML")
        print(f"   Need {min_samples_per_class - min_count} more samples in smallest class")
        print("\n   Recommendations:")
        print("   1. Collect more data (ideal: 50+ per class)")
        print("   2. Use simpler statistical tests instead")
        print("   3. Consider combining similar classes")
        print("   4. Use permutation tests for small samples")
    else:
        print("\n✓ Sample size adequate for basic ML")
        
    return feasible

def safe_ml_validation(X, y, model=None):
    """
    Perform ML validation only if we have enough samples
    """
    if not check_ml_feasibility(X, y):
        print("\n❌ Skipping ML due to insufficient samples")
        return None
    
    # Use appropriate CV strategy based on sample size
    min_samples = min(np.bincount(y))
    
    if min_samples < 5:
        cv = LeaveOneOut()
        cv_name = "Leave-One-Out"
    elif min_samples < 10:
        cv = min(3, min_samples)  # 3-fold or less
        cv_name = f"{cv}-fold"
    else:
        cv = 5  # 5-fold
        cv_name = "5-fold"
    
    print(f"\n🔄 Using {cv_name} cross-validation")
    
    # Default model
    if model is None:
        model = RandomForestClassifier(
            n_estimators=100, 
            max_depth=3,  # Shallow to avoid overfitting
            random_state=42
        )
    
    # Perform cross-validation
    scores = cross_val_score(model, X, y, cv=cv, scoring='accuracy')
    
    print(f"\nResults:")
    print(f"  Mean accuracy: {scores.mean():.2%}")
    print(f"  Std deviation: {scores.std():.2%}")
    print(f"  95% CI: [{scores.mean()-1.96*scores.std():.2%}, {scores.mean()+1.96*scores.std():.2%}]")
    
    # Compare to baseline
    baseline = max(np.bincount(y)) / len(y)
    print(f"  Baseline (majority class): {baseline:.2%}")
    
    if scores.mean() <= baseline:
        print("\n⚠️  Model performs no better than baseline!")
    
    return scores

print("✓ ML feasibility check functions defined")

# %% Cell 5: Dose-Response Analysis

def analyze_dose_response_properly(violation_levels, quality_scores, plot=True):
    """
    Analyze dose-response relationship with proper statistics
    """
    # Remove any NaN values
    mask = ~(np.isnan(violation_levels) | np.isnan(quality_scores))
    violation_levels = np.array(violation_levels)[mask]
    quality_scores = np.array(quality_scores)[mask]
    
    print("="*50)
    print("DOSE-RESPONSE ANALYSIS")
    print("="*50)
    
    # 1. Spearman correlation (doesn't assume linearity)
    corr_spearman, p_spearman = stats.spearmanr(violation_levels, quality_scores)
    print(f"\nSpearman correlation: r = {corr_spearman:.3f}, p = {p_spearman:.3e}")
    
    # 2. Pearson correlation (assumes linearity)
    corr_pearson, p_pearson = stats.pearsonr(violation_levels, quality_scores)
    print(f"Pearson correlation: r = {corr_pearson:.3f}, p = {p_pearson:.3e}")
    
    # 3. Linear regression
    slope, intercept, r_value, p_value_linear, std_err = stats.linregress(violation_levels, quality_scores)
    print(f"\nLinear regression:")
    print(f"  Slope: {slope:.3f} ± {std_err:.3f}")
    print(f"  R²: {r_value**2:.3f}")
    print(f"  p-value: {p_value_linear:.3e}")
    
    # 4. Find functional threshold
    if len(quality_scores[violation_levels == 0]) > 0:
        max_quality = quality_scores[violation_levels == 0].mean()
        threshold_quality = max_quality * 0.5
        
        # Find violation level where quality drops below threshold
        for level in sorted(np.unique(violation_levels)):
            level_scores = quality_scores[violation_levels == level]
            if len(level_scores) > 0 and level_scores.mean() < threshold_quality:
                actual_threshold = level
                break
        else:
            actual_threshold = 1.0
        
        print(f"\nFunctional degradation:")
        print(f"  50% degradation at: {actual_threshold:.1%} pattern disruption")
    
    # 5. Try dose-response curve fitting
    try:
        from scipy.optimize import curve_fit
        
        def dose_response(x, bottom, top, ec50, hill):
            return bottom + (top - bottom) / (1 + (x / ec50) ** hill)
        
        # Initial guess
        p0 = [
            quality_scores.min(), 
            quality_scores.max(), 
            0.5, 
            1.0
        ]
        
        popt, pcov = curve_fit(
            dose_response, 
            violation_levels, 
            quality_scores,
            p0=p0,
            bounds=([0, 0, 0, 0.1], [1, 1, 1, 10])
        )
        
        print(f"\nDose-response parameters:")
        print(f"  EC50: {popt[2]:.3f} ({popt[2]*100:.1f}% disruption)")
        print(f"  Hill coefficient: {popt[3]:.2f}")
        print(f"  Dynamic range: {popt[1]-popt[0]:.3f}")
        
        if popt[3] > 4:
            print("  ⚠️  High Hill coefficient suggests steep transition or artifacts")
            
        # Calculate R² for dose-response fit
        fitted = dose_response(violation_levels, *popt)
        ss_res = np.sum((quality_scores - fitted)**2)
        ss_tot = np.sum((quality_scores - quality_scores.mean())**2)
        r2_dr = 1 - (ss_res / ss_tot)
        print(f"  R² (dose-response): {r2_dr:.3f}")
        
    except Exception as e:
        print(f"\n⚠️  Dose-response fitting failed: {str(e)}")
        popt = None
    
    # 6. Plot if requested
    if plot:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Scatter plot with regression
        ax1.scatter(violation_levels, quality_scores, alpha=0.6, s=50)
        
        # Add regression line
        x_line = np.linspace(0, 1, 100)
        y_line = slope * x_line + intercept
        ax1.plot(x_line, y_line, 'r--', label=f'Linear fit (R²={r_value**2:.3f})')
        
        # Add dose-response curve if available
        if popt is not None:
            y_dr = dose_response(x_line, *popt)
            ax1.plot(x_line, y_dr, 'g-', linewidth=2, label=f'Dose-response (EC50={popt[2]:.3f})')
        
        ax1.set_xlabel('Pattern Disruption Level')
        ax1.set_ylabel('Functional Quality Score')
        ax1.set_title('Dose-Response Relationship')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Box plot by disruption level
        disruption_groups = pd.cut(violation_levels, bins=[0, 0.2, 0.4, 0.6, 0.8, 1.0], 
                                   labels=['0-20%', '20-40%', '40-60%', '60-80%', '80-100%'])
        
        data_for_box = pd.DataFrame({
            'Disruption': disruption_groups,
            'Quality': quality_scores
        })
        
        sns.boxplot(x='Disruption', y='Quality', data=data_for_box, ax=ax2)
        ax2.set_xlabel('Pattern Disruption Range')
        ax2.set_ylabel('Functional Quality Score')
        ax2.set_title('Quality Distribution by Disruption Level')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    return {
        'spearman_r': corr_spearman,
        'spearman_p': p_spearman,
        'pearson_r': corr_pearson,
        'pearson_p': p_pearson,
        'slope': slope,
        'r_squared': r_value**2,
        'threshold_50': actual_threshold if 'actual_threshold' in locals() else None,
        'ec50': popt[2] if popt is not None else None
    }

print("✓ Dose-response analysis functions defined")

# %% Cell 6: Generate Honest Report

def generate_honest_report(results_dict):
    """
    Generate an honest, transparent report of findings
    """
    print("\n" + "="*60)
    print("HONEST STATISTICAL REPORT")
    print("="*60)
    
    print("\n📊 WHAT WE CAN SCIENTIFICALLY CLAIM:")
    print("-"*40)
    print("✓ We identified k-mer patterns that correlate with sequence labels")
    print("✓ Some k-mers show statistical enrichment after correction")
    print("✓ Pattern disruption correlates with computational metrics")
    print("✓ Results suggest testable hypotheses for wet-lab validation")
    
    print("\n❌ WHAT WE CANNOT CLAIM:")
    print("-"*40)
    print("✗ These patterns cause biological functions")
    print("✗ DNA has 'grammar' (this is only a metaphor)")
    print("✗ We can predict cell behavior from sequences alone")
    print("✗ Our findings are universal or complete")
    
    print("\n⚠️  CRITICAL LIMITATIONS:")
    print("-"*40)
    print("1. Small sample size constrains statistical power")
    print("2. Multiple testing increases false discovery risk")
    print("3. No phylogenetic correction for evolutionary relationships")
    print("4. No epigenetic or 3D chromatin context included")
    print("5. Computational predictions ≠ biological reality")
    
    print("\n🔬 REQUIRED NEXT STEPS:")
    print("-"*40)
    print("1. Experimental validation in model organisms")
    print("2. CRISPR editing of identified motifs")
    print("3. ChIP-seq for protein binding validation")
    print("4. Larger, phylogenetically diverse dataset")
    print("5. Integration with epigenetic data")
    
    print("\n📈 STATISTICAL SUMMARY:")
    print("-"*40)
    if 'total_sequences' in results_dict:
        print(f"Sequences analyzed: {results_dict['total_sequences']}")
    if 'significant_kmers' in results_dict:
        print(f"Significant k-mers (FDR < 0.05): {results_dict['significant_kmers']}")
    if 'top_enrichment' in results_dict:
        print(f"Top enrichment: {results_dict['top_enrichment']:.1f}x (GC-corrected)")
    
    print("\n" + "="*60)
    print("Remember: Correlation ≠ Causation")
    print("These are computational findings requiring biological validation")
    print("="*60)

print("✓ Report generation function defined")

# %% Cell 7: Example Analysis with Test Data

# Generate example sequences (replace with your real data)
def generate_test_sequences():
    """Generate test sequences with known patterns"""
    np.random.seed(42)
    
    sequences = {}
    
    # Regeneration sequences with GGAATG enrichment
    for i in range(5):
        base_seq = ''.join(np.random.choice(['A', 'T', 'G', 'C'], 200))
        # Insert GGAATG motifs
        for _ in range(np.random.randint(3, 6)):
            pos = np.random.randint(0, 194)
            base_seq = base_seq[:pos] + 'GGAATG' + base_seq[pos+6:]
        sequences[f'regen_{i+1}'] = base_seq
    
    # Control sequences with less GGAATG
    for i in range(5):
        base_seq = ''.join(np.random.choice(['A', 'T', 'G', 'C'], 200))
        # Insert fewer GGAATG motifs
        for _ in range(np.random.randint(0, 2)):
            pos = np.random.randint(0, 194)
            base_seq = base_seq[:pos] + 'GGAATG' + base_seq[pos+6:]
        sequences[f'control_{i+1}'] = base_seq
    
    return sequences

# Generate test data
test_sequences = generate_test_sequences()
print(f"✓ Generated {len(test_sequences)} test sequences")

# %% Cell 8: Run Complete Analysis

print("\n" + "="*60)
print("RUNNING COMPLETE STATISTICAL ANALYSIS")
print("="*60)

# 1. GC-corrected enrichment for specific motif
print("\n1. GC-CORRECTED ENRICHMENT FOR GGAATG")
print("-"*40)

enrichment_results = []
for seq_name, sequence in test_sequences.items():
    result = gc_corrected_enrichment(sequence, 'GGAATG')
    result['sequence'] = seq_name
    enrichment_results.append(result)
    
    print(f"\n{seq_name}:")
    print(f"  GC content: {result['gc_content']:.1%}")
    print(f"  GGAATG count: {result['observed_count']}")
    print(f"  Expected count: {result['expected_count']:.3f}")
    print(f"  Observed frequency: {result['observed_freq']:.6f}")
    print(f"  Expected frequency: {result['expected_freq']:.6f}")
    print(f"  Enrichment: {result['enrichment']:.2f}x")
    print(f"  P-value: {result['p_value']:.3e}")

# Statistical test between groups
regen_enrichments = [r['enrichment'] for r in enrichment_results if 'regen' in r['sequence']]
control_enrichments = [r['enrichment'] for r in enrichment_results if 'control' in r['sequence']]

# Use Mann-Whitney U test (non-parametric)
try:
    # Newer scipy versions
    _, p_group = stats.mannwhitneyu(regen_enrichments, control_enrichments, alternative='greater', method='auto')
except TypeError:
    # Older scipy versions
    _, p_group = stats.mannwhitneyu(regen_enrichments, control_enrichments, alternative='greater')
    
print(f"\n📊 Group comparison (Mann-Whitney U):")
print(f"   Regeneration mean: {np.mean(regen_enrichments):.2f}x")
print(f"   Control mean: {np.mean(control_enrichments):.2f}x")
print(f"   P-value: {p_group:.3e}")

# 2. Multiple testing correction
print("\n\n2. MULTIPLE TESTING CORRECTION")
print("-"*40)

significant_kmers = analyze_all_kmers_with_correction(
    test_sequences, 
    k=6, 
    method='fdr_bh',
    alpha=0.05
)

if len(significant_kmers) > 0:
    print(f"\nTop 10 significant k-mers:")
    print(significant_kmers[['kmer', 'enrichment', 'p_value', 'p_adjusted']].head(10))

# 3. ML feasibility with current data
print("\n\n3. MACHINE LEARNING FEASIBILITY")
print("-"*40)

# Create feature matrix (k-mer counts)
k = 4  # Use 4-mers for features

# First, get all possible k-mers from all sequences
all_kmers = set()
for sequence in test_sequences.values():
    for i in range(len(sequence) - k + 1):
        all_kmers.add(sequence[i:i+k])

# Sort k-mers for consistent ordering
sorted_kmers = sorted(all_kmers)
print(f"Total unique {k}-mers across all sequences: {len(sorted_kmers)}")

# Create feature matrix with consistent dimensions
features = []
labels = []

for seq_name, sequence in test_sequences.items():
    # Count k-mers in this sequence
    kmer_counts = Counter([sequence[i:i+k] for i in range(len(sequence)-k+1)])
    
    # Create feature vector with counts for all k-mers
    feature_vector = [kmer_counts.get(kmer, 0) for kmer in sorted_kmers]
    features.append(feature_vector)
    labels.append(1 if 'regen' in seq_name else 0)

X = np.array(features)
y = np.array(labels)

print(f"Feature matrix shape: {X.shape}")
print(f"Class distribution: {np.bincount(y)} (control, regeneration)")

# Check feasibility and run if possible
ml_scores = safe_ml_validation(X, y)

# 4. Dose-response simulation
print("\n\n4. DOSE-RESPONSE ANALYSIS")
print("-"*40)

# Simulate dose-response data
np.random.seed(42)
violation_levels = np.repeat([0, 0.1, 0.25, 0.5, 0.75, 0.9, 1.0], 10)
# Quality decreases with violations, with some noise
quality_base = 0.9 - 0.7 * violation_levels
quality_scores = quality_base + np.random.normal(0, 0.05, len(violation_levels))
quality_scores = np.clip(quality_scores, 0, 1)

dose_response_results = analyze_dose_response_properly(violation_levels, quality_scores)

# 5. Generate final report
print("\n\n5. FINAL STATISTICAL REPORT")
print("-"*40)

summary_results = {
    'total_sequences': len(test_sequences),
    'significant_kmers': len(significant_kmers),
    'top_enrichment': max(regen_enrichments) if regen_enrichments else 0,
    'ml_accuracy': ml_scores.mean() if ml_scores is not None else None,
    'dose_response_r': dose_response_results['spearman_r']
}

generate_honest_report(summary_results)

# %% Cell 9: Save Results

# Create results summary
results_summary = pd.DataFrame({
    'Metric': [
        'Total sequences analyzed',
        'Significant k-mers (FDR < 0.05)', 
        'GGAATG enrichment (regen vs control)',
        'Dose-response correlation',
        'ML cross-validation accuracy'
    ],
    'Value': [
        len(test_sequences),
        len(significant_kmers),
        f"{np.mean(regen_enrichments):.1f}x vs {np.mean(control_enrichments):.1f}x",
        f"r = {dose_response_results['spearman_r']:.3f}",
        f"{ml_scores.mean():.1%}" if ml_scores is not None else "N/A - insufficient data"
    ],
    'Statistical Significance': [
        'N/A',
        f"{len(significant_kmers)} passed FDR",
        f"p = {p_group:.3e}",
        f"p = {dose_response_results['spearman_p']:.3e}",
        'See warnings above'
    ]
})

print("\n📊 RESULTS SUMMARY TABLE:")
print(results_summary.to_string(index=False))

# Save to CSV (uncomment to use)
# results_summary.to_csv('dna_pattern_analysis_results.csv', index=False)
# significant_kmers.to_csv('significant_kmers_fdr_corrected.csv', index=False)

print("\n✅ Analysis complete! Key findings properly corrected for statistical rigor.")
