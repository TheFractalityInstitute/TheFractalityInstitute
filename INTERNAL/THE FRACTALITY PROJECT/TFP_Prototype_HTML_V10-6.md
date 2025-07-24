<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Fractality Bubble UI v10.6 - The Population</title>
  
  <script type="importmap">
  {
    "imports": {
      "three": "./three.module.js"
    }
  }
  </script>

  <style>
    body { margin: 0; overflow: hidden; background: #111; }
  </style>
</head>
<body>
  <script type="module">
    import * as THREE from 'three';
    // We will add OrbitControls back in the next step
    // import { OrbitControls } from './OrbitControls.js';

    // --- DATA ---
    function getDefaultData() { const nodes = [ { id: 1, name: "The Fractiverse", info: "The total ontological container.", radius: 8, color: "#ffffff" }, { id: 2, name: "Duality", info: "The primal division.", radius: 5, color: "#f0f0f0" }, { id: 3, name: "Motion", info: "Dynamic process.", radius: 3, color: "#87CEEB" }, { id: 10, name: "Stillness", info: "Latent potential.", radius: 3, color: "#9370DB" }, { id: 5, name: "Dimension of Mind", info: "Abstract cognition.", radius: 3.5, color: "#FFD700" }, { id: 12, name: "Chaos", info: "Boundary-membrane.", radius: 2, color: "#DC143C" }, ]; const connections = [ { from: 1, to: 2, type: 'contains' }, { from: 2, to: 3, type: 'contains' }, { from: 2, to: 10, type: 'contains' }, { from: 2, to: 12, type: 'contains' }, { from: 3, to: 5, type: 'contains' }]; return { nodes, connections }; }
    const { nodes: fractalNodes, connections: fractalConnections } = getDefaultData();
    
    // --- CORE SETUP ---
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    document.body.appendChild(renderer.domElement);
    
    // Camera Position
    camera.position.set(0, 0, 50);
    camera.lookAt(0,0,0);

    // --- SCENE CREATION & LAYOUT ---
    const nodeMeshes = [];

    // Loop through all nodes in the data
    fractalNodes.forEach((nodeData, index) => {
        const geometry = new THREE.SphereGeometry(nodeData.radius, 32, 32);
        const material = new THREE.MeshBasicMaterial({ color: nodeData.color, wireframe: true });
        const mesh = new THREE.Mesh(geometry, material);

        // Arrange in a simple line for stability testing
        mesh.position.set((index * 15) - (fractalNodes.length * 7.5), 0, 0);

        mesh.userData = { id: nodeData.id, name: nodeData.name, info: nodeData.info };
        scene.add(mesh);
        nodeMeshes.push(mesh);
    });

    // --- RENDER LOOP ---
    function animate() {
        requestAnimationFrame(animate);
        // Simple rotation for visual feedback
        scene.rotation.y += 0.001;
        renderer.render(scene, camera);
    }
    animate();

    // --- RESIZE HANDLER ---
    window.addEventListener('resize', () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    });
  </script>
</body>
</html>
