# FNI_001: Architecture Overview

## Project Scope
Design a wearable neural interface that integrates with the Fractality Project. The system should interpret real-time brain signals and modulate the Fractality UI, especially the Bubble Graph and Perception Tuner system.

---

## System Overview

### 1. Signal Acquisition Layer
- EEG headsets (e.g. OpenBCI, Muse, Emotiv)
- Optional: EMG, EDA, heart rate for auxiliary data

### 2. Processing & Transmission Layer
- On-device signal filtering and compression
- Wireless transfer (Bluetooth/WiFi) to receiver

### 3. Interpretation Layer
- Local/remote AI node parses signal into symbolic data
- Protocol: Fractality Brain Interface Protocol (FBIP)

### 4. Integration Layer
- JSON command stream modulates Fractality UI
- Hooks into F.U.D.G.E. for perception node manipulation

---

## Use Case Categories

### Passive Resonance Mapping
- Detect mental/emotional state to highlight node clusters

### Active Thought Tagging
- Spike-detection interpreted as selection, creation, or connection of nodes

### Biofeedback & Looping
- Visual/audio cues reinforce cognitive patterns

---

## Technical Stack Summary

| Layer                | Tech Options                          |
|----------------------|----------------------------------------|
| Hardware             | OpenBCI, Muse, NeuroSky, Emotiv        |
| Signal Processing    | BrainFlow SDK, Python (MNE), JavaScript |
| Data Protocol        | JSON, WebSockets, REST endpoints       |
| Fractality Interface | JavaScript (Bubble UI), Markdown       |

---

## Feasibility Tiers

| Tier | Description                                 | Status     |
|------|---------------------------------------------|------------|
| 1    | Simple EEG → Node interaction (manual map)  | Short-term |
| 2    | Pattern library → Symbolic node creation    | Mid-term   |
| 3    | Closed loop: signal ↔ UI ↔ cognition        | Long-term  |

---

## Roadmap
1. Define FBIP Protocol (FNI_002)
2. Select hardware (FNI_004)
3. Build Node-to-Pattern library (FNI_003)
4. Link to Bubble Graph UI (FNI_007)
