<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no" />
  <title>Fractality Bubble UI v6.4 - The Graph Foundation</title>
  
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
    
    /* MODIFIED: Edit button is now below the Home button */
    #edit-nodes-btn {
        position: fixed;
        top: 80px;
        right: 15px;
        z-index: 20;
        background: rgba(20, 20, 30, 0.85);
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: white;
        font-size: 24px;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        cursor: pointer;
        backdrop-filter: blur(5px);
    }
    
    /* Other CSS is identical */
    #node-manager { display: none; position: fixed; right: 15px; top: 145px; width: 320px; max-height: 60%; background: rgba(20, 20, 30, 0.9); backdrop-filter: blur(5px); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; z-index: 30; color: white; padding: 15px; overflow-y: auto; }
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
    <h3>Fractal Node Information v6.4</h3>
    <div id="info">⟡ Graph foundation in place.</div>
  </div>

  <button id="reset-view-btn" title="Reset View">⌂</button>
  <button id="edit-nodes-btn" title="Edit Nodes">✎</button>
  <div id="node-manager"><h4>Node Manager</h4><ul id="node-list"></ul><button>Add New Node</button></div>

  <script type="module">
    import * as THREE from 'three';
    import { OrbitControls } from './OrbitControls.js';

    // --- NEW DATA STRUCTURE: GRAPH MODEL ---
    function getDefaultData() {
        const nodes = [
            { id: 1, name: "The Fractiverse", info: "The total ontological container.", radius: 10, color: "#ffffff" },
            { id: 2, name: "Duality", info: "The primal division.", radius: 6, color: "#f0f0f0" },
            { id: 3, name: "Motion", info: "Dynamic process.", radius: 4, color: "#87CEEB" },
            { id: 10, name: "Stillness", info: "Latent potential.", radius: 4, color: "#9370DB" },
            { id: 5, name: "Dimension of Mind", info: "Abstract cognition.", radius: 3.5, color: "#FFD700" },
            { id: 15, name: "Unity Field", info: "Meta-ethical substrate.", radius: 3, color: "#E0FFFF" },
            // ... and so on for all other nodes
        ];

        const connections = [
            // Hierarchical connections (like parentId)
            { from: 1, to: 2, type: 'contains', weight: 1.0 },
            { from: 2, to: 3, type: 'contains', weight: 1.0 },
            { from: 2, to: 10, type: 'contains', weight: 1.0 },
            { from: 3, to: 5, type: 'contains', weight: 1.0 },
            
            // Associative connections (the "neural net" part)
            { from: 15, to: 5, type: 'resonates_with', weight: 0.8 }, // Unity Field resonates with Mind
            { from: 3, to: 10, type: 'is_opposite_of', weight: -1.0 } // Motion is opposite of Stillness
        ];
        
        return { nodes, connections };
    }

    function loadData() {
        const savedData = localStorage.getItem('fractalityGraphData');
        if (savedData) {
            return JSON.parse(savedData);
        }
        return getDefaultData();
    }
    
    // --- RENDERER, SCENE, AND CORE SETUP ---
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    document.body.appendChild(renderer.domElement);
    const initialCameraPosition = new THREE.Vector3(0, 0, 35);
    camera.position.copy(initialCameraPosition);
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    scene.add(new THREE.AmbientLight(0x404040, 2.0));

    // --- SCENE STATE AND INITIALIZATION ---
    let nodeMeshes = [];
    const { nodes: fractalNodes, connections: fractalConnections } = loadData();
    
    // Simple initial layout for now
    function createSceneFromNodes(nodes) {
        nodeMeshes.forEach(mesh => scene.remove(mesh));
        nodeMeshes = [];
        nodes.forEach((nodeData, index) => {
            const geometry = new THREE.SphereGeometry(nodeData.radius, 36, 36);
            const material = new THREE.MeshStandardMaterial({ color: nodeData.color, transparent: true, opacity: 0.8, wireframe: true });
            const mesh = new THREE.Mesh(geometry, material);
            // Temporary simple layout - we will replace this with the physics engine
            mesh.position.set((index % 5 - 2) * 15, (Math.floor(index / 5) - 1) * 15, 0);
            mesh.userData = { id: nodeData.id, name: nodeData.name, info: nodeData.info };
            scene.add(mesh);
            nodeMeshes.push(mesh);
        });
    }

    createSceneFromNodes(fractalNodes);

    // Placeholder for drawing connection lines
    function drawConnections(connections) {
        // In v7.0, we will draw lines or other visual indicators for these connections
    }
    drawConnections(fractalConnections);

    // --- UI AND INTERACTION LOGIC (Simplified for this transitional step) ---
    const infoPanel = document.getElementById('info');
    document.getElementById('reset-view-btn').addEventListener('click', () => { 
        localStorage.removeItem('fractalityGraphData');
        location.reload();
    });
    const editNodesBtn = document.getElementById('edit-nodes-btn');
    editNodesBtn.style.display = 'none'; // Hide until we build the new editor

    function animate() { requestAnimationFrame(animate); controls.update(); renderer.render(scene, camera); }
    animate();

  </script>
</body>
</html>
