<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Fractality Bubble UI v9.7 - Interactive Universe</title>
  
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
    // --- STEP 1: Import OrbitControls ---
    import { OrbitControls } from './OrbitControls.js';

    // The Core Components
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    document.body.appendChild(renderer.domElement);

    // --- STEP 2: Instantiate OrbitControls ---
    // It needs the camera to control and the renderer's DOM element for mouse/touch events.
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true; // Makes the movement smoother

    // The Object
    const geometry = new THREE.SphereGeometry(5, 32, 32);
    const material = new THREE.MeshBasicMaterial({ color: 0x00ff00, wireframe: true }); 
    const sphere = new THREE.Mesh(geometry, material);
    scene.add(sphere);

    // The Camera Position
    camera.position.z = 20;

    // The Render Loop
    function animate() {
        requestAnimationFrame(animate);

        // We no longer need to rotate the sphere manually
        // sphere.rotation.x += 0.005;
        // sphere.rotation.y += 0.005;

        // --- STEP 3: Update the controls in the render loop ---
        // This is necessary for damping to work.
        controls.update();

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