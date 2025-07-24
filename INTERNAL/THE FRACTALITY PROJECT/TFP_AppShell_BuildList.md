- [[TFP_AppShell_Build_0-0-1]]
v0.0.1
 * Architectural Goal: To create the initial, stable Application Shell and prove the core rendering pipeline with a scalable technique.
 * Rendering Engine: Implements THREE.InstancedMesh to render all nodes in a single, efficient draw call. This replaces the previous, less performant forEach loop.
 * Data Model: Establishes the minimal, "dumb node" data structure, loading the full ontology but only using core properties (id, radius, color) for this initial render.
 * Functionality: The application will display a static, non-interactive cluster of 100 randomly positioned spheres to stress-test the new rendering engine. OrbitControls will be enabled for camera movement.
 * Primary Metric: The goal is to achieve a stable 60 FPS while rendering a large number of objects, validating the "Performance First" principle of our new architecture.

- [[TFP_AppShell_Build_0-1-0]] - Gemini 2.5 pro. First build of final app shell based on 15.2.2 framework.
v0.1.0
 * Architectural Goal: To refactor our stable prototype (v15.2.2) into the official TFP Application Shell, clearly separating the Data, Intelligence (F.U.D.G.E.), and Visualization layers in the code structure.
 * Bug Fix: This version will incorporate the fixes for the two bugs you identified in v15.2.2: the mobile tap-to-select will be made fully functional, and the Delete buttons in the Node Manager will be correctly implemented and displayed.
 * Functionality: The user experience will be identical to our target for v15.2.2, but the underlying code will be reorganized into a clean, scalable, and modular "skeleton" ready for all future work.
- [[TFP_AppShell_Build_0-2-0]] - 
v0.2.0
 * Architectural Goal: To integrate the interactive FUDGE layout engine and the core user interface with our now-proven high-performance InstancedMesh renderer.
 * Data Integration: Re-introduce the getDefaultData and loadData functions to bring your full ontology into the application.
 * Layout Engine Integration: The deterministic "Family View" layout logic will be used to calculate the positions for the visible nodes.
 * Rendering Integration: The calculated positions will be fed directly into the InstancedMesh buffer, allowing us to display the interactive layout with high performance.
 * Interaction & UI: Re-introduce the handleInteraction logic and the core UI panels (overlay, info, home button) to allow for focus-based navigation.

[[TFP_AppShell_Build_0-2-1]] - minor patch

[[TFP_AppShell_Build_0-2-2]]
v0.2.2
 * Architectural Goal: To fix the initial view logic within the FUDGE to correctly display the root container node.
 * Logic Correction: The calculateLayout function will be modified. When the focused node is the root "The Fractiverse" node (id: 1), it will now return a layout containing only that node at the center of the scene.
 * Interaction: When the user clicks on the newly visible "The Fractiverse" node, the handleInteraction function will then call setFocus again, which will correctly display its children as intended.
 * Expected Result: On load, the user will see a single, centered "The Fractiverse" sphere, matching the behavior of our last stable prototype and providing a proper entry point into the application.








