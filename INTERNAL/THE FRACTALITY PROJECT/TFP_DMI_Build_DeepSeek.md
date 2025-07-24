<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fractality Project - Data Management Console</title>
    <style>
        :root {
            --primary: #1a1a2e;
            --secondary: #16213e;
            --accent: #0f3460;
            --highlight: #e94560;
            --text: #f1f1f1;
            --success: #4ade80;
            --warning: #facc15;
            --error: #f87171;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        body {
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            color: var(--text);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }
        
        @media (max-width: 768px) {
            .container {
                grid-template-columns: 1fr;
            }
        }
        
        header {
            grid-column: 1 / -1;
            text-align: center;
            padding: 20px 0;
            border-bottom: 2px solid var(--accent);
            margin-bottom: 20px;
        }
        
        h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
            background: linear-gradient(90deg, var(--highlight), #ff7aa2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .subtitle {
            font-size: 1.2rem;
            color: #a9b7c6;
            max-width: 800px;
            margin: 0 auto;
        }
        
        .panel {
            background: rgba(30, 30, 46, 0.8);
            border-radius: 12px;
            padding: 25px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .panel-title {
            font-size: 1.5rem;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 1px solid var(--accent);
            color: var(--highlight);
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .panel-title i {
            font-size: 1.8rem;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 500;
            color: #cbd5e1;
        }
        
        input, textarea, select {
            width: 100%;
            padding: 12px 15px;
            border-radius: 8px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            background: rgba(15, 23, 42, 0.7);
            color: var(--text);
            font-size: 1rem;
            transition: all 0.3s ease;
        }
        
        input:focus, textarea:focus, select:focus {
            outline: none;
            border-color: var(--highlight);
            box-shadow: 0 0 0 3px rgba(233, 69, 96, 0.2);
        }
        
        textarea {
            min-height: 150px;
            resize: vertical;
            font-family: monospace;
        }
        
        .protocol-example {
            background: rgba(15, 23, 42, 0.7);
            border-radius: 8px;
            padding: 15px;
            margin-top: 15px;
            font-family: monospace;
            font-size: 0.9rem;
            line-height: 1.6;
            color: #94a3b8;
            overflow-x: auto;
        }
        
        .btn {
            padding: 12px 25px;
            border-radius: 8px;
            border: none;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }
        
        .btn-primary {
            background: var(--highlight);
            color: white;
        }
        
        .btn-primary:hover {
            background: #d83756;
            transform: translateY(-2px);
        }
        
        .btn-secondary {
            background: var(--accent);
            color: white;
        }
        
        .btn-secondary:hover {
            background: #0d2a4d;
            transform: translateY(-2px);
        }
        
        .actions {
            display: flex;
            gap: 15px;
            margin-top: 25px;
        }
        
        .node-preview {
            background: rgba(15, 23, 42, 0.7);
            border-radius: 8px;
            padding: 15px;
            margin-top: 20px;
            max-height: 300px;
            overflow-y: auto;
        }
        
        pre {
            white-space: pre-wrap;
            font-family: monospace;
            font-size: 0.9rem;
            line-height: 1.5;
        }
        
        .notification {
            padding: 15px;
            border-radius: 8px;
            margin: 15px 0;
            display: flex;
            align-items: center;
            gap: 12px;
        }
        
        .success {
            background: rgba(74, 222, 128, 0.15);
            border: 1px solid var(--success);
            color: var(--success);
        }
        
        .error {
            background: rgba(248, 113, 113, 0.15);
            border: 1px solid var(--error);
            color: var(--error);
        }
        
        .info {
            background: rgba(96, 165, 250, 0.15);
            border: 1px solid #60a5fa;
            color: #60a5fa;
        }
        
        .footer {
            grid-column: 1 / -1;
            text-align: center;
            padding: 30px 0;
            margin-top: 30px;
            border-top: 1px solid var(--accent);
            color: #94a3b8;
            font-size: 0.9rem;
        }
        
        .mode-switch {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }
        
        .mode-btn {
            flex: 1;
            text-align: center;
            padding: 12px;
            background: rgba(15, 23, 42, 0.7);
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
            border: 1px solid transparent;
        }
        
        .mode-btn.active {
            background: var(--accent);
            border-color: var(--highlight);
            color: var(--highlight);
        }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined" rel="stylesheet">
</head>
<body>
    <div class="container">
        <header>
            <h1>Fractality Project</h1>
            <p class="subtitle">Data Management Console - Create and manage fractal nodes with both manual forms and AI-generated protocols</p>
        </header>
        
        <div class="panel">
            <div class="panel-title">
                <span class="material-symbols-outlined">edit_note</span>
                Node Creation Interface
            </div>
            
            <div class="mode-switch">
                <div class="mode-btn active" id="human-mode-btn">Human Interface</div>
                <div class="mode-btn" id="ai-mode-btn">AI Protocol Interface</div>
            </div>
            
            <div id="human-form">
                <div class="form-group">
                    <label for="node-id">Node ID (Required)</label>
                    <input type="text" id="node-id" placeholder="e.g., duality, motion, trust-protocol">
                </div>
                
                <div class="form-group">
                    <label for="node-name">Display Name</label>
                    <input type="text" id="node-name" placeholder="e.g., Duality Principle">
                </div>
                
                <div class="form-group">
                    <label for="node-info">Description</label>
                    <textarea id="node-info" placeholder="Describe this node's meaning and purpose in the fractal universe"></textarea>
                </div>
                
                <div class="form-group">
                    <label for="node-parent">Parent Node</label>
                    <select id="node-parent">
                        <option value="">-- Select Parent --</option>
                        <option value="fractiverse">The Fractiverse (Root)</option>
                        <option value="duality">Duality</option>
                        <option value="motion">Motion</option>
                        <option value="stillness">Stillness</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="node-children">Child Nodes (comma separated IDs)</label>
                    <input type="text" id="node-children" placeholder="e.g., linear-motion, quantum-motion">
                </div>
                
                <div class="form-group">
                    <label for="node-connections">Connections (comma separated IDs)</label>
                    <input type="text" id="node-connections" placeholder="e.g., chaos-node, mind-dimension">
                </div>
                
                <div class="form-group">
                    <label>Visual Properties</label>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                        <div>
                            <label for="node-radius">Radius</label>
                            <input type="number" id="node-radius" step="0.1" value="1.0">
                        </div>
                        <div>
                            <label for="node-color">Color</label>
                            <input type="color" id="node-color" value="#4f46e5">
                        </div>
                    </div>
                </div>
                
                <div class="actions">
                    <button class="btn btn-primary" id="add-node-btn">
                        <span class="material-symbols-outlined">add_circle</span>
                        Add Node
                    </button>
                    <button class="btn btn-secondary" id="reset-form-btn">
                        <span class="material-symbols-outlined">restart_alt</span>
                        Reset Form
                    </button>
                </div>
            </div>
            
            <div id="ai-form" style="display: none;">
                <div class="form-group">
                    <label for="ai-protocol">AI Protocol String</label>
                    <textarea id="ai-protocol" placeholder="Paste AI-generated protocol string here"></textarea>
                    
                    <div class="protocol-example">
                        <p># Example Fractality Node Protocol</p>
                        <p>[NODE]</p>
                        <p>id: quantum-motion</p>
                        <p>name: Quantum Motion</p>
                        <p>info: The probabilistic movement at subatomic scales</p>
                        <p>parent: motion</p>
                        <p>children: wave-particle, uncertainty-principle</p>
                        <p>connections: quantum-field, probability-wave</p>
                        <p>radius: 1.2</p>
                        <p>color: #6d28d9</p>
                        <p>[END]</p>
                    </div>
                </div>
                
                <div class="actions">
                    <button class="btn btn-primary" id="process-ai-btn">
                        <span class="material-symbols-outlined">auto_awesome</span>
                        Process AI Protocol
                    </button>
                    <button class="btn btn-secondary" id="generate-example-btn">
                        <span class="material-symbols-outlined">science</span>
                        Generate Example
                    </button>
                </div>
            </div>
            
            <div id="notification-area"></div>
        </div>
        
        <div class="panel">
            <div class="panel-title">
                <span class="material-symbols-outlined">database</span>
                Node Data Preview & Export
            </div>
            
            <div class="form-group">
                <label>Current Node Structure</label>
                <div class="node-preview">
                    <pre id="node-preview">{
  "nodes": {
    "fractiverse": {
      "id": "fractiverse",
      "name": "The Fractiverse",
      "info": "The total ontological container",
      "radius": 8,
      "color": "#ffffff",
      "parent": null,
      "children": ["duality"]
    },
    "duality": {
      "id": "duality",
      "name": "Duality",
      "info": "The primal division",
      "radius": 5,
      "color": "#f0f0f0",
      "parent": "fractiverse",
      "children": ["motion", "stillness"]
    }
  },
  "connections": []
}</pre>
                </div>
            </div>
            
            <div class="actions">
                <button class="btn btn-primary" id="export-json-btn">
                    <span class="material-symbols-outlined">download</span>
                    Export as JSON
                </button>
                <button class="btn btn-secondary" id="clear-data-btn">
                    <span class="material-symbols-outlined">delete</span>
                    Clear All Data
                </button>
            </div>
            
            <div class="form-group" style="margin-top: 30px;">
                <label>AI Protocol Documentation</label>
                <div class="protocol-example">
                    <p><strong>Fractality Node Protocol Specification</strong></p>
                    <p>Format nodes using this simple markdown-like syntax:</p>
                    <p>[NODE]</p>
                    <p>id: unique_node_id (required)</p>
                    <p>name: Display Name</p>
                    <p>info: Description of the node</p>
                    <p>parent: parent_node_id</p>
                    <p>children: child_id1, child_id2, ...</p>
                    <p>connections: connected_node1, connected_node2, ...</p>
                    <p>radius: 1.5 (default: 1.0)</p>
                    <p>color: #FF0000 (hex color)</p>
                    <p>[END]</p>
                    <p>---</p>
                    <p>You can define multiple nodes in a single protocol string</p>
                </div>
            </div>
        </div>
        
        <div class="footer">
            Fractality Project Data Management Console v1.0 | Designed for seamless human and AI collaboration
        </div>
    </div>
    
    <script>
        // Sample initial data
        const fractalData = {
            nodes: {
                fractiverse: {
                    id: "fractiverse",
                    name: "The Fractiverse",
                    info: "The total ontological container",
                    radius: 8,
                    color: "#ffffff",
                    parent: null,
                    children: ["duality"]
                },
                duality: {
                    id: "duality",
                    name: "Duality",
                    info: "The primal division",
                    radius: 5,
                    color: "#f0f0f0",
                    parent: "fractiverse",
                    children: ["motion", "stillness"]
                }
            },
            connections: []
        };
        
        // DOM Elements
        const humanForm = document.getElementById('human-form');
        const aiForm = document.getElementById('ai-form');
        const humanModeBtn = document.getElementById('human-mode-btn');
        const aiModeBtn = document.getElementById('ai-mode-btn');
        const nodePreview = document.getElementById('node-preview');
        const notificationArea = document.getElementById('notification-area');
        
        // Initialize
        updatePreview();
        
        // Event Listeners
        humanModeBtn.addEventListener('click', () => {
            humanModeBtn.classList.add('active');
            aiModeBtn.classList.remove('active');
            humanForm.style.display = 'block';
            aiForm.style.display = 'none';
        });
        
        aiModeBtn.addEventListener('click', () => {
            aiModeBtn.classList.add('active');
            humanModeBtn.classList.remove('active');
            aiForm.style.display = 'block';
            humanForm.style.display = 'none';
        });
        
        document.getElementById('add-node-btn').addEventListener('click', addNodeFromForm);
        document.getElementById('reset-form-btn').addEventListener('click', resetForm);
        document.getElementById('process-ai-btn').addEventListener('click', processAIProtocol);
        document.getElementById('generate-example-btn').addEventListener('click', generateExample);
        document.getElementById('export-json-btn').addEventListener('click', exportAsJSON);
        document.getElementById('clear-data-btn').addEventListener('click', clearAllData);
        
        // Functions
        function addNodeFromForm() {
            const id = document.getElementById('node-id').value.trim();
            const name = document.getElementById('node-name').value.trim();
            const info = document.getElementById('node-info').value.trim();
            const parent = document.getElementById('node-parent').value;
            const children = document.getElementById('node-children').value.split(',').map(c => c.trim()).filter(c => c);
            const connections = document.getElementById('node-connections').value.split(',').map(c => c.trim()).filter(c => c);
            const radius = parseFloat(document.getElementById('node-radius').value) || 1.0;
            const color = document.getElementById('node-color').value;
            
            if (!id) {
                showNotification('Node ID is required!', 'error');
                return;
            }
            
            if (fractalData.nodes[id]) {
                showNotification(`Node with ID "${id}" already exists!`, 'error');
                return;
            }
            
            // Add the node
            fractalData.nodes[id] = {
                id,
                name: name || id,
                info: info || `Description for ${id}`,
                radius,
                color,
                parent: parent || null,
                children
            };
            
            // Add connections
            connections.forEach(connId => {
                if (!fractalData.connections.includes(`${id}-${connId}`) && 
                    !fractalData.connections.includes(`${connId}-${id}`)) {
                    fractalData.connections.push(`${id}-${connId}`);
                }
            });
            
            // Update parent's children
            if (parent && fractalData.nodes[parent]) {
                if (!fractalData.nodes[parent].children.includes(id)) {
                    fractalData.nodes[parent].children.push(id);
                }
            }
            
            showNotification(`Node "${id}" added successfully!`, 'success');
            resetForm();
            updatePreview();
        }
        
        function processAIProtocol() {
            const protocol = document.getElementById('ai-protocol').value.trim();
            if (!protocol) {
                showNotification('Please enter an AI protocol string', 'error');
                return;
            }
            
            const nodeBlocks = protocol.split('[NODE]').slice(1);
            let addedCount = 0;
            
            for (const block of nodeBlocks) {
                const nodeData = parseNodeBlock(block);
                if (nodeData) {
                    // Add the node
                    fractalData.nodes[nodeData.id] = nodeData;
                    addedCount++;
                    
                    // Add connections
                    if (nodeData.connections) {
                        nodeData.connections.forEach(connId => {
                            if (!fractalData.connections.includes(`${nodeData.id}-${connId}`) && 
                                !fractalData.connections.includes(`${connId}-${nodeData.id}`)) {
                                fractalData.connections.push(`${nodeData.id}-${connId}`);
                            }
                        });
                    }
                }
            }
            
            if (addedCount > 0) {
                showNotification(`Added ${addedCount} node(s) from AI protocol`, 'success');
                updatePreview();
            } else {
                showNotification('No valid nodes found in the protocol', 'error');
            }
        }
        
        function parseNodeBlock(block) {
            const endIndex = block.indexOf('[END]');
            if (endIndex === -1) return null;
            
            const content = block.substring(0, endIndex).trim();
            const lines = content.split('\n').map(line => line.trim()).filter(line => line);
            
            const node = { 
                id: '',
                name: '',
                info: '',
                radius: 1.0,
                color: '#4f46e5',
                parent: null,
                children: [],
                connections: []
            };
            
            for (const line of lines) {
                if (line.startsWith('#')) continue; // Skip comments
                
                const [key, value] = line.split(':').map(part => part.trim());
                if (!key || !value) continue;
                
                switch (key.toLowerCase()) {
                    case 'id':
                        node.id = value;
                        break;
                    case 'name':
                        node.name = value;
                        break;
                    case 'info':
                        node.info = value;
                        break;
                    case 'parent':
                        node.parent = value;
                        break;
                    case 'children':
                        node.children = value.split(',').map(c => c.trim()).filter(c => c);
                        break;
                    case 'connections':
                        node.connections = value.split(',').map(c => c.trim()).filter(c => c);
                        break;
                    case 'radius':
                        node.radius = parseFloat(value) || 1.0;
                        break;
                    case 'color':
                        node.color = value.startsWith('#') ? value : `#${value}`;
                        break;
                }
            }
            
            if (!node.id) return null;
            if (!node.name) node.name = node.id;
            
            return node;
        }
        
        function generateExample() {
            const example = `[NODE]
id: quantum-motion
name: Quantum Motion
info: The probabilistic movement at subatomic scales
parent: motion
children: wave-particle, uncertainty-principle
connections: quantum-field, probability-wave
radius: 1.2
color: #6d28d9
[END]

[NODE]
id: wave-particle
name: Wave-Particle Duality
info: The concept that quantum entities exhibit both wave and particle properties
parent: quantum-motion
connections: uncertainty-principle
radius: 0.8
color: #8b5cf6
[END]`;
            
            document.getElementById('ai-protocol').value = example;
            showNotification('Generated example protocol - ready to process!', 'info');
        }
        
        function exportAsJSON() {
            const jsonStr = JSON.stringify(fractalData, null, 2);
            const blob = new Blob([jsonStr], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            
            const a = document.createElement('a');
            a.href = url;
            a.download = 'fractality_nodes.json';
            document.body.appendChild(a);
            a.click();
            
            setTimeout(() => {
                document.body.removeChild(a);
                URL.revokeObjectURL(url);
            }, 100);
            
            showNotification('Data exported as JSON file!', 'success');
        }
        
        function clearAllData() {
            if (confirm('Are you sure you want to clear all node data? This cannot be undone.')) {
                fractalData.nodes = {
                    fractiverse: fractalData.nodes.fractiverse
                };
                fractalData.connections = [];
                updatePreview();
                showNotification('All nodes cleared! Only root node remains.', 'info');
            }
        }
        
        function resetForm() {
            document.getElementById('node-id').value = '';
            document.getElementById('node-name').value = '';
            document.getElementById('node-info').value = '';
            document.getElementById('node-parent').value = '';
            document.getElementById('node-children').value = '';
            document.getElementById('node-connections').value = '';
            document.getElementById('node-radius').value = '1.0';
            document.getElementById('node-color').value = '#4f46e5';
        }
        
        function updatePreview() {
            nodePreview.textContent = JSON.stringify(fractalData, null, 2);
        }
        
        function showNotification(message, type) {
            const notification = document.createElement('div');
            notification.className = `notification ${type}`;
            
            let icon = 'info';
            if (type === 'success') icon = 'check_circle';
            if (type === 'error') icon = 'error';
            
            notification.innerHTML = `
                <span class="material-symbols-outlined">${icon}</span>
                <span>${message}</span>
            `;
            
            notificationArea.appendChild(notification);
            
            setTimeout(() => {
                notification.style.opacity = '0';
                setTimeout(() => notification.remove(), 300);
            }, 3000);
        }
    </script>
</body>
</html>