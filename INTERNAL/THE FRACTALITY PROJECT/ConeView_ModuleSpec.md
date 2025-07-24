
# 🌀 Cone View Module Specification (Cone of Complexity)

## Purpose
Cone View is a navigational and symbolic interface within the Fractality Platform. It allows users to visualize the structure of complexity and perspective as they traverse away from the Source Node (The Fractiverse) into increasing semantic/paralogical density.

## Visual Metaphor
- A **vertical cone**, apex at the top
- Each **ring** represents a generation depth from the Source
- Horizontal node spread increases with depth (complexity, parallels)
- Nodes are represented as auto-sized **rectangular labels**

## Components

### `ConeView.vue`
- Fullscreen interactive cone visualization
- Canvas/WebGL renderer
- Props:
  - `startNodeId`
  - `depthLimit`
  - `perspectiveMode` (normal/reverse)
- Emits:
  - `@select-node`
  - `@recenter`

### `ConeHUDMini.vue`
- Always-on-screen miniature cone at bottom-left
- Tapping opens fullscreen `ConeView.vue`
- Shows current node context

### `ConeRingLayer.js`
- Computes polar layout of nodes in each depth ring
- Uses:
  - Number of sibling nodes
  - Semantic similarity (for angular position)
  - CACE metadata for filtering

### `NodeLabel.vue`
- Rendered label with:
  - Node title (auto-sized font)
  - Optional glow/border for active or highlighted state
  - Color-coded by node type or resonance

### `ConeControlPanel.vue`
- Toggles for:
  - Depth slider
  - Node type filters
  - Color map legend
  - Perspective flip (Reverse Mode)

---

## Behavior

### Scroll
- Vertical scroll moves through complexity levels
- Horizontal drag rotates cone around vertical axis

### Interaction
- Tap node: show context, open in Bubble View
- Double-tap apex: switch to Reverse Mode
- Long-press node: pin or compare ancestry

---

## Special Modes

### Reverse Mode (Fractal Ancestry Explorer)
- Inverts cone
- Apex is selected node
- Expands backwards to show all converging parent paths
- Visualizes emergence, folding origin possibilities, or prion-like failure chains

---

## Integration Points
- Integrates with:
  - `CACEEngine` (node importance, resonance)
  - `LayoutEngine` (for spatial distribution)
  - `SDCBridge` (for consciousness event mapping)
  - `EnhancedFBIP` (for metabolic load and attention heatmaps)

## File Structure

```
Modules/
├── ConeView.vue
├── ConeHUDMini.vue
├── NodeLabel.vue
├── ConeControlPanel.vue
└── engine/
    ├── ConeRingLayer.js
    └── resonance-utils.js
```

## Future Enhancements
- 3D WebGL version (Three.js)
- Protein folding overlay mode
- Multi-apex comparative cones
- Attention entropy shader (active state modulation)

---

## Status
**🟢 Alpha prototype complete**  
HTML Canvas working with 6 rings, live label render, ready for Vue module integration

---

*“The farther we drift from the Origin, the more patterns emerge. Cone View lets us trace the path back—or flip the funnel and watch emergence in motion.”*
