<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Fractality Bubble UI v9.6 - Hello, Universe</title>
  
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

    // 1. The Core Components
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    document.body.appendChild(renderer.domElement);

    // 2. The Object
    const geometry = new THREE.SphereGeometry(5, 32, 32);
    // Use MeshBasicMaterial - it requires no light to be visible
    const material = new THREE.MeshBasicMaterial({ color: 0x00ff00, wireframe: true }); 
    const sphere = new THREE.Mesh(geometry, material);
    scene.add(sphere);

    // 3. The Camera Position
    camera.position.z = 20;

    // 4. The Render Loop
    function animate() {
        requestAnimationFrame(animate);

        // A simple rotation to prove it's a live 3D object
        sphere.rotation.x += 0.005;
        sphere.rotation.y += 0.005;

        renderer.render(scene, camera);
    }

    // Start the animation
    animate();

    // Resize handler to keep it centered
    window.addEventListener('resize', () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    });
  </script>
</body>
</html>