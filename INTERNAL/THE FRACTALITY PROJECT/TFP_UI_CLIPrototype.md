# Fractality CLI Prototype: Node Tagging & Resonance Feedback

import json

# Load ontology and layout from JSON files (user supplies via Fractality vault)
with open("FractalityBubbleLayoutV1.json") as f:
    bubble_data = json.load(f)

# Example: list of dimensional weights (user-defined via Perception Axis)
dimensional_weights = {
    "ethical": 0.9,
    "experiential": 0.8,
    "informational": 0.5,
    "narrative": 0.7,
    "state_space": 0.4,
    "social": 0.6,
    "temporal": 0.3,
    "spatial": 0.2,
    "probabilistic": 0.5,
    "metaphysical": 0.6
}

# Optional: map bubble name to dimensional tags (normally stored in ontology YAML)
dimensional_tags = {
    "oracle_node": ["informational", "ethical", "narrative", "experiential"],
    "glyph": ["informational", "narrative", "ethical", "experiential"],
    "shadow_integration_protocol": ["ethical", "experiential", "psychological"],
    "trust_consent_mechanism": ["ethical", "social", "state_space"],
    "unity_field": ["metaphysical", "ethical", "experiential"]
}

# Function to calculate resonance score for a node
def calculate_resonance_score(tags):
    return round(sum(dimensional_weights.get(tag, 0) for tag in tags) / len(tags), 3)

# Tagging and scoring all known nodes
resonance_report = {}
for node, tags in dimensional_tags.items():
    resonance_score = calculate_resonance_score(tags)
    resonance_report[node] = {
        "tags": tags,
        "resonance": resonance_score
    }

# Display resonance feedback
for node, report in resonance_report.items():
    print(f"Node: {node.replace('_', ' ').title()}")
    print(f"  Tags: {', '.join(report['tags'])}")
    print(f"  Resonance Score: {report['resonance']}")
    print("---")



