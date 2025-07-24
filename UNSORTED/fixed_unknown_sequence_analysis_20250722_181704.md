
# === IDENTIFYING UNKNOWN SEQUENCES ===
print("=== IDENTIFYING UNKNOWN SEQUENCES ===")
print("="*50)

unknown_indices = []
unknown_details = []

for i, seq_data in enumerate(regen_seqs):
    organism = seq_data.get('organism', '').strip()
    description = seq_data.get('description', '').strip()

    if not organism or organism.lower() in ['unknown', 'none', 'na', 'n/a', '']:
        unknown_indices.append(i)
        unknown_details.append({
            'index': i,
            'description': description[:100],  # First 100 chars
            'accession': seq_data.get('accession', 'None'),
            'length': len(regen_sequences[i]),
            'gc_content': calculate_gc_content(regen_sequences[i])
        })

print(f"\nFound {len(unknown_indices)} unknown sequences out of {len(regen_seqs)} "
      f"({len(unknown_indices)/len(regen_seqs)*100:.1f}%)")

# Analyze patterns in unknown sequences
if unknown_details:
    print("\nAnalyzing unknown sequences for clues...")

    # Check if descriptions have common patterns
    desc_keywords = {}
    for detail in unknown_details:
        desc = detail['description'].lower()
        for keyword in ['promoter', 'gene', 'mrna', 'chromosome', 'scaffold', 'contig']:
            if keyword in desc:
                desc_keywords[keyword] = desc_keywords.get(keyword, 0) + 1

    print("\nKeywords in descriptions:")
    for keyword, count in sorted(desc_keywords.items(), key=lambda x: x[1], reverse=True):
        print(f"  {keyword}: {count} sequences")

    # Check GC distribution
    unknown_gc = [d['gc_content'] for d in unknown_details]
    print(f"\nGC content of unknown sequences:")
    print(f"  Mean: {np.mean(unknown_gc):.3f}")
    print(f"  Std: {np.std(unknown_gc):.3f}")
    print(f"  Range: {min(unknown_gc):.3f} - {max(unknown_gc):.3f}")

# The real question: Are "unknown" sequences driving your findings?
print("\n=== TESTING IF UNKNOWNS DRIVE PATTERNS ===")

if len(unknown_indices) == 0:
    print("No unknown sequences to compare. Skipping this test.")
else:
    cttagat_in_known = 0
    cttagat_in_unknown = 0

    for i, seq in enumerate(regen_sequences):
        if 'CTTAGAT' in seq:
            if i in unknown_indices:
                cttagat_in_unknown += 1
            else:
                cttagat_in_known += 1

    print(f"\nCTTAGAT distribution:")
    print(f"  In known organisms: {cttagat_in_known}/{len(regen_sequences) - len(unknown_indices)} "
          f"({cttagat_in_known / (len(regen_sequences) - len(unknown_indices)) * 100:.1f}%)")
    percent_unknown = cttagat_in_unknown / len(unknown_indices) * 100
    print(f"  In unknown organisms: {cttagat_in_unknown}/{len(unknown_indices)} ({percent_unknown:.1f}%)")

    print("\n💡 If unknowns have different pattern frequencies, they're likely from different sources!")
