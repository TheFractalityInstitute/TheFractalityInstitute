<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no" />
  <title>TFP AppShell Build v0.1.0</title>
  
  <script src="./three.min.js" defer></script>
  <script src="./OrbitControls.js" defer></script>

  <style>
    body { margin: 0; overflow: hidden; background: #111; }
    #info-panel {
        position: fixed;
        top: 10px;
        left: 10px;
        padding: 10px;
        background: rgba(0,0,0,0.5);
        color: white;
        font-family: monospace;
        border-radius: 5px;
        z-index: 100;
    }
  </style>
</head>
<body>
  <div id="info-panel"></div>

  <script>
    window.addEventListener('DOMContentLoaded', () => {

        let camera, scene, renderer, controls;
        let instancedMesh;
        const nodeCount = 1000;
        const tempMatrix = new THREE.Matrix4();
        const tempObject = new THREE.Object3D();
        const infoPanel = document.getElementById('info-panel');
        let lastTime = performance.now();
        let frameCount = 0;

        function init() {
            // --- SCENE & CAMERA ---
            scene = new THREE.Scene();
            camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
            camera.position.z = 75;

            // --- RENDERER ---
            renderer = new THREE.WebGLRenderer({ antialias: true });
            renderer.setPixelRatio(window.devicePixelRatio);
            renderer.setSize(window.innerWidth, window.innerHeight);
            document.body.appendChild(renderer.domElement);

            // --- CONTROLS ---
            controls = new THREE.OrbitControls(camera, renderer.domElement);
            controls.enableDamping = true;

            // --- INSTANCED MESH SETUP ---
            const geometry = new THREE.SphereGeometry(1, 16, 16);
            // Switched to MeshBasicMaterial as it requires no light
            const material = new THREE.MeshBasicMaterial({ wireframe: true });
            
            instancedMesh = new THREE.InstancedMesh(geometry, material, nodeCount);

            // --- DATA MODEL (Minimal "Dumb" Nodes) ---
            for (let i = 0; i < nodeCount; i++) {
                tempObject.position.set(
                    (Math.random() - 0.5) * 100,
                    (Math.random() - 0.5) * 100,
                    (Math.random() - 0.5) * 100
                );
                
                const scale = Math.random() * 2 + 0.5;
                tempObject.scale.set(scale, scale, scale);

                tempObject.updateMatrix();
                instancedMesh.setMatrixAt(i, tempObject.matrix);
                instancedMesh.setColorAt(i, new THREE.Color(Math.random() * 0xffffff));
            }

            scene.add(instancedMesh);

            // --- EVENT LISTENERS ---
            window.addEventListener('resize', onWindowResize);
        }

        function onWindowResize() {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        }

        function animate() {
            requestAnimationFrame(animate);
            controls.update();
            
            // --- FPS COUNTER ---
            const time = performance.now();
            frameCount++;
            if ( time >= lastTime + 1000 ) {
                const fps = ( frameCount * 1000 ) / ( time - lastTime );
                infoPanel.textContent = `Nodes: ${nodeCount}\nFPS: ${fps.toFixed(2)}`;
                frameCount = 0;
                lastTime = time;
            }

            renderer.render(scene, camera);
        }

        init();
        animate();
    });
  </script>
</body>
</html>
