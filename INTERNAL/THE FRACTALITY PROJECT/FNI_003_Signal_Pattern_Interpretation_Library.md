# FNI_003: Signal Pattern Interpretation Library

## Purpose
Establish a modular, extensible library of brainwave signal patterns and their associated interpretations within the Fractality framework. Each pattern corresponds to a symbolic or structural action.

---

## Pattern Table (Core Brainwaves)

| Pattern Name   | Description                             | Cognitive State             | Fractality Action               |
|----------------|-----------------------------------------|-----------------------------|----------------------------------|
| Alpha Peak     | Relaxed, focused attention              | Meditative focus            | Highlight node cluster          |
| Beta Burst     | Active concentration or problem-solving | High cognitive load         | Generate new node               |
| Theta Surge    | Deep ideation, hypnagogia               | Dreamlike, creative         | Divergence trail / mythic tag   |
| Delta Dip      | Drowsy, low-conscious input             | Near-unconscious            | Dim irrelevant clusters         |
| Gamma Sync     | Sudden insight, unification             | Integrative awareness       | Merge overlapping node groups   |
| P300 Response  | Novelty/recognition of meaning          | Interest detection          | Auto-link visible ideas         |

---

## Composite States (Hybrid Patterns)

| Composite State       | Component Signals           | Interpretation               | Fractality Response             |
|-----------------------|-----------------------------|-------------------------------|----------------------------------|
| Focused Creation      | High Alpha + Beta Spikes    | Intentional ideation          | Generate node + highlight trail |
| Integrative Insight   | Gamma + Theta Synchrony     | Deep synthesis, reframing     | Cluster merge + resonance pulse |
| Passive Curiosity     | Mild P300 + Theta           | Ambient intrigue              | Suggest related nodes           |

---

## Emotional Modulation (Future Input Layer)

| BioSignal Type | Emotional State       | Augmented Behavior                  |
|----------------|-----------------------|--------------------------------------|
| EDA            | Arousal / stress      | Warn of over-complex node spread    |
| HRV            | Calm / coherence      | Reinforce coherent node layout      |
| EMG (face)     | Microexpression shift | Color-shift active node frame       |

---

## Pattern Recognition Logic

- Sliding window FFT analysis of EEG input
- Threshold spike detection (standardized per user)
- Pattern recognition via small neural nets or rule-based scoring
- Event → JSON dispatch via FBIP

---

## Custom Extensions

- Define user-specific patterns: “Grazi-Gamma” state → activates mythic overlay
- External sync with voice, touch, gesture cues
- Symbolic imprinting: Associate pattern with fractal glyph or totem

---

## Modular Architecture

- Each pattern = `.json` or `.js` module with:
    - Signal criteria
    - Fractality action callback
    - Optional visual/audio cue

```json
{
  "name": "gamma_sync",
  "criteria": {
    "frequency_range": [30, 100],
    "power_threshold": 0.6
  },
  "mapped_action": "merge_node_cluster",
  "feedback": {
    "visual": "pulse_glow",
    "audio": "bell_sync"
  }
}
```

---

## Future Expansion

- Personalized pattern training via Reinforcement Learning
- Dynamic pattern adaptation over time
- Pattern-to-Mythic-Node conversion system (symbol generator layer)
