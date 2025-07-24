<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no" />
  <title>Fractality Bubble UI v7.0 - The Parallax Engine</title>
  
  <script type="importmap">
  {
    "imports": {
      "three": "./three.module.js"
    }
  }
  </script>

  <style>
    /* CSS is identical to previous version */
    body { margin: 0; overflow: hidden; background: #111; color: white; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    #overlay { position: fixed; top: 15px; left: 15px; z-index: 10; background: rgba(20, 20, 30, 0.85); padding: 15px; border-radius: 12px; max-width: 320px; backdrop-filter: blur(5px); border: 1px solid rgba(255, 255, 255, 0.1); box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5); }
    #reset-view-btn { position: fixed; top: 15px; right: 15px; z-index: 20; background: rgba(20, 20, 30, 0.85); border: 1px solid rgba(255, 255, 255, 0.1); color: white; font-size: 24px; width: 50px; height: 50px; border-radius: 50%; cursor: pointer; backdrop-filter: blur(5px); text-align: center; line-height: 50px; }
    #edit-nodes-btn { position: fixed; top: 80px; right: 15px; z-index: 20; background: rgba(20, 20, 30, 0.85); border: 1px solid rgba(255, 255, 255, 0.1); color: white; font-size: 24px; width: 50px; height: 50px; border-radius: 50%; cursor: pointer; backdrop-filter: blur(5px); }
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
    <h3>Fractal Node Information v7.0</h3>
    <div id="info">⟡ The universe is settling...</div>
  </div>

  <button id="reset-view-btn" title="Reset View">⌂</button>
  <button id="edit-nodes-btn" title="Edit Nodes">✎</button>
  <div id="node-manager"><h4>Node Manager</h4><ul id="node-list"></ul><button>Add New Node</button></div>

  <script type="module">
    import * as THREE from 'three';
    import { OrbitControls } from './OrbitControls.js';

    // --- DATA STRUCTURE: GRAPH MODEL ---
    function getDefaultData() {
        const nodes = [
            { id: 1, name: "The Fractiverse", info: "The total ontological container.", radius: 10, color: "#ffffff" },
            { id: 2, name: "Duality", info: "The primal division.", radius: 6, color: "#f0f0f0" },
            { id: 3, name: "Motion", info: "Dynamic process.", radius: 4, color: "#87CEEB" },
            { id: 10, name: "Stillness", info: "Latent potential.", radius: 4, color: "#9370DB" },
            { id: 5, name: "Dimension of Mind", info: "Abstract cognition.", radius: 3.5, color: "#FFD700" },
            { id: 15, name: "Unity Field", info: "Meta-ethical substrate.", radius: 3, color: "#E0FFFF" },
            { id: 12, name: "Chaos", info: "Boundary-membrane.", radius: 2, color: "#DC143C" },
            { id: 14, name: "Shadow Integration", info: "Reconciling dissonant aspects.", radius: 1.5, color: "#C0C0C0" },
            { id: 9, name: "GLYPH", info: "Symbolic interface.", radius: 1.5, color: "#40E0D0" },
        ];

        const connections = [
            // Hierarchical connections are strong
            { from: 1, to: 2, type: 'contains', weight: 1.0 },
            { from: 2, to: 3, type: 'contains', weight: 1.0 },
            { from: 2, to: 10, type: 'contains', weight: 1.0 },
            { from: 2, to: 12, type: 'contains', weight: 0.8 }, // Chaos is part of Duality
            { from: 3, to: 5, type: 'contains', weight: 1.0 },
            
            // Associative connections can have different weights
            { from: 15, to: 5, type: 'resonates_with', weight: 0.6 }, // Unity Field resonates with Mind
            { from: 9, to: 15, type: 'interfaces_with', weight: 0.5 }, // GLYPH interfaces with Unity Field
            { from: 14, to: 12, type: 'works_on', weight: 0.7 }, // Shadow Integration works on Chaos
            { from: 14, to: 5, type: 'informs', weight: 0.4 },     // Shadow Integration informs the Mind
        ];
        
        return { nodes, connections };
    }
    function loadData() { const savedData = localStorage.getItem('fractalityGraphData'); if (savedData) { return JSON.parse(savedData); } return getDefaultData(); }
    
    // --- RENDERER, SCENE, AND CORE SETUP ---
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    document.body.appendChild(renderer.domElement);
    const initialCameraPosition = new THREE.Vector3(0, 0, 50); // Start further back
    camera.position.copy(initialCameraPosition);
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true; // Re-enable for smooth manual control
    scene.add(new THREE.AmbientLight(0x404040, 2.0));
    const pointLight = new THREE.PointLight(0xffffff, 1.0, 300);
    scene.add(pointLight);

    // --- SCENE STATE AND INITIALIZATION ---
    let nodeMeshes = [];
    const { nodes: fractalNodes, connections: fractalConnections } = loadData();
    
    function createSceneFromNodes(nodes) {
        nodeMeshes.forEach(mesh => scene.remove(mesh));
        nodeMeshes = [];
        nodes.forEach(nodeData => {
            const geometry = new THREE.SphereGeometry(nodeData.radius, 36, 36);
            const material = new THREE.MeshStandardMaterial({ color: nodeData.color, transparent: true, opacity: 0.9, wireframe: true, roughness: 0.5 });
            const mesh = new THREE.Mesh(geometry, material);
            
            // Initialize with physics properties and a random starting position
            mesh.userData = { 
                id: nodeData.id, 
                name: nodeData.name, 
                info: nodeData.info,
                velocity: new THREE.Vector3(),
                force: new THREE.Vector3()
            };
            mesh.position.set(Math.random() - 0.5, Math.random() - 0.5, Math.random() - 0.5).normalize().multiplyScalar(10);
            
            scene.add(mesh);
            nodeMeshes.push(mesh);
        });
    }
    createSceneFromNodes(fractalNodes);

    // =================================================================
    //         THE PARALLAX ENGINE v1.0 (Force-Directed Layout)
    // =================================================================
    const physicsParams = {
        repulsion: 200.0,
        springStiffness: 0.05,
        damping: 0.92 // Friction
    };

    function applyRepulsionForce() {
        for (let i = 0; i < nodeMeshes.length; i++) {
            for (let j = i + 1; j < nodeMeshes.length; j++) {
                const nodeA = nodeMeshes[i];
                const nodeB = nodeMeshes[j];
                const direction = new THREE.Vector3().subVectors(nodeA.position, nodeB.position);
                const distanceSq = direction.lengthSq();
                if (distanceSq > 0) {
                    const forceStrength = physicsParams.repulsion / distanceSq;
                    const force = direction.normalize().multiplyScalar(forceStrength);
                    nodeA.userData.force.add(force);
                    nodeB.userData.force.sub(force);
                }
            }
        }
    }

    function applyAttractionForce() {
        fractalConnections.forEach(conn => {
            const nodeFrom = nodeMeshes.find(m => m.userData.id === conn.from);
            const nodeTo = nodeMeshes.find(m => m.userData.id === conn.to);
            if (nodeFrom && nodeTo) {
                const direction = new THREE.Vector3().subVectors(nodeTo.position, nodeFrom.position);
                const displacement = direction.length();
                const forceStrength = (displacement) * physicsParams.springStiffness * conn.weight;
                const force = direction.normalize().multiplyScalar(forceStrength);
                nodeFrom.userData.force.add(force);
                nodeTo.userData.force.sub(force);
            }
        });
    }
    
    function updatePhysics(deltaTime) {
        nodeMeshes.forEach(node => {
            // Add force to velocity
            node.userData.velocity.add(node.userData.force.clone().multiplyScalar(deltaTime));
            // Apply damping (friction)
            node.userData.velocity.multiplyScalar(physicsParams.damping);
            // Update position with velocity
            node.position.add(node.userData.velocity.clone().multiplyScalar(deltaTime));
            // Reset force for the next frame
            node.userData.force.set(0, 0, 0);
        });
    }

    // --- MAIN ANIMATION LOOP ---
    const clock = new THREE.Clock();
    function animate() { 
        requestAnimationFrame(animate); 
        const deltaTime = clock.getDelta();
        
        applyRepulsionForce();
        applyAttractionForce();
        updatePhysics(deltaTime);
        
        controls.update(); 
        pointLight.position.copy(camera.position); // Light follows the camera
        renderer.render(scene, camera); 
    }

    // Simplified UI for this version
    document.getElementById('edit-nodes-btn').style.display = 'none';
    document.getElementById('reset-view-btn').addEventListener('click', () => { location.reload(); });

    animate();
  </script>
</body>
</html>
