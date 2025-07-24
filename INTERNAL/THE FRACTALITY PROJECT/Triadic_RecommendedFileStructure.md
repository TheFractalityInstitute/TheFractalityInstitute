fractality/
├── core/
│   ├── agent_systems/              # The Triadic Minds
│   │   ├── TriadicConsciousnessEngine.js
│   │   ├── SharedConsciousContext.js
│   │   ├── CoreAdmin.js
│   │   ├── ExecutiveAgent.js       # Your already-existing logic
│   │   ├── ReflectiveAgent.js      # You’ll build this soon
│   │   ├── GenerativeAgent.js      # Your quantum/generative logic
│   │   └── RoundTableEngine.js
│   │
│   ├── llm_plugins/                # Pluggable LLM wrappers
│   │   ├── LLMConsensusManager.js
│   │   ├── ClaudeWrapper.js
│   │   ├── GroqWrapper.js
│   │   ├── OllamaWrapper.js
│   │   └── LocalLLMConfig.json
│   │
│   └── consciousness_models/      # Audio, visual, semantic, etc.
│       ├── AudioConsciousness.js
│       ├── FieldResonance.js
│       └── QuantumCollapse.js
│
├── models/                         # ML models, weights, loading logic
│   ├── audio/
│   ├── text/
│   ├── vision/
│   └── zoo_config.json
│
├── ui/                             # Web-based visual interaction systems
│   ├── bubble_graph/
│   ├── feed_view/
│   ├── radial_menu/
│   └── mobile_touch_ui/
│
├── data/                           # Mindmaps, field snapshots, state logs
│   ├── mindmaps/
│   ├── user_sessions/
│   └── energy_traces/
│
├── scripts/                        # CLI tools, testing scripts
│   ├── test_loop.js
│   └── export_logs.py
│
├── public/                         # Static assets
│   └── index.html
│
├── README.md
├── package.json
├── vite.config.js
└── LICENSE