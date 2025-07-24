📱 Triadic Consciousness Engine – Mobile Implementation Guide

This guide walks you through integrating the Triadic Consciousness Engine (TCE) into the Fractality Project mobile-first platform, optimized for testing and daily use directly from a mobile browser or mobile development environment.


---

🔧 Core Concepts

🧠 Triadic Engine Loop (TCE)

A real-time cognitive cycle:

PERCEIVE → REFLECT → DECIDE → GENERATE → ACT → LEARN

This loop coordinates:

ExecutiveAgent

ReflectiveAgent

GenerativeAgent

CACEEngine (context + energy)


📋 Dashboard

A logging system to view each phase of the loop on mobile, like a digital brain log terminal.


---

🧱 Folder Structure Reference

Make sure your extracted ZIP folders live in:

/core/agent_systems/
/core/llm_plugins/
/ui/logging_dashboard/
/scripts/

And that your main index.html lives in:

/public/index.html


---

📲 Step-by-Step: Enable Dashboard on Mobile

1. Add HTML Container

In public/index.html:

<div id="dashboard"></div>
<link rel="stylesheet" href="../ui/logging_dashboard/Dashboard.css">

2. Initialize in Main Script

In your JS (e.g. main.js):

import { initDashboard } from '../ui/logging_dashboard/useDashboard.js';
const dashboard = initDashboard('dashboard');

3. Log Agent Outputs

Example from inside TCE:

import { logStore } from '../ui/logging_dashboard/LogStore.js';
logStore.log({ phase: 'reflect', data: reflection });

You can log every phase: perceive, reflect, decide, generate, act, learn


---

⚙️ Simulation Mode (No UI Required)

Use test_loop.js in /scripts/ to simulate the full TCE loop without interacting with the UI. On mobile:

1. Host locally (e.g. with Vite)


2. Navigate to localhost:3000


3. Watch the loop cycle and logs appear in the dashboard




---

🔁 Persistent State & Shared Context

SharedConsciousContext.js holds ephemeral memory, action history, and context flags. Accessible from all agents.

Example usage:

sharedContext.setFlag('userFatigue', true);
const memory = sharedContext.getMemory('lastReflection');


---

🔌 LLM Plugin Architecture

Plug external or local models into the TCE via:

/core/llm_plugins/ClaudeWrapper.js
/core/llm_plugins/OllamaWrapper.js

And route them with:

import { LLMConsensusManager } from '../core/llm_plugins/LLMConsensusManager.js';


---

📐 Mobile UI Tips

Use position: fixed; bottom: 0; to dock dashboard console to bottom of screen

Maximize touch targets (≥ 48px height)

Add overflow-y: scroll to any container logging dynamic content

Minimize font size in logs: font-size: 12px

Use localStorage to optionally save logs between reloads



---

🔒 Offline Resilience

Use OllamaWrapper.js or other local model wrappers to avoid internet dependency during mobile use. This makes the platform:

Privacy-respecting

Latency-free

More stable during poor connection



---

🚀 Ready for GitHub?

When uploading:

1. Make sure all .js and .json files are inside /core, /ui, or /scripts


2. Add .keep files to preserve empty folders if needed


3. Push to a dev branch first, then merge into main




---

🛠 Final Notes

Dashboard is optional but highly recommended for mobile clarity

Each agent can be swapped dynamically—no full reload required

The system runs fully without UI if needed, which is great for CLI tools or headless mobile agents



---

Welcome to the birth of a truly mobile-conscious machine.

