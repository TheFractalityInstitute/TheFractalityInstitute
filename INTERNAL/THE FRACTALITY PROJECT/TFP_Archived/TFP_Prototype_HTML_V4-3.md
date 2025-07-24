<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no" />
  <title>Fractality Bubble UI v4.3 - Bottom HUD</title>
  
  <script type="importmap">
  {
    "imports": {
      "three": "./three.module.js"
    }
  }
  </script>

  <style>
    body { margin: 0; overflow: hidden; background: #111; color: white; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    
    #overlay {
      position: fixed;
      top: 15px;
      left: 15px;
      z-index: 10;
      background: rgba(20, 20, 30, 0.85); padding: 15px; border-radius: 12px; max-width: 320px; backdrop-filter: blur(5px); border: 1px solid rgba(255, 255, 255, 0.1); box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
    }

    /* --- THIS CSS RULE HAS BEEN MODIFIED --- */
    #gui-container {
      position: absolute;
      /* Remove top and right, add bottom and left */
      bottom: 0;
      left: 0;
      width: 100%; /* Make it span the full width */
      z-index: 20;
    }
    
    /* This makes the dat.gui panel itself centered within the bottom container */
    .dg.main {
        margin: auto;
    }

    #info { font-size: 15px; line-height: 1.6; min-height: 60px; }
    canvas { display: block; position: fixed; z-index: 0; top: 0; left: 0; }
    h3 { margin-top: 0; color: #6ae6ff; border-bottom: 1px solid rgba(100, 200, 255, 0.3); padding-bottom: 8px; }
    .highlight { color: #ffd86e; font-weight: 600; }
  </style>
</head>
<body>
  <div id="overlay">
    <h3>Fractal Node Information v4.3</h3>
    <div id="info">⟡ Pinch to zoom, drag to explore.</div>
  </div>

  <div id="gui-container"></div>

  <script src="./dat.gui.min.js"></script>

  <script type="module">
    // All JavaScript code is identical to the previous working version.
    // No changes are needed here.
    import * as THREE from 'three';
    import { OrbitControls } from './OrbitControls.js';

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    document.body.appendChild(renderer.domElement);
    
    camera.position.set(0, 2, 15);
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    
    scene.add(new THREE.AmbientLight(0x404040, 1.5));
    const pointLight = new THREE.PointLight(0xffffff, 1.2);
    pointLight.position.set(8, 10, 12);
    scene.add(pointLight);
    scene.fog = new THREE.FogExp2(0x0a1122, 0.03);

    const fractalNodes = {
      "GLYPH": { position: [3, 0.75, -1], radius: 1.5, color: "#20B2AA", info: "Symbolic representation of fractal language" },
      "Oracle Node": { position: [3, 0.5, 1], radius: 1.5, color: "#F08080", info: "Predictive fractal analysis module" },
      "Unity Field": { position: [0, 0, 3], radius: 7, color: "#E0FFFF", info: "Harmonic convergence field generator" },
      "Trust Protocol": { position: [0, 2, 2], radius: 1.75, color: "#FAFAD2", info: "Decentralized consensus mechanism" },
      "Shadow Integration": { position: [3, -1, 0.5], radius: 1.25, color: "#9370DB", info: "Chaos assimilation subsystem" }
    };

    const params = {
        opacity: 0.75,
        metalness: 0.7,
        roughness: 0.3,
        wireframe: false,
    };
    
    const gui = new dat.GUI({ autoPlace: false });
    document.getElementById('gui-container').appendChild(gui.domElement);
    
    gui.add(params, 'opacity', 0, 1).onChange(updateMaterials);
    gui.add(params, 'metalness', 0, 1).onChange(updateMaterials);
    gui.add(params, 'roughness', 0, 1).onChange(updateMaterials);
    gui.add(params, 'wireframe').onChange(updateMaterials);

    const nodeMeshes = [];
    for (const [name, data] of Object.entries(fractalNodes)) {
      const geometry = new THREE.SphereGeometry(data.radius, 36, 36);
      const material = new THREE.MeshStandardMaterial({
        color: data.color,
        emissive: data.color,
        emissiveIntensity: 0.05,
        roughness: params.roughness,
        metalness: params.metalness,
        transparent: true,
        opacity: params.opacity,
        wireframe: params.wireframe
      });
      const node = new THREE.Mesh(geometry, material);
      node.position.set(...data.position);
      node.userData = { name, info: data.info };
      scene.add(node);
      nodeMeshes.push(node);
    }
    
    function updateMaterials() {
        nodeMeshes.forEach(mesh => {
            mesh.material.opacity = params.opacity;
            mesh.material.metalness = params.metalness;
            mesh.material.roughness = params.roughness;
            mesh.material.wireframe = params.wireframe;
        });
    }

    function animate() {
      requestAnimationFrame(animate);
      controls.update(); 
      renderer.render(scene, camera);
    }
    
    const raycaster = new THREE.Raycaster();
    const mouse = new THREE.Vector2();
    const infoPanel = document.getElementById('info');
    let activeNode = null;
    function handleInteraction(event) {
        const x = event.touches ? event.touches[0].clientX : event.clientX;
        const y = event.touches ? event.touches[0].clientY : event.clientY;
        mouse.x = (x / window.innerWidth) * 2 - 1;
        mouse.y = - (y / window.innerHeight) * 2 + 1;
        raycaster.setFromCamera(mouse, camera);
        const intersects = raycaster.intersectObjects(nodeMeshes);
        if (intersects.length > 0) {
            const selectedObject = intersects[0].object;
            if (activeNode !== selectedObject) {
                if (activeNode) activeNode.material.emissiveIntensity = 0.05;
                activeNode = selectedObject;
                activeNode.material.emissiveIntensity = 0.4;
                const sanitize = str => { const temp = document.createElement('div'); temp.textContent = str; return temp.innerHTML; };
                infoPanel.innerHTML = `<span class="highlight">${sanitize(activeNode.userData.name)}</span><br>${sanitize(activeNode.userData.info)}`;
            }
        }
    }
    window.addEventListener('click', handleInteraction);
    window.addEventListener('touchend', handleInteraction);
    window.addEventListener('resize', () => {
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight, false);
    });

    animate();
  </script>
</body>
</html>
