# FNI_004: Wearable Hardware Survey

## Purpose
Identify and evaluate the most viable EEG and BCI devices for integration with the Fractality system, based on signal quality, openness, modularity, SDK availability, and compatibility with our protocols.

---

## Evaluation Criteria

| Criteria                | Description                                                      |
|-------------------------|------------------------------------------------------------------|
| Signal Quality          | Channel count, sampling rate, signal-to-noise ratio             |
| SDK/API Availability    | Ease of integration with Python/JS stack                        |
| Wireless Capability     | BLE/WiFi support for real-time transmission                     |
| Modularity              | Ability to customize electrodes or expand sensing range         |
| Community/Support       | Active user base, documentation, forum activity                 |
| Open Source/Firmware    | Openness to modification and protocol layering                  |
| Price/Access            | General accessibility for prototyping and community deployment  |

---

## Device Survey

### 🧠 OpenBCI (Ganglion / Cyton)
- **Signal Quality**: 4–16 channels, 200–1000Hz
- **SDK**: BrainFlow SDK (C/C++, Python, JS)
- **Wireless**: BLE, WiFi (WiFi shield)
- **Modularity**: Highly modular, customizable headsets
- **Open Source**: Full firmware/hardware access
- **Ideal For**: Power users, symbolic interface experiments

---

### 🧠 Muse 2 / Muse S
- **Signal Quality**: 4 channels, dry electrodes, ~256Hz
- **SDK**: Muse Direct, Mind Monitor (some reverse-engineered tools)
- **Wireless**: BLE
- **Modularity**: Limited (fixed headband)
- **Open Source**: Partially closed ecosystem
- **Ideal For**: Meditative-state mapping, casual tracking

---

### 🧠 Emotiv Insight / Epoc X
- **Signal Quality**: 5–14 channels, high SNR
- **SDK**: EmotivPRO SDK (paid tier for full access)
- **Wireless**: BLE/WiFi
- **Modularity**: Fixed design
- **Open Source**: Closed SDK layers
- **Ideal For**: Turnkey integration, commercial UX research

---

### 🧠 NeuroSky MindWave
- **Signal Quality**: 1 channel, basic metrics
- **SDK**: Basic SDK, some JS/Python wrappers
- **Wireless**: BLE
- **Modularity**: None
- **Open Source**: Mostly closed
- **Ideal For**: Entry-level signal testing only

---

## Ranked Recommendations

| Rank | Device           | Reasoning                                            |
|------|------------------|------------------------------------------------------|
| 🥇 1 | OpenBCI Ganglion | Open, robust, modular, ideal for protocol layering  |
| 🥈 2 | Muse S           | Low-profile, great for meditative signal inputs     |
| 🥉 3 | Emotiv Insight   | Clean commercial option, good for rapid iteration   |

---

## Suggested Stack

1. **Short-Term Dev**: Muse S → Fractality Passive Mapping
2. **Mid-Term Prototype**: OpenBCI → Signal-to-Node JSON bridge
3. **Long-Term Platform**: OpenBCI + BioSignals → Symbolic AI Agent

---

## Additional Notes

- All devices should stream data into a Fractality-compatible receiver (Python/Node).
- Protocol wrappers will be added for each device as we develop the Fractality Brain Interface Layer (FBIP).
- Modular upgrade paths: Combine EEG with EMG, EDA, HRV, eye-tracking for future versions.

