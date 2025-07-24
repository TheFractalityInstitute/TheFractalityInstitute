import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import warnings
warnings.filterwarnings('ignore')

# SYSTEMATIC ANALYSIS OF SCALING FACTORS FOR RIEMANN DETECTION IN EEG

# First 50 Riemann zeros
riemann_zeros = [
    14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
    37.586178, 40.918719, 43.327073, 48.005151, 49.773832,
    52.970321, 56.446248, 59.347044, 60.831778, 65.112544,
    67.079811, 69.546402, 72.067158, 75.704691, 77.144840,
    79.337375, 82.910381, 84.735493, 87.425275, 90.864478,
    92.491899, 94.651344, 95.870634, 98.831194, 101.317851,
    103.725538, 105.446623, 107.168611, 111.029536, 111.874659,
    114.320220, 116.226680, 118.790783, 121.370125, 122.946829,
    124.256819, 127.516683, 129.578704, 131.087688, 133.497737,
    134.756510, 138.116042, 139.736209, 141.123707, 143.111846
]

def generate_realistic_eeg_data(duration=120, fs=256):
    """Generate realistic EEG-like data with multiple channels"""
    
    n_samples = duration * fs
    n_channels = 8
    time = np.linspace(0, duration, n_samples)
    
    eeg_data = []
    channel_names = ['Fp1', 'Fp2', 'F3', 'F4', 'C3', 'C4', 'O1', 'O2']
    
    for i in range(n_channels):
        freqs = np.fft.fftfreq(n_samples, 1/fs)
        power = np.zeros_like(freqs)
        power[1:n_samples//2] = 1 / np.sqrt(freqs[1:n_samples//2])
        
        # EEG rhythms
        alpha_power = 3 if channel_names[i].startswith('O') else 1.5
        alpha_band = (np.abs(freqs) > 8) & (np.abs(freqs) < 13)
        power[alpha_band] *= alpha_power
        
        beta_power = 2 if channel_names[i].startswith('F') else 1
        beta_band = (np.abs(freqs) > 13) & (np.abs(freqs) < 30)
        power[beta_band] *= beta_power
        
        theta_band = (np.abs(freqs) > 4) & (np.abs(freqs) < 8)
        power[theta_band] *= 1.2
        
        phases = np.random.uniform(-np.pi, np.pi, len(freqs))
        spectrum = np.sqrt(power) * np.exp(1j * phases)
        channel_signal = np.real(np.fft.ifft(spectrum))
        
        channel_signal = channel_signal * 50 / np.std(channel_signal)
        eeg_data.append(channel_signal)
    
    return np.array(eeg_data), channel_names, fs, time

def analyze_single_channel_riemann(channel_data, fs, scaling_factor):
    """Analyze a single channel for Riemann signatures with given scaling factor"""
    
    # Preprocess
    channel_data = signal.detrend(channel_data)
    sos = signal.butter(4, [0.5, 50], btype='band', fs=fs, output='sos')
    filtered_data = signal.sosfilt(sos, channel_data)
    
    # Compute spectrum
    freqs_welch, psd_welch = signal.welch(filtered_data, fs, nperseg=fs*4)
    
    # Find peaks
    peak_threshold = np.percentile(psd_welch, 90)
    min_distance = max(1, int(0.5*fs/len(freqs_welch)))
    peak_indices, _ = signal.find_peaks(psd_welch, 
                                      height=peak_threshold, 
                                      distance=min_distance)
    detected_peaks = freqs_welch[peak_indices]
    
    # Map Riemann zeros with given scaling factor
    expected_peaks = []
    for zero in riemann_zeros[:40]:
        freq = 0.5 + (zero - 14.134) * scaling_factor
        if 0.5 < freq < 45:
            expected_peaks.append(freq)
    
    # Count matches
    matches = 0
    tolerance = 0.5  # Hz
    
    for expected in expected_peaks:
        if any(abs(detected - expected) < tolerance for detected in detected_peaks):
            matches += 1
    
    detection_score = matches / len(expected_peaks) * 100 if expected_peaks else 0
    
    return detection_score, len(expected_peaks), matches

def test_scaling_factors(eeg_data, channel_names, fs):
    """Test a range of scaling factors"""
    
    print("=== TESTING SCALING FACTORS FOR RIEMANN DETECTION ===\n")
    
    # Range of scaling factors to test
    scaling_factors = np.linspace(0.5, 3.0, 51)  # Test 51 values from 0.5 to 3.0
    
    # Store results for each channel
    results = {name: [] for name in channel_names}
    
    # Test each scaling factor
    for sf in scaling_factors:
        for idx, channel_name in enumerate(channel_names):
            score, n_expected, n_matched = analyze_single_channel_riemann(
                eeg_data[idx], fs, sf
            )
            results[channel_name].append(score)
    
    return scaling_factors, results

def calculate_baseline_range(eeg_data, fs, n_shuffles=10):
    """Calculate baseline detection rates across scaling factors"""
    
    print("Calculating baseline rates...")
    scaling_factors = np.linspace(0.5, 3.0, 11)  # Fewer points for speed
    baseline_scores = []
    
    # Create shuffled data
    original_channel = eeg_data[0]
    fft_data = np.fft.fft(original_channel)
    random_phases = np.random.uniform(-np.pi, np.pi, len(fft_data))
    random_phases[0] = 0
    fft_shuffled = np.abs(fft_data) * np.exp(1j * random_phases)
    shuffled_channel = np.real(np.fft.ifft(fft_shuffled))
    
    # Test each scaling factor on shuffled data
    for sf in scaling_factors:
        scores = []
        for _ in range(n_shuffles):
            score, _, _ = analyze_single_channel_riemann(shuffled_channel, fs, sf)
            scores.append(score)
        baseline_scores.append(np.mean(scores))
    
    # Interpolate to full range
    full_scaling = np.linspace(0.5, 3.0, 51)
    baseline_interpolated = np.interp(full_scaling, scaling_factors, baseline_scores)
    
    return baseline_interpolated

# MAIN ANALYSIS
print("Generating EEG data...")
eeg_data, channel_names, fs, time = generate_realistic_eeg_data()

print("Testing scaling factors across all channels...")
scaling_factors, results = test_scaling_factors(eeg_data, channel_names, fs)

print("Calculating statistical baseline...")
baseline = calculate_baseline_range(eeg_data, fs)

# VISUALIZATION 1: All channels across scaling factors
plt.figure(figsize=(14, 8))

# Plot detection scores for each channel
for channel_name, scores in results.items():
    plt.plot(scaling_factors, scores, label=channel_name, linewidth=2)

# Add baseline
plt.plot(scaling_factors, baseline, 'k--', linewidth=2, alpha=0.7, label='Baseline')
plt.fill_between(scaling_factors, baseline - 5, baseline + 5, 
                 alpha=0.2, color='gray', label='Baseline ± 5%')

plt.xlabel('Scaling Factor', fontsize=12)
plt.ylabel('Riemann Detection Score (%)', fontsize=12)
plt.title('Riemann Signature Detection vs. Scaling Factor for All EEG Channels', fontsize=14)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True, alpha=0.3)
plt.xlim(0.5, 3.0)
plt.ylim(0, 50)

# Add vertical line at the "magic" value of 1.2
plt.axvline(x=1.2, color='red', linestyle=':', alpha=0.7, label='Original finding (1.2)')

plt.tight_layout()
plt.show()

# VISUALIZATION 2: Focus on C3 and O1 (the significant channels)
plt.figure(figsize=(12, 6))

# Subplot 1: C3
plt.subplot(1, 2, 1)
c3_scores = results['C3']
plt.plot(scaling_factors, c3_scores, 'b-', linewidth=3, label='C3 Detection')
plt.plot(scaling_factors, baseline, 'k--', linewidth=2, alpha=0.7, label='Baseline')
plt.fill_between(scaling_factors, baseline - 5, baseline + 5, 
                 alpha=0.2, color='gray')
plt.axhline(y=30, color='green', linestyle='--', alpha=0.5, label='30% threshold')
plt.axvline(x=1.2, color='red', linestyle=':', alpha=0.7)
plt.xlabel('Scaling Factor')
plt.ylabel('Detection Score (%)')
plt.title('Channel C3: Scaling Factor Analysis')
plt.legend()
plt.grid(True, alpha=0.3)
plt.xlim(0.5, 3.0)
plt.ylim(0, 40)

# Subplot 2: O1
plt.subplot(1, 2, 2)
o1_scores = results['O1']
plt.plot(scaling_factors, o1_scores, 'g-', linewidth=3, label='O1 Detection')
plt.plot(scaling_factors, baseline, 'k--', linewidth=2, alpha=0.7, label='Baseline')
plt.fill_between(scaling_factors, baseline - 5, baseline + 5, 
                 alpha=0.2, color='gray')
plt.axhline(y=26.5, color='green', linestyle='--', alpha=0.5, label='26.5% threshold')
plt.axvline(x=1.2, color='red', linestyle=':', alpha=0.7)
plt.xlabel('Scaling Factor')
plt.ylabel('Detection Score (%)')
plt.title('Channel O1: Scaling Factor Analysis')
plt.legend()
plt.grid(True, alpha=0.3)
plt.xlim(0.5, 3.0)
plt.ylim(0, 40)

plt.tight_layout()
plt.show()

# ANALYSIS: Find optimal scaling factors
print("\n=== OPTIMAL SCALING FACTORS ===")
for channel_name, scores in results.items():
    max_score = max(scores)
    optimal_sf = scaling_factors[scores.index(max_score)]
    
    # Check if significantly above baseline at optimal point
    baseline_at_optimal = baseline[scores.index(max_score)]
    is_significant = max_score > baseline_at_optimal + 10  # Rough significance
    
    print(f"{channel_name}: Peak at SF={optimal_sf:.2f} with {max_score:.1f}% detection", 
          end="")
    if is_significant:
        print(" [SIGNIFICANT]")
    else:
        print()

# Find ranges where detection is significant
print("\n=== SIGNIFICANT DETECTION RANGES ===")
for channel in ['C3', 'O1']:  # Focus on the interesting channels
    scores = results[channel]
    significant_ranges = []
    in_range = False
    start = None
    
    for i, (sf, score) in enumerate(zip(scaling_factors, scores)):
        if score > baseline[i] + 10 and not in_range:
            start = sf
            in_range = True
        elif score <= baseline[i] + 10 and in_range:
            significant_ranges.append((start, scaling_factors[i-1]))
            in_range = False
    
    if in_range:  # Handle case where significance extends to end
        significant_ranges.append((start, scaling_factors[-1]))
    
    print(f"{channel}: Significant detection in ranges {significant_ranges}")

# Create heatmap showing all channels and scaling factors
plt.figure(figsize=(12, 6))
detection_matrix = np.array([results[ch] for ch in channel_names])

plt.imshow(detection_matrix, aspect='auto', cmap='hot', interpolation='bilinear')
plt.colorbar(label='Detection Score (%)')
plt.yticks(range(len(channel_names)), channel_names)
plt.xlabel('Scaling Factor Index')
plt.ylabel('EEG Channel')
plt.title('Riemann Detection Heatmap: Channels vs Scaling Factors')

# Add markers for significant regions
for i, channel in enumerate(channel_names):
    scores = results[channel]
    for j, score in enumerate(scores):
        if score > baseline[j] + 10:
            plt.plot(j, i, 'w*', markersize=3)

# Add vertical line at scaling factor 1.2
sf_12_index = np.argmin(np.abs(scaling_factors - 1.2))
plt.axvline(x=sf_12_index, color='cyan', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()