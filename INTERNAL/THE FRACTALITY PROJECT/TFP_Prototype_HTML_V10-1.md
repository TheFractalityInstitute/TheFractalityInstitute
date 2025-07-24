<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no" />
  <title>Fractality Bubble UI v10.1 - The Grand Finale</title>
  
  <script type="importmap">
  {
    "imports": {
      "three": "./three.module.js",
      "OrbitControls": "./OrbitControls.js"
    }
  }
  </script>

  <style>
    body { margin: 0; overflow: hidden; background: #111; color: white; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    #overlay { position: fixed; top: 15px; left: 15px; z-index: 10; background: rgba(20, 20, 30, 0.85); padding: 15px; border-radius: 12px; max-width: 320px; backdrop-filter: blur(5px); border: 1px solid rgba(255, 255, 255, 0.1); box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5); }
    #reset-view-btn { position: fixed; top: 15px; right: 15px; z-index: 20; background: rgba(20, 20, 30, 0.85); border: 1px solid rgba(255, 255, 255, 0.1); color: white; font-size: 24px; width: 50px; height: 50px; border-radius: 50%; cursor: pointer; backdrop-filter: blur(5px); text-align: center; line-height: 50px; }
    #gui-container { position: absolute; bottom: 0; left: 0; width: 100%; z-index: 20; }
    .dg.main { margin: auto; }
    #info { font-size: 15px; line-height: 1.6; min-height: 60px; }
    canvas { display: block; position: fixed; z-index: 0; top: 0; left: 0; }
    h3 { margin-top: 0; color: #6ae6ff; border-bottom: 1px solid rgba(100, 200, 255, 0.3); padding-bottom: 8px; }
    .highlight { color: #ffd86e; font-weight: 600; }
  </style>
</head>
<body>
  <div id="overlay">
    <h3>Fractal Node Information v10.1</h3>
    <div id="info"></div>
  </div>
  <button id="reset-view-btn" title="Reset View">⌂</button>
  <div id="gui-container"></div>

  <script src="./dat.gui.min.js"></script>
  <script type="module">
    // --- IMPORTS NOW USE THE CORRECT MAP ---
    import * as THREE from 'three';
    import { OrbitControls } from 'OrbitControls';

    // --- DATA ---
    function getDefaultData() { const nodes = [ { id: 1, name: "The Fractiverse", info: "The total ontological container.", radius: 8, color: "#ffffff" }, { id: 2, name: "Duality", info: "The primal division.", radius: 5, color: "#f0f0f0" }, { id: 3, name: "Motion", info: "Dynamic process.", radius: 3, color: "#87CEEB" }, { id: 10, name: "Stillness", info: "Latent potential.", radius: 3, color: "#9370DB" }, { id: 5, name: "Dimension of Mind", info: "Abstract cognition.", radius: 3.5, color: "#FFD700" }, { id: 12, name: "Chaos", info: "Boundary-membrane.", radius: 2, color: "#DC143C" }, ]; const connections = [ { from: 1, to: 2, type: 'contains' }, { from: 2, to: 3, type: 'contains' }, { from: 2, to: 10, type: 'contains' }, { from: 2, to: 12, type: 'contains' }, { from: 3, to: 5, type: 'contains' }]; return { nodes, connections }; }
    function loadData() { const savedData = localStorage.getItem('fractalityGraphDataV4'); if (savedData) { return JSON.parse(savedData); } return getDefaultData(); }
    
    // --- CORE SETUP ---
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    document.body.appendChild(renderer.domElement);
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.enablePan = false;
    scene.add(new THREE.AmbientLight(0x808080));
    const pointLight = new THREE.PointLight(0xffffff, 1.0, 500);
    scene.add(pointLight);

    // --- STATE & DATA MAPPING ---
    let nodeMeshes = [];
    const { nodes: fractalNodes, connections: fractalConnections } = loadData();
    let activeFocusId = 1;
    const HIGHLIGHT_COLOR = new THREE.Color("#ffd86e");

    fractalNodes.forEach(nodeData => {
        const geometry = new THREE.SphereGeometry(nodeData.radius, 32, 32);
        const material = new THREE.MeshBasicMaterial({ color: nodeData.color, wireframe: true });
        const mesh = new THREE.Mesh(geometry, material);
        mesh.userData = { id: nodeData.id, name: nodeData.name, info: nodeData.info, originalColor: new THREE.Color(nodeData.color) };
        mesh.visible = false;
        scene.add(mesh);
        nodeMeshes.push(mesh);
    });
    
    // --- THE DETERMINISTIC LAYOUT ENGINE ---
    const params = { nodeSpacing: 15.0 };
    const gui = new dat.GUI({ autoPlace: false });
    document.getElementById('gui-container').appendChild(gui.domElement);
    gui.add(params, 'nodeSpacing', 5, 50).name('Node Spacing').onChange(() => setFocus(activeFocusId));

    function calculateLayout(focusId) {
        const layout = new Map();
        const children = connections.filter(c => c.from === focusId).map(c => c.to);
        const n = children.length;
        if (n === 0) return layout;
        
        const phi = Math.PI * (3 - Math.sqrt(5));

        children.forEach((childId, i) => {
            const y = 1 - (i / (n === 1 ? 2 : n - 1)) * 2;
            const radius = Math.sqrt(1 - y * y);
            const theta = phi * i;
            const x = Math.cos(theta) * radius;
            const z = Math.sin(theta) * radius;
            const direction = new THREE.Vector3(x, y, z);
            layout.set(childId, direction.multiplyScalar(params.nodeSpacing));
        });
        return layout;
    }

    // --- INTERACTION & ANIMATION ---
    const infoPanel = document.getElementById('info');
    
    function setFocus(newFocusId) {
        activeFocusId = newFocusId;
        const focusNodeData = fractalNodes.find(n => n.id === activeFocusId);
        
        if(focusNodeData) {
            const sanitize = str => { const temp = document.createElement('div'); temp.textContent = str; return temp.innerHTML; };
            infoPanel.innerHTML = `<span class="highlight">${sanitize(focusNodeData.name)}</span><br>${sanitize(focusNodeData.info)}`;
        }
        
        const newLayout = calculateLayout(activeFocusId);
        nodeMeshes.forEach(mesh => {
            const targetPos = newLayout.get(mesh.userData.id);
            if (targetPos) {
                mesh.position.copy(targetPos);
                mesh.visible = true;
            } else {
                mesh.visible = false;
            }
        });
    }

    document.getElementById('reset-view-btn').addEventListener('click', () => { 
        setFocus(1);
        controls.target.set(0,0,0);
        camera.position.set(0, 0, 45);
    });

    function handleInteraction(event) {
        const x = event.touches ? event.touches[0].clientX : event.clientX;
        const y = event.touches ? event.touches[0].clientY : event.clientY;
        const mouse = new THREE.Vector2((x / window.innerWidth) * 2 - 1, - (y / window.innerHeight) * 2 + 1);
        const raycaster = new THREE.Raycaster();
        raycaster.setFromCamera(mouse, camera);
        const intersects = raycaster.intersectObjects(nodeMeshes.filter(m => m.visible));
        if (intersects.length > 0) {
            setFocus(intersects[0].object.userData.id);
        }
    }
    
    const clock = new THREE.Clock();
    function animate() {
        requestAnimationFrame(animate);
        controls.update(); 
        pointLight.position.copy(camera.position);
        renderer.render(scene, camera);
    }
    
    window.addEventListener('click', handleInteraction);
    window.addEventListener('touchend', handleInteraction);
    window.addEventListener('resize', () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight, false);
    });

    // Initial setup
    setFocus(activeFocusId);
    controls.target.set(0,0,0);
    camera.position.set(0, 0, 45);
    animate();
  </script>
</body>
</html>
