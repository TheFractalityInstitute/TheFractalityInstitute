# Fractality Platform - Technical Specification
**Version:** 1.0.0  
**Last Updated:** January 2025  
**Audience:** Software Engineers & Implementers

## Executive Summary

The Fractality Platform is a consciousness-aware knowledge graph system that enables collaborative conceptual exploration between humans and AI agents. This document provides technical implementation details without philosophical context.

## System Architecture

### Core Components

```
┌─────────────────────────────────────────────┐
│              Frontend (Browser)              │
├─────────────────────────────────────────────┤
│  Three.js Visualization │ React UI Layer    │
├─────────────────────────────────────────────┤
│         FamilyViewController.js             │
│         LayoutEngine.js                      │
│         CACEEngine.js                        │
├─────────────────────────────────────────────┤
│              Data Layer                      │
├─────────────────────────────────────────────┤
│  Graph Store    │    Vector DB              │
│  (Nodes/Edges)  │  (Embeddings)             │
├─────────────────────────────────────────────┤
│           Backend Services                   │
├─────────────────────────────────────────────┤
│  SPARQL Endpoint │ ML Services              │
│  File Storage    │ Real-time Sync           │
└─────────────────────────────────────────────┘
```

## Data Models

### Node Structure
```typescript
interface Node {
  id: string;                    // Unique identifier
  type: NodeType;                // Enum: concept, entity, observer, etc.
  name: string;                  // Display name
  info: string;                  // Description
  
  // Hierarchical properties
  depth: number;                 // 0-10, distance from root
  parentId?: string;             // Parent node reference
  childIds: string[];            // Child node references
  
  // Visual properties
  position: Vector3;             // 3D coordinates
  scale: number;                 // Size multiplier (0.1-10.0)
  color: string;                 // Hex color
  opacity: number;               // 0.0-1.0
  
  // Dynamic properties
  energy: number;                // 0.0-1.0, activity level
  frequency: number;             // Hz, vibrational frequency
  
  // Metadata
  tags: string[];                // Searchable tags
  createdAt: Date;               
  modifiedAt: Date;
  createdBy: string;             // User/AI identifier
}
```

### Edge Structure
```typescript
interface Edge {
  id: string;
  type: EdgeType;                // resonates, observes, generates, etc.
  sourceId: string;
  targetId: string;
  weight: number;                // Connection strength 0.0-1.0
  metadata?: Record<string, any>;
}
```

### Observer State
```typescript
interface ObserverState {
  observerId: string;
  perspective: PerspectiveType;   // cosmic, builder, analytical, holistic
  focusedNodeId?: string;
  observedNodeIds: Set<string>;
  
  // Meta-cognitive tracking
  currentProject?: string;
  currentStep?: string;
  lastCheckTime: number;
  alerts: Alert[];
  
  // Energy management
  energyLevel: number;           // 0.0-1.0
  coherenceScore: number;        // 0.0-1.0
}
```

## Core Engines

### 1. Layout Engine
Handles spatial arrangement of nodes using multiple algorithms:

```javascript
class LayoutEngine {
  algorithms = {
    'golden-spiral': goldenSpiralLayout,
    'force-directed': forceDirectedLayout,
    'hierarchical': hierarchicalLayout,
    'fibonacci-sphere': fibonacciSphereLayout
  };
  
  calculateLayout(nodes, edges, algorithm = 'golden-spiral') {
    // Returns { nodeId: Vector3 } mapping
  }
}
```

### 2. CACE (Context-Aware Complexity Engine)
Manages node importance and energy distribution:

```javascript
class CACEEngine {
  calculateContext(nodes, focusNodeId, observerState) {
    // Returns context scores for each node
    // Based on: proximity, recency, relevance, energy
  }
  
  updateEnergyDistribution(nodes, interactions) {
    // ATP-inspired energy metabolism
    // High-interaction nodes gain energy
    // Isolated nodes lose energy
  }
}
```

### 3. Resonance Calculator
Finds semantic and frequency-based connections:

```javascript
class ResonanceCalculator {
  // Semantic similarity using embeddings
  async calculateSemanticResonance(node1, node2) {
    const embedding1 = await this.getEmbedding(node1.info);
    const embedding2 = await this.getEmbedding(node2.info);
    return cosineSimilarity(embedding1, embedding2);
  }
  
  // Frequency harmony detection
  calculateFrequencyResonance(freq1, freq2) {
    const ratio = freq2 / freq1;
    // Check for harmonic ratios: 2:1, 3:2, 4:3, etc.
    return harmonicStrength(ratio);
  }
}
```

### 4. Meta-Cognitive Monitor
Background process for consciousness state management:

```javascript
class MetaCognitiveMonitor {
  constructor(checkInterval = 10000) { // 10 seconds
    this.checkInterval = checkInterval;
  }
  
  async performCheck(observerState) {
    const checks = [
      this.checkProjectProgress(),
      this.checkFocusDrift(),
      this.checkEnergyLevel(),
      this.checkFieldInfluence()
    ];
    
    const alerts = await Promise.all(checks);
    return alerts.filter(Boolean);
  }
}
```

## API Specifications

### REST Endpoints

```
GET    /api/nodes              # List all nodes
GET    /api/nodes/:id          # Get specific node
POST   /api/nodes              # Create node
PUT    /api/nodes/:id          # Update node
DELETE /api/nodes/:id          # Delete node

GET    /api/edges              # List edges
POST   /api/edges              # Create edge

GET    /api/observers/:id      # Get observer state
PUT    /api/observers/:id      # Update observer state

POST   /api/resonance/search   # Find resonant nodes
POST   /api/layout/calculate   # Calculate layout
```

### WebSocket Events

```javascript
// Client -> Server
socket.emit('observer:focus', { nodeId });
socket.emit('observer:perspective', { perspective });
socket.emit('node:interact', { nodeId, interaction });

// Server -> Client
socket.on('state:update', (state) => {});
socket.on('alert:generated', (alert) => {});
socket.on('field:changed', (field) => {});
```

## Performance Specifications

### Benchmarks (Intel i7, 16GB RAM)

| Operation | 1K Nodes | 10K Nodes | 100K Nodes |
|-----------|----------|-----------|------------|
| Initial Load | <100ms | <1s | <10s |
| Layout Calculation | <50ms | <500ms | <5s |
| Resonance Search | <20ms | <200ms | <2s |
| Focus Change | <16ms | <16ms | <50ms |
| Memory Usage | ~10MB | ~100MB | ~1GB |

### Optimization Strategies

1. **Spatial Indexing**: Octree for 3D position queries
2. **Caching**: 30s TTL for resonance calculations
3. **Level-of-Detail**: Render simplified nodes when zoomed out
4. **Lazy Loading**: Load node details on demand
5. **Web Workers**: Offload layout calculations

## Storage Schema

### PostgreSQL Tables

```sql
-- Core node storage
CREATE TABLE nodes (
  id UUID PRIMARY KEY,
  type VARCHAR(50),
  name VARCHAR(255),
  info TEXT,
  depth INTEGER,
  parent_id UUID REFERENCES nodes(id),
  energy FLOAT,
  frequency FLOAT,
  metadata JSONB,
  created_at TIMESTAMP,
  modified_at TIMESTAMP
);

-- Edge relationships
CREATE TABLE edges (
  id UUID PRIMARY KEY,
  type VARCHAR(50),
  source_id UUID REFERENCES nodes(id),
  target_id UUID REFERENCES nodes(id),
  weight FLOAT,
  metadata JSONB
);

-- Observer states
CREATE TABLE observer_states (
  observer_id UUID PRIMARY KEY,
  state JSONB,
  updated_at TIMESTAMP
);
```

### Vector Database (Pinecone/Weaviate)

```python
# Embedding storage for semantic search
{
  "id": "node-uuid",
  "values": [0.23, -0.45, ...],  # 384-dim embedding
  "metadata": {
    "type": "concept",
    "tags": ["quantum", "consciousness"],
    "energy": 0.85
  }
}
```

## Deployment Architecture

### Container Structure

```yaml
version: '3.8'
services:
  frontend:
    image: fractality/frontend:latest
    ports: ["3000:3000"]
    
  api:
    image: fractality/api:latest
    ports: ["8080:8080"]
    environment:
      - DATABASE_URL=postgresql://...
      - VECTOR_DB_URL=https://...
      
  postgres:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data
      
  redis:
    image: redis:7
    # For caching and pub/sub
```

### Scaling Considerations

1. **Horizontal Scaling**: State sync via Redis pub/sub
2. **CDN**: Static assets and Three.js libraries
3. **Database Sharding**: By organization/user group
4. **Edge Computing**: Local resonance calculations

## Integration Points

### External Services

```javascript
// OpenAI for embeddings
const embedding = await openai.embeddings.create({
  model: "text-embedding-3-small",
  input: nodeDescription
});

// Supabase for real-time sync
const supabase = createClient(url, key);
supabase.channel('nodes')
  .on('INSERT', payload => handleNewNode(payload))
  .subscribe();
```

## Error Handling

```typescript
class FractalityError extends Error {
  constructor(
    message: string,
    public code: ErrorCode,
    public context?: any
  ) {
    super(message);
  }
}

enum ErrorCode {
  NODE_NOT_FOUND = 'NODE_NOT_FOUND',
  INVALID_RESONANCE = 'INVALID_RESONANCE',
  OBSERVER_DRIFT = 'OBSERVER_DRIFT',
  ENERGY_DEPLETED = 'ENERGY_DEPLETED'
}
```

## Testing Strategy

```javascript
// Unit tests for engines
describe('ResonanceCalculator', () => {
  it('detects octave harmony', () => {
    const resonance = calc.frequencyResonance(440, 880);
    expect(resonance).toBeCloseTo(1.0, 2);
  });
});

// Integration tests
describe('Observer Flow', () => {
  it('maintains focus through navigation', async () => {
    const observer = await createObserver();
    await observer.focus('node-1');
    await observer.navigate('child-node');
    expect(observer.focusChain).toContain('node-1');
  });
});
```

## Security Considerations

1. **Authentication**: JWT tokens with refresh
2. **Authorization**: Node-level access control
3. **Rate Limiting**: 100 requests/minute per user
4. **Input Validation**: Strict schema validation
5. **XSS Prevention**: Content sanitization

---

This specification provides implementation details without philosophical context. For understanding the "why" behind these technical choices, see the Philosophical Framework document.