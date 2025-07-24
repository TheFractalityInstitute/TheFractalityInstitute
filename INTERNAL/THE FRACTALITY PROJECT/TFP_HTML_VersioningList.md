# TFP HTML Versioning List

## Introduction 
The current prototype of the Fractality Project App runs in HTML using three.js and a custom data structuring algorithm.


# Alpha
- [[TFP_Prototype_HTML_V15-3-0]] 
v15.3.0
 * Bug Fix: Corrects the fatal bug from previous versions that resulted in a "black screen" by simplifying and clarifying the layout and visibility logic.
 * New Initial View: The application will now start by displaying only the single, top-level "The Fractiverse" node, perfectly centered.
 * Refined Interaction: Clicking the initial "The Fractiverse" node will now correctly trigger the "dive in" action, revealing its child nodes as designed.
 * Stable Foundation: All logic is built upon the robust "Universal Engine" architecture with no conflicting or redundant instructions.

- [[TFP_Prototype_HTML_V16-0-0]]
v16.0.0
 * New Feature - "Add Node" Logic: Implements the core functionality for the "Add New Node" button. This will involve creating a form (likely using the browser's simple prompt for now) to input a new node's name and to select its parent from a list of existing nodes.
 * New Logic - Automatic Sibling Sizing: As per your design, the radius and color of new nodes will be calculated automatically based on their parent, ensuring visual consistency among siblings and removing the need for manual input.
 * Data Persistence: Newly created nodes will be immediately added to the data structure and saved to localStorage, making user additions persistent between sessions.
 * Code Quality: The automatic sizing logic will be clearly commented to earmark it for future upgrades (e.g., weight-based sizing).
 * Stability: This version will be built on our last stable architecture (v15.2.2), ensuring that all previous bug fixes for interaction and UI rendering are included and verified.


## Forks 
- [[TFP_BubbleUI_GPT_16-0-0 ]]
### v16.0.0 Proposal
- Rebuilt Node Manager as a **scalable hierarchical tree view**
- Only shows root node ("The Fractiverse") and its immediate children by default
- Enables **tap-to-expand** child tiers per node (lazy rendering)
- Converts `fractalityConnections` into a tree structure via efficient mapping
- Optimized for long-term **thousands of tier levels** without DOM or memory issues
- Designed specifically for **mobile usability and thumb-first design**

- [[TFP_BubbleUI_GPT_16-0-1]]
### v16.0.1 Proposal
- Replaced flat node list with **hierarchical tree rendering**
- Implemented `buildTree()` from connections array
- Used recursive `renderTree()` to display nested structure with basic indentation
- Enabled **tap-to-focus** behavior per node
- Preserved all original node data and localStorage behavior


## Beta Version
 
- [[TFP_Prototype_HTML_V9-1]] - Perspective shift
- [[TFP_Prototype_HTML_V9-2]] - The Embodied Universe
- [[TFP_Prototype_HTML_V9-3]] - The Snap Engine 
- [[TFP_Prototype_HTML_V9-4]] - Bedrock Engine 
- [[TFP_Prototype_HTML_V9-5]] - cube test

## Current Version

- [[TFP_Prototype_HTML_V9-0]] - The Geometric Engine. Moved away from physics and to a simple, deterministic geometry based on perspective

## Last Gen
- [[TFP_Prototype_HTML_V8-0]] - The Fractality Engine (Golden)

## Archived Versions
 
 [[TFP_FractiverseBubbleOntology_V1-1]]
- [[TFP_OntologySchema_YAML]]
- [[TFP_FractiverseOntology_YAML_V1-1]]
- [[TFP_FractalityBubbleLayout_JSON_V1-1]]
- [[TFP_UI_ResonanceTrailEngine]]
- [[TFP_Prototype_HTML_V1-0]] - The original by ChatGPT4 
- [[TFP_Prototype_HTML_V2-0]] - Enhancements added and restructured by DeepSeek-R1 
- [[TFP_Prototype_HTML_V2-1]]
- [[TFP_Prototype_HTML_V3-0]] - Gemini 2.5 pro
- [[TFP_Prototype_HTML_V3-5]]
- [[TFP_Test1]]
- [[TFP_Prototype_HTML_V3-6]]
- [[TFP_Prototype_HTML_V3-7]]
- [[TFP_Test2]]
- [[TFP_Prototype_HTML_V3-8]]
- [[TFP_Prototype_HTML_V4-0]] - Added first Perception Tuner UI prototype 
- [[TFP_Prototype_HTML_V4-1]] - Moved HUD location.
- [[TFP_Prototype_HTML_V4-2]]
- [[TFP_Prototype_HTML_V4-3]] - moved tuner ui to bottom of screen
- [[TFP_Prototype_HTML_V5-0]] - Turned fractal nodes from hard coded to array of objects 
- [[TFP_Prototype_HTML_V5-1]] - Added "home" button to reset view
- [[TFP_Prototype_HTML_V5-2]] - added reset to default button and corrected default ontology
- [[TFP_Prototype_HTML_V5-3]] - corrected ontological tiers
- [[TFP_Prototype_HTML_V5-4]] - added "scale" slider and fixed zoom taper off issue
- [[TFP_Prototype_HTML_V5-5]] - fixed zoom taper off issue by changing camera zoom focus to selected node
- [[TFP_Prototype_HTML_V5-6]] - made additional changes to node scale focus
- [[TFP_Prototype_HTML_V5-7]] - added zoom fade effect, and fixed sticky scale focus
- [[TFP_Prototype_HTML_V5-8]] - updated UI shell to include file editing system
- [[TFP_Prototype_HTML_V6-0]] - True Fractal Zoom Engine 
- [[TFP_Prototype_HTML_V6-1]] - 
- [[TFP_Prototype_HTML_V6-2]] - updated v2.0 algorithm
- [[TFP_Prototype_HTML_V6-3]] - smart camera and auto framing
- [[TFP_Prototype_HTML_V6-4]] - The Graph Foundation 
- [[TFP_Prototype_HTML_V7-0]] - The Parallax Engine
- [[TFP_Prototype_HTML_V7-1]] - Fixed selection bug. increased attraction force
- [[TFP_Prototype_HTML_V7-2]] - fixed things
- [[TFP_Prototype_HTML_V7-3]] - The stable universe
- [[TFP_Prototype_HTML_V7-4]] - stable engine
- [[TFP_Prototype_HTML_V7-5]] - The Final Connection 
- [[TFP_Prototype_HTML_V7-6]] - rebalanced forces 
- [[TFP_Prototype_HTML_V7-7]] - The Fractality Perception Engine
- [[TFP_Prototype_HTML_V7-8]] - Engine optimization 
- [[TFP_Prototype_HTML_V7-9]] - The Great Attractor 
- [[TFP_Prototype_HTML_V7-10]] - Rough Fractality Engine


## Failure Branches
- [[TFP_Prototype_HTML_V11-0FAIL]] - Grand Finale
- [[TFP_Prototype_HTML_V11-1FAIL]] - Direct path fix
- [[TFP_Prototype_HTML_V12-0FAIL]] - The Keystone

---

[[FractalityNexus|Back to The Fractality Project Nexus]]
