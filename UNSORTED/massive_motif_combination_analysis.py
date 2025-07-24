# Massive Combinatorial Motif Analysis
# Finding the TRUE regeneration signatures through exhaustive search

import numpy as np
import pandas as pd
from itertools import combinations, product
from scipy import stats
from collections import defaultdict, Counter
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import multiprocessing as mp
from tqdm import tqdm
import pickle

print("🚀 MASSIVE COMBINATORIAL MOTIF ANALYSIS")
print("="*60)
print(f"Started: {datetime.now()}")
print("This will find the REAL regeneration signatures!\n")

# %% Part 1: Expand the search - get MORE sequences

def fetch_more_sequences():
    """Expand our sequence collection with targeted searches"""
    
    print("📥 FETCHING ADDITIONAL SEQUENCES...")
    
    # Additional search strategies
    additional_searches = {
        'regeneration_genes': [
            'FGF8', 'FGF10', 'FGF20', 'BMP2', 'BMP4', 'BMP7',
            'WNT3', 'WNT5', 'WNT8', 'NOTCH1', 'NOTCH2',
            'MSX1', 'MSX2', 'PAX6', 'PAX7', 'SOX2', 'SOX9',
            'KLF4', 'LIN28', 'NANOG', 'POU5F1'
        ],
        'regeneration_terms': [
            'blastema promoter', 'regeneration enhancer',
            'wound response element', 'stem cell enhancer',
            'dedifferentiation promoter', 'reprogramming enhancer'
        ],
        'model_organisms': [
            'Hydra magnipapillata', 'Nematostella vectensis',
            'Hofstenia miamia', 'Macrostomum lignano',
            'Pristionchus pacificus', 'Leucoraja erinacea'
        ]
    }
    
    # This would fetch more sequences - placeholder for now
    print("  (Using existing dataset - modify to fetch more)")
    return all_kingdom_sequences

# %% Part 2: Comprehensive motif discovery

def discover_all_motifs(sequences_dict, k_values=[4, 5, 6, 7, 8]):
    """Discover ALL k-mers across all sequences"""
    
    print("\n🔍 DISCOVERING ALL MOTIFS...")
    all_motifs = defaultdict(set)
    
    for k in k_values:
        print(f"  Finding all {k}-mers...")
        for kingdom, categories in sequences_dict.items():
            for category, seq_list in categories.items():
                for seq_data in seq_list:
                    seq = seq_data['sequence']
                    for i in range(len(seq) - k + 1):
                        motif = seq[i:i+k]
                        if 'N' not in motif:  # Skip ambiguous
                            all_motifs[k].add(motif)
        
        print(f"    Found {len(all_motifs[k]):,} unique {k}-mers")
    
    return all_motifs

# %% Part 3: Calculate enrichment for ALL motifs

def calculate_all_enrichments(sequences_dict, all_motifs):
    """Calculate enrichment for every motif"""
    
    print("\n📊 CALCULATING ENRICHMENTS FOR ALL MOTIFS...")
    
    # Categorize sequences
    regen_seqs = []
    death_seqs = []
    
    for kingdom, categories in sequences_dict.items():
        for category, seq_list in categories.items():
            if 'regen' in category.lower():
                regen_seqs.extend(seq_list)
            elif 'death' in category.lower() or 'apop' in category.lower():
                death_seqs.extend(seq_list)
    
    print(f"  Regeneration sequences: {len(regen_seqs)}")
    print(f"  Death sequences: {len(death_seqs)}")
    
    # Calculate frequencies
    motif_stats = {}
    
    for k, motifs in all_motifs.items():
        print(f"\n  Processing {k}-mers...")
        
        for motif in tqdm(motifs, desc=f"  {k}-mers"):
            # Count in regeneration
            regen_count = sum(1 for seq in regen_seqs if motif in seq['sequence'])
            regen_freq = regen_count / len(regen_seqs) if regen_seqs else 0
            
            # Count in death
            death_count = sum(1 for seq in death_seqs if motif in seq['sequence'])
            death_freq = death_count / len(death_seqs) if death_seqs else 0
            
            if death_freq > 0:
                enrichment = regen_freq / death_freq
                log2_enrichment = np.log2(enrichment)
            else:
                enrichment = float('inf') if regen_freq > 0 else 0
                log2_enrichment = 10 if regen_freq > 0 else 0
            
            # Fisher's exact test
            if regen_count + death_count >= 5:  # Minimum occurrences
                contingency = [[regen_count, len(regen_seqs) - regen_count],
                              [death_count, len(death_seqs) - death_count]]
                _, p_value = stats.fisher_exact(contingency)
            else:
                p_value = 1.0
            
            motif_stats[motif] = {
                'k': k,
                'regen_count': regen_count,
                'death_count': death_count,
                'regen_freq': regen_freq,
                'death_freq': death_freq,
                'enrichment': enrichment,
                'log2_enrichment': log2_enrichment,
                'p_value': p_value
            }
    
    return motif_stats, regen_seqs, death_seqs

# %% Part 4: Find motif combinations

def find_motif_combinations(regen_seqs, death_seqs, top_motifs, max_combo_size=3):
    """Find combinations of motifs that best distinguish regeneration"""
    
    print(f"\n🔗 FINDING MOTIF COMBINATIONS (up to {max_combo_size})...")
    
    combination_stats = {}
    
    for combo_size in range(2, max_combo_size + 1):
        print(f"\n  Testing {combo_size}-motif combinations...")
        
        for motif_combo in tqdm(combinations(top_motifs, combo_size), 
                               desc=f"  {combo_size}-combos"):
            # Count sequences with ALL motifs in combo
            regen_with_all = 0
            death_with_all = 0
            
            for seq in regen_seqs:
                if all(motif in seq['sequence'] for motif in motif_combo):
                    regen_with_all += 1
            
            for seq in death_seqs:
                if all(motif in seq['sequence'] for motif in motif_combo):
                    death_with_all += 1
            
            # Calculate stats
            regen_freq = regen_with_all / len(regen_seqs) if regen_seqs else 0
            death_freq = death_with_all / len(death_seqs) if death_seqs else 0
            
            if death_freq > 0:
                enrichment = regen_freq / death_freq
                log2_enrichment = np.log2(enrichment)
            else:
                enrichment = float('inf') if regen_freq > 0 else 0
                log2_enrichment = 10 if regen_freq > 0 else 0
            
            # Only keep if found in sufficient sequences
            if regen_with_all + death_with_all >= 5:
                combination_stats[motif_combo] = {
                    'regen_count': regen_with_all,
                    'death_count': death_with_all,
                    'regen_freq': regen_freq,
                    'death_freq': death_freq,
                    'enrichment': enrichment,
                    'log2_enrichment': log2_enrichment
                }
    
    return combination_stats

# %% Part 5: Analyze spacing patterns for top combinations

def analyze_combination_spacing(sequences, motif_combination):
    """Analyze spacing between motifs in a combination"""
    
    spacing_patterns = []
    
    for seq_data in sequences:
        seq = seq_data['sequence']
        
        # Find all positions
        positions = {}
        for motif in motif_combination:
            pos_list = []
            for i in range(len(seq) - len(motif) + 1):
                if seq[i:i+len(motif)] == motif:
                    pos_list.append(i)
            if pos_list:
                positions[motif] = pos_list
        
        # If all motifs present, calculate spacings
        if len(positions) == len(motif_combination):
            # Get closest pairs
            motif_list = list(motif_combination)
            for i in range(len(motif_list)-1):
                for j in range(i+1, len(motif_list)):
                    m1, m2 = motif_list[i], motif_list[j]
                    if m1 in positions and m2 in positions:
                        # Find minimum distance
                        min_dist = float('inf')
                        for p1 in positions[m1]:
                            for p2 in positions[m2]:
                                dist = abs(p2 - p1)
                                if dist < min_dist:
                                    min_dist = dist
                        
                        if min_dist < 1000:  # Reasonable distance
                            spacing_patterns.append({
                                'motif1': m1,
                                'motif2': m2,
                                'distance': min_dist
                            })
    
    return spacing_patterns

# %% Part 6: The Hydra special case analysis

def analyze_hydra_cluster():
    """Deep dive into the Hydra GGAATG-TGACGTCA cluster"""
    
    print("\n🔬 ANALYZING THE HYDRA CLUSTER...")
    
    # Find Hydra sequences
    hydra_seqs = []
    for kingdom, categories in all_kingdom_sequences.items():
        for category, seq_list in categories.items():
            for seq_data in seq_list:
                if 'hydra' in seq_data.get('organism', '').lower():
                    hydra_seqs.append(seq_data)
    
    print(f"  Found {len(hydra_seqs)} Hydra sequences")
    
    # Analyze the -4bp spacing
    for seq_data in hydra_seqs:
        seq = seq_data['sequence']
        
        # Find all close motif pairs (<20bp)
        motifs_to_check = ['GGAATG', 'TGACGTCA', 'ATAAA', 'CACGTG', 'GATAAG']
        close_pairs = []
        
        for m1 in motifs_to_check:
            for m2 in motifs_to_check:
                if m1 != m2:
                    pos1 = seq.find(m1)
                    pos2 = seq.find(m2)
                    
                    if pos1 != -1 and pos2 != -1:
                        distance = pos2 - pos1
                        if abs(distance) < 20:
                            close_pairs.append((m1, m2, distance))
        
        if close_pairs:
            print(f"\n  Close motif pairs in {seq_data.get('organism')}:")
            for m1, m2, dist in close_pairs:
                print(f"    {m1} → {m2}: {dist} bp")

# %% Part 7: Machine learning approach

def ml_motif_discovery(motif_stats, regen_seqs, death_seqs):
    """Use ML to find optimal motif combinations"""
    
    print("\n🤖 MACHINE LEARNING APPROACH...")
    
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.feature_selection import SelectKBest, chi2
    from sklearn.model_selection import cross_val_score
    
    # Select top motifs by individual enrichment
    sorted_motifs = sorted(motif_stats.items(), 
                          key=lambda x: abs(x[1]['log2_enrichment']), 
                          reverse=True)
    
    top_200_motifs = [m[0] for m in sorted_motifs[:200]]
    
    # Create feature matrix
    print("  Building feature matrix...")
    X = []
    y = []
    
    # Regeneration sequences
    for seq_data in regen_seqs:
        seq = seq_data['sequence']
        features = [1 if motif in seq else 0 for motif in top_200_motifs]
        X.append(features)
        y.append(1)
    
    # Death sequences
    for seq_data in death_seqs:
        seq = seq_data['sequence']
        features = [1 if motif in seq else 0 for motif in top_200_motifs]
        X.append(features)
        y.append(0)
    
    X = np.array(X)
    y = np.array(y)
    
    print(f"  Feature matrix: {X.shape}")
    
    # Feature selection
    print("  Selecting best features...")
    selector = SelectKBest(chi2, k=50)
    X_selected = selector.fit_transform(X, y)
    selected_indices = selector.get_support(indices=True)
    selected_motifs = [top_200_motifs[i] for i in selected_indices]
    
    # Train classifier
    print("  Training Random Forest...")
    rf = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
    scores = cross_val_score(rf, X_selected, y, cv=5)
    print(f"  Cross-validation accuracy: {scores.mean():.2%} (+/- {scores.std():.2%})")
    
    # Get feature importance
    rf.fit(X_selected, y)
    feature_importance = list(zip(selected_motifs, rf.feature_importances_))
    feature_importance.sort(key=lambda x: x[1], reverse=True)
    
    print("\n  Top 10 most important motifs (by ML):")
    for motif, importance in feature_importance[:10]:
        stats = motif_stats[motif]
        print(f"    {motif}: importance={importance:.3f}, "
              f"enrichment={stats['enrichment']:.2f}x")
    
    return selected_motifs, feature_importance

# %% Part 8: Comprehensive visualization

def create_comprehensive_report(motif_stats, combination_stats, feature_importance):
    """Create detailed visualizations"""
    
    print("\n📊 CREATING COMPREHENSIVE REPORT...")
    
    fig = plt.figure(figsize=(20, 24))
    
    # 1. Volcano plot of ALL motifs
    ax1 = plt.subplot(4, 2, 1)
    log2_enrichments = []
    neg_log_p = []
    colors = []
    
    for motif, stats in motif_stats.items():
        if stats['p_value'] > 0 and stats['enrichment'] > 0:
            log2_enrichments.append(stats['log2_enrichment'])
            neg_log_p.append(-np.log10(stats['p_value']))
            
            if stats['log2_enrichment'] > 1 and stats['p_value'] < 0.01:
                colors.append('green')
            elif stats['log2_enrichment'] < -1 and stats['p_value'] < 0.01:
                colors.append('red')
            else:
                colors.append('gray')
    
    ax1.scatter(log2_enrichments, neg_log_p, c=colors, alpha=0.6, s=10)
    ax1.axvline(0, color='black', linestyle='--', alpha=0.3)
    ax1.axvline(1, color='green', linestyle='--', alpha=0.3)
    ax1.axvline(-1, color='red', linestyle='--', alpha=0.3)
    ax1.axhline(-np.log10(0.01), color='blue', linestyle='--', alpha=0.3)
    ax1.set_xlabel('Log2(Regeneration/Death)')
    ax1.set_ylabel('-Log10(p-value)')
    ax1.set_title('Volcano Plot: All Motifs')
    
    # 2. Top enriched motifs
    ax2 = plt.subplot(4, 2, 2)
    top_regen = sorted(motif_stats.items(), 
                      key=lambda x: x[1]['log2_enrichment'], 
                      reverse=True)[:20]
    
    motifs = [m[0] for m in top_regen]
    enrichments = [m[1]['log2_enrichment'] for m in top_regen]
    
    ax2.barh(range(len(motifs)), enrichments, color='green', alpha=0.7)
    ax2.set_yticks(range(len(motifs)))
    ax2.set_yticklabels(motifs, fontsize=8)
    ax2.set_xlabel('Log2 Enrichment')
    ax2.set_title('Top 20 Regeneration-Enriched Motifs')
    
    # 3. Top motif combinations
    ax3 = plt.subplot(4, 2, 3)
    if combination_stats:
        top_combos = sorted(combination_stats.items(),
                           key=lambda x: x[1]['log2_enrichment'],
                           reverse=True)[:15]
        
        combo_names = ['+'.join(c[0]) for c in top_combos]
        combo_enrichments = [c[1]['log2_enrichment'] for c in top_combos]
        
        ax3.barh(range(len(combo_names)), combo_enrichments, color='purple', alpha=0.7)
        ax3.set_yticks(range(len(combo_names)))
        ax3.set_yticklabels(combo_names, fontsize=7)
        ax3.set_xlabel('Log2 Enrichment')
        ax3.set_title('Top Motif Combinations')
    
    # 4. ML feature importance
    ax4 = plt.subplot(4, 2, 4)
    if feature_importance:
        top_features = feature_importance[:15]
        feature_names = [f[0] for f in top_features]
        importances = [f[1] for f in top_features]
        
        ax4.barh(range(len(feature_names)), importances, color='orange', alpha=0.7)
        ax4.set_yticks(range(len(feature_names)))
        ax4.set_yticklabels(feature_names, fontsize=8)
        ax4.set_xlabel('Feature Importance')
        ax4.set_title('Machine Learning: Top Features')
    
    # 5. Motif length distribution
    ax5 = plt.subplot(4, 2, 5)
    length_counts = defaultdict(int)
    for motif, stats in motif_stats.items():
        if stats['log2_enrichment'] > 1:
            length_counts[len(motif)] += 1
    
    lengths = sorted(length_counts.keys())
    counts = [length_counts[l] for l in lengths]
    
    ax5.bar(lengths, counts, color='blue', alpha=0.7)
    ax5.set_xlabel('Motif Length')
    ax5.set_ylabel('Count')
    ax5.set_title('Length Distribution of Enriched Motifs')
    
    # 6. Summary statistics table
    ax6 = plt.subplot(4, 2, 6)
    ax6.axis('off')
    
    summary_text = f"""
    SUMMARY STATISTICS
    ==================
    
    Total motifs analyzed: {len(motif_stats):,}
    Significantly enriched in regeneration: {sum(1 for m in motif_stats.values() if m['log2_enrichment'] > 1 and m['p_value'] < 0.01):,}
    Significantly enriched in death: {sum(1 for m in motif_stats.values() if m['log2_enrichment'] < -1 and m['p_value'] < 0.01):,}
    
    Most enriched single motif: {top_regen[0][0]} ({top_regen[0][1]['enrichment']:.1f}x)
    
    Total combinations tested: {len(combination_stats):,}
    Best combination: {'+'.join(top_combos[0][0]) if combination_stats else 'N/A'}
    """
    
    ax6.text(0.1, 0.9, summary_text, transform=ax6.transAxes,
             fontsize=10, verticalalignment='top', fontfamily='monospace')
    
    plt.tight_layout()
    plt.savefig('massive_motif_analysis_report.png', dpi=300, bbox_inches='tight')
    plt.show()

# %% Main Execution

if __name__ == "__main__":
    # Use existing sequences or fetch more
    sequences = fetch_more_sequences()
    
    # Discover all motifs
    all_motifs = discover_all_motifs(sequences, k_values=[4, 5, 6, 7, 8])
    
    # Calculate enrichments
    motif_stats, regen_seqs, death_seqs = calculate_all_enrichments(sequences, all_motifs)
    
    # Save intermediate results
    print("\n💾 Saving intermediate results...")
    with open('motif_stats.pkl', 'wb') as f:
        pickle.dump(motif_stats, f)
    
    # Get top enriched motifs
    sorted_motifs = sorted(motif_stats.items(), 
                          key=lambda x: abs(x[1]['log2_enrichment']), 
                          reverse=True)
    
    # Filter for significant motifs
    significant_motifs = [m[0] for m in sorted_motifs 
                         if m[1]['p_value'] < 0.01 and 
                         abs(m[1]['log2_enrichment']) > 0.5][:100]
    
    print(f"\nFound {len(significant_motifs)} significant motifs")
    
    # Find combinations
    combination_stats = find_motif_combinations(regen_seqs, death_seqs, 
                                               significant_motifs[:30], 
                                               max_combo_size=3)
    
    # Machine learning
    selected_motifs, feature_importance = ml_motif_discovery(motif_stats, 
                                                            regen_seqs, death_seqs)
    
    # Special analyses
    analyze_hydra_cluster()
    
    # Create report
    create_comprehensive_report(motif_stats, combination_stats, feature_importance)
    
    # Final summary
    print("\n" + "="*60)
    print("ANALYSIS COMPLETE!")
    print("="*60)
    print(f"Ended: {datetime.now()}")
    
    # Top findings
    print("\n🏆 TOP FINDINGS:")
    print("-"*40)
    
    print("\nTop 5 regeneration-enriched motifs:")
    for motif, stats in sorted_motifs[:5]:
        if stats['log2_enrichment'] > 0:
            print(f"  {motif}: {stats['enrichment']:.2f}x enrichment "
                  f"(p={stats['p_value']:.2e})")
    
    print("\nTop 3 motif combinations:")
    if combination_stats:
        top_combos = sorted(combination_stats.items(),
                           key=lambda x: x[1]['log2_enrichment'],
                           reverse=True)[:3]
        for combo, stats in top_combos:
            print(f"  {'+'.join(combo)}: {stats['enrichment']:.2f}x enrichment")
    
    print("\n✅ All results saved!")
    print("Check 'massive_motif_analysis_report.png' for visualizations")
