# Formal Definitions for Fractal Trinity Ontology

## Context

This document formalizes the five core concepts of the Fractal Trinity Ontology in response to philosophical critiques demanding rigorous definitions. The goal is to transform poetic vision into precise philosophical and mathematical foundations suitable for implementation in Protégé/OWL.

## Core Concept Definitions

### 1. Fractiverse

**Intuitive Vision**: "The infinite lattice of all that exists"

**Formal Definition**:
```
Fractiverse =def A tuple F = ⟨N, E, λ, σ, root⟩ where:
  - N: finite set of nodes (conceptual entities)
  - E ⊆ N × N: structural relations (parent-child, sibling)
  - λ: N → Labels: labeling function
  - σ: N → P(N): self-similarity function mapping nodes to substructures
  - root ∈ N: distinguished root node
  
Axioms:
  1. Connectedness: ∀n ∈ N, ∃ path(root, n)
  2. Self-similarity: ∀n ∈ N, structure(σ(n)) ≈ structure(F)
  3. Finite depth: ∃d ∈ ℕ, ∀n ∈ N, depth(n) ≤ d
```

**Necessary Conditions**:
- Must be a connected graph
- Must have hierarchical structure
- Must exhibit self-similarity at some scale

**Sufficient Conditions**:
- Any finite, rooted, connected DAG with labeled nodes and a self-similarity measure

**Test Cases**:
1. ✓ A mind map with 10 nodes and hierarchy
2. ✓ A single node (trivial case)
3. ✗ A disconnected graph (violates connectedness)
4. ✗ An infinite graph (violates finite depth)

### 2. Observer

**Formal Definition**:
```
Observer =def A tuple O = ⟨id, S, focus, P, t⟩ where:
  - id: unique identifier
  - S ⊆ N: subset of Fractiverse nodes currently accessible to O
  - focus ∈ S: currently attended node (or ∅)
  - P: perspective function S → [0,1] (salience mapping)
  - t ∈ Time: temporal position
  
Operations:
  - attend: Observer × Node → Observer (changes focus)
  - access: Observer × P(Node) → Observer (changes S)
  - perspective_shift: Observer × (S → [0,1]) → Observer
```

**Necessary Conditions**:
- Must have access to some subset of Fractiverse
- Must have at most one focus at time t
- Must assign salience values to accessible nodes

**Sufficient Conditions**:
- Any entity with identifier, accessible nodes, and attention function

### 3. Fractality

**Formal Definition**:
```
Fractality =def A relation between Observer and Fractiverse:
  
fractality(O, F, t) iff:
  1. O.S ⊆ F.N (observer accesses part of Fractiverse)
  2. O.focus ∈ O.S ∪ {∅} (focus is accessible or null)
  3. ∃ path in F from any n ∈ O.S to O.focus (coherent attention)
  4. O.P is continuous on the graph metric of F (smooth salience)
  
Degree of Fractality:
  φ(O, F, t) = |O.S| / |F.N| × coherence(O.P) × stability(O.focus, t)
```

**Properties**:
- Fractality is time-dependent
- Fractality admits of degrees (0 to 1)
- Multiple observers can have different Fractality relations to same Fractiverse

### 4. Resonance Field

**Formal Definition**:
```
ResonanceField =def An emergent structure RF = ⟨N_rf, E_rf, W, τ, source⟩ where:
  - N_rf ⊆ N: participating nodes from Fractiverse
  - E_rf: induced edges based on co-activation
  - W: E_rf → [0,1]: edge weights (resonance strength)
  - τ: Time → [0,1]: decay function
  - source ⊆ O × N: observer-node pairs that generated field
  
Generation Rule:
  resonance_field(O, n₁, n₂, t) generates edge (n₁,n₂) with weight w iff:
    1. n₁, n₂ ∈ O.S (both nodes accessible)
    2. |O.P(n₁) - O.P(n₂)| < ε (similar salience)
    3. semantic_similarity(n₁, n₂) > threshold
    4. temporal_proximity(attend(O,n₁), attend(O,n₂)) < δ
```

**Emergence Conditions**:
- Requires active observer
- Requires multiple nodes with high similarity
- Strengthens with repeated co-activation
- Decays without reinforcement

### 5. Node

**Formal Definition**:
```
Node =def A tuple n = ⟨id, content, type, properties, relations⟩ where:
  - id: UUID (unique identifier)
  - content: semantic content (text, embedding vector, or formula)
  - type ∈ {Structure, Process, Concept, Instance}
  - properties: Map<String, Value> (arbitrary properties)
  - relations: Set<(RelationType, NodeId)>
  
Constraints:
  1. Well-founded: no circular parent relations
  2. Typed: relations must respect type constraints
  3. Semantic: content must be interpretable
```

## Core Axioms: How Concepts Interact

**Axiom 1 (Observation Creates Fields)**:
```
∀O,F,t: fractality(O,F,t) ∧ |O.S| > 1 
  → ∃RF: resonance_field(RF) ∧ generated_by(RF, O, t)
```

**Axiom 2 (Fields Influence Observation)**:
```
∀O,RF,t: interacts(O,RF,t) 
  → ∃O',t': O' = influenced(O,RF) ∧ t' > t
```

**Axiom 3 (Structure Persists)**:
```
∀F,t,t': F.N(t) = F.N(t') ∧ F.E(t) = F.E(t')
  (Fractiverse structure is time-invariant)
```

**Axiom 4 (Conservation of Attention)**:
```
∀O,t: Σ(n ∈ O.S) O.P(n) = 1
  (Total salience is conserved)
```

## Implementation in Protégé/OWL

### OWL Class Definitions
```turtle
:Fractiverse rdf:type owl:Class ;
    rdfs:subClassOf :Graph ;
    owl:hasKey (:root :nodeSet :edgeSet) .

:Observer rdf:type owl:Class ;
    rdfs:subClassOf :Agent ;
    owl:hasKey (:observerId :accessibleNodes :focusNode) .

:ResonanceField rdf:type owl:Class ;
    rdfs:subClassOf :EmergentStructure ;
    owl:hasKey (:participatingNodes :generatingObserver :timestamp) .

:Node rdf:type owl:Class ;
    rdfs:subClassOf :ConceptualEntity ;
    owl:hasKey (:nodeId :content :nodeType) .

:Fractality rdf:type owl:Class ;
    rdfs:subClassOf :Relation ;
    rdfs:comment "The relation between an Observer and Fractiverse" .
```

### Property Definitions
```turtle
:observes rdf:type owl:ObjectProperty ;
    rdfs:domain :Observer ;
    rdfs:range :Node ;
    rdfs:subPropertyOf :attends .

:generates rdf:type owl:ObjectProperty ;
    rdfs:domain :Observer ;
    rdfs:range :ResonanceField ;
    owl:propertyChainAxiom (:observes :activates) .

:hasAccessTo rdf:type owl:ObjectProperty ;
    rdfs:domain :Observer ;
    rdfs:range :Node ;
    owl:TransitiveProperty .

:resonatesWith rdf:type owl:ObjectProperty ;
    rdfs:domain :Node ;
    rdfs:range :Node ;
    owl:SymmetricProperty .
```

### Constraints
```turtle
:SingleFocus rdf:type owl:Restriction ;
    owl:onProperty :focusNode ;
    owl:maxCardinality "1"^^xsd:integer .

:Observer rdfs:subClassOf :SingleFocus .

:FiniteAccess rdf:type owl:Restriction ;
    owl:onProperty :hasAccessTo ;
    owl:someValuesFrom :Node .

:Observer rdfs:subClassOf :FiniteAccess .
```

## Philosophical Grounding

### Metaphysical Commitments
1. **Structural Realism**: The Fractiverse exists as a structure independent of observers
2. **Process Philosophy**: Resonance Fields are dynamic processes, not static entities
3. **Neutral Monism**: Both mental (Fractality) and physical (Fractiverse) are aspects of a more fundamental reality

### Relationship to Existing Frameworks
- **IIT**: Fractality measure φ analogous to integrated information
- **Global Workspace**: Observer's focus implements attention/access consciousness
- **Predictive Processing**: Resonance Fields as prediction error minimization

## Open Questions for Refinement

1. **Self-Similarity Formalization**: How precisely should we define the self-similarity function σ?
2. **Consciousness Aspect**: Should consciousness be a property of Observers or emerge from Fractality relations?
3. **Multiple Observers**: How do multiple Observers' fields interact/interfere?
4. **Temporal Dynamics**: Should the Fractiverse structure really be time-invariant?
5. **Quantification**: What metrics best capture "coherence" and "stability"?

## Validation Criteria

**Formal Consistency**:
- [ ] No contradictions in axiom set
- [ ] All definitions well-formed
- [ ] Inference rules preserve truth

**Philosophical Adequacy**:
- [ ] Captures intuitive notion of consciousness-structure interaction
- [ ] Avoids category errors
- [ ] Respects established philosophical distinctions

**Implementation Feasibility**:
- [ ] Expressible in OWL-DL
- [ ] Computationally tractable
- [ ] Mappable to software objects

## Next Steps

1. **Philosophical Review**: Submit definitions to philosophy colleagues for critique
2. **Formal Verification**: Use Protégé reasoner to check consistency
3. **Test Implementation**: Create small example with 10 nodes
4. **Iterate**: Refine based on failures and insights
5. **Extend**: Add secondary concepts once core is solid

---

*This formalization attempts to balance mathematical precision with philosophical depth while remaining implementable. The definitions are starting points for rigorous development, not final answers.*