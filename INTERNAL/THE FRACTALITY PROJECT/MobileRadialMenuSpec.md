📱 Fractality Mobile Radial Menu System

Overview

This document defines the Mobile Radial Menu UI system for the Fractality Project. It introduces a thumb-centric, elliptical arc menu optimized for mobile interaction, designed to maximize screen space and symbolic clarity. The menu is modular, mirrored for handedness, and integrates with the existing node layout and navigation engines.


---

🎯 Purpose

To provide an ergonomic, one-handed interface for navigating the Fractality platform on mobile devices. It offers quick access to core modules and visualizes them as interconnected nodes that expand in a symbolic radial pattern.


---

🧠 Core Concepts

1. Menu Node (Root Button)

Location:

Bottom-right for right-handed users

Bottom-left when mirrored (left-handed mode)


Behavior:

On press, expands into a radial/elliptical arc of menu category nodes



2. Reverse Node

Location: Top-left

Function: Toggles handedness (mirrors layout)

Aesthetic: Optional mirrored glyph or "hand-switch" icon


3. Menu Category Nodes

Structure:

Fan out in a partial elliptical arc around the Menu Node

Maximize use of screen area while avoiding UI clutter


Examples:

🌐 Bubble View

🔍 Cone View

🧠 Node Editor

💬 Chat Drawer

⚙️ Settings

📣 Resonance Feed



4. Nested Options (Subnodes)

On pressing a category node, a second arc appears with sub-options.

Subnodes inherit handedness layout and are recursively expandable.



---

⚙️ Technical Implementation

Positioning Logic

Use elliptical arc calculations:

function calculateEllipticalArc(center, count, radiusX, radiusY, angleStart, angleSpan) {
  const points = [];
  const angleStep = angleSpan / (count - 1);
  for (let i = 0; i < count; i++) {
    const angle = angleStart + i * angleStep;
    points.push({
      x: center.x + radiusX * Math.cos(angle),
      y: center.y + radiusY * Math.sin(angle)
    });
  }
  return points;
}

MenuController.js Responsibilities

Tracks handedness state (left/right)

Emits layout instructions to render the nodes

Handles expansion/collapse animations

Integrates with LayoutEngine and UI overlay


Touch Controls

touchstart on root button opens menu

touchend outside of arc closes menu

Taps on category nodes trigger:

Navigation

Submenu expansion



Integration Points

index.html: Mount root menu node and reverse toggle

LayoutEngine.js: Provide positioning math (elliptical + fallback to spiral)

FamilyViewController.js: Optionally provide dynamic subnodes from current context

main.js: Wire up event listeners and controller bootstrapping



---

🧪 Future Enhancements

Gesture-based radial expansion

Context-sensitive categories (based on active focus node)

Energy-aware layout bias (CACE score proximity-based ordering)

Symbolic auto-labeling from archetype metadata



---

🌌 Sample Menu Tree Structure

{
  "menu_root": {
    "position": "bottom-right",
    "categories": [
      {
        "id": "bubble_view",
        "icon": "🌐",
        "label": "Bubble View",
        "subnodes": [
          {"id": "resonance_map", "label": "Resonance"},
          {"id": "gravity_map", "label": "Gravity"}
        ]
      },
      {
        "id": "editor",
        "icon": "🧠",
        "label": "Node Editor",
        "subnodes": [
          {"id": "ai_drawer", "label": "AI Drawer"},
          {"id": "human_form", "label": "Manual Entry"}
        ]
      },
      {
        "id": "resonance_feed",
        "icon": "📣",
        "label": "Resonance Feed",
        "subnodes": [
          {"id": "personal_updates", "label": "Your Stream"},
          {"id": "global_feed", "label": "Global Feed"},
          {"id": "filtered_feed", "label": "By Resonance Tags"}
        ]
      }
    ]
  }
}


---

✅ Next Steps

[ ] Implement MenuController.js

[ ] Render radial layout with LayoutEngine

[ ] Mount menu node in mobile overlay

[ ] Enable dynamic switching of handedness

[ ] Animate elliptical expansion and collapse

[ ] Tie categories to existing Fractality modules



---

This system will unify aesthetic intuition and mobile accessibility, bringing the fractal navigation metaphor to the user's fingertips.

