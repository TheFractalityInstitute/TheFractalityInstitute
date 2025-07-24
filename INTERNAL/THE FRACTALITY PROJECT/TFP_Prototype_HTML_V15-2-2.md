<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no" />
  <title>Fractality Bubble UI v15.2.2 - The FUDGE v1</title>

  <script src="./three.min.js" defer></script>
  <script src="./OrbitControls.js" defer></script>
  <script src="./dat.gui.min.js" defer></script>

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
    #node-list li { display: flex; justify-content: space-between; align-items: center; background: rgba(255,255,255,0.05); border-radius: 4px; padding: 10px; margin-bottom: 8px; }
    .delete-btn { background: #dc3545; color: white; border: none; border-radius: 4px; cursor: pointer; padding: 2px 8px; font-weight: bold; margin-left: 10px; }
    #info { font-size: 15px; line-height: 1.6; min-height: 60px; }
    canvas { display: block; position: fixed; z-index: 0; top: 0; left: 0; }
    h3 { margin-top: 0; color: #6ae6ff; border-bottom: 1px solid rgba(100, 200, 255, 0.3); padding-bottom: 8px; }
    .highlight { color: #ffd86e; font-weight: 600; }
  </style>
</head>
<body>
  <div id="overlay">
    <h3>Fractal Node Information v15.2.2</h3>
    <div id="info"></div>
  </div>
  <button id="reset-view-btn" title="Reset View">⌂</button>
  <button id="edit-nodes-btn" title="Edit Nodes">✎</button>
  <div id="node-manager"><h4>Node Manager</h4><ul id="node-list"></ul><button>Add New Node</button></div>
  <div id="gui-container"></div>

  <script>
    window.addEventListener('DOMContentLoaded', () => {

        // --- DATA MANAGEMENT ---
        function getDefaultData() { const nodes = [ { id: 1, name: "The Fractiverse", info: "The total ontological container.", radius: 8, color: "#ffffff" }, { id: 2, name: "Duality", info: "The primal division.", radius: 5, color: "#f0f0f0" }, { id: 3, name: "Motion", info: "Dynamic process.", radius: 3, color: "#87CEEB" }, { id: 10, name: "Stillness", info: "Latent potential.", radius: 3, color: "#9370DB" }, { id: 5, name: "Dimension of Mind", info: "Abstract cognition.", radius: 3.5, color: "#FFD700" }, { id: 12, name: "Chaos", info: "Boundary-membrane.", radius: 2, color: "#DC143C" }, ]; const connections = [ { from: 1, to: 2, type: 'contains' }, { from: 2, to: 3, type: 'contains' }, { from: 2, to: 10, type: 'contains' }, { from: 2, to: 12, type: 'contains' }, { from: 3, to: 5, type: 'contains' }]; return { nodes, connections }; }
        function loadData() { const savedData = localStorage.getItem('fractalityGraphDataV5'); if (savedData) { return JSON.parse(savedData); } return getDefaultData(); }
        function saveData(data) { localStorage.setItem('fractalityGraphDataV5', JSON.stringify(data)); }
        
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
        let { nodes: fractalNodes, connections: fractalConnections } = loadData();
        let activeFocusId = 1;

        function refreshScene() {
            nodeMeshes.forEach(mesh => {
                mesh.geometry.dispose();
                mesh.material.dispose();
                scene.remove(mesh);
            });
            nodeMeshes = [];
            
            fractalNodes.forEach(nodeData => {
                const geometry = new THREE.SphereGeometry(nodeData.radius, 32, 32);
                const material = new THREE.MeshBasicMaterial({ color: nodeData.color, wireframe: true });
                const mesh = new THREE.Mesh(geometry, material);
                mesh.userData = { id: nodeData.id, name: nodeData.name, info: nodeData.info };
                mesh.visible = false;
                scene.add(mesh);
                nodeMeshes.push(mesh);
            });
            setFocus(activeFocusId);
        }
        
        // --- THE F.U.D.G.E. v1 ---
        const params = { nodeSpacing: 15.0 };
        const gui = new dat.GUI({ autoPlace: false });
        document.getElementById('gui-container').appendChild(gui.domElement);
        gui.add(params, 'nodeSpacing', 5, 50).name('Node Spacing').onChange(() => setFocus(activeFocusId));

        function calculateLayout(focusId) {
            const layout = new Map();
            const focusNodeData = fractalNodes.find(n => n.id === focusId);
            if (!focusNodeData) return layout;

            // Find parent and siblings to create the "Family View"
            const parentConnection = fractalConnections.find(c => c.to === focusId);
            const parentId = parentConnection ? parentConnection.from : null;
            
            const siblingsAndSelf = parentId ? fractalConnections.filter(c => c.from === parentId).map(c => c.to) : [focusId];

            // Center the camera on the whole group
            const BoundingBox = new THREE.Box3();
            const selfMesh = nodeMeshes.find(m => m.userData.id === focusId);
            if(selfMesh) BoundingBox.expandByObject(selfMesh);


            layout.set(focusId, { position: new THREE.Vector3(0,0,0) });

            const n = siblingsAndSelf.length;
            const phi = Math.PI * (3 - Math.sqrt(5));
            siblingsAndSelf.forEach((nodeId, i) => {
                if(nodeId === focusId) return; // Skip self, already placed at center
                const y = 1 - (i / (n - 1)) * 2;
                const radius = Math.sqrt(1 - y*y);
                const theta = phi * i;
                const x = Math.cos(theta) * radius;
                const z = Math.sin(theta) * radius;
                const direction = new THREE.Vector3(x, y, z);
                layout.set(nodeId, direction.multiplyScalar(params.nodeSpacing));
            });
            
            return layout;
        }

        // --- INTERACTION & UI ---
        const infoPanel = document.getElementById('info');
        const editNodesBtn = document.getElementById('edit-nodes-btn');
        const nodeManagerPanel = document.getElementById('node-manager');
        const nodeList = document.getElementById('node-list');

        function setFocus(newFocusId) {
            if (!fractalNodes.find(n => n.id === newFocusId)) { newFocusId = 1; }
            activeFocusId = newFocusId;
            const focusNodeData = fractalNodes.find(n => n.id === activeFocusId);
            if(focusNodeData) {
                infoPanel.innerHTML = `<span class="highlight">${focusNodeData.name}</span><br>${focusNodeData.info}`;
            }

            // Simplified Layout Logic
            const children = fractalConnections.filter(c => c.from === activeFocusId).map(c => c.to);
            const visibleIds = new Set(children);
            if(children.length === 0 && activeFocusId === 1) { // Special case for initial view
                 visibleIds.add(1);
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
            
            // Set visibility based on children of the *new* focus
            nodeMeshes.forEach(mesh => {
                if(mesh.userData.id === activeFocusId && children.length === 0){
                    mesh.position.set(0,0,0);
                    mesh.visible = true;
                } else {
                    mesh.visible = children.includes(mesh.userData.id);
                }
            });

            controls.target.set(0,0,0);
        }

        document.getElementById('reset-view-btn').addEventListener('click', () => { 
            if (confirm("Reset ALL data to original defaults? This cannot be undone.")) {
                localStorage.removeItem('fractalityGraphDataV5');
                location.reload();
            }
        });

        editNodesBtn.addEventListener('click', () => {
            nodeManagerPanel.style.display = nodeManagerPanel.style.display === 'none' ? 'block' : 'none';
            if (nodeManagerPanel.style.display === 'block') { populateNodeList(); }
        });

        function populateNodeList() {
            nodeList.innerHTML = '';
            fractalNodes.forEach(node => {
                const listItem = document.createElement('li');
                const nameSpan = document.createElement('span');
                nameSpan.textContent = `${node.name}`;
                listItem.appendChild(nameSpan);
                if (node.id !== 1) {
                    const deleteBtn = document.createElement('button');
                    deleteBtn.textContent = 'x';
                    deleteBtn.className = 'delete-btn';
                    deleteBtn.onclick = (event) => {
                        event.stopPropagation();
                        if (confirm(`Are you sure you want to delete "${node.name}"?`)) {
                            deleteNode(node.id);
                        }
                    };
                    listItem.appendChild(deleteBtn);
                }
                listItem.onclick = () => {
                    setFocus(node.id);
                    nodeManagerPanel.style.display = 'none';
                };
                nodeList.appendChild(listItem);
            });
        }
        
        function deleteNode(nodeIdToDelete) {
            const nodeToDelete = fractalNodes.find(n => n.id === nodeIdToDelete);
            if (!nodeToDelete) return;
            const parentConnection = fractalConnections.find(c => c.to === nodeIdToDelete);
            const parentId = parentConnection ? parentConnection.from : 1;
            const childConnections = fractalConnections.filter(c => c.from === nodeIdToDelete);
            childConnections.forEach(childConn => { childConn.from = parentId; });
            fractalNodes = fractalNodes.filter(n => n.id !== nodeIdToDelete);
            fractalConnections = fractalConnections.filter(c => c.to !== nodeIdToDelete);
            saveData({ nodes: fractalNodes, connections: fractalConnections });
            refreshScene();
            populateNodeList();
        }

        function handleInteraction(event) {
            let x, y;
            if (event.type === 'touchend' && event.changedTouches && event.changedTouches.length > 0) {
                x = event.changedTouches[0].clientX; y = event.changedTouches[0].clientY;
            } else if (event.type === 'click') {
                x = event.clientX; y = event.clientY;
            } else { return; }
            
            const mouse = new THREE.Vector2((x / window.innerWidth) * 2 - 1, - (y / window.innerHeight) * 2 + 1);
            const raycaster = new THREE.Raycaster();
            raycaster.setFromCamera(mouse, camera);
            const intersects = raycaster.intersectObjects(nodeMeshes.filter(m => m.visible));
            if (intersects.length > 0) {
                setFocus(intersects[0].object.userData.id);
            }
        }
        
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
        refreshScene();
        // Correct initial view to show Fractiverse itself
        const fractiverseMesh = nodeMeshes.find(m => m.userData.id === 1);
        if(fractiverseMesh) {
            fractiverseMesh.visible = true;
            fractiverseMesh.position.set(0,0,0);
        }
        setFocus(1); // Set info panel correctly
        nodeMeshes.forEach(mesh => { // Ensure only root is visible initially
            mesh.visible = (mesh.userData.id === 1);
        });
        camera.position.set(0, 0, 45);
        controls.target.set(0,0,0);
    });
  </script>
</body>
</html>
