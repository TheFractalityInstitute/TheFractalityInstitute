<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no" />
  <title>Fractality Bubble UI v14.0 - The Genesis Engine</title>

  <style>
    body { margin: 0; overflow: hidden; background: #111; color: white; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    #overlay { position: fixed; top: 15px; left: 15px; z-index: 10; background: rgba(20, 20, 30, 0.85); padding: 15px; border-radius: 12px; max-width: 320px; backdrop-filter: blur(5px); border: 1px solid rgba(255, 255, 255, 0.1); box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5); }
    #reset-view-btn { position: fixed; top: 15px; right: 15px; z-index: 20; background: rgba(20, 20, 30, 0.85); border: 1px solid rgba(255, 255, 255, 0.1); color: white; font-size: 24px; width: 50px; height: 50px; border-radius: 50%; cursor: pointer; backdrop-filter: blur(5px); text-align: center; line-height: 50px; }
    #edit-nodes-btn { position: fixed; top: 80px; right: 15px; z-index: 20; background: rgba(20, 20, 30, 0.85); border: 1px solid rgba(255, 255, 255, 0.1); color: white; font-size: 24px; width: 50px; height: 50px; border-radius: 50%; cursor: pointer; backdrop-filter: blur(5px); }
    #gui-container { position: absolute; bottom: 0; left: 0; width: 100%; z-index: 20; }
    .dg.main { margin: auto; }
    #node-manager { display: none; position: fixed; right: 15px; top: 145px; width: 320px; max-height: 60%; background: rgba(20, 20, 30, 0.9); backdrop-filter: blur(5px); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; z-index: 30; color: white; padding: 15px; overflow-y: auto; }
    #node-manager h4 { margin-top: 0; color: #6ae6ff; }
    #node-list { list-style-type: none; padding: 0; margin: 0; }
    #node-list li { background: rgba(255,255,255,0.05); border-radius: 4px; padding: 10px; margin-bottom: 8px; }
    #info { font-size: 15px; line-height: 1.6; min-height: 60px; }
    canvas { display: block; position: fixed; z-index: 0; top: 0; left: 0; }
    h3 { margin-top: 0; color: #6ae6ff; border-bottom: 1px solid rgba(100, 200, 255, 0.3); padding-bottom: 8px; }
    .highlight { color: #ffd86e; font-weight: 600; }
  </style>

  <script src="./three.min.js" defer></script>
  <script src="./OrbitControls.js" defer></script>
  <script src="./dat.gui.min.js" defer></script>

</head>
<body>
  <div id="overlay">
    <h3>Fractal Node Information v14.0</h3>
    <div id="info"></div>
  </div>
  <button id="reset-view-btn" title="Reset View">⌂</button>
  <button id="edit-nodes-btn" title="Edit Nodes">✎</button>
  <div id="node-manager"><h4>Node Manager</h4><ul id="node-list"></ul><button>Add New Node</button></div>
  <div id="gui-container"></div>

  <script>
    window.addEventListener('DOMContentLoaded', () => {

        // --- DATA ---
        function getDefaultData() { const nodes = [ { id: 1, name: "The Fractiverse", info: "The total ontological container.", radius: 8, color: "#ffffff" }, { id: 2, name: "Duality", info: "The primal division.", radius: 5, color: "#f0f0f0" }, { id: 3, name: "Motion", info: "Dynamic process.", radius: 3, color: "#87CEEB" }, { id: 10, name: "Stillness", info: "Latent potential.", radius: 3, color: "#9370DB" }, { id: 5, name: "Dimension of Mind", info: "Abstract cognition.", radius: 3.5, color: "#FFD700" }, { id: 12, name: "Chaos", info: "Boundary-membrane.", radius: 2, color: "#DC143C" }, ]; const connections = [ { from: 1, to: 2, type: 'contains' }, { from: 2, to: 3, type: 'contains' }, { from: 2, to: 10, type: 'contains' }, { from: 2, to: 12, type: 'contains' }, { from: 3, to: 5, type: 'contains' }]; return { nodes, connections }; }
        function loadData() { const savedData = localStorage.getItem('fractalityGraphDataV5'); if (savedData) { return JSON.parse(savedData); } return getDefaultData(); }
        
        // --- CORE SETUP ---
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(window.devicePixelRatio);
        document.body.appendChild(renderer.domElement);
        const controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;
        controls.enablePan = false;
        scene.add(new THREE.AmbientLight(0x808080));
        
        // --- STATE & MAPPING ---
        let nodeMeshes = [];
        const { nodes: fractalNodes, connections: fractalConnections } = loadData();
        let activeFocusId = 1;

        fractalNodes.forEach(nodeData => {
            const geometry = new THREE.SphereGeometry(nodeData.radius, 32, 32);
            const material = new THREE.MeshBasicMaterial({ color: nodeData.color, wireframe: true });
            const mesh = new THREE.Mesh(geometry, material);
            mesh.userData = { id: nodeData.id, name: nodeData.name, info: nodeData.info };
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
            // --- THE BUG FIX IS HERE ---
            // Using "fractalConnections" which is correctly defined, instead of "connections".
            const children = fractalConnections.filter(c => c.from === focusId).map(c => c.to);
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

        // --- INTERACTION & UI ---
        const infoPanel = document.getElementById('info');
        const editNodesBtn = document.getElementById('edit-nodes-btn');
        const nodeManagerPanel = document.getElementById('node-manager');
        const nodeList = document.getElementById('node-list');

        function setFocus(newFocusId) {
            activeFocusId = newFocusId;
            const focusNodeData = fractalNodes.find(n => n.id === activeFocusId);
            if(focusNodeData) {
                infoPanel.innerHTML = `<span class="highlight">${focusNodeData.name}</span><br>${focusNodeData.info}`;
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

        editNodesBtn.addEventListener('click', () => {
            const isHidden = nodeManagerPanel.style.display === 'none' || nodeManagerPanel.style.display === '';
            nodeManagerPanel.style.display = isHidden ? 'block' : 'none';
            if (isHidden) { populateNodeList(); }
        });

        function populateNodeList() {
            nodeList.innerHTML = '';
            fractalNodes.forEach(node => {
                const listItem = document.createElement('li');
                listItem.textContent = `${node.name} (ID: ${node.id})`;
                nodeList.appendChild(listItem);
            });
        }

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
        
        // --- RENDER LOOP & LISTENERS ---
        function animate() {
            requestAnimationFrame(animate);
            controls.update(); 
            renderer.render(scene, camera);
        }
        
        window.addEventListener('click', handleInteraction);
        window.addEventListener('touchend', handleInteraction);
        window.addEventListener('resize', () => {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        });

        // --- INITIAL SETUP ---
        setFocus(activeFocusId);
        controls.target.set(0,0,0);
        camera.position.set(0, 0, 45);
        animate();
    });
  </script>
</body>
</html>
