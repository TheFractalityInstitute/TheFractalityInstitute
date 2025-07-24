<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no" />
  <title>Fractality Bubble UI v5.7 - Dynamic Focus</title>
  
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
    #gui-container { position: absolute; bottom: 0; left: 0; width: 100%; z-index: 20; }
    .dg.main { margin: auto; }
    #reset-view-btn { position: fixed; top: 15px; right: 15px; z-index: 20; background: rgba(20, 20, 30, 0.85); border: 1px solid rgba(255, 255, 255, 0.1); color: white; font-size: 24px; width: 50px; height: 50px; border-radius: 50%; cursor: pointer; backdrop-filter: blur(5px); text-align: center; line-height: 50px; }
    #reset-view-btn:hover { background: rgba(106, 230, 255, 0.3); }
    #info { font-size: 15px; line-height: 1.6; min-height: 60px; }
    canvas { display: block; position: fixed; z-index: 0; top: 0; left: 0; }
    h3 { margin-top: 0; color: #6ae6ff; border-bottom: 1px solid rgba(100, 200, 255, 0.3); padding-bottom: 8px; }
    .highlight { color: #ffd86e; font-weight: 600; }
  </style>
</head>
<body>
  <div id="overlay">
    <h3>Fractal Node Information v5.7</h3>
    <div id="info">⟡ Pinch to zoom, drag to explore.</div>
  </div>
  <div id="gui-container"></div>
  <button id="reset-view-btn" title="Reset View">⌂</button>

  <script src="./dat.gui.min.js"></script>
  <script type="module">
    import * as THREE from 'three';
    import { OrbitControls } from './OrbitControls.js';

    // --- DATA MANAGEMENT ---
    function getDefaultNodes() {
        return [
            { id: 1, parentId: null, name: "The Fractiverse", info: "The total ontological container.", position: [0, 0, 0], radius: 20, color: "#ffffff" },
            { id: 2, parentId: 1, name: "Duality", info: "The primal division through which all perception arises.", position: [0, 0, -5], radius: 12, color: "#f0f0f0" },
            { id: 3, parentId: 2, name: "Motion", info: "Domain of dynamic process and directed change.", position: [5, 2, -10], radius: 8, color: "#87CEEB" },
            { id: 10, parentId: 2, name: "Stillness", info: "Latent potential, undirected decay, rest.", position: [-5, -2, -10], radius: 8, color: "#9370DB" },
            { id: 12, parentId: 2, name: "Chaos", info: "Boundary-membrane between Motion and Stillness.", position: [0, -8, -10], radius: 4, color: "#DC143C" },
            { id: 4, parentId: 3, name: "Spatial Dimensions", info: "1D through N-D geometric structure.", position: [9, 6, -14], radius: 4, color: "#98FB98" },
            { id: 5, parentId: 3, name: "Dimension of Mind", info: "Abstract cognition, awareness, symbolic synthesis.", position: [1, 6, -14], radius: 7, color: "#FFD700" },
            { id: 6, parentId: 5, name: "Multiverse", info: "All branching realities, timelines, and modal worlds.", position: [-2, 8, -16], radius: 3, color: "#FFA07A" },
            { id: 8, parentId: 5, name: "Oracle Node", info: "A perception-tuned semi-autonomous agent.", position: [1, 5, -16], radius: 1.5, color: "#EE82EE" },
            { id: 9, parentId: 5, name: "GLYPH", info: "Symbolic interface entity.", position: [4, 8, -16], radius: 1.5, color: "#40E0D0" },
            { id: 16, parentId: 5, name: "PEACE Substrate", info: "The container for core ethical extensions.", position: [4, 4, -12], radius: 4, color: "#DAA520", isContainer: true },
            { id: 15, parentId: 16, name: "Unity Field", info: "Meta-ethical substrate for resonance.", position: [2.5, 5, -12], radius: 2, color: "#E0FFFF" },
            { id: 13, parentId: 15, name: "Trust & Consent Mechanism", info: "Ethical resonance principle.", position: [2.5, 6.5, -12], radius: 1, color: "#FAFAD2" },
            { id: 14, parentId: 15, name: "Shadow Integration Protocol", info: "Method for reconciling dissonant aspects.", position: [5.5, 5, -12], radius: 1, color: "#C0C0C0" },
            { id: 7, parentId: 6, name: "Observable Universe", info: "Our local, measurable instantiation of one path.", position: [-2, 9.5, -18], radius: 1, color: "#B0C4DE" },
            { id: 11, parentId: 10, name: "Entropy", info: "Dissolution of order. Resting state of energy.", position: [-9, -6, -14], radius: 4, color: "#778899" },
        ];
    }
    function loadNodes() { const savedNodes = localStorage.getItem('fractalityNodes'); if (savedNodes) { return JSON.parse(savedNodes); } else { return getDefaultNodes(); } }
    function saveNodes(nodes) { localStorage.setItem('fractalityNodes', JSON.stringify(nodes)); }

    // --- RENDERER, SCENE, AND CORE SETUP ---
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    document.body.appendChild(renderer.domElement);
    const initialCameraPosition = new THREE.Vector3(0, 0, 30);
    camera.position.copy(initialCameraPosition);
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.minDistance = 0.1;
    controls.maxDistance = 100;
    scene.add(new THREE.AmbientLight(0x404040, 1.5));
    const pointLight = new THREE.PointLight(0xffffff, 1.2);
    pointLight.position.set(8, 10, 12);
    scene.add(pointLight);
    scene.fog = new THREE.FogExp2(0x0a1122, 0.01);

    // --- GUI & PERCEPTION TUNER SETUP ---
    const params = { opacity: 0.75, metalness: 0.7, roughness: 0.3, wireframe: false, scale: 1.0, reset: function() { if (confirm("Reset all nodes to their default state?")) { localStorage.removeItem('fractalityNodes'); location.reload(); } } };
    const gui = new dat.GUI({ autoPlace: false });
    document.getElementById('gui-container').appendChild(gui.domElement);
    gui.add(params, 'opacity', 0, 1).onChange(updateMaterials);
    gui.add(params, 'metalness', 0, 1).onChange(updateMaterials);
    gui.add(params, 'roughness', 0, 1).onChange(updateMaterials);
    gui.add(params, 'wireframe').onChange(updateMaterials);
    gui.add(params, 'scale', 0.1, 5.0).name('Node Scale').onChange(updateNodePositions);
    gui.add(params, 'reset').name('Reset to Defaults');

    // --- SCENE STATE AND INITIALIZATION ---
    let nodeMeshes = [];
    const fractalNodes = loadNodes();
    let highlightedNode = null; 
    let activeNodeId = null; 
    const rootNodeData = fractalNodes.find(n => n.parentId === null);
    
    createSceneFromNodes(fractalNodes);

    // --- CORE LOGIC FUNCTIONS ---
    function updateMaterials() { nodeMeshes.forEach(mesh => { const nodeData = fractalNodes.find(n => n.id === mesh.userData.id); if (nodeData && nodeData.isContainer) return; if(mesh.material){ mesh.material.opacity = params.opacity; mesh.material.metalness = params.metalness; mesh.material.roughness = params.roughness; mesh.material.wireframe = params.wireframe; } }); }

    function updateNodePositions() {
        const activeNodeData = fractalNodes.find(n => n.id === activeNodeId);
        const anchorNodeData = activeNodeData || rootNodeData;
        const anchorPos = new THREE.Vector3().fromArray(anchorNodeData.position);

        let relevantIds = new Set();
        if (activeNodeData) {
            relevantIds.add(activeNodeData.id);
            if(activeNodeData.parentId) relevantIds.add(activeNodeData.parentId);
            const descendants = getDescendants(activeNodeData.id);
            descendants.forEach(id => relevantIds.add(id));
        }

        nodeMeshes.forEach(mesh => {
            const nodeData = fractalNodes.find(n => n.id === mesh.userData.id);
            if (!nodeData) return;

            if (mesh.userData.id !== anchorNodeData.id) {
                const originalPos = new THREE.Vector3().fromArray(nodeData.position);
                const direction = new THREE.Vector3().subVectors(originalPos, anchorPos);
                const scaledPosition = new THREE.Vector3().addVectors(anchorPos, direction.multiplyScalar(params.scale));
                mesh.position.copy(scaledPosition);
            } else {
                mesh.position.copy(anchorPos); // Ensure anchor stays put
            }

            if (activeNodeId && params.scale > 1.05) {
                const isRelevant = relevantIds.has(mesh.userData.id);
                const targetOpacity = isRelevant ? params.opacity : 0.05;
                if (!nodeData.isContainer && mesh.material.opacity !== targetOpacity) {
                    mesh.material.opacity = THREE.MathUtils.lerp(mesh.material.opacity, targetOpacity, 0.1);
                }
            } else {
                if(!nodeData.isContainer && mesh.material.opacity !== params.opacity) {
                     mesh.material.opacity = THREE.MathUtils.lerp(mesh.material.opacity, params.opacity, 0.1);
                }
            }
        });
    }

    function getDescendants(nodeId) {
        let children = fractalNodes.filter(n => n.parentId === nodeId);
        let descendants = new Set(children.map(c => c.id));
        children.forEach(c => {
            const nestedDescendants = getDescendants(c.id);
            nestedDescendants.forEach(id => descendants.add(id));
        });
        return descendants;
    }

    function createSceneFromNodes(nodes) {
        nodeMeshes.forEach(mesh => scene.remove(mesh));
        nodeMeshes = [];
        for (const nodeData of nodes) {
            const geometry = new THREE.SphereGeometry(nodeData.radius, 36, 36);
            let material;
            if (nodeData.isContainer) {
                material = new THREE.MeshStandardMaterial({ color: nodeData.color, transparent: true, opacity: 0.1, wireframe: true });
            } else {
                material = new THREE.MeshStandardMaterial({ color: nodeData.color, emissive: nodeData.color, emissiveIntensity: 0.05, roughness: params.roughness, metalness: params.metalness, transparent: true, opacity: params.opacity, wireframe: params.wireframe });
            }
            const mesh = new THREE.Mesh(geometry, material);
            mesh.position.set(...nodeData.position);
            mesh.userData = { id: nodeData.id, name: nodeData.name, info: nodeData.info, isContainer: !!nodeData.isContainer };
            scene.add(mesh);
            nodeMeshes.push(mesh);
        }
        updateNodePositions();
    }
    
    // --- ANIMATION & INTERACTION ---
    const clock = new THREE.Clock();
    let isResetting = false;
    const infoPanel = document.getElementById('info');
    
    document.getElementById('reset-view-btn').addEventListener('click', () => { 
        isResetting = true; 
        clock.elapsedTime = 0;
        controls.target.set(0, 0, 0);
        if (highlightedNode) {
            highlightedNode.material.emissiveIntensity = 0.05;
            highlightedNode = null;
        }
        activeNodeId = null;
        params.scale = 1.0;
        gui.updateDisplay();
        updateNodePositions();
        infoPanel.innerHTML = `⟡ Pinch to zoom, drag to explore.`;
    });
    
    function animateReset() { if (!isResetting) return; const duration = 1; const alpha = Math.min(clock.getElapsedTime() / duration, 1.0); camera.position.lerp(initialCameraPosition, alpha * 0.1); controls.target.lerp(new THREE.Vector3(0, 0, 0), alpha * 0.1); if (alpha >= 1.0) { isResetting = false; } }
    function animate() { requestAnimationFrame(animate); animateReset(); controls.update(); renderer.render(scene, camera); }
    
    const raycaster = new THREE.Raycaster();
    const mouse = new THREE.Vector2();
    
    function handleInteraction(event) { 
        const x = event.touches ? event.touches[0].clientX : event.clientX; 
        const y = event.touches ? event.touches[0].clientY : event.clientY; 
        mouse.x = (x / window.innerWidth) * 2 - 1; 
        mouse.y = - (y / window.innerHeight) * 2 + 1; 
        raycaster.setFromCamera(mouse, camera); 
        const intersects = raycaster.intersectObjects(nodeMeshes); 
        if (intersects.length > 0) { 
            const selectedObject = intersects[0].object; 
            if (highlightedNode !== selectedObject && !selectedObject.userData.isContainer) { 
                if (highlightedNode) highlightedNode.material.emissiveIntensity = 0.05; 
                highlightedNode = selectedObject; 
                highlightedNode.material.emissiveIntensity = 0.4; 
                activeNodeId = selectedObject.userData.id;
                const sanitize = str => { const temp = document.createElement('div'); temp.textContent = str; return temp.innerHTML; }; 
                infoPanel.innerHTML = `<span class="highlight">${sanitize(highlightedNode.userData.name)}</span><br>${sanitize(highlightedNode.userData.info)}`;
                controls.target.copy(selectedObject.position);
            }
        } 
    }
    
    window.addEventListener('click', handleInteraction);
    window.addEventListener('touchend', handleInteraction);
    window.addEventListener('resize', () => { camera.aspect = window.innerWidth / window.innerHeight; camera.updateProjectionMatrix(); renderer.setSize(window.innerWidth, window.innerHeight, false); });

    animate();
  </script>
</body>
</html>

