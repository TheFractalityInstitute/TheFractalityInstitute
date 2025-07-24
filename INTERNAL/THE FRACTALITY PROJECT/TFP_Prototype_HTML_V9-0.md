<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no" />
  <title>Fractality Bubble UI v9.0 - The Geometric Engine</title>
  
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
    #info { font-size: 15px; line-height: 1.6; min-height: 60px; }
    canvas { display: block; position: fixed; z-index: 0; top: 0; left: 0; }
    h3 { margin-top: 0; color: #6ae6ff; border-bottom: 1px solid rgba(100, 200, 255, 0.3); padding-bottom: 8px; }
    .highlight { color: #ffd86e; font-weight: 600; }
  </style>
</head>
<body>
  <div id="overlay">
    <h3>Fractal Node Information v9.0</h3>
    <div id="info">⟡ A universe of clarity.</div>
  </div>

  <button id="reset-view-btn" title="Reset View">⌂</button>
  <div id="gui-container" style="position: absolute; bottom: 0; left: 0; width: 100%; z-index: 20;"></div>


  <script src="./dat.gui.min.js"></script>
  <script type="module">
    import * as THREE from 'three';
    import { OrbitControls } from './OrbitControls.js';

    function getDefaultData() { const nodes = [ { id: 1, name: "The Fractiverse", info: "The total ontological container.", radius: 8, color: "#ffffff" }, { id: 2, name: "Duality", info: "The primal division.", radius: 5, color: "#f0f0f0" }, { id: 3, name: "Motion", info: "Dynamic process.", radius: 3, color: "#87CEEB" }, { id: 10, name: "Stillness", info: "Latent potential.", radius: 3, color: "#9370DB" }, { id: 5, name: "Dimension of Mind", info: "Abstract cognition.", radius: 3.5, color: "#FFD700" }, { id: 15, name: "Unity Field", info: "Meta-ethical substrate.", radius: 3, color: "#E0FFFF" }, { id: 12, name: "Chaos", info: "Boundary-membrane.", radius: 2, color: "#DC143C" }, { id: 14, name: "Shadow Integration", info: "Reconciling dissonant aspects.", radius: 1.5, color: "#C0C0C0" }, { id: 9, name: "GLYPH", info: "Symbolic interface.", radius: 1.5, color: "#40E0D0" }, ]; const connections = [ { from: 1, to: 2, type: 'contains', weight: 1.0 }, { from: 2, to: 3, type: 'contains', weight: 1.0 }, { from: 2, to: 10, type: 'contains', weight: 1.0 }, { from: 2, to: 12, type: 'contains', weight: 0.8 }, { from: 3, to: 5, type: 'contains', weight: 1.0 }, { from: 15, to: 5, type: 'resonates_with', weight: 0.6 }, { from: 9, to: 15, type: 'interfaces_with', weight: 0.5 }, { from: 14, to: 12, type: 'works_on', weight: 0.7 }, { from: 14, to: 5, type: 'informs', weight: 0.4 }, ]; return { nodes, connections }; }
    function loadData() { const savedData = localStorage.getItem('fractalityGraphData'); if (savedData) { return JSON.parse(savedData); } return getDefaultData(); }
    
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    document.body.appendChild(renderer.domElement);
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    scene.add(new THREE.AmbientLight(0x808080));
    const pointLight = new THREE.PointLight(0xffffff, 1.0, 500);
    scene.add(pointLight);

    let nodeMeshes = [];
    const { nodes: fractalNodes, connections: fractalConnections } = loadData();
    let activeFocusId = 1;
    let nodeAnimations = [];
    const HIGHLIGHT_COLOR = new THREE.Color("#ffd86e");

    const adjacencyMap = new Map();
    fractalNodes.forEach(node => adjacencyMap.set(node.id, []));
    fractalConnections.forEach(conn => {
        adjacencyMap.get(conn.from).push(conn.to);
        adjacencyMap.get(conn.to).push(conn.from);
    });

    function createSceneFromNodes(nodes) {
        nodes.forEach(nodeData => {
            const geometry = new THREE.SphereGeometry(nodeData.radius, 36, 36);
            const material = new THREE.MeshStandardMaterial({ color: nodeData.color, transparent: true, opacity: 0.9, wireframe: true, roughness: 0.5 });
            const mesh = new THREE.Mesh(geometry, material);
            mesh.userData = { id: nodeData.id, name: nodeData.name, info: nodeData.info, originalColor: new THREE.Color(nodeData.color) };
            scene.add(mesh);
            nodeMeshes.push(mesh);
        });
    }
    createSceneFromNodes(fractalNodes);
    
    // --- NEW DETERMINISTIC LAYOUT ENGINE ---
    const params = { nodeSpacing: 2.5 };
    const gui = new dat.GUI({ autoPlace: false });
    document.getElementById('gui-container').appendChild(gui.domElement);
    gui.add(params, 'nodeSpacing', 1, 10).name('Node Spacing').onChange(() => setFocus(activeFocusId, true));

    function calculateLayout(focusId) {
        const layout = new Map();
        const focusNodeData = fractalNodes.find(n => n.id === focusId);
        if (!focusNodeData) return layout;

        // Center the focus node
        layout.set(focusId, { position: new THREE.Vector3(0, 0, 0), visible: true });

        // Get its direct neighbors
        const neighbors = adjacencyMap.get(focusId) || [];
        const n = neighbors.length;
        const phi = Math.PI * (3 - Math.sqrt(5)); // Golden angle

        // Arrange neighbors around the focus node
        neighbors.forEach((neighborId, i) => {
            const neighborData = fractalNodes.find(n => n.id === neighborId);
            if (!neighborData) return;

            const y = 1 - (i / (n - 1)) * 2;
            const radius = Math.sqrt(1 - y * y);
            const theta = phi * i;
            const x = Math.cos(theta) * radius;
            const z = Math.sin(theta) * radius;

            const direction = new THREE.Vector3(x, y, z);
            const distance = focusNodeData.radius + neighborData.radius + params.nodeSpacing;
            const position = direction.multiplyScalar(distance);
            layout.set(neighborId, { position, visible: true });
        });
        return layout;
    }

    function animateToLayout(newLayout) {
        nodeAnimations = []; // Clear old animations
        nodeMeshes.forEach(mesh => {
            const targetState = newLayout.get(mesh.userData.id);
            const startPos = mesh.position.clone();
            const startOpacity = mesh.material.opacity;
            
            if (targetState) { // Node is in the new layout
                nodeAnimations.push({
                    mesh: mesh,
                    startPos: startPos,
                    endPos: targetState.position,
                    startOpacity: startOpacity,
                    endOpacity: 0.9,
                    alpha: 0
                });
                mesh.visible = true;
            } else { // Node is not in the new layout, fade it out and move it away
                nodeAnimations.push({
                    mesh: mesh,
                    startPos: startPos,
                    endPos: startPos.clone().normalize().multiplyScalar(100), // Move far away
                    startOpacity: startOpacity,
                    endOpacity: 0,
                    alpha: 0
                });
            }
        });
    }

    const clock = new THREE.Clock();
    function animate() {
        requestAnimationFrame(animate);
        const deltaTime = clock.getDelta();

        // Animate nodes to their new positions
        nodeAnimations.forEach(anim => {
            if (anim.alpha < 1) {
                anim.alpha += deltaTime * 2.0; // Animation speed
                anim.alpha = Math.min(anim.alpha, 1);
                const easeAlpha = 1 - Math.pow(1 - anim.alpha, 3);
                anim.mesh.position.lerpVectors(anim.startPos, anim.endPos, easeAlpha);
                anim.mesh.material.opacity = THREE.MathUtils.lerp(anim.startOpacity, anim.endOpacity, easeAlpha);
                if (anim.alpha === 1 && anim.endOpacity === 0) {
                    anim.mesh.visible = false;
                }
            }
        });

        controls.update(); 
        pointLight.position.copy(camera.position);
        renderer.render(scene, camera);
    }
    
    const raycaster = new THREE.Raycaster();
    const mouse = new THREE.Vector2();
    const infoPanel = document.getElementById('info');
    
    function setFocus(newFocusId) {
        if (activeFocusId === newFocusId && nodeAnimations.every(a => a.alpha === 1)) return;
        
        activeFocusId = newFocusId;
        const newLayout = calculateLayout(activeFocusId);
        animateToLayout(newLayout);
        
        // Update highlight color and info panel
        nodeMeshes.forEach(mesh => {
             mesh.material.color.copy(mesh.userData.originalColor);
        });
        const focusMesh = nodeMeshes.find(m => m.userData.id === activeFocusId);
        if (focusMesh) {
            focusMesh.material.color.copy(HIGHLIGHT_COLOR);
            const sanitize = str => { const temp = document.createElement('div'); temp.textContent = str; return temp.innerHTML; };
            infoPanel.innerHTML = `<span class="highlight">${focusMesh.userData.name}</span><br>${sanitize(focusMesh.userData.info)}`;
        }
    }

    document.getElementById('reset-view-btn').addEventListener('click', () => { 
        setFocus(1);
        // Also reset camera
        controls.target.set(0,0,0);
        camera.position.set(0, 0, 45);
    });

    function handleInteraction(event) {
        const x = event.touches ? event.touches[0].clientX : event.clientX;
        const y = event.touches ? event.touches[0].clientY : event.clientY;
        mouse.x = (x / window.innerWidth) * 2 - 1;
        mouse.y = - (y / window.innerHeight) * 2 + 1;
        raycaster.setFromCamera(mouse, camera);
        const intersects = raycaster.intersectObjects(nodeMeshes.filter(m => m.visible));
        if (intersects.length > 0) {
            const selectedObject = intersects[0].object;
            setFocus(selectedObject.userData.id);
        }
    }
    
    window.addEventListener('click', handleInteraction);
    window.addEventListener('touchend', handleInteraction);
    window.addEventListener('resize', () => { camera.aspect = window.innerWidth / window.innerHeight; camera.updateProjectionMatrix(); renderer.setSize(window.innerWidth, window.innerHeight, false); });

    // Initial setup
    setFocus(activeFocusId);
    controls.target.set(0,0,0);
    camera.position.set(0, 0, 45);
    animate();
  </script>
</body>
</html>
