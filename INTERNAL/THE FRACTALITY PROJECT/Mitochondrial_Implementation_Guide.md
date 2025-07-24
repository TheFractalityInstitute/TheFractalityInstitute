# Mitochondrial Implementation Guide for The Fractality Project

## Quick Integration Steps

This guide provides practical steps to integrate the mitochondrial-consciousness principles into your existing Fractality Project codebase.

## 1. Update FractalityEngine.js

Add energy tracking to the main engine:

```javascript
// In FractalityEngine constructor, add:
this.energySystem = {
    total: 1000,
    networks: {
        executive: { energy: 500, nodes: 0 },
        memory: { energy: 300, nodes: 0 },
        sensory: { energy: 200, nodes: 0 }
    }
};

// In the update() method, after performance.startFrame(), add:
// Update metabolic state
this.cace.updateMetabolicState(deltaTime);

// In the _applyContextualVisuals() method, enhance with energy:
_applyContextualVisuals(nodes) {
    nodes.forEach(node => {
        const nodeInfo = this.consciousness.getNodeInfo(node.id);
        if (!nodeInfo) return;
        
        // Energy affects visual properties
        const energyRatio = nodeInfo.energyRatio || 1.0;
        
        // Context affects opacity and scale
        const contextFactor = 1 - (node.contextScore * 0.3);
        
        if (node.id === this.state.focusNode) {
            node.targetOpacity = 1.0;
            node.targetScale = 1.2 * energyRatio; // Energy affects size
        } else {
            node.targetOpacity = (0.3 + (0.7 * contextFactor)) * energyRatio;
            node.targetScale = (0.5 + (0.5 * node.priority / 3)) * Math.sqrt(energyRatio);
        }
        
        // Network-based coloring
        if (nodeInfo.networkColor) {
            node.color.set(nodeInfo.networkColor);
            // Modulate brightness by energy
            node.color.multiplyScalar(0.5 + 0.5 * energyRatio);
        } else {
            // Original color logic
            const hue = (node.depth * 0.15) % 1;
            const saturation = 0.3 + (0.4 * contextFactor);
            const lightness = 0.4 + (0.2 * node.priority / 3) * energyRatio;
            node.color.setHSL(hue, saturation, lightness);
        }
    });
}
```

## 2. Update UI Components

### A. Add Energy Dashboard (PerformanceDashboard.js)

```javascript
// Add to the dashboard HTML:
<div class="metric">
    <span>System ATP:</span>
    <span class="metric-value" id="system-atp">1000</span>
</div>
<div class="metric">
    <span>Metabolic Rate:</span>
    <span class="metric-value" id="metabolic-rate">1.0x</span>
</div>
<div class="network-stats">
    <div class="network-stat executive">
        <span>Executive:</span>
        <span id="exec-energy">50%</span>
    </div>
    <div class="network-stat memory">
        <span>Memory:</span>
        <span id="memory-energy">30%</span>
    </div>
    <div class="network-stat sensory">
        <span>Sensory:</span>
        <span id="sensory-energy">20%</span>
    </div>
</div>

// Add CSS for network colors:
.network-stat.executive { color: #ff00ff; }
.network-stat.memory { color: #00ffff; }
.network-stat.sensory { color: #ffff00; }
```

### B. Update NodeInfoPanel.js

```javascript
// Add energy info to node details:
show(node) {
    const nodeInfo = window.consciousness?.getNodeInfo(node.id);
    
    // ... existing code ...
    
    // Add energy section
    if (nodeInfo) {
        const energyHTML = `
            <div class="info-row">
                <span class="label">Energy:</span>
                <span class="value">${Math.round(nodeInfo.energyRatio * 100)}%</span>
            </div>
            <div class="info-row">
                <span class="label">Network:</span>
                <span class="value" style="color: ${nodeInfo.networkColor}">${nodeInfo.network}</span>
            </div>
            <div class="info-row">
                <span class="label">Health:</span>
                <span class="value">${Math.round(nodeInfo.metabolic.health * 100)}%</span>
            </div>
        `;
        
        // Insert energy info
        this.panel.querySelector('#node-metadata').insertAdjacentHTML('beforeend', energyHTML);
    }
}
```

## 3. Visual Enhancements

### A. Add Energy Particles (in FractalityRenderer.js)

```javascript
// Create energy particle system
_createEnergyParticles() {
    const particleCount = 1000;
    const geometry = new THREE.BufferGeometry();
    const positions = new Float32Array(particleCount * 3);
    const colors = new Float32Array(particleCount * 3);
    
    // Initialize random positions
    for (let i = 0; i < particleCount * 3; i += 3) {
        positions[i] = (Math.random() - 0.5) * 50;
        positions[i + 1] = (Math.random() - 0.5) * 50;
        positions[i + 2] = (Math.random() - 0.5) * 50;
    }
    
    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
    
    const material = new THREE.PointsMaterial({
        size: 0.1,
        vertexColors: true,
        transparent: true,
        opacity: 0.6,
        blending: THREE.AdditiveBlending
    });
    
    this.energyParticles = new THREE.Points(geometry, material);
    this.scene.add(this.energyParticles);
}

// Update particles based on energy flow
_updateEnergyParticles(nodes) {
    const positions = this.energyParticles.geometry.attributes.position.array;
    const colors = this.energyParticles.geometry.attributes.color.array;
    
    // Move particles between high-energy nodes
    for (let i = 0; i < positions.length; i += 3) {
        // Simple movement simulation
        positions[i] += (Math.random() - 0.5) * 0.1;
        positions[i + 1] += (Math.random() - 0.5) * 0.1;
        positions[i + 2] += (Math.random() - 0.5) * 0.1;
        
        // Color based on nearby nodes
        // (simplified - would need spatial indexing for efficiency)
        colors[i] = 1.0;     // R
        colors[i + 1] = 0.5; // G  
        colors[i + 2] = 0.5; // B
    }
    
    this.energyParticles.geometry.attributes.position.needsUpdate = true;
    this.energyParticles.geometry.attributes.color.needsUpdate = true;
}
```

### B. Energy Pulse Effect

```javascript
// Add to node visualization update
if (nodeInfo.isEnergyStarved) {
    // Red pulse for low energy
    const pulse = Math.sin(time * 5) * 0.5 + 0.5;
    node.material.emissive = new THREE.Color(pulse, 0, 0);
} else if (nodeInfo.isEnergyRich) {
    // Green pulse for high energy
    const pulse = Math.sin(time * 3) * 0.3 + 0.7;
    node.material.emissive = new THREE.Color(0, pulse, 0);
}
```

## 4. Keyboard Controls for Energy System

Add to main.js keyboard handler:

```javascript
case 'e':
case 'E':
    // Energy boost (like adrenaline)
    consciousness.energyBoost();
    console.log('⚡ Energy boost activated!');
    break;

case '+':
    // Increase metabolic rate
    consciousness.setMetabolicRate(consciousness.energy.metabolicRate + 0.1);
    console.log(`🔥 Metabolic rate: ${consciousness.energy.metabolicRate.toFixed(1)}x`);
    break;

case '-':
    // Decrease metabolic rate
    consciousness.setMetabolicRate(consciousness.energy.metabolicRate - 0.1);
    console.log(`❄️ Metabolic rate: ${consciousness.energy.metabolicRate.toFixed(1)}x`);
    break;
```

## 5. Data Structure Updates

### A. Update node metadata structure

```javascript
// In DataLoader.js or when creating nodes:
const nodeMetadata = {
    label: "Node Name",
    type: "executive", // or "memory", "sensory", etc.
    tags: ["quantum", "consciousness"],
    // Energy profile hints
    energyDemand: "high", // "low", "medium", "high"
    networkAffinity: "executive" // Preferred network
};
```

### B. Add to test data generator

```javascript
// In TestDataGenerator.js
_generateMetadata(depth, index) {
    const types = ['executive', 'memory', 'sensory', 'processing', 'routing'];
    const type = depth <= 2 ? 'executive' : 
                 depth >= 6 ? 'sensory' : 
                 types[Math.floor(Math.random() * types.length)];
    
    return {
        label: `Node ${depth}-${index}`,
        type: type,
        energyDemand: depth <= 2 ? 'high' : 'medium',
        created: Date.now()
    };
}
```

## 6. Performance Considerations

### A. Energy calculation optimization

```javascript
// Only update energy for visible nodes
const visibleNodes = this.familyView.getVisibleNodes(
    this.state.focusNode,
    this.state.viewConfig
);

// Batch energy updates
if (frameCount % 5 === 0) { // Every 5 frames
    visibleNodes.forEach(node => {
        consciousness.updateNodeMetabolism(
            consciousness.nodes.get(node.id),
            deltaTime * 5
        );
    });
}
```

### B. Level-of-detail for energy

```javascript
// Simplified energy for distant nodes
const distance = node.position.distanceTo(camera.position);
if (distance > 50) {
    // Skip detailed metabolism
    node.consciousness *= 0.99; // Simple decay
} else {
    // Full metabolic simulation
    consciousness.updateNodeMetabolism(node, deltaTime);
}
```

## 7. Debugging Tools

Add debug visualization:

```javascript
// Debug energy flow visualization
if (config.debug.showEnergyFlow) {
    const canvas = document.getElementById('energy-debug');
    const ctx = canvas.getContext('2d');
    
    // Draw network energy levels
    ctx.fillStyle = '#ff00ff';
    ctx.fillRect(10, 10, networks.executive.energy / 5, 20);
    
    ctx.fillStyle = '#00ffff';
    ctx.fillRect(10, 40, networks.memory.energy / 5, 20);
    
    ctx.fillStyle = '#ffff00';
    ctx.fillRect(10, 70, networks.sensory.energy / 5, 20);
}
```

## 8. Configuration Updates

Add to config.js:

```javascript
consciousness: {
    energy: {
        enabled: true,
        totalSystem: 1000,
        baseProduction: 50,
        visualizeFlow: true,
        particleCount: 1000
    },
    networks: {
        executive: { color: '#ff00ff', share: 0.5 },
        memory: { color: '#00ffff', share: 0.3 },
        sensory: { color: '#ffff00', share: 0.2 }
    },
    metabolism: {
        fusionEnabled: true,
        fissionEnabled: true,
        healthDecayRate: 0.99,
        temperatureRegulation: 0.5
    }
}
```

## Testing Strategy

1. **Start Simple**: Enable energy system with just visual changes
2. **Add Metabolism**: Introduce ATP production/consumption
3. **Network Integration**: Assign nodes to networks
4. **Dynamic Effects**: Add fusion/fission and energy sharing
5. **Performance Tune**: Optimize for your target device

## Gotchas & Tips

1. **Energy Balance**: Start with generous energy to avoid starvation
2. **Visual Feedback**: Always show energy state visually
3. **Gradual Changes**: Energy should flow smoothly, not jump
4. **Save/Load**: Remember to serialize energy state
5. **Mobile Performance**: Consider simpler energy model on mobile

---

*With these implementations, The Fractality Project becomes a living, breathing consciousness system where energy truly drives awareness. Each node struggles, thrives, and connects based on its metabolic vitality.*