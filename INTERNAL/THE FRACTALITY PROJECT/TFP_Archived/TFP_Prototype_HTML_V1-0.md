<!DOCTYPE html><html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Fractality Bubble UI</title>
  <style>
    body { margin: 0; overflow: hidden; background: #111; color: white; font-family: sans-serif; }
    #overlay { position: absolute; top: 10px; left: 10px; background: rgba(0,0,0,0.7); padding: 10px; border-radius: 10px; max-width: 300px; }
    #info { font-size: 14px; line-height: 1.5; }
  </style>
</head>
<body>
  <div id="overlay">
    <h3>Node Info</h3>
    <div id="info">Tap a bubble to view details.</div>
  </div>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r152/three.min.js"></script>
  <script>
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth/window.innerHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    document.body.appendChild(renderer.domElement);const light = new THREE.PointLight(0xffffff, 1);
light.position.set(10, 10, 10);
scene.add(light);

// Sample JSON (replace this with real Fractality JSON later)
const bubbles = {
  "GLYPH": { position: [3, 0.75, -1], radius: 1.5, color: "lightseagreen" },
  "Oracle Node": { position: [3, 0.5, 1], radius: 1.5, color: "lightcoral" },
  "Unity Field": { position: [0, 0, 3], radius: 7, color: "lightcyan" },
  "Trust & Consent Mechanism": { position: [0, 2, 2], radius: 1.75, color: "lightgoldenrodyellow" },
  "Shadow Integration Protocol": { position: [3, -1, 0.5], radius: 1.25, color: "mediumpurple" }
};

const bubbleMeshes = [];
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();

for (const [name, data] of Object.entries(bubbles)) {
  const geometry = new THREE.SphereGeometry(data.radius, 32, 32);
  const material = new THREE.MeshStandardMaterial({ color: data.color });
  const mesh = new THREE.Mesh(geometry, material);
  mesh.position.set(...data.position);
  mesh.userData.name = name;
  scene.add(mesh);
  bubbleMeshes.push(mesh);
}

camera.position.z = 15;

function animate() {
  requestAnimationFrame(animate);
  renderer.render(scene, camera);
}
animate();

function onTouchOrClick(event) {
  event.preventDefault();
  const x = event.touches ? event.touches[0].clientX : event.clientX;
  const y = event.touches ? event.touches[0].clientY : event.clientY;
  mouse.x = (x / window.innerWidth) * 2 - 1;
  mouse.y = - (y / window.innerHeight) * 2 + 1;
  raycaster.setFromCamera(mouse, camera);
  const intersects = raycaster.intersectObjects(bubbleMeshes);
  if (intersects.length > 0) {
    const name = intersects[0].object.userData.name;
    document.getElementById("info").textContent = `Selected: ${name}`;
  }
}

window.addEventListener('click', onTouchOrClick);
window.addEventListener('touchstart', onTouchOrClick);
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});

  </script>
</body>
</html>