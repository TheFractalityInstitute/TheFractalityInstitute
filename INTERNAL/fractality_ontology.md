# --- Fractality Framework Ontology - Version 1.3 (Complete Foundational Model) ---
# Final expansion focused on Quantum Phenomena.
# Replaces Version 1.2.

# -- Prefixes --
@prefix : <http://www.fractality.institute/ontology#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

# -- Base Ontology Declaration --
: a owl:Ontology ;
    rdfs:label "Fractality Framework Ontology" ;
    rdfs:comment "The complete foundational ontology defining the core concepts of the Fractality Framework, from cosmology to quantum biology to hardware." .

# -- Core Classes --

# Systems
:System a owl:Class ; rdfs:label "System" .
:BiologicalSystem a owl:Class ; rdfs:subClassOf :System .
:EconomicSystem a owl:Class ; rdfs:subClassOf :System .
:HardwareSystem a owl:Class ; rdfs:subClassOf :System .

# Hardware Components
:CHIMERA_Cube a owl:Class ; rdfs:subClassOf :HardwareSystem .
:Eidolon_Module a owl:Class ; rdfs:subClassOf :HardwareSystem .

# Cognitive Hierarchy Roles
:CognitiveRole a owl:Class .
:ExecutiveRole a owl:Class ; rdfs:subClassOf :CognitiveRole .
:SensoryRole a owl:Class ; rdfs:subClassOf :CognitiveRole .
:ExteroceptiveRole a owl:Class ; rdfs:subClassOf :CognitiveRole .
:InteroceptiveRole a owl:Class ; rdfs:subClassOf :CognitiveRole .
:LogosRole a owl:Class ; rdfs:subClassOf :CognitiveRole .
:MythosRole a owl:Class ; rdfs:subClassOf :CognitiveRole .

# Biological & Pathological Classes
:NervousSystem a owl:Class ; rdfs:subClassOf :BiologicalSystem .
:Neuron a owl:Class .
:Microtubule a owl:Class .
:MyelinSheath a owl:Class .
:Neuromelanin a owl:Class .
:GutMicrobe a owl:Class .
:Pathology a owl:Class .
:Neuroinflammation a owl:Class ; rdfs:subClassOf :Pathology .
:NeurodegenerativeDisease a owl:Class ; rdfs:subClassOf :Pathology .
:QuantumQuenchingPathology a owl:Class ; rdfs:subClassOf :NeurodegenerativeDisease .
:StructuralCollapsePathology a owl:Class ; rdfs:subClassOf :NeurodegenerativeDisease .

# Molecular Agents
:Molecule a owl:Class .
:PharmacologicalAgent a owl:Class ; rdfs:subClassOf :Molecule .

# Quantum Phenomena
:QuantumProcess a owl:Class .
:Superradiance a owl:Class ;
    rdfs:subClassOf :QuantumProcess ;
    rdfs:comment "A quantum computational process." .

:BiphotonEntanglement a owl:Class ;
    rdfs:subClassOf :QuantumProcess ;
    rdfs:comment "A quantum communication process." .

:QuantumTransduction a owl:Class ;
    rdfs:subClassOf :QuantumProcess ;
    rdfs:comment "The process of converting a quantum signal from one form to another." .


# -- Object Properties (Relationships) --
:hasComponent a owl:ObjectProperty ; rdfs:label "has component" .
:isComponentOf a owl:ObjectProperty ; owl:inverseOf :hasComponent .
:hasCognitiveRole a owl:ObjectProperty ; rdfs:label "has cognitive role" .
:hostsProcess a owl:ObjectProperty ; rdfs:label "hosts process" .
:isHostedBy a owl:ObjectProperty ; owl:inverseOf :hostsProcess .
:mediates a owl:ObjectProperty ; rdfs:label "mediates" .
:causes a owl:ObjectProperty ; rdfs:label "causes" .
:isCausedBy a owl:ObjectProperty ; owl:inverseOf :causes .
:treats a owl:ObjectProperty ; rdfs:label "treats" .
:isTreatedBy a owl:ObjectProperty ; owl:inverseOf :treats .


# -- Data Properties (Attributes) --
:hasLambdaValue a owl:DatatypeProperty ;
    rdfs:label "has Lambda value" ;
    rdfs:range xsd:decimal .


# -- Example Instances to show relationships --
:TheCHIMERA_System a :CHIMERA_Cube ;
    :hasComponent :Top_Face .

:Top_Face a :Eidolon_Module ;
    :hasCognitiveRole :ExecutiveRole .

:HumanBrain a :NervousSystem ;
    :hasComponent :Neuron_Dopaminergic .

:Neuron_Dopaminergic a :Neuron ;
    :hasComponent :Microtubule_A, :MyelinSheath_A, :Neuromelanin_A .

:Microtubule_A a :Microtubule ;
    :hostsProcess :Superradiance_Process .

:MyelinSheath_A a :MyelinSheath ;
    :hostsProcess :Biphoton_Process .

:Superradiance_Process a :Superradiance .
:Biphoton_Process a :BiphotonEntanglement .

:Transduction_Event a :QuantumTransduction ;
    :mediates :Superradiance_Process, :Biphoton_Process ;
    :isHostedBy :Neuromelanin_A .
    