<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Fractality Bubble UI v3.0</title>
  <style>
    body {
      margin: 0;
      overflow: hidden;
      background: #111;
      color: white;
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    #overlay {
      position: fixed;
      top: 15px;
      left: 15px;
      background: rgba(20, 20, 30, 0.85);
      padding: 15px;
      border-radius: 12px;
      max-width: 320px;
      backdrop-filter: blur(5px);
      border: 1px solid rgba(255, 255, 255, 0.1);
      z-index: 10;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
    }
    
    #info {
      font-size: 15px;
      line-height: 1.6;
      min-height: 60px;
    }
    
    #loader {
      position: fixed;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      font-size: 18px;
      color: #aaa;
      z-index: 5;
    }
    
    canvas {
      display: block;
      position: fixed;
      z-index: 0;
      top: 0;
      left: 0;
    }
    
    h3 {
      margin-top: 0;
      color: #6ae6ff;
      border-bottom: 1px solid rgba(100, 200, 255, 0.3);
      padding-bottom: 8px;
    }
    
    .highlight {
      color: #ffd86e;
      font-weight: 600;
    }
    
    #retry-btn {
      background: #6ae6ff;
      color: #111;
      border: none;
      padding: 8px 16px;
      border-radius: 4px;
      margin-top: 10px;
      cursor: pointer;
      font-weight: bold;
    }
  </style>
</head>
<body>
  <div id="loader">Loading fractal universe...</div>
  
  <div id="overlay" aria-live="polite" aria-atomic="true">
    <h3 id="overlay-heading">Fractal Node Information v3.0</h3>
    <div id="info" aria-describedby="overlay-heading">⟡ Tap any sphere to explore its fractal properties</div>
  </div>

  <script>
    // ================== THREE.JS LOADER (LOCAL ONLY TEST) ==================
function loadThreeJS() {
  return new Promise((resolve, reject) => {
    console.log('Attempting to load three.min.js locally...');
    const script = document.createElement('script');
    script.src = 'three.min.js'; // The file in your folder
    script.onload = () => {
      console.log('Local three.min.js loaded successfully.');
      resolve();
    };
    script.onerror = () => {
      console.error('Failed to load local three.min.js!');
      reject(new Error('The local three.min.js file could not be loaded.'));
    };
    document.head.appendChild(script);
  });
}


    // ================== MAIN APPLICATION ==================
    async function initFractalApp() {
      const loader = document.getElementById('loader');
      const infoPanel = document.getElementById('info');
      
      try {
        // Show loading status
        loader.textContent = 'Loading 3D engine...';
        
        // Load Three.js library
        await loadThreeJS();
        
        // Verify Three.js loaded successfully
        if (typeof THREE === 'undefined') {
          throw new Error('Three.js library failed to load from both CDN and local fallback.');
        }

        // --- Sanitization Function ---
        // For basic use, this is okay. For production, consider a robust library like DOMPurify to prevent XSS.
        const sanitize = (str) => {
          const temp = document.createElement('div');
          temp.textContent = str;
          return temp.innerHTML;
        };

        // Initialize Three.js scene
        loader.textContent = 'Initializing fractal space...';
        
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({ 
          antialias: true,
          alpha: true,
          powerPreference: "high-performance"
        });
        
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(window.devicePixelRatio);
        document.body.appendChild(renderer.domElement);
        
        // Lighting Setup
        scene.add(new THREE.AmbientLight(0x404040, 1.5));
        const pointLight = new THREE.PointLight(0xffffff, 1.2);
        pointLight.position.set(8, 10, 12);
        scene.add(pointLight);
        
        // Add subtle fog for depth
        scene.fog = new THREE.FogExp2(0x0a1122, 0.03);

        // Define the data for our fractal nodes
        const fractalNodes = {
          "GLYPH": { position: [3, 0.75, -1], radius: 1.5, color: "#20B2AA", info: "Symbolic representation of fractal language" },
          "Oracle Node": { position: [3, 0.5, 1], radius: 1.5, color: "#F08080", info: "Predictive fractal analysis module" },
          "Unity Field": { position: [0, 0, 3], radius: 7, color: "#E0FFFF", info: "Harmonic convergence field generator" },
          "Trust Protocol": { position: [0, 2, 2], radius: 1.75, color: "#FAFAD2", info: "Decentralized consensus mechanism" },
          "Shadow Integration": { position: [3, -1, 0.5], radius: 1.25, color: "#9370DB", info: "Chaos assimilation subsystem" }
        };

        const nodeMeshes = [];
        const raycaster = new THREE.Raycaster();
        const mouse = new THREE.Vector2();
        let activeNode = null;

        // Create and add fractal spheres to the scene
        for (const [name, data] of Object.entries(fractalNodes)) {
          const geometry = new THREE.SphereGeometry(data.radius, 36, 36);
          const material = new THREE.MeshStandardMaterial({ 
            color: data.color,
            emissive: data.color,
            emissiveIntensity: 0.05,
            roughness: 0.3,
            metalness: 0.7
          });
          
          const node = new THREE.Mesh(geometry, material);
          node.position.set(...data.position);
          node.userData = { name, info: data.info };
          
          scene.add(node);
          nodeMeshes.push(node);
        }

        camera.position.set(0, 2, 15);

        // Animation loop for continuous rendering and movement
        function animate() {
          requestAnimationFrame(animate);
          
          const time = Date.now() * 0.0005;
          nodeMeshes.forEach((node, index) => {
            node.position.y += Math.sin(time + index) * 0.003; // Gentle float
            node.rotation.x += 0.002;
            node.rotation.y += 0.003;
          });
          
          renderer.render(scene, camera);
        }
        
        // Interaction handler for clicks and taps
        function handleInteraction(event) {
          const x = event.touches ? event.touches[0].clientX : event.clientX;
          const y = event.touches ? event.touches[0].clientY : event.clientY;
          
          mouse.x = (x / window.innerWidth) * 2 - 1;
          mouse.y = - (y / window.innerHeight) * 2 + 1;
          
          raycaster.setFromCamera(mouse, camera);
          const intersects = raycaster.intersectObjects(nodeMeshes);
          
          if (intersects.length > 0) {
            const selectedObject = intersects[0].object;
            
            if (activeNode !== selectedObject) {
              // Reset previous active node
              if (activeNode) {
                activeNode.material.emissiveIntensity = 0.05;
              }
              
              // Set new active node
              activeNode = selectedObject;
              activeNode.material.emissiveIntensity = 0.4;
              
              // Update info display using sanitized data
              infoPanel.innerHTML = `
                <span class="highlight">${sanitize(activeNode.userData.name)}</span><br>
                ${sanitize(activeNode.userData.info)}
              `;
            }
          }
        }

        // Event listeners for interaction and window resizing
        window.addEventListener('click', handleInteraction);
        window.addEventListener('touchend', handleInteraction);
        
        window.addEventListener('resize', () => {
          camera.aspect = window.innerWidth / window.innerHeight;
          camera.updateProjectionMatrix();
          renderer.setSize(window.innerWidth, window.innerHeight, false);
        });

        // Start animation and remove loader
        animate();
        if (loader) loader.remove();
        
      } catch (error) {
        console.error("Fractal initialization error:", error);
        
        const errorMessage = error.message.includes('Three.js') 
          ? '3D engine failed to load. Please check your internet connection and try again.' 
          : `An unexpected error occurred: ${error.message}`;
        
        // Display error and a retry button
        infoPanel.innerHTML = `
          <div style="color:#ff6b6b; font-weight: bold;">Initialization Failed</div>
          <div style="font-size: 14px; margin-top: 8px;">${errorMessage}</div>
          <button id="retry-btn">Retry</button>
        `;

        if (loader) loader.remove();
        
        // --- ROBUST RETRY LOGIC ---
        const retryButton = document.getElementById('retry-btn');
        if (retryButton) {
          retryButton.addEventListener('click', () => {
            // Clean up the UI before retrying
            infoPanel.innerHTML = '⟡ Tap any sphere to explore its fractal properties';
            document.body.appendChild(loader); // Re-add loader
            // Remove the old canvas if it exists
            const oldCanvas = document.querySelector('canvas');
            if (oldCanvas) oldCanvas.remove();
            
            initFractalApp(); // Attempt to initialize again
          }, { once: true }); // Use { once: true } to ensure the listener is auto-removed after one click
        }
      }
    }

    // Start the application once the DOM is fully loaded
    document.addEventListener('DOMContentLoaded', initFractalApp);
  </script>
</body>
</html>
