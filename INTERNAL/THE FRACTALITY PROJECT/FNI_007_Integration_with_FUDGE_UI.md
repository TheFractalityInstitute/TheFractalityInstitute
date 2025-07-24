# FNI_007: Integration with F.U.D.G.E. UI

## Purpose
Define how neural input streams (via FBIP and local node assistants) are translated into dynamic modifications of the Bubble Graph and Perception Tuner interfaces.

---

## Mapping Schema

| Neural Input          | UI Action                            | Aesthetic Feedback               |
|-----------------------|---------------------------------------|----------------------------------|
| Alpha spike           | Emphasize calm nodes (larger radius) | Soothing glow, fade in          |
| Beta burst            | Create branch node                   | Snap animation + ripple          |
| Theta surge           | Dream divergence trail               | Trail animation + dream hue      |
| Gamma synchronization | Merge overlapping ideas              | Nodes fuse + shimmer             |
| P300 detection        | Confirm suggested link               | Flash pulse + audio ping         |

---

## Visual Parameters Modifiable

- Node radius / font size
- Node hue / saturation / glow
- Link strength / thickness
- Spatial clustering behavior
- Animation dynamics (pulse, ripple, trail)

---

## Integration Layer API

```json
{
  "event": "neural_trigger",
  "action": "expand_node",
  "node_id": "xyz42",
  "style": {
    "glow": true,
    "pulse": "soft",
    "color": "#88f"
  }
}
```

---

## UI States

- **Passive Mode**: Background modulation
- **Interactive Mode**: Symbol-triggered engagement
- **Feedback Mode**: Loop response to resonance alignment

---

## Future Expansion

- Add HUD overlay showing live EEG interpretation
- Symbolic glyphs dynamically appear near active clusters
- Layered resonance trails based on emotion + cognition

