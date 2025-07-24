<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no" />
  <title>Fractality Bubble UI v6.0 - True Fractal Zoom</title>
  
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
    #edit-nodes-btn { position: fixed; top: 15px; right: 80px; z-index: 20; background: rgba(20, 20, 30, 0.85); border: 1px solid rgba(255, 255, 255, 0.1); color: white; font-size: 24px; width: 50px; height: 50px; border-radius: 50%; cursor: pointer; backdrop-filter: blur(5px); }
    #node-manager { display: none; position: fixed; right: 15px; top: 80px; width: 320px; max-height: 60%; background: rgba(20, 20, 30, 0.9); backdrop-filter: blur(5px); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; z-index: 30; color: white; padding: 15px; overflow-y: auto; }
    #node-manager h4 { margin-top: 0; color: #6ae6ff; }
    #node-list { list-style-type: none; padding: 0; margin: 0; }
    #node-list li { background: rgba(255,255,255,0.05); border-radius: 4px; padding: 10px; margin-bottom: 8px; }
    #info { font-size: 15px; line-height: 1.6; min-height: 60px; }
    canvas { display: block; position: fixed; z-index: 0; top: 0; left: 0; }
    h3 { margin-top: 0; color: #6ae6ff; border-bottom: 1px solid rgba(100, 200, 255, 0.3); padding-bottom: 8px; }
    .highlight { color: #ffd86e; font-weight: 600; }
  </style>
</head>
<body>
  <div id="overlay">
    <h3>Fractal Node Information v6.0</h3>
    <div id="info">⟡ Click a node to focus.</div>
  </div>

  <div id="gui-container"></div>
  <button id="reset-view-btn" title="Reset View">⌂</button>
  <button id="edit-nodes-btn" title="Edit Nodes">✎</button>
  <div id="node-manager"><h4>Node Manager</h4><ul id="node-list"></ul><button>Add New Node</button></div>

  <script src="./dat.gui.min.js"></script>
  <script type="module">
    import * as THREE from 'three';
    import { OrbitControls } from './OrbitControls.js';

    // --- DATA MANAGEMENT ---
    function getDefaultNodes() {
        // POSITIONS ARE NOW RELATIVE TO THEIR PARENT
        return [
            { id: 1, parentId: null, name: "The Fractiverse", info: "The total ontological container.", position: [0, 0, 0], radius: 10, color: "#ffffff" },
            { id: 2, parentId: 1, name: "Duality", info: "The primal division.", position: [0, 0, -5], radius: 6, color: "#f0f0f0" },
            { id: 3, parentId: 2, name: "Motion", info: "Dynamic process.", position: [5, 0, 0], radius: 4, color: "#87CEEB" },
            { id: 10, parentId: 2, name: "Stillness", info: "Latent potential.", position: [-5, 0, 0], radius: 4, color: "#9370DB" },
            { id: 12, parentId: 2, name: "Chaos", info: "Boundary-membrane.", position: [0, -5, 0], radius: 2, color: "#DC143C" },
            { id: 4, parentId: 3, name: "Spatial Dimensions", info: "Geometric structure.", position: [3, 2, 0], radius: 2, color: "#98FB98" },
            { id: 5, parentId: 3, name: "Dimension of Mind", info: "Abstract cognition.", position: [-3, 2, 0], radius: 3.5, color: "#FFD700" },
            { id: 6, parentId: 5, name: "Multiverse", info: "Branching realities.", position: [-2, 1, 0], radius: 1.5, color: "#FFA07A" },
            { id: 8, parentId: 5, name: "Oracle Node", info: "Semi-autonomous agent.", position: [0, -2, 0], radius: 1, color: "#EE82EE" },
            { id: 9, parentId: 5, name: "GLYPH", info: "Symbolic interface.", position: [2, 1, 0], radius: 1, color: "#40E0D0" },
            { id: 16, parentId: 5, name: "PEACE Substrate", info: "Ethical extensions.", position: [0, 2.5, 0], radius: 2, color: "#DAA520", isContainer: true },
            { id: 15, parentId: 16, name: "Unity Field", info: "Meta-ethical substrate.", position: [0, 0, 0], radius: 1.5, color: "#E0FFFF" },
            { id: 13, parentId: 15, name: "Trust & Consent", info: "Ethical resonance.", position: [-0.5, 0.5, 0], radius: 0.5, color: "#FAFAD2" },
            { id: 14, parentId: 15, name: "Shadow Integration", info: "Reconciling dissonant aspects.", position: [0.5, 0.5, 0], radius: 0.5, color: "#C0C0C0" },
            { id: 7, parentId: 6, name: "Observable Universe", info: "Our local instantiation.", position: [0, 1, 0], radius: 0.5, color: "#B0C4DE" },
            { id: 11, parentId: 10, name: "Entropy", info: "Dissolution of order.", position: [0, 0, 2], radius: 2, color: "#778899" },
        ];
    }
    function loadNodes() { const savedNodes = localStorage.getItem('fractalityNodes'); if (savedNodes) { return JSON.parse(savedNodes); } else { return getDefaultNodes(); } }
    
    // --- RENDERER, SCENE, AND CORE SETUP ---
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    document.body.appendChild(renderer.domElement);
    const initialCameraPosition = new THREE.Vector3(0, 0, 25);
    camera.position.copy(initialCameraPosition);
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    scene.add(new THREE.AmbientLight(0x404040, 2.0));
    const pointLight = new THREE.PointLight(0xffffff, 1.5, 200);
    scene.add(pointLight);
    scene.fog = new THREE.FogExp2(0x0a1122, 0.02);

    // --- SCENE STATE AND INITIALIZATION ---
    let nodeMeshes = [];
    const fractalNodes = loadNodes();
    let highlightedNode = null; 
    let activeFocusId = fractalNodes.find(n => n.parentId === null).id; // Start focused on the root
    
    // --- NEW LAYOUT ENGINE ---
    const layoutEngine = {
        calculateWorldPositions: function(focusNodeId) {
            const worldPositions = new Map();
            const focusNode = fractalNodes.find(n => n.id === focusNodeId);
            if (!focusNode) return worldPositions;

            const processNode = (node, parentPosition) => {
                const relativePos = new THREE.Vector3().fromArray(node.position);
                const worldPos = new THREE.Vector3().addVectors(parentPosition, relativePos);
                worldPositions.set(node.id, worldPos);

                const children = fractalNodes.filter(child => child.parentId === node.id);
                children.forEach(child => processNode(child, worldPos));
            };
            
            // Start recursion from the focus node, placing it at the origin
            processNode(focusNode, new THREE.Vector3(0, 0, 0));
            return worldPositions;
        },
        applyLayout: function(worldPositions) {
            nodeMeshes.forEach(mesh => {
                const newPos = worldPositions.get(mesh.userData.id);
                if (newPos) {
                    mesh.position.copy(newPos);
                    mesh.visible = true;
                } else {
                    mesh.visible = false; // Hide nodes not in the calculated layout
                }
            });
        }
    };
    
    // This function now ONLY creates the meshes, it doesn't position them.
    function createSceneFromNodes(nodes) {
        nodeMeshes.forEach(mesh => scene.remove(mesh));
        nodeMeshes = [];
        for (const nodeData of nodes) {
            const geometry = new THREE.SphereGeometry(nodeData.radius, 36, 36);
            const material = new THREE.MeshStandardMaterial({ color: nodeData.color, transparent: true, opacity: 0.85, roughness: 0.4, metalness: 0.5 });
            const mesh = new THREE.Mesh(geometry, material);
            mesh.userData = { id: nodeData.id, name: nodeData.name, info: nodeData.info };
            scene.add(mesh);
            nodeMeshes.push(mesh);
        }
    }

    createSceneFromNodes(fractalNodes);
    // Apply the initial layout
    const initialLayout = layoutEngine.calculateWorldPositions(activeFocusId);
    layoutEngine.applyLayout(initialLayout);


    // --- ANIMATION & INTERACTION ---
    const infoPanel = document.getElementById('info');
    
    document.getElementById('reset-view-btn').addEventListener('click', () => { 
        const rootId = fractalNodes.find(n => n.parentId === null).id;
        activeFocusId = rootId;
        const newLayout = layoutEngine.calculateWorldPositions(rootId);
        layoutEngine.applyLayout(newLayout);
        
        camera.position.copy(initialCameraPosition);
        controls.target.set(0, 0, 0);
        infoPanel.innerHTML = `⟡ Click a node to focus.`;
    });
    
    function animate() { requestAnimationFrame(animate); controls.update(); renderer.render(scene, camera); }
    
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
            if (activeFocusId !== selectedObject.userData.id) {
                // Set new focus and recalculate the entire scene layout
                activeFocusId = selectedObject.userData.id;
                const newLayout = layoutEngine.calculateWorldPositions(activeFocusId);
                layoutEngine.applyLayout(newLayout);
                
                // Also update the info panel and controls target
                const sanitize = str => { const temp = document.createElement('div'); temp.textContent = str; return temp.innerHTML; }; 
                infoPanel.innerHTML = `<span class="highlight">${selectedObject.userData.name}</span><br>${sanitize(selectedObject.userData.info)}`;
                controls.target.set(0, 0, 0); // Target is always the new origin
            }
        } 
    }
    
    window.addEventListener('click', handleInteraction);
    window.addEventListener('touchend', handleInteraction);
    window.addEventListener('resize', () => { camera.aspect = window.innerWidth / window.innerHeight; camera.updateProjectionMatrix(); renderer.setSize(window.innerWidth, window.innerHeight, false); });

    animate();
    
    // Remove the dat.GUI for now to simplify, we will add it back with the editor
    document.getElementById('gui-container').style.display = 'none';
  </script>
</body>
</html>
