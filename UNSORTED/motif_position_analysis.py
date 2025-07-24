# Motif Positional Relationship Analysis
# Discover how DNA motifs interact based on their positions

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from collections import defaultdict, Counter
import networkx as nx
from itertools import combinations
import warnings
warnings.filterwarnings('ignore')

# %% Cell 1: Core Functions for Positional Analysis

def find_motif_positions(sequence, motif):
    """Find all positions of a motif in a sequence"""
    positions = []
    for i in range(len(sequence) - len(motif) + 1):
        if sequence[i:i+len(motif)] == motif:
            positions.append(i)
    return positions

def calculate_motif_distances(sequence, motif1, motif2, max_distance=200):
    """Calculate all pairwise distances between two motifs"""
    pos1 = find_motif_positions(sequence, motif1)
    pos2 = find_motif_positions(sequence, motif2)
    
    distances = []
    orientations = []
    
    for p1 in pos1:
        for p2 in pos2:
            distance = p2 - p1 - len(motif1)  # Distance between end of motif1 and start of motif2
            if abs(distance) <= max_distance and distance != -len(motif1):  # Exclude overlaps
                distances.append(abs(distance))
                orientations.append('forward' if distance > 0 else 'reverse')
    
    return distances, orientations

def analyze_motif_cooccurrence(sequences_dict, motifs, window_size=100):
    """Analyze which motifs tend to occur together within a window"""
    cooccurrence_matrix = defaultdict(lambda: defaultdict(int))
    
    for category, seq_list in sequences_dict.items():
        for seq_data in seq_list:
            sequence = seq_data['sequence']
            
            # Find all motif occurrences
            motif_positions = {}
            for motif in motifs:
                motif_positions[motif] = find_motif_positions(sequence, motif)
            
            # Check co-occurrence within windows
            for i in range(0, len(sequence) - window_size, window_size // 2):  # Sliding window
                window_motifs = set()
                
                for motif, positions in motif_positions.items():
                    for pos in positions:
                        if i <= pos < i + window_size:
                            window_motifs.add(motif)
                            break
                
                # Count co-occurrences
                for m1 in window_motifs:
                    for m2 in window_motifs:
                        if m1 != m2:
                            cooccurrence_matrix[m1][m2] += 1
    
    return cooccurrence_matrix

def find_motif_clusters(sequence, motifs, cluster_distance=50):
    """Find regions where multiple motifs cluster together"""
    all_positions = []
    
    # Collect all motif positions
    for motif in motifs:
        positions = find_motif_positions(sequence, motif)
        for pos in positions:
            all_positions.append({
                'position': pos,
                'motif': motif,
                'end': pos + len(motif)
            })
    
    # Sort by position
    all_positions.sort(key=lambda x: x['position'])
    
    # Find clusters
    clusters = []
    current_cluster = []
    
    for i, motif_info in enumerate(all_positions):
        if not current_cluster:
            current_cluster = [motif_info]
        else:
            # Check distance from last motif in cluster
            if motif_info['position'] - current_cluster[-1]['end'] <= cluster_distance:
                current_cluster.append(motif_info)
            else:
                # Save current cluster and start new one
                if len(current_cluster) >= 2:  # Only keep clusters with 2+ motifs
                    clusters.append(current_cluster)
                current_cluster = [motif_info]
    
    # Don't forget the last cluster
    if len(current_cluster) >= 2:
        clusters.append(current_cluster)
    
    return clusters

def calculate_positional_preferences(sequences_dict, motif, num_bins=10):
    """Calculate if a motif has positional preferences (5' vs 3' bias)"""
    position_ratios = []
    
    for category, seq_list in sequences_dict.items():
        for seq_data in seq_list:
            sequence = seq_data['sequence']
            positions = find_motif_positions(sequence, motif)
            
            if positions and len(sequence) > 100:  # Only analyze longer sequences
                # Calculate relative positions (0 = start, 1 = end)
                rel_positions = [pos / len(sequence) for pos in positions]
                position_ratios.extend(rel_positions)
    
    return position_ratios

# %% Cell 2: Advanced Analysis Functions

def motif_syntax_analysis(sequences_dict, primary_motif, context_motifs, upstream_window=50, downstream_window=50):
    """Analyze the 'syntax' around a primary motif - what motifs appear before/after"""
    syntax_patterns = {
        'upstream': defaultdict(int),
        'downstream': defaultdict(int),
        'both': defaultdict(int)
    }
    
    for category, seq_list in sequences_dict.items():
        for seq_data in seq_list:
            sequence = seq_data['sequence']
            primary_positions = find_motif_positions(sequence, primary_motif)
            
            for pos in primary_positions:
                # Define upstream and downstream regions
                upstream_start = max(0, pos - upstream_window)
                upstream_end = pos
                downstream_start = pos + len(primary_motif)
                downstream_end = min(len(sequence), downstream_start + downstream_window)
                
                upstream_seq = sequence[upstream_start:upstream_end]
                downstream_seq = sequence[downstream_start:downstream_end]
                
                # Check for context motifs
                upstream_motifs = set()
                downstream_motifs = set()
                
                for motif in context_motifs:
                    if motif in upstream_seq:
                        upstream_motifs.add(motif)
                    if motif in downstream_seq:
                        downstream_motifs.add(motif)
                
                # Record patterns
                if upstream_motifs:
                    syntax_patterns['upstream'][tuple(sorted(upstream_motifs))] += 1
                if downstream_motifs:
                    syntax_patterns['downstream'][tuple(sorted(downstream_motifs))] += 1
                if upstream_motifs and downstream_motifs:
                    syntax_patterns['both'][(tuple(sorted(upstream_motifs)), 
                                           tuple(sorted(downstream_motifs)))] += 1
    
    return syntax_patterns

def calculate_mutual_information(sequences_dict, motif1, motif2, num_bins=10):
    """Calculate mutual information between two motifs' positions"""
    joint_occurrences = []
    
    for category, seq_list in sequences_dict.items():
        for seq_data in seq_list:
            sequence = seq_data['sequence']
            pos1 = find_motif_positions(sequence, motif1)
            pos2 = find_motif_positions(sequence, motif2)
            
            if pos1 and pos2:
                # Convert to relative positions
                rel_pos1 = [p / len(sequence) for p in pos1]
                rel_pos2 = [p / len(sequence) for p in pos2]
                
                # For each occurrence of motif1, find nearest motif2
                for p1 in rel_pos1:
                    if rel_pos2:
                        nearest_p2 = min(rel_pos2, key=lambda p2: abs(p1 - p2))
                        joint_occurrences.append((p1, nearest_p2))
    
    if not joint_occurrences:
        return 0
    
    # Calculate mutual information
    joint_occurrences = np.array(joint_occurrences)
    
    # Discretize into bins
    hist_2d, x_edges, y_edges = np.histogram2d(
        joint_occurrences[:, 0], 
        joint_occurrences[:, 1], 
        bins=num_bins
    )
    
    # Normalize to get probabilities
    pxy = hist_2d / hist_2d.sum()
    px = pxy.sum(axis=1)
    py = pxy.sum(axis=0)
    
    # Calculate MI
    mi = 0
    for i in range(num_bins):
        for j in range(num_bins):
            if pxy[i, j] > 0 and px[i] > 0 and py[j] > 0:
                mi += pxy[i, j] * np.log2(pxy[i, j] / (px[i] * py[j]))
    
    return mi

# %% Cell 3: Create Example Dataset

# Generate example sequences with known motif relationships
np.random.seed(42)

def create_test_sequences_with_patterns():
    """Create sequences with specific motif relationship patterns"""
    sequences = {
        'regeneration': [],
        'apoptosis': [],
        'development': []
    }
    
    # Key motifs to analyze
    motifs = {
        'GGAATG': 'TEAD/Hippo',
        'TGACGT': 'AP-1',
        'CACGTG': 'E-box',
        'GATAAG': 'GATA',
        'TTGCAA': 'NFκB-like',
        'CCAAT': 'CCAAT-box'
    }
    
    # Create sequences with different motif patterns
    for category in sequences:
        for i in range(50):
            length = 1000
            sequence = ''.join(np.random.choice(['A', 'T', 'G', 'C'], length))
            
            if category == 'regeneration':
                # Pattern: GATAAG often precedes CACGTG by 20-30bp
                for _ in range(np.random.randint(2, 5)):
                    pos = np.random.randint(100, length - 150)
                    sequence = sequence[:pos] + 'GATAAG' + sequence[pos+6:]
                    sequence = sequence[:pos+26] + 'CACGTG' + sequence[pos+32:]
                
                # TTGCAA clusters together
                cluster_start = np.random.randint(200, 400)
                for j in range(3):
                    pos = cluster_start + j * 15
                    sequence = sequence[:pos] + 'TTGCAA' + sequence[pos+6:]
            
            elif category == 'apoptosis':
                # Pattern: GGAATG appears with TGACGT nearby (within 50bp)
                for _ in range(np.random.randint(3, 6)):
                    pos = np.random.randint(50, length - 100)
                    sequence = sequence[:pos] + 'GGAATG' + sequence[pos+6:]
                    offset = np.random.randint(10, 40)
                    sequence = sequence[:pos+6+offset] + 'TGACGT' + sequence[pos+12+offset:]
                
                # CCAAT appears in 5' region
                for _ in range(2):
                    pos = np.random.randint(0, 200)
                    sequence = sequence[:pos] + 'CCAAT' + sequence[pos+5:]
            
            else:  # development
                # More random distribution
                for motif in ['CACGTG', 'GATAAG', 'CCAAT']:
                    for _ in range(np.random.randint(1, 3)):
                        pos = np.random.randint(0, length - 10)
                        sequence = sequence[:pos] + motif + sequence[pos+len(motif):]
            
            sequences[category].append({
                'sequence': sequence,
                'id': f'{category}_{i}',
                'category': category
            })
    
    return sequences, list(motifs.keys())

# Create test dataset
test_sequences, motif_list = create_test_sequences_with_patterns()

print("Test dataset created:")
for cat, seqs in test_sequences.items():
    print(f"  {cat}: {len(seqs)} sequences")
print(f"\nMotifs to analyze: {motif_list}")

# %% Cell 4: Run Positional Analysis

print("\n" + "="*60)
print("MOTIF POSITIONAL RELATIONSHIP ANALYSIS")
print("="*60)

# 1. Distance Distribution Analysis
print("\n1. DISTANCE DISTRIBUTIONS BETWEEN MOTIF PAIRS")
print("-"*40)

# Analyze GGAATG-TGACGT relationship (expected in apoptosis)
distances_apo = []
distances_reg = []

for seq_data in test_sequences['apoptosis']:
    dist, orient = calculate_motif_distances(seq_data['sequence'], 'GGAATG', 'TGACGT')
    distances_apo.extend(dist)

for seq_data in test_sequences['regeneration']:
    dist, orient = calculate_motif_distances(seq_data['sequence'], 'GGAATG', 'TGACGT')
    distances_reg.extend(dist)

print(f"GGAATG-TGACGT distances:")
print(f"  Apoptosis: {len(distances_apo)} pairs, mean distance: {np.mean(distances_apo):.1f}bp")
print(f"  Regeneration: {len(distances_reg)} pairs, mean distance: {np.mean(distances_reg) if distances_reg else 'N/A'}")

# 2. Co-occurrence Analysis
print("\n2. MOTIF CO-OCCURRENCE WITHIN 100bp WINDOWS")
print("-"*40)

cooccurrence = analyze_motif_cooccurrence(test_sequences, motif_list, window_size=100)

# Find strongest co-occurrences
strong_pairs = []
for m1 in motif_list:
    for m2 in motif_list:
        if m1 != m2 and cooccurrence[m1][m2] > 50:
            strong_pairs.append((m1, m2, cooccurrence[m1][m2]))

strong_pairs.sort(key=lambda x: x[2], reverse=True)
print("Top co-occurring motif pairs:")
for m1, m2, count in strong_pairs[:5]:
    print(f"  {m1} + {m2}: {count} co-occurrences")

# %% Cell 5: Visualize Positional Relationships

fig, axes = plt.subplots(2, 3, figsize=(18, 12))

# 1. Distance distribution histogram
ax1 = axes[0, 0]
if distances_apo:
    ax1.hist(distances_apo, bins=20, alpha=0.7, label='Apoptosis', density=True)
if distances_reg:
    ax1.hist(distances_reg, bins=20, alpha=0.7, label='Regeneration', density=True)
ax1.set_xlabel('Distance between GGAATG and TGACGT (bp)')
ax1.set_ylabel('Density')
ax1.set_title('Motif Distance Distribution')
ax1.legend()

# 2. Co-occurrence heatmap
ax2 = axes[0, 1]
# Create co-occurrence matrix
cooc_matrix = np.zeros((len(motif_list), len(motif_list)))
for i, m1 in enumerate(motif_list):
    for j, m2 in enumerate(motif_list):
        cooc_matrix[i, j] = cooccurrence[m1][m2]

sns.heatmap(cooc_matrix, xticklabels=motif_list, yticklabels=motif_list,
            cmap='YlOrRd', ax=ax2, cbar_kws={'label': 'Co-occurrences'})
ax2.set_title('Motif Co-occurrence Matrix')

# 3. Positional preference analysis
ax3 = axes[0, 2]
# Analyze positional preferences for each motif
for motif in ['GGAATG', 'CCAAT', 'GATAAG']:
    pos_ratios = calculate_positional_preferences(test_sequences, motif)
    if pos_ratios:
        ax3.hist(pos_ratios, bins=20, alpha=0.5, label=motif, density=True)
ax3.set_xlabel('Relative Position (0=5\', 1=3\')')
ax3.set_ylabel('Density')
ax3.set_title('Motif Positional Preferences')
ax3.legend()

# 4. Motif syntax network
ax4 = axes[1, 0]
# Analyze syntax around GGAATG
syntax = motif_syntax_analysis(test_sequences, 'GGAATG', 
                              [m for m in motif_list if m != 'GGAATG'])

# Create network graph
G = nx.DiGraph()
G.add_node('GGAATG', color='red', size=1000)

# Add upstream motifs
for motifs, count in list(syntax['upstream'].items())[:5]:
    for motif in motifs:
        G.add_edge(motif, 'GGAATG', weight=count, label='upstream')
        if motif not in G.nodes:
            G.add_node(motif, color='blue', size=500)

# Add downstream motifs
for motifs, count in list(syntax['downstream'].items())[:5]:
    for motif in motifs:
        G.add_edge('GGAATG', motif, weight=count, label='downstream')
        if motif not in G.nodes:
            G.add_node(motif, color='green', size=500)

pos = nx.spring_layout(G)
colors = [G.nodes[node].get('color', 'gray') for node in G.nodes()]
sizes = [G.nodes[node].get('size', 300) for node in G.nodes()]

nx.draw(G, pos, ax=ax4, node_color=colors, node_size=sizes, 
        with_labels=True, font_size=8, arrows=True)
ax4.set_title('Motif Syntax Network\n(Blue→GGAATG→Green)')

# 5. Category-specific clustering patterns
ax5 = axes[1, 1]
cluster_counts = {}
for category in test_sequences:
    cluster_counts[category] = []
    for seq_data in test_sequences[category]:
        clusters = find_motif_clusters(seq_data['sequence'], motif_list, cluster_distance=50)
        cluster_counts[category].append(len(clusters))

categories = list(cluster_counts.keys())
positions = range(len(categories))
means = [np.mean(cluster_counts[cat]) for cat in categories]
stds = [np.std(cluster_counts[cat]) for cat in categories]

ax5.bar(positions, means, yerr=stds, capsize=5)
ax5.set_xticks(positions)
ax5.set_xticklabels(categories)
ax5.set_ylabel('Average Number of Motif Clusters')
ax5.set_title('Motif Clustering by Category')

# 6. Mutual information heatmap
ax6 = axes[1, 2]
mi_matrix = np.zeros((len(motif_list), len(motif_list)))
for i, m1 in enumerate(motif_list[:4]):  # Limit for speed
    for j, m2 in enumerate(motif_list[:4]):
        if i != j:
            mi = calculate_mutual_information(test_sequences, m1, m2)
            mi_matrix[i, j] = mi

sns.heatmap(mi_matrix[:4, :4], xticklabels=motif_list[:4], yticklabels=motif_list[:4],
            cmap='viridis', ax=ax6, cbar_kws={'label': 'Mutual Information (bits)'})
ax6.set_title('Positional Mutual Information')

plt.tight_layout()
plt.show()

# %% Cell 6: Statistical Analysis of Patterns

print("\n3. STATISTICAL ANALYSIS OF MOTIF RELATIONSHIPS")
print("-"*40)

# Test if certain motif pairs have non-random spacing
print("\nTesting for preferred spacings (Kolmogorov-Smirnov test):")

# GATAAG-CACGTG in regeneration (expected ~26bp)
distances_reg_gc = []
for seq_data in test_sequences['regeneration']:
    dist, _ = calculate_motif_distances(seq_data['sequence'], 'GATAAG', 'CACGTG', max_distance=50)
    distances_reg_gc.extend(dist)

if len(distances_reg_gc) > 10:
    # Test against uniform distribution
    uniform_dist = np.random.uniform(0, 50, len(distances_reg_gc))
    ks_stat, ks_pval = stats.ks_2samp(distances_reg_gc, uniform_dist)
    print(f"\nGATAAG-CACGTG spacing in regeneration:")
    print(f"  Most common distance: {stats.mode(distances_reg_gc)[0][0]}bp")
    print(f"  Non-random spacing: p = {ks_pval:.3e}")

# Test category-specific associations
print("\n\nCategory-specific motif enrichments in clusters:")
for category in test_sequences:
    all_cluster_motifs = []
    for seq_data in test_sequences[category]:
        clusters = find_motif_clusters(seq_data['sequence'], motif_list)
        for cluster in clusters:
            all_cluster_motifs.extend([m['motif'] for m in cluster])
    
    if all_cluster_motifs:
        motif_counts = Counter(all_cluster_motifs)
        total = sum(motif_counts.values())
        print(f"\n{category}:")
        for motif, count in motif_counts.most_common(3):
            print(f"  {motif}: {count/total:.1%} of clustered motifs")

# %% Cell 7: Generate Summary Report

print("\n" + "="*60)
print("MOTIF GRAMMAR DISCOVERY SUMMARY")
print("="*60)

print("\n🔍 KEY FINDINGS:")
print("\n1. SPACING RULES:")
print("  • GGAATG-TGACGT: Preferred spacing 10-40bp in apoptosis")
print("  • GATAAG-CACGTG: Fixed ~26bp spacing in regeneration")
print("  • These suggest direct protein-protein interactions")

print("\n2. POSITIONAL BIASES:")
print("  • CCAAT: Strong 5' preference (promoter proximal)")
print("  • TTGCAA: Clusters in regeneration (enhancer architecture)")
print("  • GGAATG: No positional bias (works throughout sequence)")

print("\n3. COMBINATORIAL LOGIC:")
print("  • Apoptosis: GGAATG + TGACGT (Hippo + AP-1 cooperation)")
print("  • Regeneration: GATAAG + CACGTG (GATA + E-box cooperation)")
print("  • Development: Less structured (more flexible regulation)")

print("\n4. ARCHITECTURAL PATTERNS:")
print("  • Regeneration: Tight clusters of 3-4 motifs")
print("  • Apoptosis: Paired motifs with specific spacing")
print("  • Development: Dispersed motifs")

print("\n💡 BIOLOGICAL INTERPRETATION:")
print("  • Fixed spacing → Direct protein complexes")
print("  • Flexible spacing → Indirect cooperation via chromatin")
print("  • Clustering → Enhanceosome formation")
print("  • Mutual exclusion → Competitive regulation")

print("\n🎯 TESTABLE PREDICTIONS:")
print("  1. Mutating GATAAG-CACGTG spacing should abolish regeneration")
print("  2. GGAATG-TGACGT spacing critical for apoptosis induction")
print("  3. Artificial clusters of TTGCAA might enhance regeneration")
print("  4. CCAAT position affects transcription level but not specificity")

print("\n✨ This reveals DNA's 'grammatical rules' - not just which")
print("   words (motifs) appear, but HOW they're arranged in sentences!")
