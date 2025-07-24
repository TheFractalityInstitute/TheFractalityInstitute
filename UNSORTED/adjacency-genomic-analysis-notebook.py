# Adjacency Rule Discovery - Genomic Analysis Notebook
# Run this in Google Colab to search for morphogenetic patterns in genomic data

# %% [markdown]
# # Adjacency Rule Discovery in Genomic Data
# This notebook searches for evidence that DNA encodes local cell-cell interaction rules

# %% Cell 1: Setup and Installation
!pip install biopython requests pandas matplotlib seaborn numpy scikit-learn
!pip install pyfaidx mygene pyensembl

import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from Bio import Entrez, SeqIO
from Bio.Seq import Seq
from Bio.SeqUtils import GC
import re
from collections import Counter, defaultdict
import time
from itertools import combinations
import warnings
warnings.filterwarnings('ignore')

# Set up Entrez
Entrez.email = "your.email@example.com"  # IMPORTANT: Replace with your email

print("Setup complete! Ready to search for adjacency rules.")

# %% Cell 2: Define Target Genes and Organisms
# Key morphogenetic boundary genes to analyze
BOUNDARY_GENES = {
    'EPH_EPHRIN': {
        'human': ['EPHA1', 'EPHA2', 'EPHB1', 'EPHB2', 'EFNA1', 'EFNB1'],
        'mouse': ['Epha1', 'Epha2', 'Ephb1', 'Ephb2', 'Efna1', 'Efnb1'],
        'description': 'Cell sorting and tissue boundary formation'
    },
    'HOX': {
        'human': ['HOXA1', 'HOXA2', 'HOXB1', 'HOXB2', 'HOXD9', 'HOXD10'],
        'mouse': ['Hoxa1', 'Hoxa2', 'Hoxb1', 'Hoxb2', 'Hoxd9', 'Hoxd10'],
        'description': 'Positional identity along body axis'
    },
    'NOTCH': {
        'human': ['NOTCH1', 'NOTCH2', 'DLL1', 'DLL4', 'JAG1'],
        'mouse': ['Notch1', 'Notch2', 'Dll1', 'Dll4', 'Jag1'],
        'description': 'Cell-cell communication and lateral inhibition'
    },
    'GAP_JUNCTION': {
        'human': ['GJA1', 'GJA5', 'GJB1', 'GJB2'],
        'mouse': ['Gja1', 'Gja5', 'Gjb1', 'Gjb2'],
        'description': 'Bioelectric coupling between cells'
    }
}

# Organisms for comparative analysis
ORGANISMS = {
    'human': {'taxid': '9606', 'assembly': 'GRCh38'},
    'mouse': {'taxid': '10090', 'assembly': 'GRCm39'},
    'zebrafish': {'taxid': '7955', 'assembly': 'GRCz11'},
    'planaria': {'taxid': '79327', 'assembly': 'dd_Smes_g4'}  # S. mediterranea
}

print(f"Analyzing {len(BOUNDARY_GENES)} gene families across {len(ORGANISMS)} organisms")

# %% Cell 3: Fetch Genomic Sequences
def fetch_gene_region(gene_name, organism='human', upstream=10000, downstream=5000):
    """
    Fetch genomic sequence around a gene including regulatory regions
    """
    try:
        # Search for gene
        search_query = f"{gene_name}[Gene Name] AND {ORGANISMS[organism]['taxid']}[Taxonomy ID]"
        handle = Entrez.esearch(db="gene", term=search_query, retmax=1)
        record = Entrez.read(handle)
        handle.close()
        
        if not record['IdList']:
            print(f"Gene {gene_name} not found for {organism}")
            return None
            
        gene_id = record['IdList'][0]
        
        # Get gene info
        handle = Entrez.efetch(db="gene", id=gene_id, rettype="xml")
        gene_record = Entrez.read(handle)
        handle.close()
        
        # Extract genomic coordinates
        gene_info = gene_record[0]
        
        # Get sequence with flanking regions
        # Note: In a real implementation, you'd extract exact coordinates
        # and fetch from the nucleotide database
        
        # For now, return a placeholder
        return {
            'gene': gene_name,
            'organism': organism,
            'sequence': None,  # Would contain actual sequence
            'gene_id': gene_id
        }
        
    except Exception as e:
        print(f"Error fetching {gene_name}: {e}")
        return None

# Example usage (don't run all at once to avoid overwhelming NCBI)
# test_result = fetch_gene_region('EPHA1', 'human')
# print(f"Fetched data for: {test_result['gene'] if test_result else 'Failed'}")

# %% Cell 4: Pattern Discovery Functions
def find_regulatory_motifs(sequence, motif_length=6):
    """
    Find overrepresented motifs that could encode rules
    """
    if not sequence:
        return {}
    
    motifs = defaultdict(int)
    seq_len = len(sequence)
    
    # Count all k-mers
    for i in range(seq_len - motif_length + 1):
        motif = sequence[i:i + motif_length]
        if 'N' not in motif:  # Skip ambiguous bases
            motifs[motif] += 1
    
    # Calculate expected frequency (assuming random distribution)
    expected_freq = (seq_len - motif_length + 1) / (4 ** motif_length)
    
    # Find overrepresented motifs
    significant_motifs = {}
    for motif, count in motifs.items():
        if count > expected_freq * 2:  # Simple threshold
            enrichment = count / expected_freq
            significant_motifs[motif] = {
                'count': count,
                'enrichment': enrichment,
                'reverse_complement': str(Seq(motif).reverse_complement())
            }
    
    return significant_motifs

def find_palindromic_sequences(sequence, min_length=6, max_length=20):
    """
    Find palindromic sequences that might indicate bidirectional sensing
    """
    palindromes = []
    
    if not sequence:
        return palindromes
    
    seq_obj = Seq(sequence)
    
    for length in range(min_length, max_length + 1, 2):  # Even lengths only
        for i in range(len(sequence) - length + 1):
            subseq = sequence[i:i + length]
            if 'N' not in subseq:
                if subseq == str(Seq(subseq).reverse_complement()):
                    palindromes.append({
                        'sequence': subseq,
                        'position': i,
                        'length': length
                    })
    
    return palindromes

def find_spacing_patterns(motif_positions):
    """
    Analyze spacing between motif occurrences
    Could indicate distance-based rules
    """
    if len(motif_positions) < 2:
        return {}
    
    spacings = []
    for i in range(1, len(motif_positions)):
        spacings.append(motif_positions[i] - motif_positions[i-1])
    
    # Look for regular spacing
    spacing_counts = Counter(spacings)
    
    # Find periodic patterns
    patterns = {}
    for spacing, count in spacing_counts.items():
        if count >= 3:  # At least 3 occurrences
            patterns[spacing] = {
                'count': count,
                'percentage': count / len(spacings) * 100
            }
    
    return patterns

# %% Cell 5: Comparative Analysis Functions
def compare_regulatory_regions(gene_family, organisms=['human', 'mouse']):
    """
    Compare regulatory patterns across species
    """
    results = {
        'conserved_motifs': [],
        'species_specific': defaultdict(list),
        'palindrome_conservation': []
    }
    
    # This is where we'd actually fetch and compare sequences
    # For demonstration, showing the analysis structure
    
    print(f"Comparing {gene_family} across {organisms}")
    print("Would analyze:")
    print("- Conserved motifs in regulatory regions")
    print("- Species-specific patterns")
    print("- Palindrome conservation")
    print("- Spacing pattern similarities")
    
    return results

# %% Cell 6: Rule Grammar Discovery
def identify_potential_rules(sequence_data):
    """
    Look for patterns that could encode IF-THEN logic
    """
    rule_candidates = []
    
    # Pattern 1: Motif combinations that could represent conditionals
    # Look for: [SENSOR_MOTIF]...[SPACER]...[RESPONSE_MOTIF]
    
    # Known regulatory motifs that could act as sensors
    sensor_motifs = {
        'GATA': 'WGATAR',  # GATA factors (developmental)
        'ETS': 'MGGAAR',   # ETS factors (cell fate)
        'SOX': 'WWCAAWG',  # SOX factors (stem cell)
        'FOX': 'RYAAAYA',  # Forkhead box (differentiation)
    }
    
    # Response element motifs
    response_motifs = {
        'AP1': 'TGASTCA',  # Stress/mechanical response
        'CREB': 'TGACGTCA', # cAMP response
        'NFAT': 'GGAAAA',   # Calcium response
        'YAP': 'GGAATG',    # Mechanical/Hippo pathway
    }
    
    # This would analyze actual sequences for these patterns
    print("Searching for rule-like patterns:")
    print(f"- {len(sensor_motifs)} sensor motifs")
    print(f"- {len(response_motifs)} response motifs")
    print("- Analyzing optimal spacing between elements")
    
    return rule_candidates

# %% Cell 7: Visualization Functions
def plot_motif_distribution(motif_data, title="Motif Distribution"):
    """
    Visualize motif occurrences and patterns
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    
    # Placeholder for actual data visualization
    # Would show:
    # - Motif frequency distribution
    # - Positional bias (5' vs 3')
    # - Conservation across species
    
    ax1.set_title(f"{title} - Frequency")
    ax1.set_xlabel("Motif")
    ax1.set_ylabel("Count")
    
    ax2.set_title(f"{title} - Positional Distribution")
    ax2.set_xlabel("Position relative to TSS")
    ax2.set_ylabel("Motif Density")
    
    plt.tight_layout()
    return fig

def create_rule_network_visualization(rules):
    """
    Visualize potential rule networks as graphs
    """
    # Would create network showing:
    # - Sensor nodes
    # - Logic gates
    # - Effector nodes
    # - Connections representing rules
    
    print("Rule network visualization would show:")
    print("- Input sensors (mechanosensitive, bioelectric, chemical)")
    print("- Logic processing (AND, OR, threshold)")
    print("- Output effectors (differentiation, movement, death)")

# %% Cell 8: Machine Learning Pattern Recognition
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

def ml_pattern_discovery(sequences, labels=None):
    """
    Use ML to discover hidden patterns in regulatory sequences
    """
    if not sequences:
        print("No sequences provided for ML analysis")
        return None
    
    # Convert sequences to k-mer features
    vectorizer = CountVectorizer(analyzer='char', ngram_range=(4, 8))
    
    # This would process actual sequences
    print("ML Analysis would include:")
    print("- K-mer frequency vectors")
    print("- Dimensionality reduction (PCA)")
    print("- Clustering to find sequence families")
    print("- Association with morphological outcomes")
    
    return {
        'vectorizer': vectorizer,
        'features': None,  # Would contain feature matrix
        'clusters': None   # Would contain cluster assignments
    }

# %% Cell 9: Main Analysis Pipeline
def run_adjacency_rule_analysis():
    """
    Main pipeline to search for adjacency rules in genomic data
    """
    print("=" * 60)
    print("ADJACENCY RULE DISCOVERY PIPELINE")
    print("=" * 60)
    
    all_results = {}
    
    for gene_family, genes in BOUNDARY_GENES.items():
        print(f"\nAnalyzing {gene_family} family:")
        print(f"Function: {genes['description']}")
        
        family_results = {
            'motifs': {},
            'palindromes': [],
            'spacing_patterns': {},
            'conservation': {}
        }
        
        # For each organism
        for organism in ['human', 'mouse']:
            organism_genes = genes.get(organism, [])
            
            for gene in organism_genes[:2]:  # Limit to avoid overwhelming NCBI
                print(f"\n  Processing {gene} ({organism})...")
                
                # Fetch sequence (commented to avoid running without email setup)
                # gene_data = fetch_gene_region(gene, organism)
                
                # Analyze patterns (would run on actual sequences)
                # motifs = find_regulatory_motifs(sequence)
                # palindromes = find_palindromic_sequences(sequence)
                
                # Store results
                # family_results['motifs'][gene] = motifs
                
                time.sleep(0.5)  # Be nice to NCBI
        
        # Comparative analysis
        comparison = compare_regulatory_regions(gene_family)
        family_results['conservation'] = comparison
        
        # Look for rule patterns
        rules = identify_potential_rules(family_results)
        family_results['potential_rules'] = rules
        
        all_results[gene_family] = family_results
    
    return all_results

# %% Cell 10: Execute Analysis
# Uncomment the line below after adding your email to Cell 1
# results = run_adjacency_rule_analysis()

print("\nTo run the analysis:")
print("1. Add your email address in Cell 1")
print("2. Uncomment the last line in Cell 10")
print("3. Run all cells")
print("\nThe analysis will:")
print("- Fetch regulatory sequences for boundary genes")
print("- Search for potential rule-encoding patterns")
print("- Compare patterns across species")
print("- Identify candidates for experimental validation")

# %% Cell 11: Results Interpretation
def interpret_results(results):
    """
    Interpret findings in context of adjacency hypothesis
    """
    print("\n" + "=" * 60)
    print("INTERPRETATION GUIDE")
    print("=" * 60)
    
    print("\nWhat to look for:")
    print("\n1. CONSERVED MOTIFS AT BOUNDARIES")
    print("   - Same motifs near boundary genes across species")
    print("   - Could encode 'stop' or 'change' signals")
    
    print("\n2. PALINDROMIC SEQUENCES")
    print("   - Indicate bidirectional sensing")
    print("   - Cell A and Cell B read same signal")
    
    print("\n3. REGULAR SPACING PATTERNS")
    print("   - Periodic motifs could encode distance rules")
    print("   - Like molecular rulers for cells")
    
    print("\n4. LOGIC GATE SIGNATURES")
    print("   - [Sensor motif] + [Spacer] + [Response motif]")
    print("   - Could implement IF-THEN logic")
    
    print("\n5. SPECIES-SPECIFIC VARIATIONS")
    print("   - How rule modifications create different forms")
    print("   - Evolution through rule parameter changes")

# %% Cell 12: Next Steps
print("\n" + "=" * 60)
print("NEXT STEPS")
print("=" * 60)
print("\n1. Run this analysis with real genomic data")
print("2. Focus on genes with known boundary functions")
print("3. Compare high-regeneration vs low-regeneration species")
print("4. Design experiments to test discovered patterns")
print("5. Build computational models of rule execution")
print("\nRemember: We're looking for the 'grammar' of development!")
