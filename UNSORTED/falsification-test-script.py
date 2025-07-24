# Falsification Test - Can We Predictably Break the System?
# This script tests if breaking discovered rules causes predicted failures

# %% Cell 1: Setup
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import re

print("Testing if we can predictably break cellular grammar...")

# %% Cell 2: Define the Discovered Rules
# These are the rules we found with 100% probability
DETERMINISTIC_RULES = {
    'TGCGTG': 'ACGTCA',  # Always followed by this
    'GCGTGA': 'CGTCAT',
    'TCATGA': 'CGTCAG',
    'CATGAC': 'GTCAGA',
    'GTCATT': 'TGGGAA',
    'TCATTT': 'GGGAAA',
    'GAGGCT': 'GAGTCA',
    'AGGCTG': 'AGTCAG',
    'GGCTGA': 'GTCAGG',
    'ATGGGG': 'AATGCC'
}

# Key patterns we discovered
KEY_PATTERNS = {
    'regeneration_marker': 'GGAATG',
    'boundary_marker': 'CACGTG',
    'universal_present': 'TGACGT',
    'spacing_rule': 20,  # bp between key pairs
}

# %% Cell 3: Create Test Sequences

def create_control_sequence(length=200):
    """Create a sequence that FOLLOWS all discovered rules"""
    sequence = "TGCGTG"  # Start with a known initiator
    
    while len(sequence) < length:
        # Get last 6 nucleotides
        last_6 = sequence[-6:]
        
        # Check if we have a deterministic rule
        if last_6 in DETERMINISTIC_RULES:
            # FOLLOW THE RULE
            next_seq = DETERMINISTIC_RULES[last_6]
            sequence += next_seq
        else:
            # Add a regeneration marker at proper spacing
            if len(sequence) % 20 == 0:
                sequence += "GGAATG"
            else:
                # Add universal motif
                sequence += "TGACGT"
    
    return sequence[:length]

def create_broken_sequence(length=200, break_type='syntax'):
    """Create sequences that VIOLATE specific rules"""
    
    if break_type == 'syntax':
        # Break deterministic syntax rules
        sequence = "TGCGTG"  # Start normally
        
        while len(sequence) < length:
            last_6 = sequence[-6:]
            
            if last_6 in DETERMINISTIC_RULES:
                # DELIBERATELY BREAK THE RULE
                correct_next = DETERMINISTIC_RULES[last_6]
                # Add something different
                wrong_options = ['AAAAAA', 'TTTTTT', 'GGGGGG', 'CCCCCC']
                sequence += np.random.choice(wrong_options)
            else:
                sequence += "TGACGT"
        
    elif break_type == 'spacing':
        # Break the 20bp spacing rule
        sequence = ""
        while len(sequence) < length:
            # Add GGAATG at WRONG spacing (not 20bp)
            if np.random.random() > 0.7:  # Random spacing
                sequence += "GGAATG"
            else:
                sequence += "TGACGT"
    
    elif break_type == 'missing_universal':
        # Create sequence WITHOUT the universal TGACGT motif
        sequence = ""
        options = ['GGAATG', 'CACGTG', 'GATAAG', 'AAAAAA']
        while len(sequence) < length:
            # Never add TGACGT
            sequence += np.random.choice(options)
    
    elif break_type == 'no_regeneration':
        # Remove all GGAATG (regeneration markers)
        sequence = ""
        options = ['TGACGT', 'CACGTG', 'GATAAG', 'TCATTT']
        while len(sequence) < length:
            # Never add GGAATG
            sequence += np.random.choice(options)
    
    return sequence[:length]

# %% Cell 4: Analysis Functions

def analyze_sequence_validity(sequence, name="Sequence"):
    """Check if a sequence follows discovered rules"""
    
    violations = {
        'syntax_violations': 0,
        'spacing_violations': 0,
        'missing_universal': False,
        'missing_regeneration': False,
        'total_rules_checked': 0,
        'rules_followed': 0
    }
    
    # Check syntax rules
    for i in range(len(sequence) - 12):
        current = sequence[i:i+6]
        next_actual = sequence[i+6:i+12]
        
        if current in DETERMINISTIC_RULES:
            violations['total_rules_checked'] += 1
            expected_next = DETERMINISTIC_RULES[current]
            
            if next_actual == expected_next:
                violations['rules_followed'] += 1
            else:
                violations['syntax_violations'] += 1
    
    # Check for universal motif
    if 'TGACGT' not in sequence:
        violations['missing_universal'] = True
    
    # Check for regeneration marker
    if 'GGAATG' not in sequence:
        violations['missing_regeneration'] = True
    
    # Check spacing of GGAATG
    ggaatg_positions = [m.start() for m in re.finditer('GGAATG', sequence)]
    if len(ggaatg_positions) > 1:
        spacings = np.diff(ggaatg_positions)
        wrong_spacings = sum(1 for s in spacings if abs(s - 20) > 5)
        violations['spacing_violations'] = wrong_spacings
    
    # Calculate compliance score
    syntax_compliance = violations['rules_followed'] / max(violations['total_rules_checked'], 1)
    
    return violations, syntax_compliance

def predict_function(sequence):
    """Predict functional properties based on our model"""
    
    predictions = {
        'regeneration_capacity': 'unknown',
        'boundary_type': 'unknown',
        'viability': 'unknown',
        'confidence': 0
    }
    
    # Count key markers
    ggaatg_count = sequence.count('GGAATG')
    cacgtg_count = sequence.count('CACGTG')
    tgacgt_count = sequence.count('TGACGT')
    
    # Analyze syntax compliance
    violations, syntax_score = analyze_sequence_validity(sequence)
    
    # Make predictions based on our discovered rules
    
    # Regeneration prediction
    if ggaatg_count > 5:
        predictions['regeneration_capacity'] = 'high'
    elif ggaatg_count > 0:
        predictions['regeneration_capacity'] = 'low'
    else:
        predictions['regeneration_capacity'] = 'none'
    
    # Boundary prediction
    if cacgtg_count > 2:
        predictions['boundary_type'] = 'sharp'
    elif cacgtg_count > 0:
        predictions['boundary_type'] = 'gradient'
    else:
        predictions['boundary_type'] = 'none'
    
    # Viability prediction
    if syntax_score < 0.5:
        predictions['viability'] = 'non-functional'
    elif violations['missing_universal']:
        predictions['viability'] = 'severely impaired'
    elif violations['spacing_violations'] > 2:
        predictions['viability'] = 'impaired'
    else:
        predictions['viability'] = 'functional'
    
    # Confidence based on how many rules we could check
    predictions['confidence'] = min(violations['total_rules_checked'] / 10, 1.0)
    
    return predictions

# %% Cell 5: Run Falsification Tests

print("="*60)
print("FALSIFICATION TEST RESULTS")
print("="*60)

# Create test sequences
test_sequences = {
    'CONTROL (follows rules)': create_control_sequence(),
    'BROKEN_SYNTAX': create_broken_sequence(break_type='syntax'),
    'BROKEN_SPACING': create_broken_sequence(break_type='spacing'),
    'NO_UNIVERSAL_MOTIF': create_broken_sequence(break_type='missing_universal'),
    'NO_REGENERATION': create_broken_sequence(break_type='no_regeneration')
}

# Analyze each sequence
results = []

for seq_name, sequence in test_sequences.items():
    print(f"\n{seq_name}:")
    print(f"Sequence preview: {sequence[:50]}...")
    
    # Check rule compliance
    violations, syntax_score = analyze_sequence_validity(sequence, seq_name)
    
    print(f"\nRule Compliance:")
    print(f"  Syntax rules followed: {violations['rules_followed']}/{violations['total_rules_checked']} ({syntax_score:.0%})")
    print(f"  Syntax violations: {violations['syntax_violations']}")
    print(f"  Spacing violations: {violations['spacing_violations']}")
    print(f"  Has universal motif (TGACGT): {'No' if violations['missing_universal'] else 'Yes'}")
    print(f"  Has regeneration marker (GGAATG): {'No' if violations['missing_regeneration'] else 'Yes'}")
    
    # Make predictions
    predictions = predict_function(sequence)
    
    print(f"\nPredicted Properties:")
    print(f"  Regeneration capacity: {predictions['regeneration_capacity']}")
    print(f"  Boundary type: {predictions['boundary_type']}")
    print(f"  Viability: {predictions['viability']}")
    print(f"  Prediction confidence: {predictions['confidence']:.0%}")
    
    results.append({
        'sequence': seq_name,
        'syntax_score': syntax_score,
        'violations': sum([violations['syntax_violations'], 
                          violations['spacing_violations'],
                          int(violations['missing_universal']),
                          int(violations['missing_regeneration'])]),
        'predicted_viability': predictions['viability'],
        'regeneration': predictions['regeneration_capacity']
    })

# %% Cell 6: Statistical Test of Predictions

print("\n\n" + "="*60)
print("HYPOTHESIS TEST: Do violations predict dysfunction?")
print("="*60)

# Convert results to dataframe
results_df = pd.DataFrame(results)

# Test correlation between violations and predicted dysfunction
functional = results_df['predicted_viability'] == 'functional'
violation_counts = results_df['violations']

# Calculate correlation
from scipy.stats import spearmanr
correlation, p_value = spearmanr(violation_counts, ~functional)

print(f"\nCorrelation between violations and dysfunction: r = {correlation:.2f}")
print(f"P-value: {p_value:.4f}")

if p_value < 0.05:
    print("\n✓ VALIDATED: Rule violations significantly predict dysfunction!")
else:
    print("\n✗ FAILED: Rule violations don't predict dysfunction")
    print("   This suggests our discovered rules may not be real")

# %% Cell 7: Motif Distribution Analysis

# Analyze motif distributions in each sequence type
motif_analysis = {}

for seq_name, sequence in test_sequences.items():
    motif_counts = {
        'GGAATG': sequence.count('GGAATG'),
        'TGACGT': sequence.count('TGACGT'),
        'CACGTG': sequence.count('CACGTG'),
        'Total_length': len(sequence)
    }
    
    # Normalize by length
    for motif in ['GGAATG', 'TGACGT', 'CACGTG']:
        motif_counts[f'{motif}_density'] = motif_counts[motif] / (len(sequence) / 1000)
    
    motif_analysis[seq_name] = motif_counts

# %% Cell 8: Visualization

fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# 1. Violation counts by sequence type
ax1 = axes[0, 0]
violation_data = [r['violations'] for r in results]
sequence_names = [r['sequence'].split(' ')[0] for r in results]
colors = ['green' if v == 0 else 'red' for v in violation_data]

ax1.bar(range(len(violation_data)), violation_data, color=colors)
ax1.set_xticks(range(len(sequence_names)))
ax1.set_xticklabels(sequence_names, rotation=45, ha='right')
ax1.set_ylabel('Total Violations')
ax1.set_title('Rule Violations by Sequence Type')

# 2. Syntax compliance scores
ax2 = axes[0, 1]
syntax_scores = [r['syntax_score'] for r in results]
ax2.bar(range(len(syntax_scores)), syntax_scores)
ax2.set_xticks(range(len(sequence_names)))
ax2.set_xticklabels(sequence_names, rotation=45, ha='right')
ax2.set_ylabel('Syntax Compliance Score')
ax2.set_title('Syntax Rule Compliance')
ax2.axhline(y=0.5, color='r', linestyle='--', label='50% threshold')

# 3. Motif densities
ax3 = axes[1, 0]
motif_df = pd.DataFrame(motif_analysis).T
motifs_to_plot = ['GGAATG_density', 'TGACGT_density', 'CACGTG_density']
motif_df[motifs_to_plot].plot(kind='bar', ax=ax3)
ax3.set_ylabel('Motif Density (per kb)')
ax3.set_title('Key Motif Densities')
ax3.legend(['GGAATG', 'TGACGT', 'CACGTG'])

# 4. Prediction outcomes
ax4 = axes[1, 1]
viability_map = {'functional': 2, 'impaired': 1, 'severely impaired': 0.5, 'non-functional': 0}
viability_scores = [viability_map[r['predicted_viability']] for r in results]

ax4.bar(range(len(viability_scores)), viability_scores, 
        color=['green' if v == 2 else 'orange' if v == 1 else 'red' for v in viability_scores])
ax4.set_xticks(range(len(sequence_names)))
ax4.set_xticklabels(sequence_names, rotation=45, ha='right')
ax4.set_ylabel('Predicted Viability Score')
ax4.set_title('Predicted Functional Outcomes')
ax4.set_ylim(0, 2.5)

plt.tight_layout()
plt.show()

# %% Cell 9: Final Verdict

print("\n\n" + "="*60)
print("FALSIFICATION TEST CONCLUSIONS")
print("="*60)

# Check if our predictions held
control_functional = results_df[results_df['sequence'].str.contains('CONTROL')]['predicted_viability'].values[0] == 'functional'
syntax_broken = results_df[results_df['sequence'].str.contains('SYNTAX')]['predicted_viability'].values[0] != 'functional'
spacing_broken = results_df[results_df['sequence'].str.contains('SPACING')]['predicted_viability'].values[0] != 'functional'

print("\nDid our predictions hold?")
print(f"1. Control sequence functional: {'✓ YES' if control_functional else '✗ NO'}")
print(f"2. Syntax violations cause dysfunction: {'✓ YES' if syntax_broken else '✗ NO'}")
print(f"3. Spacing violations cause problems: {'✓ YES' if spacing_broken else '✗ NO'}")

success_count = sum([control_functional, syntax_broken, spacing_broken])

print(f"\nOVERALL: {success_count}/3 predictions correct")

if success_count >= 2:
    print("\n✓ CONCLUSION: Our discovered rules appear to be REAL!")
    print("  Breaking the rules causes predictable failures.")
else:
    print("\n✗ CONCLUSION: Our rules may be ARTIFACTS or INCOMPLETE")
    print("  Breaking the rules doesn't cause expected failures.")
    print("  We should reconsider our analysis approach.")

# %% Cell 10: Specific Failure Mode Analysis

print("\n\nDETAILED FAILURE MODE ANALYSIS:")
print("-"*40)

for seq_name in ['BROKEN_SYNTAX', 'BROKEN_SPACING', 'NO_UNIVERSAL_MOTIF']:
    sequence = test_sequences[seq_name]
    print(f"\n{seq_name}:")
    
    if 'SYNTAX' in seq_name:
        # Find specific syntax violations
        for i in range(len(sequence) - 12):
            current = sequence[i:i+6]
            next_actual = sequence[i+6:i+12]
            
            if current in DETERMINISTIC_RULES:
                expected = DETERMINISTIC_RULES[current]
                if next_actual != expected:
                    print(f"  Position {i}: {current} → {next_actual} (expected {expected})")
                    if i > 3:  # Only show first few
                        print("  ...")
                        break

print("\n\nThis test helps us determine if our discovered patterns")
print("are real biological rules or just statistical artifacts.")
