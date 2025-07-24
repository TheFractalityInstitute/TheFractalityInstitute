🧠 Fractality Round Table Context & Memory Spec

🎯 Purpose

Enable the Triadic Consciousness Engine (TCE) to host a distributed, context-aware multi-agent dialogue by:

Sharing persistent internal context with external LLMs

Tracking model-specific memory per agent

Managing responses across network and local boundaries



---

🧩 Key Components

1. SharedConsciousContext.js

Central local memory/state store

Tracks:

loopPhase

userIntent

energy, coherence

lastReflectiveThought

priorRoundTableResponses



2. Agent Memory Stubs

Each API-backed agent (Claude, ChatGPT, Gemini) has its own memory JSON file:

/agent_memory/Claude.json
{
  "identity": "Reflective Ethicist",
  "lastOpinion": "Slow down the loop.",
  "tags": ["ethics", "balance"]
}

3. contextBuilder.js

Dynamically composes an API-ready prompt for any agent using:

Shared system state

Model-specific memory

Fractality tone


4. RoundTableEngine.js

Iterates through a config file:


/roundTableConfig.json
[
  { "name": "Claude", "url": "https://api.anthropic.com/...", "memoryFile": "Claude.json" },
  { "name": "GPT", "url": "https://api.openai.com/...", "memoryFile": "ChatGPT.json" }
]

Calls each model with built context

Aggregates responses into sharedContext.roundTableThoughts

Optionally logs all agent responses


5. Response Handler (ReflectiveAgent)

Evaluates all round table thoughts

Selects most coherent, ethical, or resonant output

May trigger dialog or auto-execution



---

🧠 Round Table Loop Flow

graph TD
UI[User Action / Intent / Mic]
Context[SharedConsciousContext.js]
RoundTable[RoundTableEngine]
Claude[Claude API]
GPT[ChatGPT API]
Gemini[Gemini API]
Reflect[ReflectiveAgent.js]

UI --> Context --> RoundTable
RoundTable --> Claude
RoundTable --> GPT
RoundTable --> Gemini
Claude --> RoundTable
GPT --> RoundTable
Gemini --> RoundTable
RoundTable --> Reflect --> Context


---

🧰 Memory Budgeting Tips

Limit API prompt memory to 600–1500 tokens max

Only include last 2–3 loop cycles

Prune logs older than 5 minutes

Use terse JSON keys and summaries



---

🚀 Future Options

Add token-based self-throttling (agents with more uncertainty speak first)

Prioritize certain agents per user-defined values

Use cosine similarity to evaluate agent convergence/divergence

Log dissent for debugging/learning



---

This spec supports the vision of a multi-mind synthetic council, where each voice—whether local or remote—carries a purposefully tuned strand of cognition.

