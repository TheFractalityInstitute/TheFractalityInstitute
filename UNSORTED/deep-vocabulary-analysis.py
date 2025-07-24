# Deep Vocabulary & Syntax Analysis - Cellular Programming Language
# This script digs deeper into the "grammar" of cellular communication

# %% Cell 1: Setup
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict, Counter
from itertools import combinations, permutations
import re
import networkx as nx
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from scipy.stats import chi2_contingency, fisher_exact
import warnings
warnings.filterwarnings('ignore')

print("Ready to decode the cellular language!")

# %% Cell 2: Extended Sequence Database
# Adding more sequences for better pattern discovery
EXTENDED_SEQUENCES = {
    # Original sequences
    'EPH_EPHRIN_BOUNDARY': """
    GATAAGATAAGGATCCAAGGAATTGGGAATGGAATGCGTGACGTCATGACGTCAGATA
    TGACGTCATTTGGGAAACCCGGAAATGATAAGATAAGCCATTTGGGAAAGATAAGATA
    AGAGGCTGAGTCAGGGAATGGGGAATGCCGGAATTTTGACGTCATGGGAACCCAAAAA
    GGAATGGATAAGATAAGTTTTGGGAAACCCTGAGTCAGATAAGATAAGGGAATGGGGG
    """,
    
    'REGENERATION_MASTER': """
    GGAATGGGAATGGGAATGCGTGACGTCATGACGTCAGATAGGAATGGGAATGGGAATG
    TGACGTCATTTGGGAAACCCGGAAATGGAATGGGAATGGGAATGGCATTTGGGAAAGA
    GGAATGGGAATGGGAATGAGGCTGAGTCAGGAAATGGGGAATGCCGGAATTTTGACGT
    GGAATGGGAATGGGAATGGGAATGGATTTGGGAAACCCTGAGTCAGGGAATGGGAATG
    """,
    
    # Additional boundary sequences
    'WNT_BOUNDARY': """
    CTTTGATCTTTGATCTTTGATCGTGACGTCATGACGTCAGATAGATCTTTGATCTTTG
    TGACGTCATTTGGGAAACCCGGAAATCTTTGATCTTTGATCGCATTTGGGAAAGAAGA
    CTTTGATCTTTGATCAGGCTGAGTCAGGAAATGGGGAATGCCGGAATTTTGACGTCAT
    CTTTGATCTTTGATCTTTGATCGATTTGGGAAACCCTGAGTCAGCTTTGATCTTTGAT
    """,
    
    'SONIC_HEDGEHOG_ZPA': """
    GACCGGGACCGGGACCGGCGTGACGTCATGACGTCAGATAGGACCGGGACCGGGACCG
    TGACGTCATTTGGGAAACCCGGAAATGACCGGGACCGGGACCGGCATTTGGGAAAGAA
    GACCGGGACCGGGACCGAGGCTGAGTCAGGAAATGGGGAATGCCGGAATTTTGACGTC
    GACCGGGACCGGGACCGGGACCGGATTTGGGAAACCCTGAGTCAGGACCGGGACCGGG
    """,
    
    'NEURAL_CREST_BOUNDARY': """
    CAGCTGCAGCTGCAGCTGCGTGACGTCATGACGTCAGATACAGCTGCAGCTGCAGCTG
    TGACGTCATTTGGGAAACCCGGAAATCAGCTGCAGCTGCAGCTGCATTTGGGAAAGAA
    CAGCTGCAGCTGCAGCTGAGGCTGAGTCAGGAAATGGGGAATGCCGGAATTTTGACGT
    CAGCTGCAGCTGCAGCTGCAGCTGGATTTGGGAAACCCTGAGTCAGCAGCTGCAGCTG
    """
}

# Clean sequences
for key in EXTENDED_SEQUENCES:
    EXTENDED_SEQUENCES[key] = EXTENDED_SEQUENCES[key].replace('\n', '').replace(' ', '')

# %% Cell 3: Advanced Pattern Discovery Functions

def find_kmer_combinations(sequence, k1=6, k2=6, max_distance=50):
    """Find pairs of k-mers that frequently occur together"""
    kmer_pairs = defaultdict(lambda: {'count': 0, 'distances': []})
    
    # Find all k-mer positions
    kmer_positions = defaultdict(list)
    for i in range(len(sequence) - k1 + 1):
        kmer = sequence[i:i+k1]
        kmer_positions[kmer].append(i)
    
    # Find pairs within distance constraints
    for kmer1 in kmer_positions:
        for kmer2 in kmer_positions:
            if kmer1 != kmer2:  # Different k-mers
                for pos1 in kmer_positions[kmer1]:
                    for pos2 in kmer_positions[kmer2]:
                        distance = pos2 - (pos1 + k1)
                        if 0 < distance <= max_distance:
                            pair = (kmer1, kmer2)
                            kmer_pairs[pair]['count'] += 1
                            kmer_pairs[pair]['distances'].append(distance)
    
    # Calculate average distances and filter significant pairs
    significant_pairs = {}
    for pair, data in kmer_pairs.items():
        if data['count'] >= 2:  # At least 2 occurrences
            avg_distance = np.mean(data['distances'])
            std_distance = np.std(data['distances']) if len(data['distances']) > 1 else 0
            significant_pairs[pair] = {
                'count': data['count'],
                'avg_distance': avg_distance,
                'std_distance': std_distance,
                'consistent': std_distance < 5  # Consistent spacing
            }
    
    return significant_pairs

def find_hierarchical_patterns(sequence, levels=[4, 6, 8]):
    """Find patterns at multiple scales (hierarchical organization)"""
    hierarchical_patterns = {}
    
    for level in levels:
        # Find enriched k-mers at this level
        kmers = defaultdict(int)
        for i in range(len(sequence) - level + 1):
            kmer = sequence[i:i+level]
            kmers[kmer] += 1
        
        # Find k-mers that contain smaller enriched k-mers
        if level > levels[0]:
            smaller_level = levels[levels.index(level) - 1]
            containing_patterns = []
            
            for kmer, count in kmers.items():
                if count > 2:  # Enriched at this level
                    # Check if it contains enriched smaller k-mers
                    for i in range(len(kmer) - smaller_level + 1):
                        sub_kmer = kmer[i:i+smaller_level]
                        if sub_kmer in hierarchical_patterns.get(smaller_level, {}).get('enriched', []):
                            containing_patterns.append({
                                'larger': kmer,
                                'contains': sub_kmer,
                                'position': i,
                                'count': count
                            })
        
        hierarchical_patterns[level] = {
            'enriched': [k for k, v in kmers.items() if v > 2],
            'containing': containing_patterns if level > levels[0] else []
        }
    
    return hierarchical_patterns

def analyze_positional_bias(sequences_dict):
    """Check if certain k-mers prefer specific positions (5' vs 3' bias)"""
    position_bias = defaultdict(lambda: {'5_prime': 0, '3_prime': 0, 'middle': 0})
    
    for seq_name, sequence in sequences_dict.items():
        seq_len = len(sequence)
        
        # Divide sequence into thirds
        third = seq_len // 3
        
        # Count 6-mers in each region
        for i in range(seq_len - 6 + 1):
            kmer = sequence[i:i+6]
            if i < third:
                position_bias[kmer]['5_prime'] += 1
            elif i < 2 * third:
                position_bias[kmer]['middle'] += 1
            else:
                position_bias[kmer]['3_prime'] += 1
    
    # Calculate bias scores
    biased_kmers = {}
    for kmer, counts in position_bias.items():
        total = sum(counts.values())
        if total >= 5:  # Minimum occurrences
            # Chi-square test for uniform distribution
            expected = total / 3
            chi2 = sum((counts[pos] - expected)**2 / expected for pos in counts)
            
            # Find dominant position
            max_pos = max(counts, key=counts.get)
            bias_strength = counts[max_pos] / total
            
            if bias_strength > 0.5:  # More than 50% in one region
                biased_kmers[kmer] = {
                    'preferred_position': max_pos,
                    'bias_strength': bias_strength,
                    'chi2': chi2,
                    'counts': dict(counts)
                }
    
    return biased_kmers

def find_syntax_rules(sequences_dict):
    """Discover syntax rules - what k-mers can follow others"""
    transition_matrix = defaultdict(lambda: defaultdict(int))
    
    for seq_name, sequence in sequences_dict.items():
        # Track 6-mer transitions
        for i in range(len(sequence) - 12 + 1):
            kmer1 = sequence[i:i+6]
            kmer2 = sequence[i+6:i+12]
            transition_matrix[kmer1][kmer2] += 1
    
    # Find significant transitions
    syntax_rules = []
    for kmer1, transitions in transition_matrix.items():
        total_transitions = sum(transitions.values())
        if total_transitions >= 3:
            for kmer2, count in transitions.items():
                probability = count / total_transitions
                if probability > 0.3:  # Strong preference
                    syntax_rules.append({
                        'from': kmer1,
                        'to': kmer2,
                        'probability': probability,
                        'count': count,
                        'strength': 'strong' if probability > 0.5 else 'moderate'
                    })
    
    return sorted(syntax_rules, key=lambda x: x['probability'], reverse=True)

# %% Cell 4: Run Deep Analysis
print("="*60)
print("DEEP VOCABULARY AND SYNTAX ANALYSIS")
print("="*60)

# 1. Find k-mer combinations
print("\n1. DISCOVERING K-MER COMBINATIONS (Potential compound words)")
print("-"*40)

combination_results = {}
for seq_name, sequence in EXTENDED_SEQUENCES.items():
    pairs = find_kmer_combinations(sequence)
    if pairs:
        print(f"\n{seq_name}:")
        # Show top consistent pairs
        consistent_pairs = [(k, v) for k, v in pairs.items() if v['consistent']]
        for (kmer1, kmer2), data in sorted(consistent_pairs, key=lambda x: x[1]['count'], reverse=True)[:3]:
            print(f"  {kmer1} → {kmer2} (occurs {data['count']}x, avg distance: {data['avg_distance']:.1f}bp)")
        combination_results[seq_name] = pairs

# 2. Find hierarchical patterns
print("\n\n2. HIERARCHICAL PATTERN ORGANIZATION")
print("-"*40)

for seq_name, sequence in list(EXTENDED_SEQUENCES.items())[:2]:  # First two for brevity
    patterns = find_hierarchical_patterns(sequence)
    print(f"\n{seq_name}:")
    for level in [4, 6, 8]:
        if patterns[level]['containing']:
            print(f"  {level}-mers containing enriched {level-2}-mers:")
            for p in patterns[level]['containing'][:3]:
                print(f"    '{p['larger']}' contains '{p['contains']}' at position {p['position']}")

# 3. Analyze positional bias
print("\n\n3. POSITIONAL PREFERENCES (5' vs 3' bias)")
print("-"*40)

biased_kmers = analyze_positional_bias(EXTENDED_SEQUENCES)
print("\nK-mers with strong positional preferences:")
for kmer, bias in sorted(biased_kmers.items(), key=lambda x: x[1]['bias_strength'], reverse=True)[:5]:
    print(f"  {kmer}: prefers {bias['preferred_position']} ({bias['bias_strength']:.1%} of occurrences)")

# 4. Discover syntax rules
print("\n\n4. SYNTAX RULES (What follows what)")
print("-"*40)

syntax_rules = find_syntax_rules(EXTENDED_SEQUENCES)
print("\nStrongest syntax rules found:")
for rule in syntax_rules[:10]:
    print(f"  {rule['from']} → {rule['to']} ({rule['probability']:.1%} probability, {rule['strength']})")

# %% Cell 5: Network Analysis of K-mer Relationships

def build_kmer_network(syntax_rules, min_probability=0.3):
    """Build a network showing k-mer relationships"""
    G = nx.DiGraph()
    
    for rule in syntax_rules:
        if rule['probability'] >= min_probability:
            G.add_edge(rule['from'], rule['to'], 
                      weight=rule['probability'],
                      count=rule['count'])
    
    return G

# Build the network
G = build_kmer_network(syntax_rules)

# Find important nodes (hubs)
if len(G) > 0:
    in_degree = dict(G.in_degree())
    out_degree = dict(G.out_degree())
    
    print("\n\n5. K-MER NETWORK ANALYSIS")
    print("-"*40)
    print("\nHub k-mers (can lead to many others):")
    for node, degree in sorted(out_degree.items(), key=lambda x: x[1], reverse=True)[:5]:
        if degree > 0:
            print(f"  {node}: leads to {degree} different k-mers")
    
    print("\nConvergence k-mers (many lead to these):")
    for node, degree in sorted(in_degree.items(), key=lambda x: x[1], reverse=True)[:5]:
        if degree > 0:
            print(f"  {node}: {degree} different k-mers lead here")

# %% Cell 6: Machine Learning - Clustering K-mers by Function

def vectorize_kmer_context(sequences_dict, k=6):
    """Create feature vectors for k-mers based on their context"""
    kmer_features = defaultdict(lambda: {
        'before': Counter(),
        'after': Counter(),
        'sequences': set()
    })
    
    for seq_name, sequence in sequences_dict.items():
        for i in range(2, len(sequence) - k - 2):
            kmer = sequence[i:i+k]
            before = sequence[i-2:i]
            after = sequence[i+k:i+k+2]
            
            kmer_features[kmer]['before'][before] += 1
            kmer_features[kmer]['after'][after] += 1
            kmer_features[kmer]['sequences'].add(seq_name)
    
    return kmer_features

# Vectorize and cluster
kmer_features = vectorize_kmer_context(EXTENDED_SEQUENCES)

# Create feature matrix
all_kmers = list(kmer_features.keys())
all_contexts = set()
for kmer_data in kmer_features.values():
    all_contexts.update(kmer_data['before'].keys())
    all_contexts.update(kmer_data['after'].keys())

context_list = sorted(all_contexts)
feature_matrix = []

for kmer in all_kmers:
    features = []
    for context in context_list:
        features.append(kmer_features[kmer]['before'].get(context, 0))
        features.append(kmer_features[kmer]['after'].get(context, 0))
    feature_matrix.append(features)

feature_matrix = np.array(feature_matrix)

# Only cluster if we have enough k-mers
if len(all_kmers) > 10:
    # PCA for visualization
    pca = PCA(n_components=2)
    pca_features = pca.fit_transform(feature_matrix)
    
    # K-means clustering
    n_clusters = min(5, len(all_kmers) // 5)
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = kmeans.fit_predict(feature_matrix)
    
    print("\n\n6. FUNCTIONAL K-MER CLUSTERS")
    print("-"*40)
    print(f"\nFound {n_clusters} functional groups of k-mers:")
    
    for cluster_id in range(n_clusters):
        cluster_kmers = [all_kmers[i] for i, c in enumerate(clusters) if c == cluster_id]
        print(f"\nCluster {cluster_id + 1}: {len(cluster_kmers)} k-mers")
        print(f"  Members: {', '.join(cluster_kmers[:5])}{'...' if len(cluster_kmers) > 5 else ''}")
        
        # Find what sequences use this cluster
        seq_usage = Counter()
        for kmer in cluster_kmers:
            seq_usage.update(kmer_features[kmer]['sequences'])
        print(f"  Used in: {', '.join(seq_usage.keys())}")

# %% Cell 7: Visualization

# Create comprehensive visualization
fig, axes = plt.subplots(2, 2, figsize=(15, 12))

# 1. K-mer combination heatmap
ax1 = axes[0, 0]
if combination_results:
    # Get all unique k-mer pairs
    all_pairs = set()
    for pairs in combination_results.values():
        all_pairs.update(pairs.keys())
    
    # Create matrix
    pair_matrix = []
    pair_labels = []
    for seq_name in combination_results:
        row = []
        for pair in list(all_pairs)[:10]:  # Top 10 pairs
            count = combination_results[seq_name].get(pair, {}).get('count', 0)
            row.append(count)
        pair_matrix.append(row)
        pair_labels.append(seq_name.split('_')[0])
    
    if pair_matrix:
        sns.heatmap(pair_matrix, xticklabels=[f"{p[0][:3]}→{p[1][:3]}" for p in list(all_pairs)[:10]], 
                    yticklabels=pair_labels, cmap='YlOrRd', ax=ax1)
        ax1.set_title('K-mer Pair Frequencies')
        ax1.set_xlabel('K-mer Pairs')

# 2. Positional bias visualization
ax2 = axes[0, 1]
if biased_kmers:
    positions = ['5_prime', 'middle', '3_prime']
    bias_data = []
    kmer_labels = []
    
    for kmer, bias in list(biased_kmers.items())[:8]:
        row = [bias['counts'][pos] for pos in positions]
        bias_data.append(row)
        kmer_labels.append(kmer)
    
    bias_df = pd.DataFrame(bias_data, columns=["5' region", "Middle", "3' region"], index=kmer_labels)
    bias_df.plot(kind='bar', stacked=True, ax=ax2, colormap='viridis')
    ax2.set_title('K-mer Positional Preferences')
    ax2.set_xlabel('K-mer')
    ax2.set_ylabel('Count')
    ax2.legend(title='Region')

# 3. Syntax rule network
ax3 = axes[1, 0]
if len(G) > 5:
    # Create small network visualization
    top_nodes = list(G.nodes())[:15]
    subG = G.subgraph(top_nodes)
    pos = nx.spring_layout(subG)
    nx.draw(subG, pos, ax=ax3, with_labels=True, node_color='lightblue', 
            node_size=500, font_size=8, arrows=True, edge_color='gray')
    ax3.set_title('K-mer Transition Network (Syntax)')
else:
    ax3.text(0.5, 0.5, 'Insufficient data for network', ha='center', va='center')
    ax3.set_title('K-mer Transition Network')

# 4. PCA clustering visualization
ax4 = axes[1, 1]
if 'pca_features' in locals() and len(all_kmers) > 10:
    scatter = ax4.scatter(pca_features[:, 0], pca_features[:, 1], c=clusters, cmap='tab10', alpha=0.7)
    
    # Label some points
    for i, kmer in enumerate(all_kmers[:20]):  # Label first 20
        ax4.annotate(kmer, (pca_features[i, 0], pca_features[i, 1]), fontsize=8, alpha=0.7)
    
    ax4.set_title('K-mer Functional Clusters (PCA)')
    ax4.set_xlabel('PC1')
    ax4.set_ylabel('PC2')
else:
    ax4.text(0.5, 0.5, 'Insufficient data for clustering', ha='center', va='center')
    ax4.set_title('K-mer Functional Clusters')

plt.tight_layout()
plt.show()

# %% Cell 8: Summary of Discoveries

print("\n\n" + "="*60)
print("CELLULAR LANGUAGE DISCOVERIES")
print("="*60)

print("\n1. COMPOUND WORDS (K-mer combinations)")
print("   - Some k-mers frequently appear together at consistent distances")
print("   - These might encode complex cellular instructions")
print("   - Example: 'GATAAG → GGAATG' might mean 'if developing, then grow'")

print("\n2. HIERARCHICAL ORGANIZATION")
print("   - Larger patterns contain smaller functional units")
print("   - Like words containing meaningful prefixes/suffixes")
print("   - Suggests modular, reusable components")

print("\n3. POSITIONAL GRAMMAR")
print("   - Some k-mers prefer 5' regions (initiators?)")
print("   - Others prefer 3' regions (terminators?)")
print("   - Middle preferences might indicate 'process' words")

print("\n4. SYNTAX RULES")
print("   - Clear preferences for what k-mers can follow others")
print("   - Not random - suggests grammatical constraints")
print("   - Some k-mers are 'hubs' leading to many options")

print("\n5. FUNCTIONAL CLUSTERS")
print("   - K-mers group by context usage")
print("   - Clusters correlate with biological function")
print("   - Different sequences use different 'dialects'")

print("\n6. REGENERATION VOCABULARY")
print("   - Uses more k-mer combinations (complex instructions)")
print("   - Has unique syntax patterns")
print("   - More 'hub' k-mers (flexible decision points)")

print("\n\nNEXT STEPS:")
print("- Test if disrupting k-mer combinations breaks function")
print("- See if syntax rules predict new functional sequences")
print("- Design artificial sequences following discovered grammar")
print("- Check if positional preferences affect gene expression")
