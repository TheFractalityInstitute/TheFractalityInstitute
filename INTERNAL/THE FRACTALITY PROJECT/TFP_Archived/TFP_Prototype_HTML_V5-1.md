<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no" />
  <title>Fractality Bubble UI v5.1 - Camera Navigation</title>
  
  <script type="importmap">
  {
    "imports": {
      "three": "./three.module.js"
    }
  }
  </script>

  <style>
    /* ... other CSS is identical ... */
    body { margin: 0; overflow: hidden; background: #111; color: white; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    #overlay { position: fixed; top: 15px; left: 15px; z-index: 10; background: rgba(20, 20, 30, 0.85); padding: 15px; border-radius: 12px; max-width: 320px; backdrop-filter: blur(5px); border: 1px solid rgba(255, 255, 255, 0.1); box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5); }
    #gui-container { position: absolute; bottom: 0; left: 0; width: 100%; z-index: 20; }
    .dg.main { margin: auto; }

    /* --- ADD CSS FOR THE NEW RESET BUTTON --- */
    #reset-view-btn {
      position: fixed;
      top: 15px;
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
      text-align: center;
      line-height: 50px;
    }
    #reset-view-btn:hover {
        background: rgba(106, 230, 255, 0.3);
    }

    #info { font-size: 15px; line-height: 1.6; min-height: 60px; }
    canvas { display: block; position: fixed; z-index: 0; top: 0; left: 0; }
    h3 { margin-top: 0; color: #6ae6ff; border-bottom: 1px solid rgba(100, 200, 255, 0.3); padding-bottom: 8px; }
    .highlight { color: #ffd86e; font-weight: 600; }
  </style>
</head>
<body>
  <div id="overlay">
    <h3>Fractal Node Information v5.1</h3>
    <div id="info">⟡ Pinch to zoom, drag to explore.</div>
  </div>

  <div id="gui-container"></div>
  <button id="reset-view-btn" title="Reset View">⌂</button>

  <script src="./dat.gui.min.js"></script>
  <script type="module">
    import * as THREE from 'three';
    import { OrbitControls } from './OrbitControls.js';

    // --- Data Management (same as v5.0) ---
    function getDefaultNodes() { /* ... identical ... */ return [ { id: 1, parentId: null, name: "Unity Field", info: "Harmonic convergence field generator", position: [0, 0, 3], radius: 7, color: "#E0FFFF" }, { id: 2, parentId: 1, name: "Trust Protocol", info: "Decentralized consensus mechanism", position: [0, 2, 2], radius: 1.75, color: "#FAFAD2" }, { id: 3, parentId: 1, name: "GLYPH", info: "Symbolic representation of fractal language", position: [3, 0.75, -1], radius: 1.5, color: "#20B2AA" }, { id: 4, parentId: 3, name: "Oracle Node", info: "Predictive fractal analysis module", position: [3, 0.5, 1], radius: 1.5, color: "#F08080" }, { id: 5, parentId: 1, name: "Shadow Integration", info: "Chaos assimilation subsystem", position: [3, -1, 0.5], radius: 1.25, color: "#9370DB" } ]; }
    function loadNodes() { /* ... identical ... */ const savedNodes = localStorage.getItem('fractalityNodes'); if (savedNodes) { return JSON.parse(savedNodes); } else { return getDefaultNodes(); } }
    function saveNodes(nodes) { /* ... identical ... */ localStorage.setItem('fractalityNodes', JSON.stringify(nodes)); }

    // --- Scene Setup (same as v5.0) ---
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    document.body.appendChild(renderer.domElement);
    
    // --- CAMERA AND CONTROLS SETUP ---
    const initialCameraPosition = new THREE.Vector3(0, 2, 15);
    camera.position.copy(initialCameraPosition);
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    
    // --- Lighting, Fog, GUI, Scene Creation (same as v5.0) ---
    scene.add(new THREE.AmbientLight(0x404040, 1.5));
    const pointLight = new THREE.PointLight(0xffffff, 1.2);
    pointLight.position.set(8, 10, 12);
    scene.add(pointLight);
    scene.fog = new THREE.FogExp2(0x0a1122, 0.03);
    const params = { opacity: 0.75, metalness: 0.7, roughness: 0.3, wireframe: false };
    const gui = new dat.GUI({ autoPlace: false });
    document.getElementById('gui-container').appendChild(gui.domElement);
    gui.add(params, 'opacity', 0, 1).onChange(updateMaterials);
    gui.add(params, 'metalness', 0, 1).onChange(updateMaterials);
    gui.add(params, 'roughness', 0, 1).onChange(updateMaterials);
    gui.add(params, 'wireframe').onChange(updateMaterials);
    let nodeMeshes = [];
    let fractalNodes = loadNodes();
    createSceneFromNodes(fractalNodes);

    // --- CAMERA RESET LOGIC ---
    const resetViewButton = document.getElementById('reset-view-btn');
    let isResetting = false;
    const clock = new THREE.Clock();

    resetViewButton.addEventListener('click', () => {
        isResetting = true;
        clock.elapsedTime = 0; // Reset clock for the animation
    });
    
    function animateReset() {
        if (!isResetting) return;

        const duration = 1; // 1 second animation
        const alpha = Math.min(clock.getElapsedTime() / duration, 1.0);
        
        // Smoothly move camera position towards the initial position
        camera.position.lerp(initialCameraPosition, alpha * 0.1); // Using a small lerp factor for smoother feel
        // Smoothly move the controls target towards the center
        controls.target.lerp(new THREE.Vector3(0, 0, 0), alpha * 0.1);

        if (alpha >= 1.0) {
            isResetting = false;
        }
    }


    // --- MAIN ANIMATION LOOP ---
    function animate() {
        requestAnimationFrame(animate);
        animateReset(); // Check if we need to run the reset animation
        controls.update(); 
        renderer.render(scene, camera);
    }
    
    // --- Helper & Interaction Functions (same as v5.0) ---
    function createSceneFromNodes(nodes) { /* ... identical ... */ nodeMeshes.forEach(mesh => scene.remove(mesh)); nodeMeshes = []; for (const nodeData of nodes) { const geometry = new THREE.SphereGeometry(nodeData.radius, 36, 36); const material = new THREE.MeshStandardMaterial({ color: nodeData.color, emissive: nodeData.color, emissiveIntensity: 0.05, roughness: params.roughness, metalness: params.metalness, transparent: true, opacity: params.opacity, wireframe: params.wireframe }); const mesh = new THREE.Mesh(geometry, material); mesh.position.set(...nodeData.position); mesh.userData = { id: nodeData.id, name: nodeData.name, info: nodeData.info }; scene.add(mesh); nodeMeshes.push(mesh); } }
    function updateMaterials() { /* ... identical ... */ nodeMeshes.forEach(mesh => { mesh.material.opacity = params.opacity; mesh.material.metalness = params.metalness; mesh.material.roughness = params.roughness; mesh.material.wireframe = params.wireframe; }); }
    const raycaster = new THREE.Raycaster();
    const mouse = new THREE.Vector2();
    const infoPanel = document.getElementById('info');
    let activeNode = null;
    function handleInteraction(event) { /* ... identical ... */ const x = event.touches ? event.touches[0].clientX : event.clientX; const y = event.touches ? event.touches[0].clientY : event.clientY; mouse.x = (x / window.innerWidth) * 2 - 1; mouse.y = - (y / window.innerHeight) * 2 + 1; raycaster.setFromCamera(mouse, camera); const intersects = raycaster.intersectObjects(nodeMeshes); if (intersects.length > 0) { const selectedObject = intersects[0].object; if (activeNode !== selectedObject) { if (activeNode) activeNode.material.emissiveIntensity = 0.05; activeNode = selectedObject; activeNode.material.emissiveIntensity = 0.4; const sanitize = str => { const temp = document.createElement('div'); temp.textContent = str; return temp.innerHTML; }; infoPanel.innerHTML = `<span class="highlight">${sanitize(activeNode.userData.name)}</span><br>${sanitize(activeNode.userData.info)}`; } } }
    window.addEventListener('click', handleInteraction);
    window.addEventListener('touchend', handleInteraction);
    window.addEventListener('resize', () => { /* ... identical ... */ camera.aspect = window.innerWidth / window.innerHeight; camera.updateProjectionMatrix(); renderer.setSize(window.innerWidth, window.innerHeight, false); });

    animate();
  </script>
</body>
</html>
