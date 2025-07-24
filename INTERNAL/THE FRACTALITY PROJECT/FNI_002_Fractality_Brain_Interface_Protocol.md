# FNI_002: Fractality Brain Interface Protocol (FBIP)

## Purpose
Define the translation layer between raw or processed brain signals and the symbolic, actionable instructions that modulate the Fractality system.

---

## Core Structure

### Protocol Format (JSON)

```json
{
  "type": "neural_event",
  "signal": "alpha_peak",
  "intensity": 0.73,
  "duration_ms": 320,
  "timestamp": "2025-06-21T18:45:00Z",
  "mapped_action": {
    "action_type": "highlight_cluster",
    "target_node_id": "node_4839",
    "strength": 0.73
  }
}
```

---

## Event Types

| Signal Type    | Description                             | Sample Mapping                      |
|----------------|-----------------------------------------|-------------------------------------|
| alpha_peak     | Calm, focused awareness                 | Highlight nearby conceptual cluster |
| beta_burst     | High activity, cognition spike          | Generate new node                   |
| theta_surge    | Imaginative / subconscious activation   | Trail divergence / dream node spawn |
| p300_response  | Recognition / interest detection        | Auto-link similar nodes             |
| gamma_sync     | Integration, insight                    | Merge overlapping ideas             |

---

## Action Types (for Fractality)

| Action Type         | Description                                |
|---------------------|--------------------------------------------|
| highlight_cluster   | Emphasize node group visually              |
| generate_node       | Create node with optional label/tag        |
| link_nodes          | Create link between two active nodes       |
| expand_node         | Auto-expand nested node cluster            |
| pulse_feedback      | Trigger haptic/audio/visual cue loop       |

---

## Signal-to-Action Mapping Logic

### Passive
- Signal fluctuations are interpreted in the background.
- Clusters subtly brighten/dim based on emotional alignment.

### Active
- Conscious intent detected through brainwave spikes.
- Explicit UI changes: node creation, trail generation, linking.

---

## Integration Notes

- **Language-Agnostic**: Delivered via JSON over WebSocket or local pipe.
- **Modular**: Each signal handler is a plug-in.
- **Live Mode**: Stream continuous updates into Fractality UI engine.
- **Offline Mode**: Buffer + apply when user reconnects or reviews.

---

## Future Expansion

- Add support for multi-modal input: voice + EEG fusion.
- Incorporate AI prediction models for high-level intention mapping.
- Add consent layer for symbolic gesture approval.

---

## Sample Combined Flow

1. Alpha rhythm increases → `highlight_cluster`
2. Beta burst detected → `generate_node`
3. P300 signals interest in visible idea → `link_nodes`
4. Visual feedback loop initiated → `pulse_feedback`
