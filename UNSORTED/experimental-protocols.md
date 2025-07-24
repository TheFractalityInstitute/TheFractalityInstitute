# FI-EXP-002: Detailed Experimental Protocols for Consciousness Research
## Rigorous Methods for Professional and Citizen Scientists
**Document ID:** FI-EXP-002  
**Canon:** I - Empirical  
**Date:** December 19, 2024  
**Status:** Active Protocols  
**Version:** 2.0

═══════════════════════════════════════════════════════════════
CANON DECLARATION - EMPIRICAL CANON (I)
Document ID: FI-EXP-002
Canon: I - Empirical
Epistemological Status: Experimental Methodology
Evidence Level: ☑ Based on established methods ☑ Novel applications
Peer Review Status: ☑ Internal ☐ External ☐ Published

These protocols provide step-by-step procedures for consciousness
research experiments. All methods are designed to be rigorous yet
accessible, with clear options for different equipment levels.
Pre-registration required before data collection.
═══════════════════════════════════════════════════════════════

## 1.0 Overview and General Principles

### 1.1 Protocol Standards

Every protocol must include:
- Clear hypothesis with falsification criteria
- Power analysis and sample size
- Randomization procedures  
- Blinding methods
- Control conditions
- Statistical analysis plan
- Equipment alternatives
- Safety considerations

### 1.2 Equipment Tiers

**Tier A**: Professional lab equipment
**Tier B**: Prosumer devices (OpenBCI, etc.)
**Tier C**: Consumer devices (Muse, etc.)
**Tier D**: No equipment needed

Each protocol specifies minimum tier required.

## 2.0 Protocol Suite A: Frequency Pattern Detection

### 2.1 Protocol A1: Riemann Zero Detection in Resting EEG

**Hypothesis**: Human EEG contains frequency patterns correlating with Riemann zeta zero distribution beyond chance.

**Equipment**: Tier B minimum (32+ channels preferred)

**Participants**: N=150 per group (based on power analysis for d=0.3)

**Procedure**:

```markdown
SETUP PHASE (30 minutes):
1. Environmental preparation
   □ Quiet room, ambient temp 20-22°C
   □ Dim lighting (10-50 lux)
   □ Faraday cage or minimize EM interference
   □ Comfortable chair, feet flat

2. Participant preparation
   □ Informed consent review
   □ Remove jewelry/electronics
   □ Hair preparation (part for electrodes)
   □ Impedance check (<5kΩ all channels)

3. Baseline measurements
   □ 5-min eyes open (fixation cross)
   □ 5-min eyes closed
   □ Heart rate and breathing rate
   □ Subjective state questionnaire

DATA COLLECTION (45 minutes):
1. Resting state recording
   □ 20-min eyes closed
   □ "Rest but stay awake"
   □ Movement markers logged
   □ Break at 10 min (stay connected)

2. Control conditions
   □ 10-min guided counting (1-10 repeat)
   □ 10-min music listening (standard track)
   □ 5-min recovery baseline

3. Quality checks every 5 minutes
   □ Impedance still <5kΩ
   □ No excessive artifacts
   □ Participant awake
   □ Recording integrity

ANALYSIS PIPELINE:
1. Preprocessing
   - Bandpass filter: 0.5-45 Hz
   - Notch filter at line frequency
   - ICA artifact removal
   - Epoch rejection (±75μV)

2. Frequency analysis
   - Welch's method (4s windows, 50% overlap)
   - Extract peak frequencies
   - Calculate inter-peak intervals
   - Scale to match Riemann distribution

3. Statistical testing
   - Correlation with Riemann spacings
   - Permutation test (10,000 iterations)
   - Multiple comparison correction
   - Effect size calculation
```

**Control Analyses**:
- Test against Fibonacci sequence
- Test against random distributions
- Phase-scrambled surrogate data
- Different scaling factors

**Safety**: Standard EEG safety protocols

### 2.2 Protocol A2: Meditation-Induced Frequency Shifts

**Hypothesis**: Advanced meditators show stronger Riemann correlations than controls.

**Equipment**: Tier B minimum

**Participants**: 
- 50 meditators (>5 years, >1hr/day)
- 50 matched controls
- 50 musicians (rhythm control)

**Procedure Modifications**:
```markdown
MEDITATION PHASE (30 minutes):
1. Baseline (10 min)
   - Standard resting state
   - Breath awareness

2. Deep meditation (20 min)
   - Practitioner's primary technique
   - Bell at 10 min (gentle reminder)
   - No specific instructions

3. Post-meditation (10 min)
   - Gradual return
   - Maintained recording
   - State assessment
```

**Additional Measurements**:
- Heart rate variability
- Respiratory rate
- Subjective depth scale
- Previous session comparison

## 3.0 Protocol Suite B: Coherence and Synchrony

### 3.1 Protocol B1: Inter-Brain Synchrony During Connection

**Hypothesis**: Dyads in rapport show increased inter-brain coherence.

**Equipment**: Tier B minimum (synchronized recording)

**Participants**: 30 dyads (friends/partners/strangers)

**Setup**:
```markdown
DUAL RECORDING SETUP:
1. Hardware synchronization
   □ Common trigger source
   □ <1ms timing precision
   □ Drift monitoring
   □ Backup sync markers

2. Spatial arrangement
   □ 1.5m apart, facing
   □ Eye contact possible
   □ No physical contact
   □ Matched environments

3. Baseline isolation (10 min)
   □ Visual barrier
   □ No communication
   □ Independent tasks
   □ Separate recordings
```

**Experimental Conditions**:
```markdown
1. SILENT CONNECTION (10 min)
   - Eye contact maintained
   - No speaking/gestures
   - "Feel connected"
   - Natural blinking OK

2. SYNCHRONIZED BREATHING (10 min)
   - Follow LED pacer
   - 6 breaths/minute
   - Eye contact optional
   - Comfort prioritized

3. SHARED MEDITATION (10 min)
   - Loving-kindness focus
   - Include partner
   - Eyes closed OK
   - Natural rhythm

4. CONVERSATION (10 min)
   - Meaningful topic
   - Take turns speaking
   - Natural interaction
   - Stay connected
```

**Analysis**:
```python
def calculate_inter_brain_synchrony(eeg1, eeg2):
    """
    Phase locking value between brains
    """
    # Hilbert transform for phase
    phase1 = np.angle(hilbert(eeg1))
    phase2 = np.angle(hilbert(eeg2))
    
    # Phase locking value
    plv = np.abs(np.mean(np.exp(1j*(phase1-phase2))))
    
    # Statistical significance
    surrogate_plvs = []
    for i in range(1000):
        shuffled = np.random.permutation(phase2)
        surr_plv = np.abs(np.mean(np.exp(1j*(phase1-shuffled))))
        surrogate_plvs.append(surr_plv)
    
    p_value = sum(surrogate_plvs > plv) / 1000
    return plv, p_value
```

### 3.2 Protocol B2: Group Coherence During Collective Practices

**Hypothesis**: Groups in synchronized activities show emergent coherence patterns.

**Equipment**: Tier C acceptable (portable for groups)

**Participants**: Groups of 8-12

**Activities**:
```markdown
1. DRUMMING CIRCLE (20 min)
   - Simple rhythm taught
   - Gradual synchronization
   - Leader optional
   - Volume comfortable

2. GROUP MEDITATION (20 min)
   - Guided initially
   - Silent middle section
   - Synchronized breathing
   - Bells for timing

3. MOVEMENT PRACTICE (20 min)
   - Tai chi or qigong
   - Mirror neurons engaged
   - Slow, synchronized
   - Standing or seated

4. CHANTING (20 min)
   - Simple vowel sounds
   - Natural harmonics
   - Volume comfortable
   - Breaks as needed
```

## 4.0 Protocol Suite C: Altered States

### 4.1 Protocol C1: Flow State Induction and Measurement

**Hypothesis**: Flow states show distinct neural signatures including gamma/theta coupling.

**Equipment**: Tier B minimum

**Participants**: 40 experts in flow-inducing activities

**Flow Induction Methods**:
```markdown
1. VIDEO GAME FLOW (Tetris paradigm)
   Setup:
   - Adaptive difficulty algorithm
   - Starts 20% below skill
   - Increases with performance
   - Decreases with errors
   
   Measurements:
   - Game performance metrics
   - Self-reported flow (every 5 min)
   - Continuous EEG
   - Eye tracking (optional)

2. MUSICAL FLOW (improvisation)
   Setup:
   - Backing track provided
   - Familiar key/tempo
   - Record audio output
   - Minimize movement artifacts
   
   Measurements:
   - Musical complexity analysis
   - Self-reported flow
   - EEG (wireless preferred)
   - Motion capture (optional)

3. MATHEMATICAL FLOW (problem solving)
   Setup:
   - Adaptive problem sets
   - Multiple solution paths
   - Time pressure optional
   - Instant feedback
   
   Measurements:
   - Solution accuracy/speed
   - Strategy analysis
   - Think-aloud protocol
   - Continuous EEG
```

**Neural Markers**:
```python
def identify_flow_state(eeg_data):
    """
    Multi-feature flow detection
    """
    features = {
        'theta_power': bandpower(eeg_data, 4, 8),
        'alpha_power': bandpower(eeg_data, 8, 13),
        'gamma_power': bandpower(eeg_data, 30, 45),
        'theta_gamma_coupling': phase_amplitude_coupling(
            eeg_data, (4,8), (30,45)
        ),
        'complexity': lempel_ziv_complexity(eeg_data),
        'long_range_correlation': dfa(eeg_data)
    }
    
    # Machine learning classifier
    flow_probability = flow_classifier.predict_proba(features)
    return flow_probability
```

### 4.2 Protocol C2: Sleep State Consciousness

**Hypothesis**: Lucid REM shows increased gamma in frontal regions vs normal REM.

**Equipment**: Tier A required (PSG)

**Participants**: 20 frequent lucid dreamers

**Procedure**:
```markdown
SLEEP LAB PROTOCOL:
Night 1: Adaptation
- Full PSG hookup
- Sleep as normal
- No interventions
- Baseline data

Night 2: Lucid induction
- Reality check training
- Wake-back-to-bed at REM
- Mnemonic induction
- Signal protocol

LUCIDITY SIGNALS:
- Pre-agreed eye movements (LRLR)
- Verified in REM sleep
- Time-stamped precisely
- Post-hoc validation

MEASUREMENTS:
- Standard PSG montage
- High-density EEG (64ch)
- Dream reports
- Lucidity questionnaire
```

## 5.0 Protocol Suite D: Citizen-Accessible Studies

### 5.1 Protocol D1: Smartphone-Based Attention Rhythms

**Hypothesis**: Attention fluctuates at predictable frequencies detectable via reaction time.

**Equipment**: Tier D (smartphone only)

**Participants**: Target 10,000 globally

**App-Based Protocol**:
```markdown
DAILY SESSIONS (5 min):
1. Calibration (30 sec)
   - Device flat on table
   - Dominant thumb ready
   - Practice trials
   - Baseline reaction time

2. Continuous performance (4 min)
   - Random dot appears
   - Tap immediately
   - 100-2000ms intervals
   - Error feedback

3. State assessment (30 sec)
   - Alertness (1-10)
   - Mood (1-10)
   - Time of day
   - Caffeine/substances

DATA UPLOADED:
- Reaction times (ms precision)
- Tap pressure (if available)
- Accelerometer data
- Anonymous ID only
```

**Analysis Pipeline**:
```python
def analyze_attention_rhythms(reaction_times):
    """
    Extract periodic components in attention
    """
    # Interpolate to regular sampling
    regular_rt = interpolate_regular(reaction_times, fs=10)
    
    # Spectral analysis
    freqs, powers = welch(regular_rt, fs=10, nperseg=60)
    
    # Find peaks
    peaks = find_peaks(powers, prominence=2*np.std(powers))
    
    # Test against known rhythms
    known_rhythms = [0.05, 0.1, 0.25, 1.0]  # Hz
    matches = test_rhythm_match(freqs[peaks], known_rhythms)
    
    return {
        'peak_freqs': freqs[peaks],
        'rhythm_matches': matches,
        'quality_score': calculate_quality(reaction_times)
    }
```

### 5.2 Protocol D2: Mass Meditation Coherence

**Hypothesis**: Synchronized global meditation creates detectable field effects.

**Equipment**: Tier D (smartphone magnetometer)

**Participants**: Target 1000+ per event

**Event Protocol**:
```markdown
PRE-EVENT (24 hours):
- Register location (timezone)
- Download guided audio
- Test magnetometer
- Set reminder

SYNCHRONIZED SESSION (30 min):
UTC timing for global sync

0-5 min: Settling
- Find quiet space
- Phone on flat surface
- Start recording
- Begin audio guide

5-25 min: Core meditation
- Loving-kindness focus
- Global connection intent
- Breath synchronization
- Maintain stillness

25-30 min: Integration
- Slow return
- Final measurements
- Subjective report
- Upload data

DATA COLLECTED:
- 3-axis magnetometer (50Hz)
- GPS location (anonymized to city)
- Timestamp (UTC precise)
- Movement detection
- Subjective ratings
```

## 6.0 Safety Protocols

### 6.1 General Safety

**All Experiments**:
- IRB approval required
- Informed consent mandatory
- Right to withdraw anytime
- Data anonymization default
- Adverse event reporting

### 6.2 Specific Precautions

**EEG Studies**:
- Skin prep allergies check
- Seizure history screening
- Infection control protocols
- Electrical safety standards

**Altered States**:
- Mental health screening
- Integration support ready
- Clinical referrals available
- Substance interaction check

**Group Studies**:
- COVID protocols current
- Personal space respected
- Opt-out without stigma
- Cultural sensitivity

## 7.0 Data Management

### 7.1 Collection Standards

```yaml
File Naming:
  format: "STUDY_PARTICIPANT_DATE_SESSION"
  example: "RMN_P001_20240315_S1"

Data Format:
  raw: European Data Format (EDF)
  processed: HDF5 with metadata
  behavioral: CSV with headers
  surveys: JSON structured

Metadata Required:
  - Equipment model/settings
  - Environmental conditions
  - Participant state
  - Protocol deviations
  - Quality indicators
```

### 7.2 Quality Assurance

**Automatic Checks**:
- Signal quality metrics
- Artifact percentage
- Protocol compliance
- Timing precision
- Missing data flags

**Manual Review**:
- 10% random audit
- All flagged sessions
- First session per participant
- Equipment changes
- Unusual patterns

## 8.0 Statistical Standards

### 8.1 Pre-Registration Template

```markdown
Study: [Name]
Hypotheses: [Specific, directional]
Sample Size: [N, power analysis]
Analysis Plan:
  - Primary outcome: [Measure, test]
  - Secondary outcomes: [Listed]
  - Covariates: [Age, experience, etc.]
  - Missing data: [Handling plan]
  - Multiple comparisons: [Correction]
Stopping Rules: [Criteria]
Blinding: [Who, how]
```

### 8.2 Reporting Requirements

**Always Include**:
- Effect sizes with CI
- Exact p-values
- Power achieved
- Deviations from protocol
- All analyses attempted

## 9.0 Replication Facilitation

### 9.1 Materials Sharing

**Repository Contains**:
- Complete protocols
- Analysis scripts
- Stimulus files
- Equipment settings
- Training materials

### 9.2 Direct Support

- Video tutorials
- Q&A forums
- Monthly office hours
- Troubleshooting guide
- Collaboration matching

## 10.0 Innovation Encouraged

### 10.1 Protocol Modifications

Researchers may propose modifications if:
- Scientific rationale provided
- Safety maintained
- Core hypothesis preserved
- Changes pre-registered
- Results comparable

### 10.2 New Protocol Development

Community can submit new protocols:
1. Draft using template
2. Peer review (3 reviewers)
3. Pilot testing required
4. Ethics approval
5. Integration into suite

---

## Protocol Commitment

*"We commit to conducting consciousness research with the highest methodological standards while maintaining accessibility. These protocols balance rigor with practicality, enabling both professional scientists and citizen researchers to contribute meaningful data to our understanding of consciousness."*

---

**Access Protocols**: protocols.fractality.institute
**Submit New Protocol**: protocols.fractality.institute/submit
**Training Videos**: protocols.fractality.institute/training
**Support**: protocols@fractality.institute

*"In consciousness research, the method IS the message. Rigorous, open protocols ensure our findings reflect reality, not our wishes."*