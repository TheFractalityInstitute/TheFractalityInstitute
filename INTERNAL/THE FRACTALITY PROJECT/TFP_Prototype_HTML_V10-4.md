<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Fractality Bubble UI v10.4 - The Direct Path</title>
  
  <style>
    body { margin: 0; overflow: hidden; background: #111; }
  </style>
</head>
<body>
  <script type="module">
    // --- IMPORT using a DIRECT, RELATIVE PATH ---
    import * as THREE from './three.module.js';

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
    camera.position.set(0, 0, 45);
    camera.lookAt(0,0,0);

    // --- SCENE CREATION & LAYOUT ---
    const nodeMeshes = [];
    const activeFocusId = 1;

    function createAndLayoutNodes(focusId) {
        const children = connections.filter(c => c.from === focusId).map(c => c.to);
        const n = children.length;
        if (n === 0) return;
        
        const phi = Math.PI * (3 - Math.sqrt(5));

        children.forEach((childId, i) => {
            const nodeData = fractalNodes.find(n => n.id === childId);
            if (!nodeData) return;

            const geometry = new THREE.SphereGeometry(nodeData.radius, 32, 32);
            const material = new THREE.MeshBasicMaterial({ color: nodeData.color, wireframe: true });
            const mesh = new THREE.Mesh(geometry, material);

            const y = 1 - (i / (n === 1 ? 2 : n - 1)) * 2;
            const radius = Math.sqrt(1 - y * y);
            const theta = phi * i;
            const x = Math.cos(theta) * radius;
            const z = Math.sin(theta) * radius;
            
            mesh.position.set(x, y, z).multiplyScalar(15);
            
            scene.add(mesh);
            nodeMeshes.push(mesh);
        });
    }

    createAndLayoutNodes(activeFocusId);

    // --- RENDER LOOP ---
    function animate() {
        requestAnimationFrame(animate);
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
