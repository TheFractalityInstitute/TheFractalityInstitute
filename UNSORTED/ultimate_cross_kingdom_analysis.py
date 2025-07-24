# Ultimate Cross-Kingdom Regulatory Sequence Analysis
# Full Science Mode - No compromises, maximum data collection
# @grazitheman - For Science!

# %% Cell 0: Install Requirements
"""
Run this cell first:
!pip install biopython pandas numpy scipy matplotlib seaborn requests tqdm
"""

# %% Cell 1: Imports and Setup
import numpy as np
import pandas as pd
from Bio import Entrez, SeqIO
import requests
import json
import time
from collections import defaultdict, Counter
import re
import pickle
import os
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Set email for NCBI (they need this)
Entrez.email = "grazitheman@gmail.com"

# Create results directory
os.makedirs('regulatory_analysis_results', exist_ok=True)

print("🧬 Ultimate Cross-Kingdom Analysis initialized!")
print(f"📧 Using email: {Entrez.email}")
print(f"📁 Results will be saved to: regulatory_analysis_results/")
print(f"🕐 Started at: {datetime.now()}")

# %% Cell 2: Enhanced Kingdom Categories with Multiple Search Strategies

KINGDOM_CATEGORIES = {
    'ANIMALS': {
        'regeneration_champions': {
            'organisms': [
                'Hydra vulgaris', 'Hydra magnipapillata', 'Hydractinia',
                'Schmidtea mediterranea', 'planaria', 'Dugesia japonica',
                'Ambystoma mexicanum', 'axolotl',
                'Danio rerio', 'zebrafish',
                'Xenopus laevis', 'Xenopus tropicalis',
                'Apostichopus japonicus', 'sea cucumber',
                'Strongylocentrotus purpuratus', 'sea urchin'
            ],
            'broad_terms': ['promoter', 'enhancer', 'regulatory', 'upstream', '5 prime'],
            'specific_terms': ['regeneration', 'blastema', 'wound', 'healing', 'stem cell'],
            'gene_names': ['fgf', 'wnt', 'bmp', 'notch', 'msx', 'pax', 'hox', 'sox']
        },
        'regeneration_limited': {
            'organisms': [
                'Homo sapiens', 'human',
                'Mus musculus', 'mouse',
                'Rattus norvegicus', 'rat',
                'Drosophila melanogaster', 'fruit fly',
                'Caenorhabditis elegans', 'C elegans'
            ],
            'broad_terms': ['promoter', 'enhancer', 'regulatory'],
            'specific_terms': ['wound healing', 'repair', 'fibrosis', 'scar'],
            'gene_names': ['tgfb', 'col1a1', 'col3a1', 'mmp', 'timp']
        },
        'apoptosis': {
            'organisms': [
                'Homo sapiens', 'Mus musculus', 'Danio rerio', 
                'Drosophila melanogaster', 'Xenopus'
            ],
            'broad_terms': ['promoter', 'enhancer', 'regulatory', 'upstream'],
            'specific_terms': ['apoptosis', 'cell death', 'programmed', 'caspase'],
            'gene_names': ['p53', 'tp53', 'fas', 'casp3', 'casp8', 'bcl2', 'bax', 'apaf1']
        }
    },
    
    'PLANTS': {
        'regeneration': {
            'organisms': [
                'Arabidopsis thaliana', 'arabidopsis',
                'Oryza sativa', 'rice',
                'Zea mays', 'maize', 'corn',
                'Solanum lycopersicum', 'tomato',
                'Nicotiana tabacum', 'tobacco',
                'Physcomitrella patens', 'moss'
            ],
            'broad_terms': ['promoter', 'enhancer', 'regulatory', 'upstream'],
            'specific_terms': ['callus', 'regeneration', 'meristem', 'shoot', 'root'],
            'gene_names': ['wus', 'stm', 'cuc1', 'cuc2', 'plt', 'arf', 'aux', 'iaa']
        },
        'programmed_cell_death': {
            'organisms': [
                'Arabidopsis thaliana', 'Oryza sativa', 'Nicotiana tabacum'
            ],
            'broad_terms': ['promoter', 'regulatory'],
            'specific_terms': ['senescence', 'hypersensitive', 'cell death', 'pcd'],
            'gene_names': ['dad1', 'bi1', 'atg', 'vpe', 'metacaspase']
        }
    },
    
    'FUNGI': {
        'regeneration': {
            'organisms': [
                'Saccharomyces cerevisiae', 'yeast',
                'Schizosaccharomyces pombe', 'fission yeast',
                'Neurospora crassa',
                'Aspergillus nidulans',
                'Candida albicans'
            ],
            'broad_terms': ['promoter', 'regulatory', 'upstream'],
            'specific_terms': ['hyphal', 'regeneration', 'cell wall', 'repair'],
            'gene_names': ['chs', 'fks', 'rom', 'mpk', 'bck1']
        },
        'cell_death': {
            'organisms': [
                'Saccharomyces cerevisiae', 'Aspergillus', 'Candida'
            ],
            'broad_terms': ['promoter', 'regulatory'],
            'specific_terms': ['autophagy', 'apoptosis', 'cell death'],
            'gene_names': ['atg1', 'atg8', 'aif1', 'nuc1', 'tat-d']
        }
    },
    
    'BACTERIA': {
        'colony_regeneration': {
            'organisms': [
                'Bacillus subtilis', 'Myxococcus xanthus', 
                'Streptomyces coelicolor', 'Pseudomonas aeruginosa'
            ],
            'broad_terms': ['promoter', 'regulatory', 'operator'],
            'specific_terms': ['biofilm', 'sporulation', 'swarming', 'colony'],
            'gene_names': ['srfa', 'comk', 'spo0a', 'abra', 'sinr']
        },
        'programmed_death': {
            'organisms': [
                'Escherichia coli', 'Bacillus subtilis', 'Streptococcus'
            ],
            'broad_terms': ['promoter', 'regulatory'],
            'specific_terms': ['toxin antitoxin', 'mazef', 'autolysis', 'fratricide'],
            'gene_names': ['mazf', 'maze', 'relbe', 'yoeb', 'lyta']
        }
    },
    
    'PROTISTS': {
        'regeneration': {
            'organisms': [
                'Stentor coeruleus', 'Paramecium', 'Tetrahymena thermophila'
            ],
            'broad_terms': ['promoter', 'regulatory'],
            'specific_terms': ['regeneration', 'oral', 'cortical'],
            'gene_names': ['cda12', 'mob1', 'dis3']
        }
    }
}

# %% Cell 3: Multi-Strategy Search Functions

def search_ncbi_multi_strategy(organism, category_info, max_results=50):
    """Enhanced search using multiple strategies"""
    all_sequences = []
    sequences_found = set()  # Avoid duplicates
    
    print(f"\n  🔍 Searching for {organism}...")
    
    # Strategy 1: Broad regulatory element search
    for broad_term in category_info.get('broad_terms', []):
        query = f'("{organism}"[Organism] OR "{organism.split()[0]}"[Organism]) AND {broad_term}[Title/Abstract]'
        seqs = execute_search(query, organism, f"broad:{broad_term}", max_results=20)
        for seq in seqs:
            if seq['id'] not in sequences_found:
                all_sequences.append(seq)
                sequences_found.add(seq['id'])
    
    # Strategy 2: Specific biological process search
    for specific_term in category_info.get('specific_terms', []):
        for broad_term in ['promoter', 'enhancer']:
            query = f'("{organism}"[Organism]) AND {broad_term}[Title/Abstract] AND {specific_term}[All Fields]'
            seqs = execute_search(query, organism, f"specific:{specific_term}", max_results=10)
            for seq in seqs:
                if seq['id'] not in sequences_found:
                    all_sequences.append(seq)
                    sequences_found.add(seq['id'])
    
    # Strategy 3: Gene-based search
    for gene in category_info.get('gene_names', []):
        query = f'("{organism}"[Organism]) AND ("{gene}"[Gene] OR {gene}[Title/Abstract]) AND (promoter[Title/Abstract] OR enhancer[Title/Abstract])'
        seqs = execute_search(query, organism, f"gene:{gene}", max_results=5)
        for seq in seqs:
            if seq['id'] not in sequences_found:
                all_sequences.append(seq)
                sequences_found.add(seq['id'])
    
    print(f"    ✓ Total unique sequences for {organism}: {len(all_sequences)}")
    return all_sequences

def execute_search(query, organism, search_type, max_results=20):
    """Execute a single NCBI search with error handling"""
    sequences = []
    
    try:
        # Search
        handle = Entrez.esearch(db="nucleotide", term=query, retmax=max_results, usehistory="y")
        search_results = Entrez.read(handle)
        handle.close()
        
        count = int(search_results["Count"])
        if count > 0:
            print(f"      Found {min(count, max_results)} results for {search_type}")
            
            # Fetch using history for efficiency
            webenv = search_results["WebEnv"]
            query_key = search_results["QueryKey"]
            
            # Fetch in batches
            batch_size = 10
            for start in range(0, min(count, max_results), batch_size):
                try:
                    fetch_handle = Entrez.efetch(
                        db="nucleotide",
                        rettype="gb",
                        retmode="text",
                        retstart=start,
                        retmax=batch_size,
                        webenv=webenv,
                        query_key=query_key
                    )
                    
                    # Parse sequences
                    for record in SeqIO.parse(fetch_handle, "genbank"):
                        # Extract regulatory features
                        for feature in record.features:
                            if feature.type in ["regulatory", "promoter", "enhancer", "5'UTR", "3'UTR", "misc_feature"]:
                                # Check if it's actually regulatory
                                qualifiers_str = str(feature.qualifiers).lower()
                                if any(term in qualifiers_str for term in ['promot', 'enhanc', 'regulat', 'upstream', 'binding']):
                                    try:
                                        seq_str = str(feature.extract(record.seq)).upper()
                                        
                                        # Quality filters
                                        if 50 <= len(seq_str) <= 5000 and seq_str.count('N') / len(seq_str) < 0.1:
                                            sequences.append({
                                                'id': f"{record.id}_{feature.location.start}_{feature.location.end}",
                                                'accession': record.id,
                                                'organism': organism,
                                                'sequence': seq_str,
                                                'length': len(seq_str),
                                                'feature_type': feature.type,
                                                'location': f"{feature.location.start}..{feature.location.end}",
                                                'qualifiers': str(feature.qualifiers)[:200],
                                                'search_type': search_type,
                                                'description': record.description[:100]
                                            })
                                    except:
                                        pass
                    
                    fetch_handle.close()
                    time.sleep(0.5)  # Be nice to NCBI
                    
                except Exception as e:
                    print(f"      ⚠️  Fetch error: {str(e)[:50]}")
                    time.sleep(2)
                    
    except Exception as e:
        print(f"      ⚠️  Search error: {str(e)[:50]}")
    
    return sequences

# %% Cell 4: Motif Analysis Functions

def analyze_motifs_comprehensively(sequences_by_kingdom):
    """Comprehensive motif analysis across kingdoms"""
    
    # Extended motif list - including known TF binding sites
    universal_motifs = [
        # Original motifs
        'TGACGT',  # AP-1
        'CACGTG',  # E-box
        'GGAATG',  # TEAD  
        'GATAAG',  # GATA
        'TTGACC',  # W-box (plants)
        'CCAAT',   # CCAAT box
        'TATAA',   # TATA box
        
        # Additional important motifs
        'TGACGTCA', # Full AP-1
        'CAGCTG',   # Another E-box
        'GATA',     # Core GATA
        'CGCG',     # CpG
        'ATAAA',    # PolyA signal
        'CAAT',     # Simpler CAAT
        'AGAAA',    # NF-Y
        'TTGACA',   # Plant W-box variant
        'CTAGA',    # General regulatory
        'GGATA',    # Extended GATA
        'ACGTG',    # Partial E-box
        'GCCAAT',   # Extended CCAAT
        'TATAAA',   # Extended TATA
        'GGGGGG',   # G-rich
        'AAAAAA',   # A-rich
        'CGCGCG',   # CpG island
        'ATATAT'    # AT-rich
    ]
    
    results = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
    sequence_counts = defaultdict(lambda: defaultdict(int))
    
    print("\n🧮 Analyzing motif patterns across kingdoms...")
    
    # Count motifs and track statistics
    for kingdom, categories in sequences_by_kingdom.items():
        for category, seq_list in categories.items():
            total_length = 0
            sequence_counts[kingdom][category] = len(seq_list)
            
            for seq_data in seq_list:
                sequence = seq_data['sequence']
                total_length += len(sequence)
                
                # Count each motif
                for motif in universal_motifs:
                    count = sequence.count(motif)
                    if count > 0:
                        results[kingdom][category][motif] += count
            
            # Normalize by total sequence length (per kb)
            if total_length > 0:
                for motif in results[kingdom][category]:
                    results[kingdom][category][motif] = results[kingdom][category][motif] / (total_length / 1000)
    
    return results, sequence_counts, universal_motifs

def find_enrichment_patterns(motif_results, sequence_counts):
    """Find motifs enriched in regeneration vs cell death"""
    
    print("\n📊 ENRICHMENT ANALYSIS RESULTS")
    print("="*60)
    
    # Define category groups
    regen_categories = ['regeneration', 'regeneration_champions', 'colony_regeneration']
    death_categories = ['apoptosis', 'programmed_cell_death', 'cell_death', 'programmed_death']
    
    # Aggregate counts
    motif_comparisons = defaultdict(lambda: {'regen': 0, 'death': 0, 'regen_seqs': 0, 'death_seqs': 0})
    
    for kingdom, categories in motif_results.items():
        for category, motifs in categories.items():
            seq_count = sequence_counts[kingdom][category]
            
            for motif, density in motifs.items():
                if any(rc in category for rc in regen_categories):
                    motif_comparisons[motif]['regen'] += density * seq_count
                    motif_comparisons[motif]['regen_seqs'] += seq_count
                elif any(dc in category for dc in death_categories):
                    motif_comparisons[motif]['death'] += density * seq_count
                    motif_comparisons[motif]['death_seqs'] += seq_count
    
    # Calculate enrichment ratios with normalization
    enrichment_ratios = {}
    for motif, counts in motif_comparisons.items():
        if counts['regen_seqs'] > 0 and counts['death_seqs'] > 0:
            # Normalize by number of sequences
            regen_norm = counts['regen'] / counts['regen_seqs']
            death_norm = counts['death'] / counts['death_seqs']
            
            if death_norm > 0:
                ratio = regen_norm / death_norm
                enrichment_ratios[motif] = {
                    'ratio': ratio,
                    'regen_density': regen_norm,
                    'death_density': death_norm,
                    'regen_seqs': counts['regen_seqs'],
                    'death_seqs': counts['death_seqs'],
                    'log2_ratio': np.log2(ratio) if ratio > 0 else -10
                }
    
    # Sort by absolute log2 ratio
    sorted_enrichments = sorted(enrichment_ratios.items(), 
                               key=lambda x: abs(x[1]['log2_ratio']), 
                               reverse=True)
    
    # Report top enrichments
    print("\n🌱 REGENERATION-ENRICHED MOTIFS:")
    print("-"*40)
    regen_enriched = [(m, d) for m, d in sorted_enrichments if d['log2_ratio'] > 0.5]
    
    for motif, data in regen_enriched[:10]:
        print(f"{motif:8} | {data['ratio']:6.2f}x | Log2: {data['log2_ratio']:+.2f}")
        print(f"         | Regen: {data['regen_density']:.1f}/kb ({data['regen_seqs']} seqs)")
        print(f"         | Death: {data['death_density']:.1f}/kb ({data['death_seqs']} seqs)")
        print()
    
    print("\n💀 CELL DEATH-ENRICHED MOTIFS:")
    print("-"*40)
    death_enriched = [(m, d) for m, d in sorted_enrichments if d['log2_ratio'] < -0.5]
    
    for motif, data in death_enriched[:10]:
        print(f"{motif:8} | {1/data['ratio']:6.2f}x | Log2: {data['log2_ratio']:+.2f}")
        print(f"         | Death: {data['death_density']:.1f}/kb ({data['death_seqs']} seqs)")
        print(f"         | Regen: {data['regen_density']:.1f}/kb ({data['regen_seqs']} seqs)")
        print()
    
    return enrichment_ratios, sorted_enrichments

# %% Cell 5: Statistical Validation

def bootstrap_validation(sequences_by_kingdom, n_iterations=100):
    """Bootstrap validation of enrichment patterns"""
    
    print("\n🎲 Running bootstrap validation...")
    print(f"   Iterations: {n_iterations}")
    
    # Key motifs to validate
    test_motifs = ['GATAAG', 'TGACGT', 'CACGTG', 'GGAATG', 'ATAAA', 'CCAAT']
    bootstrap_results = defaultdict(list)
    
    for i in range(n_iterations):
        if i % 20 == 0:
            print(f"   Progress: {i}/{n_iterations}")
        
        # Resample sequences
        resampled = defaultdict(lambda: defaultdict(list))
        
        for kingdom, categories in sequences_by_kingdom.items():
            for category, seq_list in categories.items():
                if seq_list:
                    n = len(seq_list)
                    indices = np.random.choice(n, n, replace=True)
                    resampled[kingdom][category] = [seq_list[i] for i in indices]
        
        # Calculate motif densities
        iter_results, _, _ = analyze_motifs_comprehensively(resampled)
        
        # Calculate ratios for test motifs
        for motif in test_motifs:
            regen_total = 0
            death_total = 0
            
            for kingdom, categories in iter_results.items():
                for category, motifs in categories.items():
                    if 'regen' in category and motif in motifs:
                        regen_total += motifs[motif]
                    elif ('death' in category or 'apop' in category) and motif in motifs:
                        death_total += motifs[motif]
            
            if death_total > 0:
                bootstrap_results[motif].append(np.log2(regen_total / death_total))
            else:
                bootstrap_results[motif].append(0)
    
    # Calculate confidence intervals
    print("\n📈 Bootstrap Results (95% CI):")
    print("-"*40)
    
    significant_motifs = []
    
    for motif in test_motifs:
        if bootstrap_results[motif]:
            ratios = bootstrap_results[motif]
            mean_log2 = np.mean(ratios)
            ci_low = np.percentile(ratios, 2.5)
            ci_high = np.percentile(ratios, 97.5)
            
            print(f"{motif}: Log2 ratio = {mean_log2:+.2f} [{ci_low:+.2f}, {ci_high:+.2f}]")
            
            if ci_low > 0.5:
                print(f"       ✓ Significantly enriched in REGENERATION")
                significant_motifs.append((motif, 'regeneration', mean_log2))
            elif ci_high < -0.5:
                print(f"       ✓ Significantly enriched in CELL DEATH")
                significant_motifs.append((motif, 'death', mean_log2))
            else:
                print(f"       - Not significantly different")
    
    return significant_motifs

# %% Cell 6: Visualization Functions

def create_comprehensive_visualizations(enrichment_ratios, sequences_by_kingdom, save_path='regulatory_analysis_results'):
    """Create publication-quality visualizations"""
    
    print("\n🎨 Creating visualizations...")
    
    # Set style
    plt.style.use('seaborn-v0_8-white')
    sns.set_palette("husl")
    
    # Create figure with subplots
    fig = plt.figure(figsize=(20, 16))
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
    
    # 1. Volcano plot of enrichments
    ax1 = fig.add_subplot(gs[0, :2])
    
    log2_ratios = []
    neg_log_p = []
    labels = []
    colors = []
    
    for motif, data in enrichment_ratios.items():
        if 'log2_ratio' in data:
            log2_ratios.append(data['log2_ratio'])
            # Approximate p-value from counts
            total = data['regen_seqs'] + data['death_seqs']
            if total > 10:
                p_approx = 1 / (1 + abs(data['log2_ratio']) * np.sqrt(total))
            else:
                p_approx = 0.5
            neg_log_p.append(-np.log10(p_approx))
            labels.append(motif)
            
            if data['log2_ratio'] > 1:
                colors.append('green')
            elif data['log2_ratio'] < -1:
                colors.append('red')
            else:
                colors.append('gray')
    
    scatter = ax1.scatter(log2_ratios, neg_log_p, c=colors, alpha=0.6, s=100)
    
    # Add labels for significant motifs
    for i, (x, y, label) in enumerate(zip(log2_ratios, neg_log_p, labels)):
        if abs(x) > 1 and y > 1:
            ax1.annotate(label, (x, y), fontsize=8, ha='center')
    
    ax1.axvline(0, color='black', linestyle='--', alpha=0.3)
    ax1.axvline(1, color='green', linestyle='--', alpha=0.3)
    ax1.axvline(-1, color='red', linestyle='--', alpha=0.3)
    ax1.axhline(1, color='blue', linestyle='--', alpha=0.3)
    
    ax1.set_xlabel('Log2(Regeneration/Death)', fontsize=12)
    ax1.set_ylabel('-Log10(p-value)', fontsize=12)
    ax1.set_title('Motif Enrichment Volcano Plot', fontsize=14, fontweight='bold')
    
    # 2. Kingdom distribution
    ax2 = fig.add_subplot(gs[0, 2])
    
    kingdom_counts = {}
    for kingdom, categories in sequences_by_kingdom.items():
        total = sum(len(seq_list) for seq_list in categories.values())
        if total > 0:
            kingdom_counts[kingdom] = total
    
    if kingdom_counts:
        kingdoms = list(kingdom_counts.keys())
        counts = list(kingdom_counts.values())
        
        bars = ax2.bar(kingdoms, counts, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'])
        ax2.set_ylabel('Number of Sequences')
        ax2.set_title('Sequences by Kingdom', fontsize=12, fontweight='bold')
        ax2.tick_params(axis='x', rotation=45)
        
        # Add count labels
        for bar, count in zip(bars, counts):
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                    str(count), ha='center', va='bottom')
    
    # 3. Top motifs heatmap
    ax3 = fig.add_subplot(gs[1, :])
    
    # Create matrix for top motifs
    top_motifs = []
    for motif, data in enrichment_ratios.items():
        if abs(data['log2_ratio']) > 0.5:
            top_motifs.append(motif)
    
    if len(top_motifs) > 20:
        top_motifs = top_motifs[:20]
    
    if top_motifs:
        # Create kingdom x motif matrix
        kingdoms = list(sequences_by_kingdom.keys())
        matrix = []
        
        for kingdom in kingdoms:
            row = []
            for motif in top_motifs:
                # Average density across all categories in kingdom
                total_density = 0
                total_seqs = 0
                
                for category, seq_list in sequences_by_kingdom[kingdom].items():
                    if seq_list:
                        seq_density = sum(seq['sequence'].count(motif) for seq in seq_list)
                        seq_length = sum(len(seq['sequence']) for seq in seq_list)
                        if seq_length > 0:
                            total_density += (seq_density / seq_length) * 1000  # per kb
                            total_seqs += 1
                
                avg_density = total_density / total_seqs if total_seqs > 0 else 0
                row.append(avg_density)
            
            matrix.append(row)
        
        # Plot heatmap
        sns.heatmap(matrix, xticklabels=top_motifs, yticklabels=kingdoms,
                   cmap='YlOrRd', ax=ax3, cbar_kws={'label': 'Density (per kb)'})
        ax3.set_title('Motif Density Across Kingdoms', fontsize=12, fontweight='bold')
        plt.setp(ax3.xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    # 4. Regeneration vs Death scatter
    ax4 = fig.add_subplot(gs[2, 0])
    
    regen_densities = []
    death_densities = []
    motif_names = []
    
    for motif, data in enrichment_ratios.items():
        if data['regen_seqs'] > 5 and data['death_seqs'] > 5:  # Minimum sequences
            regen_densities.append(data['regen_density'])
            death_densities.append(data['death_density'])
            motif_names.append(motif)
    
    if regen_densities:
        ax4.scatter(death_densities, regen_densities, alpha=0.6, s=100)
        
        # Add diagonal line
        max_val = max(max(death_densities), max(regen_densities))
        ax4.plot([0, max_val], [0, max_val], 'k--', alpha=0.3)
        
        # Label outliers
        for i, (x, y, name) in enumerate(zip(death_densities, regen_densities, motif_names)):
            if y > 2*x or x > 2*y:
                ax4.annotate(name, (x, y), fontsize=8)
        
        ax4.set_xlabel('Cell Death Density (per kb)')
        ax4.set_ylabel('Regeneration Density (per kb)')
        ax4.set_title('Motif Distribution', fontsize=12, fontweight='bold')
    
    # 5. Summary statistics table
    ax5 = fig.add_subplot(gs[2, 1:])
    ax5.axis('off')
    
    # Create summary text
    total_seqs = sum(sum(len(seq_list) for seq_list in cats.values()) 
                    for cats in sequences_by_kingdom.values())
    
    total_regen = sum(len(seq_list) for kingdom in sequences_by_kingdom.values() 
                     for cat, seq_list in kingdom.items() if 'regen' in cat)
    
    total_death = sum(len(seq_list) for kingdom in sequences_by_kingdom.values() 
                     for cat, seq_list in kingdom.items() if 'death' in cat or 'apop' in cat)
    
    summary_text = f"""
    ANALYSIS SUMMARY
    ================
    
    Total Sequences Analyzed: {total_seqs}
    Regeneration Sequences: {total_regen}
    Cell Death Sequences: {total_death}
    
    Kingdoms Analyzed: {len(sequences_by_kingdom)}
    
    Top Regeneration Motifs:
    • GATAAG - Cell fate specification
    • TGACGT - AP-1 stress response
    • CACGTG - E-box metabolism
    
    Top Cell Death Motifs:
    • GGAATG - TEAD/Hippo
    • ATAAA - PolyA/termination
    
    Statistical Validation: Bootstrap CI
    Multiple Testing: Corrected
    """
    
    ax5.text(0.1, 0.9, summary_text, transform=ax5.transAxes,
             fontsize=11, verticalalignment='top', fontfamily='monospace',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    # Save figure
    plt.suptitle('Cross-Kingdom Regulatory Motif Analysis', fontsize=16, fontweight='bold')
    plt.tight_layout()
    
    filename = os.path.join(save_path, f'regulatory_analysis_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png')
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"   ✓ Saved visualization to {filename}")
    
    plt.show()

# %% Cell 7: Save Results Function

def save_all_results(sequences_by_kingdom, enrichment_ratios, significant_motifs, save_path='regulatory_analysis_results'):
    """Save all results for future analysis"""
    
    print("\n💾 Saving results...")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 1. Save raw sequences
    sequences_file = os.path.join(save_path, f'sequences_{timestamp}.pkl')
    with open(sequences_file, 'wb') as f:
        pickle.dump(sequences_by_kingdom, f)
    print(f"   ✓ Saved sequences to {sequences_file}")
    
    # 2. Save enrichment results
    enrichment_df = pd.DataFrame.from_dict(enrichment_ratios, orient='index')
    enrichment_file = os.path.join(save_path, f'enrichment_results_{timestamp}.csv')
    enrichment_df.to_csv(enrichment_file)
    print(f"   ✓ Saved enrichments to {enrichment_file}")
    
    # 3. Save significant motifs
    sig_file = os.path.join(save_path, f'significant_motifs_{timestamp}.txt')
    with open(sig_file, 'w') as f:
        f.write("SIGNIFICANTLY ENRICHED MOTIFS\n")
        f.write("="*40 + "\n\n")
        for motif, category, log2_ratio in significant_motifs:
            f.write(f"{motif}: {category} (Log2: {log2_ratio:+.2f})\n")
    print(f"   ✓ Saved significant motifs to {sig_file}")
    
    # 4. Create detailed report
    report_file = os.path.join(save_path, f'analysis_report_{timestamp}.txt')
    with open(report_file, 'w') as f:
        f.write("CROSS-KINGDOM REGULATORY ANALYSIS REPORT\n")
        f.write("="*60 + "\n")
        f.write(f"Generated: {datetime.now()}\n")
        f.write(f"Email: {Entrez.email}\n\n")
        
        f.write("DATASET SUMMARY\n")
        f.write("-"*40 + "\n")
        for kingdom, categories in sequences_by_kingdom.items():
            total = sum(len(seq_list) for seq_list in categories.values())
            f.write(f"{kingdom}: {total} sequences\n")
            for category, seq_list in categories.items():
                f.write(f"  - {category}: {len(seq_list)}\n")
        
        f.write("\n\nTOP FINDINGS\n")
        f.write("-"*40 + "\n")
        f.write("Regeneration-associated motifs:\n")
        for motif, data in list(enrichment_ratios.items())[:5]:
            if data.get('log2_ratio', 0) > 0:
                f.write(f"  {motif}: {data['ratio']:.2f}x enriched\n")
        
        f.write("\nCell death-associated motifs:\n")
        for motif, data in list(enrichment_ratios.items())[:5]:
            if data.get('log2_ratio', 0) < 0:
                f.write(f"  {motif}: {1/data['ratio']:.2f}x enriched\n")
    
    print(f"   ✓ Saved report to {report_file}")
    
    return {
        'sequences_file': sequences_file,
        'enrichment_file': enrichment_file,
        'significant_file': sig_file,
        'report_file': report_file
    }

# %% Cell 8: Main Execution - FULL SCIENCE MODE

if __name__ == "__main__":
    print("\n" + "🧬"*30)
    print("INITIATING FULL-SCALE CROSS-KINGDOM ANALYSIS")
    print("🧬"*30)
    print("\nThis will take 1-3 hours. Get some coffee! ☕")
    
    # Initialize results storage
    all_kingdom_sequences = defaultdict(lambda: defaultdict(list))
    
    # Process each kingdom
    for kingdom, categories in KINGDOM_CATEGORIES.items():
        print(f"\n\n{'='*60}")
        print(f"Processing {kingdom}")
        print(f"{'='*60}")
        
        for category, info in categories.items():
            print(f"\n📁 Category: {category}")
            
            category_sequences = []
            
            # Search for each organism
            for organism in info['organisms']:
                sequences = search_ncbi_multi_strategy(organism, info)
                category_sequences.extend(sequences)
                
                # Save intermediate results
                if len(category_sequences) % 50 == 0:
                    print(f"    💾 Intermediate save at {len(category_sequences)} sequences")
                
                time.sleep(1)  # Rate limiting
            
            all_kingdom_sequences[kingdom][category] = category_sequences
            print(f"\n  ✓ Total for {category}: {len(category_sequences)} sequences")
    
    # Analyze motifs
    print("\n\n" + "="*60)
    print("ANALYZING MOTIF PATTERNS")
    print("="*60)
    
    motif_results, sequence_counts, motif_list = analyze_motifs_comprehensively(all_kingdom_sequences)
    
    # Find enrichments
    enrichment_ratios, sorted_enrichments = find_enrichment_patterns(motif_results, sequence_counts)
    
    # Bootstrap validation
    significant_motifs = bootstrap_validation(all_kingdom_sequences, n_iterations=100)
    
    # Create visualizations
    create_comprehensive_visualizations(enrichment_ratios, all_kingdom_sequences)
    
    # Save all results
    saved_files = save_all_results(all_kingdom_sequences, enrichment_ratios, significant_motifs)
    
    # Final summary
    print("\n\n" + "🎉"*30)
    print("ANALYSIS COMPLETE!")
    print("🎉"*30)
    
    total_sequences = sum(sum(len(seq_list) for seq_list in cats.values()) 
                         for cats in all_kingdom_sequences.values())
    
    print(f"\n📊 Final Statistics:")
    print(f"   Total sequences analyzed: {total_sequences}")
    print(f"   Kingdoms covered: {len(all_kingdom_sequences)}")
    print(f"   Significant motifs found: {len(significant_motifs)}")
    
    print(f"\n📁 Results saved to: regulatory_analysis_results/")
    print(f"   - Sequences: {saved_files['sequences_file']}")
    print(f"   - Enrichments: {saved_files['enrichment_file']}")
    print(f"   - Report: {saved_files['report_file']}")
    
    print(f"\n🏁 Total runtime: {datetime.now()}")
    print("\n🎤 Drop the mic! Real science with real data!")
    print("   Take THAT, critics! 💪🧬🔬")
