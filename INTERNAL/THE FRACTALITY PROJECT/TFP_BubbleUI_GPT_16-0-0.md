<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no" />
  <title>Fractality Bubble UI v16.0.0 - FUDGE + Hierarchy</title>

  <script src="./three.min.js" defer></script>
  <script src="./OrbitControls.js" defer></script>
  <script src="./dat.gui.min.js" defer></script>

  <style>
    body { margin: 0; overflow: hidden; background: #111; color: white; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    #overlay { position: fixed; top: 15px; left: 15px; z-index: 10; background: rgba(20, 20, 30, 0.85); padding: 15px; border-radius: 12px; max-width: 320px; backdrop-filter: blur(5px); border: 1px solid rgba(255, 255, 255, 0.1); box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5); }
    #reset-view-btn, #edit-nodes-btn { position: fixed; top: 15px; z-index: 20; background: rgba(20, 20, 30, 0.85); border: 1px solid rgba(255, 255, 255, 0.1); color: white; font-size: 24px; width: 50px; height: 50px; border-radius: 50%; cursor: pointer; backdrop-filter: blur(5px); text-align: center; line-height: 50px; }
    #reset-view-btn { right: 15px; }
    #edit-nodes-btn { right: 75px; }
    #node-manager { display: none; position: fixed; right: 15px; top: 80px; width: 330px; max-height: 70%; background: rgba(20, 20, 30, 0.95); backdrop-filter: blur(5px); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; z-index: 30; color: white; padding: 15px; overflow-y: auto; font-size: 14px; }
    #node-manager h4 { margin-top: 0; color: #6ae6ff; }
    .tree-node { margin: 4px 0; padding-left: 10px; border-left: 1px solid rgba(255,255,255,0.1); }
    .node-label { display: flex; align-items: center; justify-content: space-between; cursor: pointer; background: rgba(255,255,255,0.05); border-radius: 4px; padding: 6px 8px; margin-bottom: 4px; }
    .child-nodes { margin-left: 10px; }
    .toggle-btn { background: none; border: none; color: #6ae6ff; font-weight: bold; font-size: 16px; margin-right: 5px; }
    #add-node-btn { width: 100%; padding: 10px; background: #6ae6ff; color: #111; border: none; border-radius: 4px; font-weight: bold; margin-top: 10px; cursor: pointer; }
    #info { font-size: 15px; line-height: 1.6; min-height: 60px; }
    canvas { display: block; position: fixed; z-index: 0; top: 0; left: 0; }
    h3 { margin-top: 0; color: #6ae6ff; border-bottom: 1px solid rgba(100, 200, 255, 0.3); padding-bottom: 8px; }
    .highlight { color: #ffd86e; font-weight: 600; }
  </style>
</head>
<body>
  <div id="overlay">
    <h3>Fractal Node Information</h3>
    <div id="info"></div>
  </div>
  <button id="reset-view-btn" title="Reset View">⌂</button>
  <button id="edit-nodes-btn" title="Edit Nodes">✎</button>
  <div id="node-manager"><h4>Node Hierarchy</h4><div id="tree-root"></div><button id="add-node-btn">Add New Node</button></div>

  <script>
    window.addEventListener('DOMContentLoaded', () => {
      const getDefaultData = () => ({
        nodes: [
          { id: 1, name: "The Fractiverse", info: "The total ontological container.", radius: 8, color: "#ffffff" },
          { id: 2, name: "Duality", info: "The primal division.", radius: 5, color: "#f0f0f0" },
          { id: 3, name: "Motion", info: "Dynamic process.", radius: 3, color: "#87CEEB" },
          { id: 10, name: "Stillness", info: "Latent potential.", radius: 3, color: "#9370DB" },
          { id: 5, name: "Dimension of Mind", info: "Abstract cognition.", radius: 3.5, color: "#FFD700" },
          { id: 12, name: "Chaos", info: "Boundary-membrane.", radius: 2, color: "#DC143C" },
        ],
        connections: [
          { from: 1, to: 2 },
          { from: 2, to: 3 },
          { from: 2, to: 10 },
          { from: 2, to: 12 },
          { from: 3, to: 5 },
        ]
      });

      const saveData = (data) => localStorage.setItem('fractalityGraphDataV5', JSON.stringify(data));
      const loadData = () => {
        const saved = localStorage.getItem('fractalityGraphDataV5');
        return saved ? JSON.parse(saved) : getDefaultData();
      };

      let { nodes, connections } = loadData();

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

      const nodeMeshes = new Map();
      const params = { nodeSpacing: 15 };
      const gui = new dat.GUI({ autoPlace: false });
      document.body.appendChild(gui.domElement);
      gui.add(params, 'nodeSpacing', 5, 50).name('Node Spacing').onChange(() => refreshScene());

      const infoPanel = document.getElementById('info');
      let activeFocusId = 1;

      const refreshScene = () => {
        nodeMeshes.forEach(mesh => {
          scene.remove(mesh);
          mesh.geometry.dispose();
          mesh.material.dispose();
        });
        nodeMeshes.clear();

        nodes.forEach(node => {
          const geom = new THREE.SphereGeometry(node.radius, 32, 32);
          const mat = new THREE.MeshBasicMaterial({ color: node.color, wireframe: true });
          const mesh = new THREE.Mesh(geom, mat);
          mesh.userData = { id: node.id, name: node.name, info: node.info };
          mesh.visible = false;
          scene.add(mesh);
          nodeMeshes.set(node.id, mesh);
        });

        updateLayout();
      };

      const getChildren = (id) => connections.filter(c => c.from === id).map(c => c.to);
      const calculateLayout = (focusId) => {
        const layout = new Map();
        const children = getChildren(focusId);
        const n = children.length;
        const phi = Math.PI * (3 - Math.sqrt(5));
        children.forEach((id, i) => {
          const y = 1 - (i / (n - 1 || 1)) * 2;
          const r = Math.sqrt(1 - y * y);
          const theta = phi * i;
          const x = Math.cos(theta) * r;
          const z = Math.sin(theta) * r;
          layout.set(id, new THREE.Vector3(x, y, z).multiplyScalar(params.nodeSpacing));
        });
        return layout;
      };

      const updateLayout = () => {
        const layout = calculateLayout(activeFocusId);
        nodeMeshes.forEach((mesh, id) => {
          if (id === activeFocusId) {
            mesh.position.set(0, 0, 0);
            mesh.visible = true;
          } else if (layout.has(id)) {
            mesh.position.copy(layout.get(id));
            mesh.visible = true;
          } else {
            mesh.visible = false;
          }
        });
        const focusNode = nodes.find(n => n.id === activeFocusId);
        if (focusNode) {
          infoPanel.innerHTML = `<span class="highlight">${focusNode.name}</span><br>${focusNode.info}`;
        }
      };

      const setFocus = (id) => {
        activeFocusId = id;
        updateLayout();
        controls.target.set(0, 0, 0);
      };

      const handleInteraction = (event) => {
        const x = event.touches ? event.touches[0].clientX : event.clientX;
        const y = event.touches ? event.touches[0].clientY : event.clientY;
        const mouse = new THREE.Vector2((x / window.innerWidth) * 2 - 1, -(y / window.innerHeight) * 2 + 1);
        const raycaster = new THREE.Raycaster();
        raycaster.setFromCamera(mouse, camera);
        const intersects = raycaster.intersectObjects([...nodeMeshes.values()].filter(m => m.visible));
        if (intersects.length) {
          setFocus(intersects[0].object.userData.id);
        }
      };

      const animate = () => {
        requestAnimationFrame(animate);
        controls.update();
        renderer.render(scene, camera);
      };

      window.addEventListener('click', handleInteraction);
      window.addEventListener('touchend', handleInteraction);
      window.addEventListener('resize', () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
      });

      document.getElementById('edit-nodes-btn').addEventListener('click', () => {
        const nodePanel = document.getElementById('node-manager');
        const isHidden = nodePanel.style.display === 'none' || nodePanel.style.display === '';
        nodePanel.style.display = isHidden ? 'block' : 'none';
        if (isHidden) populateTreeUI();
      });

      document.getElementById('reset-view-btn').addEventListener('click', () => {
        if (confirm("Reset ALL data to default? This cannot be undone.")) {
          localStorage.removeItem('fractalityGraphDataV5');
          location.reload();
        }
      });

      document.getElementById('add-node-btn').addEventListener('click', () => {
        const parentList = nodes.map(n => `${n.id}: ${n.name}`).join('\n');
        const parentId = parseInt(prompt(`Choose a parent node ID:\n${parentList}`));
        const parentNode = nodes.find(n => n.id === parentId);
        if (!parentNode) return alert("Invalid parent ID.");

        const name = prompt("Enter the node name:");
        const info = prompt("Enter node info:");
        const newId = Math.max(...nodes.map(n => n.id)) + 1;
        const newRadius = parentNode.radius * 0.6;
        const parentColor = new THREE.Color(parentNode.color);
        const newColor = parentColor.offsetHSL(0.1, 0.05, 0);

        const newNode = { id: newId, name, info, radius: newRadius, color: `#${newColor.getHexString()}` };
        const newConnection = { from: parentId, to: newId };

        nodes.push(newNode);
        connections.push(newConnection);
        saveData({ nodes, connections });
        populateTreeUI();
        refreshScene();
      });

      const buildTree = (id) => {
        const node = nodes.find(n => n.id === id);
        if (!node) return null;
        return {
          ...node,
          children: getChildren(id).map(childId => buildTree(childId))
        };
      };

      const renderTree = (tree, container) => {
        const wrapper = document.createElement('div');
        wrapper.className = 'tree-node';
        const label = document.createElement('div');
        label.className = 'node-label';
        label.innerHTML = `<span>${tree.name}</span>`;
        label.onclick = () => setFocus(tree.id);
        wrapper.appendChild(label);
        if (tree.children.length > 0) {
          const childWrapper = document.createElement('div');
          childWrapper.className = 'child-nodes';
          tree.children.forEach(child => renderTree(child, childWrapper));
          wrapper.appendChild(childWrapper);
        }
        container.appendChild(wrapper);
      };

      const populateTreeUI = () => {
        const treeRoot = document.getElementById('tree-root');
        treeRoot.innerHTML = '';
        const rootTree = buildTree(1);
        if (rootTree) renderTree(rootTree, treeRoot);
      };

      camera.position.set(0, 0, 45);
      refreshScene();
      animate();
    });
  </script>
</body>
</html>