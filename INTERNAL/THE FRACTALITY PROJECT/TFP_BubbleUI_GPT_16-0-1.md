<!DOCTYPE html><html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no" />
  <title>Fractality Bubble UI v16.0.1 - Hierarchical View</title>  <script src="./three.min.js" defer></script>  <script src="./OrbitControls.js" defer></script>  <script src="./dat.gui.min.js" defer></script>  <style>
    body { margin: 0; overflow: hidden; background: #111; color: white; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    #overlay { position: fixed; top: 15px; left: 15px; z-index: 10; background: rgba(20, 20, 30, 0.85); padding: 15px; border-radius: 12px; max-width: 320px; backdrop-filter: blur(5px); border: 1px solid rgba(255, 255, 255, 0.1); box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5); }
    #reset-view-btn { position: fixed; top: 15px; right: 15px; z-index: 20; background: rgba(20, 20, 30, 0.85); border: 1px solid rgba(255, 255, 255, 0.1); color: white; font-size: 24px; width: 50px; height: 50px; border-radius: 50%; cursor: pointer; backdrop-filter: blur(5px); text-align: center; line-height: 50px; }
    #edit-nodes-btn { position: fixed; top: 80px; right: 15px; z-index: 20; background: rgba(20, 20, 30, 0.85); border: 1px solid rgba(255, 255, 255, 0.1); color: white; font-size: 24px; width: 50px; height: 50px; border-radius: 50%; cursor: pointer; backdrop-filter: blur(5px); }
    #gui-container { position: absolute; bottom: 0; left: 0; width: 100%; z-index: 20; }
    .dg.main { margin: auto; }
    #node-manager { display: none; position: fixed; right: 15px; top: 145px; width: 320px; max-height: 60%; background: rgba(20, 20, 30, 0.9); backdrop-filter: blur(5px); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; z-index: 30; color: white; padding: 15px; overflow-y: auto; }
    #node-manager h4 { margin-top: 0; color: #6ae6ff; }
    #tree-root { font-size: 14px; line-height: 1.6; }
    .tree-node { cursor: pointer; display: block; margin-bottom: 4px; }
    .tree-indent { display: inline-block; width: 1em; }
    #add-node-btn { width: 100%; padding: 10px; background: #6ae6ff; color: #111; border: none; border-radius: 4px; font-weight: bold; margin-top: 10px; cursor: pointer; }
    #info { font-size: 15px; line-height: 1.6; min-height: 60px; }
    canvas { display: block; position: fixed; z-index: 0; top: 0; left: 0; }
    h3 { margin-top: 0; color: #6ae6ff; border-bottom: 1px solid rgba(100, 200, 255, 0.3); padding-bottom: 8px; }
    .highlight { color: #ffd86e; font-weight: 600; }
  </style></head>
<body>
  <div id="overlay">
    <h3>Fractal Node Information</h3>
    <div id="info"></div>
  </div>
  <button id="reset-view-btn" title="Reset View">⌂</button>
  <button id="edit-nodes-btn" title="Edit Nodes">✎</button>
  <div id="node-manager">
    <h4>Node Manager (Hierarchy)</h4>
    <div id="tree-root"></div>
    <button id="add-node-btn">Add New Node</button>
  </div>
  <div id="gui-container"></div>
  <script>
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    document.body.appendChild(renderer.domElement);
    const controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.enablePan = false;
    scene.add(new THREE.AmbientLight(0x808080));const gui = new dat.GUI({ autoPlace: false });
document.getElementById('gui-container').appendChild(gui.domElement);
const params = { nodeSpacing: 15.0 };
gui.add(params, 'nodeSpacing', 5, 50).name('Node Spacing');

function getDefaultData() {
  return {
    nodes: [
      { id: 1, name: "The Fractiverse", info: "The container of all tiers.", radius: 8, color: "#ffffff" },
      { id: 2, name: "Duality", info: "The primal split.", radius: 5, color: "#f0f0f0" },
      { id: 3, name: "Motion", info: "Kinetic force.", radius: 3, color: "#87CEEB" },
      { id: 4, name: "Stillness", info: "Latent entropy.", radius: 3, color: "#9370DB" },
      { id: 5, name: "Mind", info: "Cognitive domain.", radius: 3.5, color: "#FFD700" },
    ],
    connections: [
      { from: 1, to: 2 },
      { from: 2, to: 3 },
      { from: 2, to: 4 },
      { from: 3, to: 5 },
    ]
  };
}

function loadData() {
  const saved = localStorage.getItem('fractalityGraphDataV5');
  return saved ? JSON.parse(saved) : getDefaultData();
}

function saveData(data) {
  localStorage.setItem('fractalityGraphDataV5', JSON.stringify(data));
}

let nodeMeshes = [];
let { nodes: fractalNodes, connections: fractalConnections } = loadData();
let activeFocusId = 1;

function buildTree(rootId) {
  const rootNode = fractalNodes.find(n => n.id === rootId);
  if (!rootNode) return null;
  const children = fractalConnections.filter(c => c.from === rootId).map(c => buildTree(c.to)).filter(n => n);
  return { ...rootNode, children };
}

function renderTree(node, container, depth = 0) {
  if (!node) return;
  const div = document.createElement('div');
  div.className = 'tree-node';
  div.style.marginLeft = `${depth * 16}px`;
  div.textContent = node.name;
  div.onclick = () => { setFocus(node.id); document.getElementById('node-manager').style.display = 'none'; };
  container.appendChild(div);
  node.children.forEach(child => renderTree(child, container, depth + 1));
}

function populateTreeUI() {
  const root = document.getElementById('tree-root');
  root.innerHTML = '';
  const tree = buildTree(1);
  renderTree(tree, root);
}

function setFocus(newId) {
  const focus = fractalNodes.find(n => n.id === newId);
  if (!focus) return;
  activeFocusId = newId;
  document.getElementById('info').innerHTML = `<span class="highlight">${focus.name}</span><br>${focus.info}`;
  controls.target.set(0, 0, 0);
}

document.getElementById('reset-view-btn').addEventListener('click', () => {
  if (confirm("Reset data to default?")) {
    localStorage.removeItem('fractalityGraphDataV5');
    location.reload();
  }
});

document.getElementById('edit-nodes-btn').addEventListener('click', () => {
  const panel = document.getElementById('node-manager');
  const show = panel.style.display === 'none' || panel.style.display === '';
  panel.style.display = show ? 'block' : 'none';
  if (show) populateTreeUI();
});

refreshScene();
camera.position.set(0, 0, 45);
animate();

function animate() {
  requestAnimationFrame(animate);
  controls.update();
  renderer.render(scene, camera);
}

function refreshScene() {
  nodeMeshes.forEach(m => { m.geometry.dispose(); m.material.dispose(); scene.remove(m); });
  nodeMeshes = [];
  fractalNodes.forEach(node => {
    const geo = new THREE.SphereGeometry(node.radius, 32, 32);
    const mat = new THREE.MeshBasicMaterial({ color: node.color, wireframe: true });
    const mesh = new THREE.Mesh(geo, mat);
    mesh.userData = node;
    scene.add(mesh);
    nodeMeshes.push(mesh);
  });
}

  </script>
</body>
</html>