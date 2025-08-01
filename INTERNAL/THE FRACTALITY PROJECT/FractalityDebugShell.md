<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔧 Fractality Debug Shell</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Courier New', monospace;
            background: #0a0a0a;
            color: #00ff00;
            overflow-x: hidden;
        }
        
        #debug-console {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 50vh;
            background: rgba(0, 0, 0, 0.9);
            border-bottom: 2px solid #00ff00;
            overflow-y: auto;
            padding: 10px;
            font-size: 12px;
            z-index: 1000;
        }
        
        #canvas-container {
            position: absolute;
            top: 50vh;
            left: 0;
            width: 100%;
            height: 50vh;
            background: #111;
        }
        
        canvas {
            width: 100%;
            height: 100%;
            display: block;
        }
        
        .test-result {
            margin: 5px 0;
            padding: 5px;
            border-left: 3px solid;
        }
        
        .pass {
            border-color: #00ff00;
            background: rgba(0, 255, 0, 0.1);
        }
        
        .fail {
            border-color: #ff0000;
            background: rgba(255, 0, 0, 0.1);
            color: #ff5555;
        }
        
        .info {
            border-color: #00aaff;
            background: rgba(0, 170, 255, 0.1);
            color: #55aaff;
        }
        
        .warning {
            border-color: #ffaa00;
            background: rgba(255, 170, 0, 0.1);
            color: #ffaa55;
        }
        
        #controls {
            position: absolute;
            bottom: 10px;
            left: 10px;
            z-index: 1001;
        }
        
        button {
            background: #333;
            color: #00ff00;
            border: 1px solid #00ff00;
            padding: 8px 16px;
            margin: 2px;
            border-radius: 4px;
            cursor: pointer;
            font-family: inherit;
            font-size: 11px;
        }
        
        button:hover {
            background: #00ff00;
            color: #000;
        }
        
        .section-header {
            font-size: 14px;
            font-weight: bold;
            margin: 10px 0 5px 0;
            color: #ffff00;
        }
        
        .error-details {
            font-size: 10px;
            color: #ff8888;
            margin-left: 10px;
            white-space: pre-wrap;
        }
    </style>
</head>
<body>
    <div id="debug-console">
        <div class="section-header">🔧 FRACTALITY DEBUG SHELL v1.0</div>
        <div class="info">Starting comprehensive system test...</div>
    </div>
    
    <div id="canvas-container">
        <canvas id="test-canvas"></canvas>
    </div>
    
    <div id="controls">
        <button onclick="runFullTest()">🔄 Run Full Test</button>
        <button onclick="testThreeJS()">📦 Test Three.js</button>
        <button onclick="testDataStructures()">📊 Test Data</button>
        <button onclick="testEngines()">⚙️ Test Engines</button>
        <button onclick="clearConsole()">🗑️ Clear</button>
    </div>

    <!-- Include Three.js - Update this path to match your setup -->
    <script src="three.min.js"></script>
    
    <script>
        // Debug Console System
        class DebugConsole {
            constructor() {
                this.console = document.getElementById('debug-console');
                this.testCount = 0;
                this.passCount = 0;
                this.failCount = 0;
            }
            
            log(message, type = 'info') {
                const div = document.createElement('div');
                div.className = `test-result ${type}`;
                
                const timestamp = new Date().toLocaleTimeString();
                const icon = {
                    'pass': '✅',
                    'fail': '❌', 
                    'info': 'ℹ️',
                    'warning': '⚠️'
                }[type] || 'ℹ️';
                
                div.innerHTML = `[${timestamp}] ${icon} ${message}`;
                this.console.appendChild(div);
                this.console.scrollTop = this.console.scrollHeight;
                
                if (type === 'pass') this.passCount++;
                if (type === 'fail') this.failCount++;
                this.testCount++;
            }
            
            error(message, error = null) {
                this.log(message, 'fail');
                if (error) {
                    const errorDiv = document.createElement('div');
                    errorDiv.className = 'error-details';
                    errorDiv.textContent = error.toString();
                    this.console.appendChild(errorDiv);
                }
            }
            
            section(title) {
                const div = document.createElement('div');
                div.className = 'section-header';
                div.textContent = `🔍 ${title}`;
                this.console.appendChild(div);
            }
            
            summary() {
                this.section(`SUMMARY: ${this.passCount}/${this.testCount} tests passed`);
                const rate = this.testCount > 0 ? (this.passCount / this.testCount * 100).toFixed(1) : 0;
                this.log(`Success rate: ${rate}%`, rate > 80 ? 'pass' : rate > 50 ? 'warning' : 'fail');
            }
            
            clear() {
                this.console.innerHTML = '<div class="section-header">🔧 FRACTALITY DEBUG SHELL v1.0</div>';
                this.testCount = 0;
                this.passCount = 0;
                this.failCount = 0;
            }
        }
        
        const debug = new DebugConsole();
        
        // Test Results Storage
        const testResults = {
            threeJS: false,
            webGL: false,
            nodeData: false,
            engines: false,
            rendering: false
        };
        
        // === CORE DATA STRUCTURES (Embedded) ===
        
        class NodeData {
            constructor(id, depth = 0) {
                this.id = id;
                this.depth = depth;
                this.parentId = null;
                this.childIds = [];
                this.position = { x: 0, y: 0, z: 0 };
                this.metadata = {
                    label: id,
                    type: 'concept',
                    tags: []
                };
                
                // Visual properties
                this.color = new THREE.Color(0x4f46e5);
                this.scale = 1.0;
                this.opacity = 1.0;
                this.targetOpacity = 1.0;
                this.targetScale = 1.0;
                
                // CACE properties
                this.contextScore = 0;
                this.priority = 1;
                this.energy = 1.0;
            }
        }
        
        class NodeGraph {
            constructor() {
                this.nodes = new Map();
                this.stats = {
                    totalNodes: 0,
                    maxDepth: 0,
                    avgChildCount: 0
                };
            }
            
            addNode(node) {
                this.nodes.set(node.id, node);
                this._updateStats();
                return node;
            }
            
            getNode(id) {
                return this.nodes.get(id);
            }
            
            getChildren(nodeId) {
                const node = this.getNode(nodeId);
                if (!node) return [];
                
                return node.childIds
                    .map(id => this.getNode(id))
                    .filter(Boolean);
            }
            
            getNodesAtDepth(depth) {
                return Array.from(this.nodes.values())
                    .filter(node => node.depth === depth);
            }
            
            _updateStats() {
                this.stats.totalNodes = this.nodes.size;
                this.stats.maxDepth = Math.max(...Array.from(this.nodes.values()).map(n => n.depth));
                
                const totalChildren = Array.from(this.nodes.values())
                    .reduce((sum, node) => sum + node.childIds.length, 0);
                this.stats.avgChildCount = this.nodes.size > 0 ? totalChildren / this.nodes.size : 0;
            }
        }
        
        // === TEST DATA GENERATOR ===
        
        function generateTestData() {
            debug.log("Generating test data...");
            
            const graph = new NodeGraph();
            
            try {
                // Create root node
                const root = new NodeData('root', 0);
                root.metadata.label = 'Root Universe';
                root.position = { x: 0, y: 0, z: 0 };
                graph.addNode(root);
                
                // Create primary concepts
                const concepts = [
                    { id: 'consciousness', label: 'Consciousness', color: 0x8b5cf6 },
                    { id: 'fractal-geometry', label: 'Fractal Geometry', color: 0x06b6d4 },
                    { id: 'emergence', label: 'Emergence', color: 0x10b981 },
                    { id: 'quantum-mechanics', label: 'Quantum Mechanics', color: 0xf59e0b }
                ];
                
                concepts.forEach((concept, i) => {
                    const node = new NodeData(concept.id, 1);
                    node.metadata.label = concept.label;
                    node.parentId = 'root';
                    node.color = new THREE.Color(concept.color);
                    
                    // Position in circle around root
                    const angle = (i / concepts.length) * Math.PI * 2;
                    node.position = {
                        x: Math.cos(angle) * 5,
                        y: 0,
                        z: Math.sin(angle) * 5
                    };
                    
                    root.childIds.push(node.id);
                    graph.addNode(node);
                    
                    // Add some child concepts
                    for (let j = 0; j < 3; j++) {
                        const childId = `${concept.id}-child-${j}`;
                        const child = new NodeData(childId, 2);
                        child.metadata.label = `${concept.label} ${j + 1}`;
                        child.parentId = concept.id;
                        child.color = new THREE.Color(concept.color).multiplyScalar(0.8);
                        
                        // Position around parent
                        const childAngle = (j / 3) * Math.PI * 2;
                        child.position = {
                            x: node.position.x + Math.cos(childAngle) * 2,
                            y: 0,
                            z: node.position.z + Math.sin(childAngle) * 2
                        };
                        
                        node.childIds.push(child.id);
                        graph.addNode(child);
                    }
                });
                
                debug.log(`Generated ${graph.stats.totalNodes} test nodes`, 'pass');
                return graph;
                
            } catch (error) {
                debug.error("Failed to generate test data", error);
                return null;
            }
        }
        
        // === ENGINE COMPONENTS (Simplified) ===
        
        class SimpleFractalityEngine {
            constructor(canvas) {
                this.canvas = canvas;
                this.scene = null;
                this.camera = null;
                this.renderer = null;
                this.nodeGraph = null;
                this.focusNode = null;
                this.nodeObjects = new Map();
                
                // State
                this.running = false;
                this.frameCount = 0;
            }
            
            async init() {
                debug.log("Initializing Fractality Engine...");
                
                try {
                    // Create scene
                    this.scene = new THREE.Scene();
                    this.scene.background = new THREE.Color(0x0a0a0a);
                    
                    // Create camera
                    const aspect = this.canvas.clientWidth / this.canvas.clientHeight;
                    this.camera = new THREE.PerspectiveCamera(75, aspect, 0.1, 1000);
                    this.camera.position.set(0, 5, 15);
                    this.camera.lookAt(0, 0, 0);
                    
                    // Create renderer
                    this.renderer = new THREE.WebGLRenderer({ 
                        canvas: this.canvas,
                        antialias: true 
                    });
                    this.renderer.setSize(this.canvas.clientWidth, this.canvas.clientHeight);
                    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
                    
                    // Add lighting
                    const ambientLight = new THREE.AmbientLight(0x404040, 0.6);
                    this.scene.add(ambientLight);
                    
                    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
                    directionalLight.position.set(10, 10, 5);
                    this.scene.add(directionalLight);
                    
                    debug.log("Engine initialized successfully", 'pass');
                    return true;
                    
                } catch (error) {
                    debug.error("Engine initialization failed", error);
                    return false;
                }
            }
            
            loadData(nodeGraph) {
                debug.log("Loading data into engine...");
                
                try {
                    this.nodeGraph = nodeGraph;
                    this._createNodeObjects();
                    
                    // Set focus to root
                    const rootNodes = nodeGraph.getNodesAtDepth(0);
                    if (rootNodes.length > 0) {
                        this.setFocus(rootNodes[0].id);
                    }
                    
                    debug.log(`Loaded ${nodeGraph.stats.totalNodes} nodes`, 'pass');
                    return true;
                    
                } catch (error) {
                    debug.error("Data loading failed", error);
                    return false;
                }
            }
            
            _createNodeObjects() {
                // Clear existing objects
                this.nodeObjects.forEach(obj => this.scene.remove(obj));
                this.nodeObjects.clear();
                
                // Create new objects
                this.nodeGraph.nodes.forEach(node => {
                    const geometry = new THREE.SphereGeometry(0.5, 16, 16);
                    const material = new THREE.MeshPhongMaterial({ 
                        color: node.color,
                        transparent: true,
                        opacity: node.opacity
                    });
                    
                    const mesh = new THREE.Mesh(geometry, material);
                    mesh.position.set(node.position.x, node.position.y, node.position.z);
                    mesh.scale.setScalar(node.scale);
                    mesh.userData = { nodeId: node.id };
                    
                    this.scene.add(mesh);
                    this.nodeObjects.set(node.id, mesh);
                });
            }
            
            setFocus(nodeId) {
                debug.log(`Setting focus to: ${nodeId}`);
                this.focusNode = nodeId;
                
                // Update visual properties
                this.nodeObjects.forEach((mesh, id) => {
                    if (id === nodeId) {
                        mesh.material.emissive.setHex(0x444444);
                        mesh.scale.setScalar(1.5);
                    } else {
                        mesh.material.emissive.setHex(0x000000);
                        mesh.scale.setScalar(1.0);
                    }
                });
            }
            
            start() {
                this.running = true;
                this._animate();
                debug.log("Engine started", 'pass');
            }
            
            stop() {
                this.running = false;
                debug.log("Engine stopped");
            }
            
            _animate() {
                if (!this.running) return;
                
                requestAnimationFrame(() => this._animate());
                
                // Simple rotation animation
                this.frameCount++;
                const time = this.frameCount * 0.01;
                
                this.nodeObjects.forEach((mesh, nodeId) => {
                    mesh.rotation.y = time * 0.5;
                    
                    // Add subtle floating
                    const baseY = this.nodeGraph.getNode(nodeId).position.y;
                    mesh.position.y = baseY + Math.sin(time + mesh.position.x) * 0.2;
                });
                
                this.renderer.render(this.scene, this.camera);
            }
            
            handleResize() {
                const width = this.canvas.clientWidth;
                const height = this.canvas.clientHeight;
                
                this.camera.aspect = width / height;
                this.camera.updateProjectionMatrix();
                this.renderer.setSize(width, height);
            }
        }
        
        // === TEST FUNCTIONS ===
        
        function testThreeJS() {
            debug.section("THREE.JS COMPATIBILITY TEST");
            
            try {
                // Test 1: THREE availability
                if (typeof THREE === 'undefined') {
                    debug.error("Three.js library not loaded");
                    return false;
                }
                debug.log("Three.js library loaded", 'pass');
                debug.log(`Three.js version: ${THREE.REVISION}`, 'info');
                
                // Test 2: WebGL support
                const canvas = document.createElement('canvas');
                const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
                if (!gl) {
                    debug.error("WebGL not supported");
                    return false;
                }
                debug.log("WebGL support confirmed", 'pass');
                
                // Test 3: Basic Three.js objects
                const scene = new THREE.Scene();
                const camera = new THREE.PerspectiveCamera(75, 1, 0.1, 1000);
                const renderer = new THREE.WebGLRenderer({ canvas });
                
                debug.log("Basic Three.js objects created", 'pass');
                
                // Test 4: Geometry and materials
                const geometry = new THREE.BoxGeometry(1, 1, 1);
                const material = new THREE.MeshBasicMaterial({ color: 0x00ff00 });
                const cube = new THREE.Mesh(geometry, material);
                
                debug.log("Geometry and materials working", 'pass');
                
                testResults.threeJS = true;
                testResults.webGL = true;
                return true;
                
            } catch (error) {
                debug.error("Three.js test failed", error);
                return false;
            }
        }
        
        function testDataStructures() {
            debug.section("DATA STRUCTURE TEST");
            
            try {
                // Test 1: NodeData creation
                const node = new NodeData('test-node', 1);
                if (!node.id || !node.color || !node.position) {
                    debug.error("NodeData structure incomplete");
                    return false;
                }
                debug.log("NodeData creation working", 'pass');
                
                // Test 2: NodeGraph functionality
                const graph = new NodeGraph();
                graph.addNode(node);
                
                if (graph.nodes.size !== 1) {
                    debug.error("NodeGraph addNode failed");
                    return false;
                }
                debug.log("NodeGraph functionality working", 'pass');
                
                // Test 3: Test data generation
                const testGraph = generateTestData();
                if (!testGraph || testGraph.nodes.size === 0) {
                    debug.error("Test data generation failed");
                    return false;
                }
                debug.log(`Test data generation working (${testGraph.nodes.size} nodes)`, 'pass');
                
                testResults.nodeData = true;
                return true;
                
            } catch (error) {
                debug.error("Data structure test failed", error);
                return false;
            }
        }
        
        function testEngines() {
            debug.section("ENGINE COMPONENT TEST");
            
            try {
                const canvas = document.getElementById('test-canvas');
                const engine = new SimpleFractalityEngine(canvas);
                
                // Test 1: Engine initialization
                engine.init().then(success => {
                    if (!success) {
                        debug.error("Engine initialization failed");
                        return false;
                    }
                    debug.log("Engine initialization working", 'pass');
                    
                    // Test 2: Data loading
                    const testGraph = generateTestData();
                    const loadSuccess = engine.loadData(testGraph);
                    
                    if (!loadSuccess) {
                        debug.error("Engine data loading failed");
                        return false;
                    }
                    debug.log("Engine data loading working", 'pass');
                    
                    // Test 3: Rendering
                    try {
                        engine.start();
                        debug.log("Engine rendering started", 'pass');
                        
                        // Test focus change after a delay
                        setTimeout(() => {
                            const nodes = Array.from(testGraph.nodes.keys());
                            if (nodes.length > 1) {
                                engine.setFocus(nodes[1]);
                                debug.log("Focus change working", 'pass');
                            }
                        }, 1000);
                        
                        testResults.engines = true;
                        testResults.rendering = true;
                        
                    } catch (renderError) {
                        debug.error("Engine rendering failed", renderError);
                        return false;
                    }
                    
                }).catch(error => {
                    debug.error("Engine async initialization failed", error);
                });
                
                return true;
                
            } catch (error) {
                debug.error("Engine test failed", error);
                return false;
            }
        }
        
        function runFullTest() {
            debug.clear();
            debug.section("RUNNING FULL DIAGNOSTIC");
            
            let allPassed = true;
            
            // Run tests sequentially
            allPassed &= testThreeJS();
            allPassed &= testDataStructures();
            allPassed &= testEngines();
            
            // Final summary
            setTimeout(() => {
                debug.summary();
                
                if (allPassed) {
                    debug.log("🎉 ALL SYSTEMS OPERATIONAL!", 'pass');
                    debug.log("Your Fractality Project setup is working correctly", 'info');
                } else {
                    debug.log("❌ ISSUES DETECTED", 'fail');
                    debug.log("Check failed tests above for troubleshooting", 'warning');
                }
                
                // Show what should work now
                debug.section("WHAT'S WORKING");
                Object.entries(testResults).forEach(([system, working]) => {
                    debug.log(`${system}: ${working ? '✅ Working' : '❌ Failed'}`, 
                             working ? 'pass' : 'fail');
                });
                
            }, 2000);
        }
        
        function clearConsole() {
            debug.clear();
        }
        
        // === AUTO-START ===
        
        window.addEventListener('load', () => {
            debug.log("Debug shell loaded", 'info');
            debug.log("Click 'Run Full Test' to diagnose your setup", 'info');
            
            // Auto-run basic test
            setTimeout(() => {
                runFullTest();
            }, 500);
        });
        
        // Handle resize
        window.addEventListener('resize', () => {
            const canvas = document.getElementById('test-canvas');
            if (canvas && window.engine) {
                window.engine.handleResize();
            }
        });
        
    </script>
</body>
</html>