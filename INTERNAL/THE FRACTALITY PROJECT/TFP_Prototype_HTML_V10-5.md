<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Fractality Bubble UI v10.5 - The Data Test</title>
  
  <style>
    body { margin: 0; overflow: hidden; background: #111; }
  </style>
</head>
<body>
  <script type="module">
    import * as THREE from './three.module.js';

    // --- The Data We Are Testing ---
    function getDefaultData() { 
        const nodes = [ { id: 1, name: "The Fractiverse", info: "The total ontological container.", radius: 8, color: "#ffffff" }, { id: 2, name: "Duality", info: "The primal division.", radius: 5, color: "#f0f0f0" }, { id: 3, name: "Motion", info: "Dynamic process.", radius: 3, color: "#87CEEB" }, { id: 10, name: "Stillness", info: "Latent potential.", radius: 3, color: "#9370DB" }, { id: 5, name: "Dimension of Mind", info: "Abstract cognition.", radius: 3.5, color: "#FFD700" }, { id: 12, name: "Chaos", info: "Boundary-membrane.", radius: 2, color: "#DC143C" }, ]; 
        const connections = [ { from: 1, to: 2, type: 'contains' }, { from: 2, to: 3, type: 'contains' }, { from: 2, to: 10, type: 'contains' }, { from: 2, to: 12, type: 'contains' }, { from: 3, to: 5, type: 'contains' }]; 
        return { nodes, connections }; 
    }

    // --- CORE SETUP ---
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    document.body.appendChild(renderer.domElement);
    
    // --- THE TEST OBJECT ---
    const geometry = new THREE.SphereGeometry(5, 32, 32);
    // Start with a default GREEN color
    const material = new THREE.MeshBasicMaterial({ color: 0x00ff00, wireframe: true }); 
    const sphere = new THREE.Mesh(geometry, material);
    scene.add(sphere);
    camera.position.z = 20;

    // --- THE TEST LOGIC ---
    try {
        const data = getDefaultData();
        // If the line above doesn't crash, this code will run.
        if (data && data.nodes && data.nodes.length > 0) {
            // Change the sphere color to PINK if the data is valid.
            material.color.set(0xff00ff); 
        }
    } catch (e) {
        // If there's an error, we won't get here, but this is good practice.
        console.error("The data block is invalid!", e);
    }
    
    // --- RENDER LOOP ---
    function animate() {
        requestAnimationFrame(animate);
        sphere.rotation.x += 0.005;
        sphere.rotation.y += 0.005;
        renderer.render(scene, camera);
    }
    animate();

    window.addEventListener('resize', () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    });
  </script>
</body>
</html>
