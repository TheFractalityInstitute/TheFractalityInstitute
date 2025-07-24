<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fractality v0.2.2 - The Living Universe</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: #000;
            color: #fff;
            overflow: hidden;
        }
        
        #canvas {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
        }
        
        #ui-overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 10;
        }
        
        #perf-monitor {
            position: fixed;
            top: 10px;
            right: 10px;
            width: 200px;
            background: rgba(0, 0, 0, 0.8);
            border: 1px solid #0ff;
            padding: 10px;
            font-size: 12px;
            font-family: 'Consolas', 'Monaco', monospace;
            pointer-events: auto;
        }
        
        #perf-monitor h3 {
            margin: 0 0 10px 0;
            color: #0ff;
            font-size: 14px;
        }
        
        #perf-monitor .metric {
            display: flex;
            justify-content: space-between;
            margin: 5px 0;
        }
        
        #perf-monitor .metric-value {
            color: #0f0;
        }
        
        #node-info {
            position: fixed;
            bottom: 20px;
            left: 20px;
            background: rgba(0, 0, 0, 0.8);
            border: 1px solid #fff;
            padding: 15px;
            min-width: 300px;
            pointer-events: auto;
            transition: opacity 0.3s;
        }
        
        #node-info h2 {
            margin: 0 0 10px 0;
            color: #fff;
            font-size: 18px;
        }
        
        #node-info .info-row {
            margin: 5px 0;
            color: #ccc;
        }
        
        #controls {
            position: fixed;
            top: 10px;
            left: 10px;
            background: rgba(0, 0, 0, 0.8);
            border: 1px solid #fff;
            padding: 15px;
            pointer-events: auto;
        }
        
        #controls button {
            display: block;
            width: 100%;
            margin: 5px 0;
            padding: 8px;
            background: #111;
            border: 1px solid #555;
            color: #fff;
            cursor: pointer;
            transition: all 0.2s;
        }
        
        #controls button:hover {
            background: #222;
            border-color: #0ff;
        }
        
        .loading {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 24px;
            color: #0ff;
        }
    </style>
</head>
<body>
    <canvas id="canvas"></canvas>
    
    <div id="ui-overlay">
        <div id="perf-monitor">
            <h3>Performance Monitor</h3>
            <div class="metric">
                <span>FPS:</span>
                <span class="metric-value" id="fps">0</span>
            </div>
            <div class="metric">
                <span>Nodes:</span>
                <span class="metric-value" id="node-count">0</span>
            </div>
            <div class="metric">
                <span>Draw Calls:</span>
                <span class="metric-value" id="draw-calls">1</span>
            </div>
            <div class="metric">
                <span>Memory:</span>
                <span class="metric-value" id="memory">0 MB</span>
            </div>
            <div class="metric">
                <span>Animation:</span>
                <span class="metric-value" id="animation-time">0 ms</span>
            </div>
        </div>
        
        <div id="controls">
            <button id="reset-view">Reset View</button>
            <button id="toggle-quality">Quality: High</button>
            <button id="stress-test">Stress Test (500 nodes)</button>
        </div>
        
        <div id="node-info" style="display: none;">
            <h2 id="node-title">Node Information</h2>
            <div class="info-row">ID: <span id="node-id"></span></div>
            <div class="info-row">Depth: <span id="node-depth"></span></div>
            <div class="info-row">Children: <span id="node-children"></span></div>
            <div class="info-row">Click to navigate</div>
        </div>
    </div>
    
    <div class="loading" id="loading">Initializing Fractality...</div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script>
        // =========================
        // CORE SYSTEMS
        // =========================
        
        // Performance Monitor
        class PerformanceMonitor {
            constructor() {
                this.frameCount = 0;
                this.lastTime = performance.now();
                this.fps = 0;
                this.frameTime = 0;
                this.animationTime = 0;
                this.samples = [];
                this.maxSamples = 60;
            }
            
            startFrame() {
                this.frameStart = performance.now();
            }
            
            endFrame() {
                const now = performance.now();
                this.frameTime = now - this.frameStart;
                
                this.samples.push(this.frameTime);
                if (this.samples.length > this.maxSamples) {
                    this.samples.shift();
                }
                
                this.frameCount++;
                if (now - this.lastTime >= 1000) {
                    this.fps = this.frameCount;
                    this.frameCount = 0;
                    this.lastTime = now;
                }
            }
            
            getAverageFrameTime() {
                if (this.samples.length === 0) return 0;
                const sum = this.samples.reduce((a, b) => a + b, 0);
                return sum / this.samples.length;
            }
            
            canUpdate(budget = 16) {
                return this.frameTime < budget;
            }
        }
        
        // State Management
        class FractalityState {
            constructor() {
                this.focusNode = null;
                this.previousFocus = null;
                this.visibleNodes = new Set();
                this.animationState = 'idle';
                this.transitionProgress = 0;
                this.history = [];
                this.maxHistory = 10;
            }
            
            setFocus(nodeId) {
                if (nodeId === this.focusNode) return;
                
                this.previousFocus = this.focusNode;
                this.focusNode = nodeId;
                this.animationState = 'transitioning';
                this.transitionProgress = 0;
                
                this.history.push({
                    from: this.previousFocus,
                    to: nodeId,
                    timestamp: Date.now()
                });
                
                if (this.history.length > this.maxHistory) {
                    this.history.shift();
                }
            }
            
            updateVisibleNodes(familyNodes) {
                this.visibleNodes = new Set(familyNodes);
            }
        }
        
        // Node Data Structure
        class NodeData {
            constructor(id, depth = 0) {
                this.id = id;
                this.depth = depth;
                this.parentId = null;
                this.childIds = [];
                this.siblingIds = [];
                this.position = new THREE.Vector3();
                this.targetPosition = new THREE.Vector3();
                this.opacity = 1;
                this.targetOpacity = 1;
                this.scale = 1;
                this.color = new THREE.Color();
                this.priority = 1;
            }
        }
        
        // Family View Controller
        class FamilyViewController {
            constructor(nodeGraph) {
                this.nodeGraph = nodeGraph;
            }
            
            getVisibleNodes(focusId) {
                if (!focusId) return [];
                
                const nodes = [];
                const focus = this.nodeGraph.get(focusId);
                if (!focus) return [];
                
                // Add focus node
                nodes.push(focus);
                
                // Add parent
                if (focus.parentId) {
                    const parent = this.nodeGraph.get(focus.parentId);
                    if (parent) nodes.push(parent);
                }
                
                // Add siblings (limit to 5)
                focus.siblingIds.slice(0, 5).forEach(id => {
                    const sibling = this.nodeGraph.get(id);
                    if (sibling) nodes.push(sibling);
                });
                
                // Add children (limit to 7)
                focus.childIds.slice(0, 7).forEach(id => {
                    const child = this.nodeGraph.get(id);
                    if (child) nodes.push(child);
                });
                
                return nodes;
            }
            
            getNodePriority(nodeId, focusId) {
                if (nodeId === focusId) return 3;
                const focus = this.nodeGraph.get(focusId);
                if (!focus) return 1;
                
                if (nodeId === focus.parentId) return 2;
                if (focus.childIds.includes(nodeId)) return 1.5;
                return 1;
            }
        }
        
        // Layout Engine
        class LayoutEngine {
            calculateLayout(nodes, focusId) {
                const positions = new Map();
                const focus = nodes.find(n => n.id === focusId);
                if (!focus) return positions;
                
                // Focus at center
                positions.set(focusId, new THREE.Vector3(0, 0, 0));
                
                // Parent behind focus
                const parent = nodes.find(n => n.id === focus.parentId);
                if (parent) {
                    positions.set(parent.id, new THREE.Vector3(0, 0, -10));
                }
                
                // Siblings in arc below
                const siblings = nodes.filter(n => focus.siblingIds.includes(n.id));
                siblings.forEach((sibling, i) => {
                    const angle = (i / siblings.length) * Math.PI - Math.PI/2;
                    positions.set(sibling.id, new THREE.Vector3(
                        Math.cos(angle) * 8,
                        -4,
                        Math.sin(angle) * 5
                    ));
                });
                
                // Children in golden spiral
                const children = nodes.filter(n => focus.childIds.includes(n.id));
                const spiral = this.generateGoldenSpiral(children.length, 5);
                children.forEach((child, i) => {
                    positions.set(child.id, spiral[i]);
                });
                
                return positions;
            }
            
            generateGoldenSpiral(count, radius) {
                const positions = [];
                const phi = Math.PI * (3 - Math.sqrt(5));
                
                for (let i = 0; i < count; i++) {
                    const y = 1 - (i / Math.max(1, count - 1)) * 2;
                    const r = Math.sqrt(1 - y * y) * radius;
                    const theta = phi * i;
                    
                    positions.push(new THREE.Vector3(
                        Math.cos(theta) * r,
                        y * radius/2 + 2,
                        Math.sin(theta) * r - 2
                    ));
                }
                
                return positions;
            }
        }
        
        // Animation System
        class AnimationSystem {
            constructor() {
                this.transitions = new Map();
                this.speed = 3.0;
            }
            
            startTransition(nodes, targetPositions) {
                nodes.forEach(node => {
                    const target = targetPositions.get(node.id);
                    if (target) {
                        node.targetPosition.copy(target);
                        node.targetOpacity = 1;
                    } else {
                        node.targetOpacity = 0;
                    }
                });
            }
            
            update(nodes, deltaTime, performance) {
                const startTime = performance.now();
                const factor = Math.min(1, deltaTime * this.speed);
                let animating = false;
                
                nodes.forEach(node => {
                    // Position interpolation
                    if (!node.position.equals(node.targetPosition)) {
                        node.position.lerp(node.targetPosition, factor);
                        animating = true;
                    }
                    
                    // Opacity interpolation
                    if (Math.abs(node.opacity - node.targetOpacity) > 0.01) {
                        node.opacity += (node.targetOpacity - node.opacity) * factor;
                        animating = true;
                    }
                    
                    // Scale based on priority
                    const targetScale = 0.5 + node.priority * 0.5;
                    if (Math.abs(node.scale - targetScale) > 0.01) {
                        node.scale += (targetScale - node.scale) * factor;
                        animating = true;
                    }
                });
                
                const animationTime = performance.now() - startTime;
                return { animating, animationTime };
            }
        }
        
        // Renderer System
        class FractalityRenderer {
            constructor(canvas) {
                this.canvas = canvas;
                this.initThree();
                this.initGeometry();
                this.initLights();
                this.quality = 1.0;
            }
            
            initThree() {
                this.scene = new THREE.Scene();
                this.scene.background = new THREE.Color(0x000000);
                this.scene.fog = new THREE.Fog(0x000000, 10, 100);
                
                this.camera = new THREE.PerspectiveCamera(
                    75,
                    window.innerWidth / window.innerHeight,
                    0.1,
                    1000
                );
                this.camera.position.set(0, 0, 15);
                
                this.renderer = new THREE.WebGLRenderer({
                    canvas: this.canvas,
                    antialias: true,
                    alpha: true
                });
                this.renderer.setSize(window.innerWidth, window.innerHeight);
                this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
            }
            
            initGeometry() {
                const geometry = new THREE.SphereGeometry(1, 16, 16);
                const material = new THREE.MeshPhongMaterial({
                    color: 0xffffff,
                    emissive: 0x222222,
                    shininess: 100,
                    transparent: true
                });
                
                // Create instanced mesh
                this.instancedMesh = new THREE.InstancedMesh(geometry, material, 500);
                this.instancedMesh.instanceMatrix.setUsage(THREE.DynamicDrawUsage);
                this.scene.add(this.instancedMesh);
                
                // Temporary objects for matrix calculations
                this.dummy = new THREE.Object3D();
                this.color = new THREE.Color();
            }
            
            initLights() {
                const ambientLight = new THREE.AmbientLight(0x404040, 0.5);
                this.scene.add(ambientLight);
                
                const pointLight = new THREE.PointLight(0x00ffff, 1, 100);
                pointLight.position.set(10, 10, 10);
                this.scene.add(pointLight);
                
                const pointLight2 = new THREE.PointLight(0xff00ff, 0.5, 100);
                pointLight2.position.set(-10, -5, 5);
                this.scene.add(pointLight2);
            }
            
            updateInstances(nodes) {
                let index = 0;
                
                nodes.forEach(node => {
                    if (node.opacity > 0.01 && index < 500) {
                        // Set position and scale
                        this.dummy.position.copy(node.position);
                        this.dummy.scale.setScalar(node.scale);
                        this.dummy.updateMatrix();
                        
                        this.instancedMesh.setMatrixAt(index, this.dummy.matrix);
                        
                        // Set color based on depth
                        const hue = (node.depth * 0.1) % 1;
                        this.color.setHSL(hue, 0.7, 0.5);
                        this.color.multiplyScalar(node.opacity);
                        this.instancedMesh.setColorAt(index, this.color);
                        
                        index++;
                    }
                });
                
                this.instancedMesh.count = index;
                this.instancedMesh.instanceMatrix.needsUpdate = true;
                this.instancedMesh.instanceColor.needsUpdate = true;
                
                return index;
            }
            
            render() {
                this.renderer.render(this.scene, this.camera);
            }
            
            resize() {
                this.camera.aspect = window.innerWidth / window.innerHeight;
                this.camera.updateProjectionMatrix();
                this.renderer.setSize(window.innerWidth, window.innerHeight);
            }
            
            setQuality(level) {
                this.quality = level;
                this.renderer.setPixelRatio(Math.min(window.devicePixelRatio * level, 2));
            }
        }
        
           // Main Engine
        class FractalityEngine {
            constructor() {
                this.canvas = document.getElementById('canvas');
                this.nodeGraph = new Map();
                this.state = new FractalityState();
                this.performance = new PerformanceMonitor();
                this.familyView = new FamilyViewController(this.nodeGraph);
                this.layout = new LayoutEngine();
                this.animation = new AnimationSystem();
                this.renderer = new FractalityRenderer(this.canvas);
                
                this.clock = new THREE.Clock();
                this.raycaster = new THREE.Raycaster();
                this.mouse = new THREE.Vector2();
                
                this.initUI();
                this.initEventListeners();
            }
            
            initUI() {
                this.ui = {
                    fps: document.getElementById('fps'),
                    nodeCount: document.getElementById('node-count'),
                    drawCalls: document.getElementById('draw-calls'),
                    memory: document.getElementById('memory'),
                    animationTime: document.getElementById('animation-time'),
                    nodeInfo: document.getElementById('node-info'),
                    nodeTitle: document.getElementById('node-title'),
                    nodeId: document.getElementById('node-id'),
                    nodeDepth: document.getElementById('node-depth'),
                    nodeChildren: document.getElementById('node-children'),
                    loading: document.getElementById('loading'),
                    qualityBtn: document.getElementById('toggle-quality')
                };
            }
            
            initEventListeners() {
                window.addEventListener('resize', () => this.renderer.resize());
                
                this.canvas.addEventListener('click', (e) => this.handleClick(e));
                this.canvas.addEventListener('mousemove', (e) => this.handleMouseMove(e));
                
                document.getElementById('reset-view').addEventListener('click', () => {
                    this.state.setFocus('root');
                    this.updateLayout();
                });
                
                document.getElementById('toggle-quality').addEventListener('click', () => {
                    const newQuality = this.renderer.quality > 0.5 ? 0.5 : 1.0;
                    this.renderer.setQuality(newQuality);
                    this.ui.qualityBtn.textContent = `Quality: ${newQuality > 0.5 ? 'High' : 'Low'}`;
                });
                
                document.getElementById('stress-test').addEventListener('click', () => {
                    this.generateTestData(500);
                    this.state.setFocus('root');
                    this.updateLayout();
                });
            }
            
            handleClick(event) {
                this.mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
                this.mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
                
                this.raycaster.setFromCamera(this.mouse, this.renderer.camera);
                const intersects = this.raycaster.intersectObject(this.renderer.instancedMesh);
                
                if (intersects.length > 0) {
                    const instanceId = intersects[0].instanceId;
                    const nodes = Array.from(this.state.visibleNodes);
                    if (instanceId < nodes.length) {
                        const clickedNode = nodes[instanceId];
                        this.state.setFocus(clickedNode.id);
                        this.updateLayout();
                    }
                }
            }
            
            handleMouseMove(event) {
                this.mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
                this.mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
                
                this.raycaster.setFromCamera(this.mouse, this.renderer.camera);
                const intersects = this.raycaster.intersectObject(this.renderer.instancedMesh);
                
                if (intersects.length > 0) {
                    const instanceId = intersects[0].instanceId;
                    const nodes = Array.from(this.state.visibleNodes);
                    if (instanceId < nodes.length) {
                        const hoveredNode = nodes[instanceId];
                        this.showNodeInfo(hoveredNode);
                    }
                } else {
                    this.hideNodeInfo();
                }
            }
            
            showNodeInfo(node) {
                this.ui.nodeInfo.style.display = 'block';
                this.ui.nodeTitle.textContent = `Node ${node.id}`;
                this.ui.nodeId.textContent = node.id;
                this.ui.nodeDepth.textContent = node.depth;
                this.ui.nodeChildren.textContent = node.childIds.length;
            }
            
            hideNodeInfo() {
                this.ui.nodeInfo.style.display = 'none';
            }
            
            generateTestData(count = 100) {
                this.nodeGraph.clear();
                
                // Create root
                const root = new NodeData('root', 0);
                this.nodeGraph.set('root', root);
                
                // Generate tree structure
                let nodeId = 1;
                const queue = [root];
                
                while (queue.length > 0 && this.nodeGraph.size < count) {
                    const parent = queue.shift();
                    const childCount = Math.floor(Math.random() * 5) + 2;
                    
                    for (let i = 0; i < childCount && this.nodeGraph.size < count; i++) {
                        const child = new NodeData(`node-${nodeId++}`, parent.depth + 1);
                        child.parentId = parent.id;
                        parent.childIds.push(child.id);
                        
                        this.nodeGraph.set(child.id, child);
                        
                        if (child.depth < 4) {
                            queue.push(child);
                        }
                    }
                }
                
                // Calculate siblings
                this.nodeGraph.forEach(node => {
                    if (node.parentId) {
                        const parent = this.nodeGraph.get(node.parentId);
                        node.siblingIds = parent.childIds.filter(id => id !== node.id);
                    }
                });
            }
            
            updateLayout() {
                const visibleNodes = this.familyView.getVisibleNodes(this.state.focusNode);
                this.state.updateVisibleNodes(visibleNodes);
                
                // Update priorities
                visibleNodes.forEach(node => {
                    node.priority = this.familyView.getNodePriority(node.id, this.state.focusNode);
                });
                
                // Calculate new layout
                const targetPositions = this.layout.calculateLayout(visibleNodes, this.state.focusNode);
                
                // Start animation
                this.animation.startTransition(visibleNodes, targetPositions);
                this.state.animationState = 'transitioning';
            }
            
            update() {
                this.performance.startFrame();
                
                const deltaTime = this.clock.getDelta();
                
                // Update animations
                const visibleNodes = Array.from(this.state.visibleNodes);
                const { animating, animationTime } = this.animation.update(
                    visibleNodes,
                    deltaTime,
                    performance
                );
                
                if (!animating && this.state.animationState === 'transitioning') {
                    this.state.animationState = 'idle';
                }
                
                // Update renderer
                const nodeCount = this.renderer.updateInstances(visibleNodes);
                
                // Render
                this.renderer.render();
                
                // Update UI
                this.updateUI(nodeCount, animationTime);
                
                this.performance.endFrame();
            }
            
            updateUI(nodeCount, animationTime) {
                // Update performance metrics (throttled)
                if (this.performance.frameCount === 0) {
                    this.ui.fps.textContent = this.performance.fps;
                    this.ui.nodeCount.textContent = nodeCount;
                    this.ui.animationTime.textContent = animationTime.toFixed(2) + ' ms';
                    
                    if (performance.memory) {
                        const mb = (performance.memory.usedJSHeapSize / 1048576).toFixed(1);
                        this.ui.memory.textContent = mb + ' MB';
                    }
                }
            }
            
            start() {
                // Generate initial test data
                this.generateTestData(100);
                
                // Set initial focus
                this.state.setFocus('root');
                this.updateLayout();
                
                // Hide loading
                this.ui.loading.style.display = 'none';
                
                // Start render loop
                const animate = () => {
                    requestAnimationFrame(animate);
                    this.update();
                };
                animate();
            }
        }
        
        // Initialize and start
        const engine = new FractalityEngine();
        engine.start();
    </script>
</body>
</html>
