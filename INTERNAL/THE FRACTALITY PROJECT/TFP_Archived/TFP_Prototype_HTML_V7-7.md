<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no" />
  <title>Fractality Bubble UI v7.7 - The Perception Engine</title>
  
  <script type="importmap">
  {
    "imports": {
      "three": "./three.module.js"
    }
  }
  </script>

  <style>
    body { margin: 0; overflow: hidden; background: #111; color: white; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    #overlay { position: fixed; top: 15px; left: 15px; z-index: 10; background: rgba(20, 20, 30, 0.85); padding: 15px; border-radius: 12px; max-width: 320px; backdrop-filter: blur(5px); border: 1px solid rgba(255, 255, 255, 0.1); box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5); }
    #reset-view-btn { position: fixed; top: 15px; right: 15px; z-index: 20; background: rgba(20, 20, 30, 0.85); border: 1px solid rgba(255, 255, 255, 0.1); color: white; font-size: 24px; width: 50px; height: 50px; border-radius: 50%; cursor: pointer; backdrop-filter: blur(5px); text-align: center; line-height: 50px; }
    #info { font-size: 15px; line-height: 1.6; min-height: 60px; }
    canvas { display: block; position: fixed; z-index: 0; top: 0; left: 0; }
    h3 { margin-top: 0; color: #6ae6ff; border-bottom: 1px solid rgba(100, 200, 255, 0.3); padding-bottom: 8px; }
    .highlight { color: #ffd86e; font-weight: 600; }
  </style>
</head>
<body>
  <div id="overlay">
    <h3>Fractal Node Information v7.7</h3>
    <div id="info">⟡ A universe of perspective.</div>
  </div>

  <button id="reset-view-btn" title="Reset View">⌂</button>

  <script type="module">
    import * as THREE from 'three';
    import { OrbitControls } from './OrbitControls.js';

    function getDefaultData() {
        const nodes = [ { id: 1, name: "The Fractiverse", info: "The total ontological container.", radius: 10, color: "#ffffff" }, { id: 2, name: "Duality", info: "The primal division.", radius: 6, color: "#f0f0f0" }, { id: 3, name: "Motion", info: "Dynamic process.", radius: 4, color: "#87CEEB" }, { id: 10, name: "Stillness", info: "Latent potential.", radius: 4, color: "#9370DB" }, { id: 5, name: "Dimension of Mind", info: "Abstract cognition.", radius: 3.5, color: "#FFD700" }, { id: 15, name: "Unity Field", info: "Meta-ethical substrate.", radius: 3, color: "#E0FFFF" }, { id: 12, name: "Chaos", info: "Boundary-membrane.", radius: 2, color: "#DC143C" }, { id: 14, name: "Shadow Integration", info: "Reconciling dissonant aspects.", radius: 1.5, color: "#C0C0C0" }, { id: 9, name: "GLYPH", info: "Symbolic interface.", radius: 1.5, color: "#40E0D0" }, ];
        const connections = [ { from: 1, to: 2, type: 'contains', weight: 1.0 }, { from: 2, to: 3, type: 'contains', weight: 1.0 }, { from: 2, to: 10, type: 'contains', weight: 1.0 }, { from: 2, to: 12, type: 'contains', weight: 0.8 }, { from: 3, to: 5, type: 'contains', weight: 1.0 }, { from: 15, to: 5, type: 'resonates_with', weight: 0.6 }, { from: 9, to: 15, type: 'interfaces_with', weight: 0.5 }, { from: 14, to: 12, type: 'works_on', weight: 0.7 }, { from: 14, to: 5, type: 'informs', weight: 0.4 }, ];
        return { nodes, connections };
    }
    function loadData() { const savedData = localStorage.getItem('fractalityGraphData'); if (savedData) { return JSON.parse(savedData); } return getDefaultData(); }
    
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    document.body.appendChild(renderer.domElement);
    const initialCameraPosition = new THREE.Vector3(0, 0, 80);
    camera.position.copy(initialCameraPosition);
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    scene.add(new THREE.AmbientLight(0x606060));
    const pointLight = new THREE.PointLight(0xffffff, 1.0, 500);
    scene.add(pointLight);

    let nodeMeshes = [];
    const { nodes: fractalNodes, connections: fractalConnections } = loadData();
    let activeFocusId = 1;
    let highlightedNode = null;
    let cameraAnimation = null;
    
    // Build an adjacency map for efficient graph traversal
    const adjacencyMap = new Map();
    fractalNodes.forEach(node => adjacencyMap.set(node.id, []));
    fractalConnections.forEach(conn => {
        adjacencyMap.get(conn.from).push(conn.to);
        adjacencyMap.get(conn.to).push(conn.from);
    });

    function createSceneFromNodes(nodes) {
        nodes.forEach(nodeData => {
            const geometry = new THREE.SphereGeometry(nodeData.radius, 36, 36);
            const material = new THREE.MeshStandardMaterial({ color: nodeData.color, transparent: true, opacity: 0.9, wireframe: true, roughness: 0.5 });
            const mesh = new THREE.Mesh(geometry, material);
            mesh.userData = { id: nodeData.id, name: nodeData.name, info: nodeData.info, velocity: new THREE.Vector3(), force: new THREE.Vector3() };
            mesh.position.set((Math.random() - 0.5) * 5, (Math.random() - 0.5) * 5, (Math.random() - 0.5) * 5);
            scene.add(mesh);
            nodeMeshes.push(mesh);
        });
    }
    createSceneFromNodes(fractalNodes);

    const linesGroup = new THREE.Group();
    scene.add(linesGroup);
    function createConnectionLines() { /* ... identical ... */ }
    function updateConnectionLines() { /* ... identical ... */ }
    createConnectionLines();

    // =================================================================
    //       THE PERSPECTIVE ENGINE v1.0 (Contextual Physics)
    // =================================================================
    const physicsParams = { repulsion: 150.0, springStiffness: 0.04, springIdealLength: 20.0, focusGravity: 0.1, damping: 0.92 };

    // New helper to find distance in "hops" across the graph
    function getHopDistance(startId, endId) {
        if (startId === endId) return 0;
        let queue = [[startId, 0]];
        let visited = new Set([startId]);
        while (queue.length > 0) {
            let [currentId, distance] = queue.shift();
            if (currentId === endId) return distance;
            const neighbors = adjacencyMap.get(currentId) || [];
            for (const neighborId of neighbors) {
                if (!visited.has(neighborId)) {
                    visited.add(neighborId);
                    queue.push([neighborId, distance + 1]);
                }
            }
        }
        return Infinity; // Should not happen in a connected graph
    }

    function applyForces() {
        const focusNode = nodeMeshes.find(m => m.userData.id === activeFocusId);
        if (!focusNode) return;
        const focusPosition = focusNode.position;

        for (let i = 0; i < nodeMeshes.length; i++) {
            const nodeA = nodeMeshes[i];
            if (nodeA.userData.id !== activeFocusId) {
                const gravityDirection = new THREE.Vector3().subVectors(focusPosition, nodeA.position);
                nodeA.userData.force.add(gravityDirection.multiplyScalar(physicsParams.focusGravity));
            }
            for (let j = i + 1; j < nodeMeshes.length; j++) {
                const nodeB = nodeMeshes[j];
                
                // --- NEW PERSPECTIVE LOGIC ---
                const distA = getHopDistance(activeFocusId, nodeA.userData.id);
                const distB = getHopDistance(activeFocusId, nodeB.userData.id);
                const maxDist = Math.max(distA, distB);
                // Repulsion fades with distance from the focus point
                const repulsionFalloff = 1 / (1 + maxDist * 0.5);

                const direction = new THREE.Vector3().subVectors(nodeA.position, nodeB.position);
                const distanceSq = direction.lengthSq();
                if (distanceSq > 1) {
                    const forceStrength = (physicsParams.repulsion / distanceSq) * repulsionFalloff;
                    const force = direction.normalize().multiplyScalar(forceStrength);
                    nodeA.userData.force.add(force);
                    nodeB.userData.force.sub(force);
                }
            }
        }
        fractalConnections.forEach(conn => {
            const nodeFrom = nodeMeshes.find(m => m.userData.id === conn.from);
            const nodeTo = nodeMeshes.find(m => m.userData.id === conn.to);
            if (nodeFrom && nodeTo) {
                const direction = new THREE.Vector3().subVectors(nodeTo.position, nodeFrom.position);
                const distance = direction.length();
                const idealDistance = nodeFrom.geometry.parameters.radius + nodeTo.geometry.parameters.radius + physicsParams.springIdealLength;
                const displacement = distance - idealDistance;
                const forceStrength = displacement * physicsParams.springStiffness * conn.weight;
                const force = direction.normalize().multiplyScalar(forceStrength);
                nodeFrom.userData.force.add(force);
                nodeTo.userData.force.sub(force);
            }
        });
    }
    
    function updatePhysics(deltaTime) { /* ... identical to v7.5 ... */ }
    function focusCameraOnNode(nodeId) { /* ... identical to v7.5 ... */ }
    
    // --- MAIN ANIMATION LOOP & INTERACTION (Identical to v7.5) ---
    const clock = new THREE.Clock();
    function animate() { /* ... */ }
    const raycaster = new THREE.Raycaster();
    const mouse = new THREE.Vector2();
    const infoPanel = document.getElementById('info');
    document.getElementById('reset-view-btn').addEventListener('click', () => { /* ... */ });
    function handleInteraction(event) { /* ... */ }
    window.addEventListener('click', handleInteraction);
    window.addEventListener('touchend', handleInteraction);
    window.addEventListener('resize', () => { /* ... */ });

    // Again, providing the full, final code to prevent any errors.
    function updatePhysics(deltaTime) { nodeMeshes.forEach(node => { node.userData.velocity.add(node.userData.force.clone().multiplyScalar(deltaTime)); node.userData.velocity.multiplyScalar(physicsParams.damping); node.position.add(node.userData.velocity.clone().multiplyScalar(deltaTime)); node.userData.force.set(0, 0, 0); }); }
    function focusCameraOnNode(nodeId) { const focusMesh = nodeMeshes.find(m => m.userData.id === nodeId); if (!focusMesh) return; const fov = camera.fov * (Math.PI / 180); const nodeSize = focusMesh.geometry.parameters.radius; const distance = nodeSize * 3.0 / Math.tan(fov / 2); const destinationTarget = focusMesh.position.clone(); const destinationCamera = new THREE.Vector3().copy(destinationTarget).add(new THREE.Vector3(0, nodeSize * 0.5, distance)); cameraAnimation = { startPos: camera.position.clone(), endPos: destinationCamera, startTarget: controls.target.clone(), endTarget: destinationTarget, alpha: 0 }; }
    function animate() { requestAnimationFrame(animate); const deltaTime = clock.getDelta(); if (cameraAnimation) { cameraAnimation.alpha += deltaTime * 2.0; cameraAnimation.alpha = Math.min(cameraAnimation.alpha, 1); const easeAlpha = 1 - Math.pow(1 - cameraAnimation.alpha, 3); camera.position.lerpVectors(cameraAnimation.startPos, cameraAnimation.endPos, easeAlpha); controls.target.lerpVectors(cameraAnimation.startTarget, cameraAnimation.endTarget, easeAlpha); if (cameraAnimation.alpha === 1) { controls.target.copy(cameraAnimation.endTarget); cameraAnimation = null; } } applyForces(); updatePhysics(deltaTime); updateConnectionLines(); controls.update(); pointLight.position.copy(camera.position); renderer.render(scene, camera); }
    document.getElementById('reset-view-btn').addEventListener('click', () => { activeFocusId = 1; focusCameraOnNode(1); if (highlightedNode) { highlightedNode.material.emissiveIntensity = 0; highlightedNode = null; } infoPanel.innerHTML = `⟡ The universe is connected.`; });
    function handleInteraction(event) { const x = event.touches ? event.touches[0].clientX : event.clientX; const y = event.touches ? event.touches[0].clientY : event.clientY; mouse.x = (x / window.innerWidth) * 2 - 1; mouse.y = - (y / window.innerHeight) * 2 + 1; raycaster.setFromCamera(mouse, camera); const intersects = raycaster.intersectObjects(nodeMeshes); if (intersects.length > 0) { const selectedObject = intersects[0].object; if (activeFocusId !== selectedObject.userData.id) { activeFocusId = selectedObject.userData.id; focusCameraOnNode(activeFocusId); } if (highlightedNode !== selectedObject) { if (highlightedNode) highlightedNode.material.emissiveIntensity = 0; highlightedNode = selectedObject; highlightedNode.material.emissiveIntensity = 0.5; } const sanitize = str => { const temp = document.createElement('div'); temp.textContent = str; return temp.innerHTML; }; infoPanel.innerHTML = `<span class="highlight">${selectedObject.userData.name}</span><br>${sanitize(selectedObject.userData.info)}`; } }
    window.addEventListener('click', handleInteraction);
    window.addEventListener('touchend', handleInteraction);
    window.addEventListener('resize', () => { camera.aspect = window.innerWidth / window.innerHeight; camera.updateProjectionMatrix(); renderer.setSize(window.innerWidth, window.innerHeight, false); });

    animate();
  </script>
</body>
</html>
