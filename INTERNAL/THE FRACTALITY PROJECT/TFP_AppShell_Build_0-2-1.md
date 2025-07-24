<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no" />
  <title>TFP AppShell Build v0.2.1</title>
  
  <script src="./three.min.js" defer></script>
  <script src="./OrbitControls.js" defer></script>

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
    <h3>Fractal Node Information v0.2.1</h3>
    <div id="info"></div>
  </div>
  <button id="reset-view-btn" title="Reset View">⌂</button>

  <script>
    window.addEventListener('DOMContentLoaded', () => {

        // --- DATA MANAGEMENT ---
        function getDefaultData() { const nodes = [ { id: 1, name: "The Fractiverse", info: "The total ontological container.", radius: 8, color: "#ffffff" }, { id: 2, name: "Duality", info: "The primal division.", radius: 5, color: "#f0f0f0" }, { id: 3, name: "Motion", info: "Dynamic process.", radius: 3, color: "#87CEEB" }, { id: 10, name: "Stillness", info: "Latent potential.", radius: 3, color: "#9370DB" }, { id: 5, name: "Dimension of Mind", info: "Abstract cognition.", radius: 3.5, color: "#FFD700" }, { id: 12, name: "Chaos", info: "Boundary-membrane.", radius: 2, color: "#DC143C" }, ]; const connections = [ { from: 1, to: 2, type: 'contains' }, { from: 2, to: 3, type: 'contains' }, { from: 2, to: 10, type: 'contains' }, { from: 2, to: 12, type: 'contains' }, { from: 3, to: 5, type: 'contains' }]; return { nodes, connections }; }
        const { nodes: fractalNodes, connections: fractalConnections } = getDefaultData();
        
        // --- CORE SETUP ---
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(window.devicePixelRatio);
        document.body.appendChild(renderer.domElement);
        const controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;
        
        // --- STATE & MAPPING ---
        let activeFocusId = 1;
        let instancedMesh;
        let visibleNodes = []; // Array to track which nodes are currently visible and their instance index
        const tempObject = new THREE.Object3D();
        const tempColor = new THREE.Color();

        // --- INSTANCED MESH SETUP ---
        const geometry = new THREE.SphereGeometry(1, 32, 32);
        // THE BUG FIX IS HERE: Removed "vertexColors: true" which conflicts with setColorAt()
        const material = new THREE.MeshBasicMaterial({ wireframe: true });
        
        instancedMesh = new THREE.InstancedMesh(geometry, material, fractalNodes.length);
        // This tells the material to use the colors we set per instance
        material.vertexColors = true;
        material.needsUpdate = true;
        
        scene.add(instancedMesh);

        // --- THE F.U.D.G.E. (Layout Engine) ---
        const NODE_SPACING = 15.0;
        function calculateLayout(focusId) {
            const layout = new Map();
            const childrenIds = connections.filter(c => c.from === focusId).map(c => c.to);
            const n = childrenIds.length;
            
            if (n === 0) { // If a node has no children, display itself at the center
                layout.set(focusId, { position: new THREE.Vector3(0,0,0) });
                return layout;
            }
            if (n === 1) { // If it has one child, display that child at the center
                layout.set(childrenIds[0], { position: new THREE.Vector3(0,0,0) });
                return layout;
            }

            const phi = Math.PI * (3 - Math.sqrt(5));
            childrenIds.forEach((childId, i) => {
                const y = 1 - (i / (n - 1)) * 2;
                const radius = Math.sqrt(1 - y * y);
                const theta = phi * i;
                const x = Math.cos(theta) * radius;
                const z = Math.sin(theta) * radius;
                layout.set(childId, { position: new THREE.Vector3(x, y, z).multiplyScalar(NODE_SPACING) });
            });
            return layout;
        }

        // --- INTERACTION & UI ---
        const infoPanel = document.getElementById('info');
        
        function setFocus(newFocusId) {
            activeFocusId = newFocusId;
            const focusNodeData = fractalNodes.find(n => n.id === activeFocusId);
            if(focusNodeData) {
                infoPanel.innerHTML = `<span class="highlight">${focusNodeData.name}</span><br>${focusNodeData.info}`;
            }
            
            const newLayout = calculateLayout(activeFocusId);
            
            visibleNodes = [];
            fractalNodes.forEach(node => {
                if (newLayout.has(node.id)) {
                    visibleNodes.push(node);
                }
            });
            
            instancedMesh.count = visibleNodes.length;
            visibleNodes.forEach((nodeData, i) => {
                const layoutData = newLayout.get(nodeData.id);
                
                tempObject.position.copy(layoutData.position);
                tempObject.scale.setScalar(nodeData.radius);
                tempObject.updateMatrix();
                instancedMesh.setMatrixAt(i, tempObject.matrix);
                instancedMesh.setColorAt(i, tempColor.set(nodeData.color));
            });

            instancedMesh.instanceMatrix.needsUpdate = true;
            if (instancedMesh.instanceColor) {
                instancedMesh.instanceColor.needsUpdate = true;
            }
            
            controls.target.set(0,0,0);
        }

        document.getElementById('reset-view-btn').addEventListener('click', () => { 
            setFocus(1);
            camera.position.set(0, 0, 45);
        });

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
            
            const intersects = raycaster.intersectObject(instancedMesh);

            if (intersects.length > 0) {
                const instanceId = intersects[0].instanceId;
                const clickedNode = visibleNodes[instanceId];
                if(clickedNode) {
                    setFocus(clickedNode.id);
                }
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
        camera.position.set(0, 0, 45);
        animate();
    });
  </script>
</body>
</html>
