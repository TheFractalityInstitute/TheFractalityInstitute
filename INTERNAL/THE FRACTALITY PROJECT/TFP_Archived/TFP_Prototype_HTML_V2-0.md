<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Fractality Bubble UI</title>
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
  </style>
</head>
<body>
  <div id="loader">Initializing fractal universe...</div>
  
  <div id="overlay" aria-live="polite" aria-atomic="true">
    <h3 id="overlay-heading">Fractal Node Information</h3>
    <div id="info" aria-describedby="overlay-heading">⟡ Tap any sphere to explore its fractal properties</div>
  </div>

  <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r152/three.min.js"></script>
  <script>
    // Sanitization function to prevent XSS
    const sanitize = (str) => {
      const div = document.createElement('div');
      div.textContent = str;
      return div.innerHTML;
    };

    try {
      // Initialize Three.js
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
      
      // Lighting setup
      const ambientLight = new THREE.AmbientLight(0x404040, 1.5);
      scene.add(ambientLight);
      
      const pointLight = new THREE.PointLight(0xffffff, 1.2);
      pointLight.position.set(8, 10, 12);
      scene.add(pointLight);
      
      // Add subtle fog effect
      scene.fog = new THREE.FogExp2(0x0a1122, 0.03);

      // Sample fractal nodes
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

      // Create fractal spheres
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
        node.userData = { 
          name: name,
          info: data.info
        };
        
        scene.add(node);
        nodeMeshes.push(node);
      }

      camera.position.z = 15;
      camera.position.y = 2;

      // Animation loop with subtle movement
      function animate() {
        requestAnimationFrame(animate);
        
        // Gentle floating animation
        const time = Date.now() * 0.0005;
        nodeMeshes.forEach((node, index) => {
          node.position.y += Math.sin(time + index) * 0.003;
          node.rotation.x += 0.002;
          node.rotation.y += 0.003;
        });
        
        renderer.render(scene, camera);
      }
      
      // Interaction handler
      function handleInteraction(event) {
        event.preventDefault();
        
        const x = event.touches ? event.touches[0].clientX : event.clientX;
        const y = event.touches ? event.touches[0].clientY : event.clientY;
        
        mouse.x = (x / window.innerWidth) * 2 - 1;
        mouse.y = - (y / window.innerHeight) * 2 + 1;
        
        raycaster.setFromCamera(mouse, camera);
        const intersects = raycaster.intersectObjects(nodeMeshes);
        
        if (intersects.length > 0) {
          const node = intersects[0].object;
          const nodeData = node.userData;
          
          // Reset previous active node
          if (activeNode) {
            activeNode.material.emissiveIntensity = 0.05;
          }
          
          // Set new active node
          activeNode = node;
          activeNode.material.emissiveIntensity = 0.4;
          
          // Update info display
          document.getElementById("info").innerHTML = `
            <span class="highlight">${sanitize(nodeData.name)}</span><br>
            ${sanitize(nodeData.info)}
          `;
        }
      }

      // Event listeners
      window.addEventListener('click', handleInteraction);
      window.addEventListener('touchend', handleInteraction);
      
      window.addEventListener('resize', () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight, false);
      });

      // Start animation and remove loader
      animate();
      document.getElementById('loader').remove();
      
    } catch (error) {
      console.error("Fractal initialization error:", error);
      document.getElementById("info").textContent = 
        `Error: ${error.message || 'Failed to initialize fractal visualization'}`;
      document.getElementById('loader').remove();
    }
  </script>
</body>
</html>