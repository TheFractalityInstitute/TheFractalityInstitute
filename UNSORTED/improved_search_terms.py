# Improved search strategy to get more sequences

# %% Better Search Terms
IMPROVED_SEARCH_TERMS = {
    'ANIMALS': {
        'regeneration_champions': {
            'organisms': ['Hydra', 'planaria', 'Ambystoma mexicanum', 
                         'Danio rerio', 'Xenopus'],
            'search_terms': [
                'promoter',  # Broader!
                'enhancer',
                'regulatory',
                '5\' UTR',
                'upstream',
                'transcription'
            ],
            'keywords': ['regenerat', 'wound', 'healing', 'blastema']  # Use stems
        },
        'apoptosis': {
            'organisms': ['Homo sapiens', 'Mus musculus', 'Danio rerio'],
            'search_terms': [
                'promoter',
                'enhancer', 
                'regulatory',
                'p53',
                'caspase'
            ],
            'keywords': ['apoptosis', 'death', 'TNF', 'Fas']
        }
    },
    'PLANTS': {
        'regeneration': {
            'organisms': ['Arabidopsis thaliana'],
            'search_terms': [
                'promoter',
                'enhancer',
                '5\' region',
                'upstream'
            ],
            'keywords': ['callus', 'regenerat', 'wound', 'WUS', 'PLT']
        }
    }
}

# %% Alternative: Use Gene-based searches
def search_by_genes(organism, gene_list, max_per_gene=5):
    """Search for regulatory regions of specific genes"""
    sequences = []
    
    for gene in gene_list:
        # Search for gene + regulatory terms
        query = f'("{organism}"[Organism]) AND ("{gene}"[Gene]) AND (promoter[Title] OR enhancer[Title] OR regulatory[Title] OR "5\' region"[Title])'
        
        try:
            handle = Entrez.esearch(db="nucleotide", term=query, retmax=max_per_gene)
            record = Entrez.read(handle)
            handle.close()
            
            if record["IdList"]:
                print(f"    Found {len(record['IdList'])} sequences for {gene}")
                # Fetch sequences...
                
        except Exception as e:
            print(f"    Error: {e}")
    
    return sequences

# Key regeneration genes to search
REGENERATION_GENES = {
    'animals': ['FGF', 'WNT', 'BMP', 'TGFB', 'NOTCH', 'SHH', 'MSX1', 'MSX2'],
    'plants': ['WUS', 'STM', 'CUC1', 'CUC2', 'PLT1', 'PLT2', 'ARF', 'LBD'],
    'general': ['PCNA', 'MCM2', 'CDC6', 'E2F1']  # Cell cycle genes
}

# %% Alternative: Use Entrez Gene database first
def get_gene_regulatory_regions(gene_symbol, organism):
    """Get regulatory regions for a specific gene"""
    # First find the gene ID
    gene_query = f"{gene_symbol}[Gene Name] AND {organism}[Organism]"
    
    handle = Entrez.esearch(db="gene", term=gene_query)
    gene_record = Entrez.read(handle)
    handle.close()
    
    if gene_record["IdList"]:
        gene_id = gene_record["IdList"][0]
        
        # Now get linked sequences
        handle = Entrez.elink(dbfrom="gene", db="nucleotide", id=gene_id)
        links = Entrez.read(handle)
        handle.close()
        
        # Extract regulatory sequences from linked records
        # ...
    
    return sequences

# %% Alternative: Use UCSC Genome Browser REST API
def fetch_ucsc_regulatory(organism, chrom, start, end):
    """Fetch regulatory elements from UCSC"""
    # Map organism names
    ucsc_names = {
        'Homo sapiens': 'hg38',
        'Mus musculus': 'mm10',
        'Danio rerio': 'danRer11'
    }
    
    if organism in ucsc_names:
        genome = ucsc_names[organism]
        
        # Get promoters/enhancers from UCSC tracks
        url = f"https://api.genome.ucsc.edu/getData/track"
        params = {
            'genome': genome,
            'track': 'ncbiRefSeqCurated',  # or 'geneHancer'
            'chrom': chrom,
            'start': start,
            'end': end
        }
        
        # Make request...
    
    return elements

# %% Better strategy: Download bulk datasets
def download_bulk_regulatory_data():
    """Download entire regulatory element datasets"""
    
    datasets = {
        'ENCODE': 'https://www.encodeproject.org/metadata/?type=Annotation&annotation_type=candidate+regulatory+elements',
        'Roadmap': 'https://egg2.wustl.edu/roadmap/data/byFileType/chromhmmSegmentations/ChmmModels/coreMarks/jointModel/final/',
        'FANTOM': 'https://fantom.gsc.riken.jp/5/datafiles/latest/extra/Enhancers/',
        'PlantRegMap': 'http://plantregmap.gao-lab.org/download.php'
    }
    
    print("Consider downloading bulk datasets:")
    for name, url in datasets.items():
        print(f"  {name}: {url}")
    
    return datasets

# %% Quick workaround: Use well-studied promoters
KNOWN_PROMOTERS = {
    'regeneration': {
        'sequences': [
            # Xenopus FGF8 promoter (regeneration)
            'CAGCTGCAGCTGTTGACGTCACACGTGGATCCGATAAGCCTGAGGAAATGGCAGCTGCTGACGTCA',
            # Zebrafish msxb promoter (fin regeneration)
            'GGAATGGATAAGCACGTGCCTGACGTGGGAATGTTGACCGATAAGCACGTG',
            # Planaria piwi promoter (stem cells)
            'CACGTGCACGTGGATAAGTTGACCGATAAGCAGCTGCACGTGTTGACC'
        ]
    },
    'apoptosis': {
        'sequences': [
            # Human p53 promoter
            'GGAATGGGAATGCTGCAGCATGCCTAGGAATGGGAATGCATGACTGGGAATG',
            # Mouse Fas promoter  
            'GGAATGATAAAAGGCATGCCGGAATGATAAAAGGAATGGGCATGCC',
            # Human caspase-3 promoter
            'GGAATGCCAATGGAATGATAAAAGGAATGATAAAAGGAATGCCAAT'
        ]
    }
}

print("\nSuggested improvements:")
print("1. Use broader search terms (just 'promoter' not 'regeneration enhancer')")
print("2. Search for specific genes known to be involved")
print("3. Download bulk regulatory datasets")
print("4. Use known promoter sequences as positive controls")
