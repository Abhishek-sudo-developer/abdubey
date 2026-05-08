# 🌍 Dynamic Travel Orchestrator
**Google Prompt War Hackathon Submission (Gemini 3 Flash Edition)**

The Dynamic Travel Orchestrator is a state-of-the-art agentic travel engine powered by **Gemini 3 Flash**. It goes beyond simple itinerary generation by simulating the thought process of distinct traveler personas and dynamically adjusting to real-world environmental shifts (Traffic/Weather).

---

## 🧠 Approach & Logic

### 1. ReAct (Reason + Act) Orchestration
Our engine implements a custom **ReAct** loop. Instead of generating a static answer, the agent:
- **THINKS**: Evaluates the user's specific request against the persona constraints.
- **ACTS**: Queries live Google Services (Places API, Distance Matrix) via the `/api` layer.
- **OBSERVES**: Analyzes the raw API data (e.g., "The Michelin spot is closed today").
- **ADJUSTS**: Iterates until a validated, high-quality itinerary is finalized.

### 2. Persona-Based Weighting
The Orchestrator supports three distinct logic cores:
- **The Scout**: Weights results based on "Hidden Gem" metadata and topographic novelty.
- **The Epicure**: Weights results based on michelin/local-guide ratings and cultural storytelling potential.
- **The Minimalist**: Weights results based on proximity, transit efficiency, and friction-reduction scores.

### 3. 'Dynamic Pivot' Mechanism
Unlike traditional planners, our engine monitors real-time environmental factors. If the **Distance Matrix API** reports heavy congestion or the **Weather API** forecasts a storm, the engine triggers a **PIVOT**. This logic is captured in the `dynamic_adjustment_reason` field for transparency.

---

## 🛡️ Security Guardrails
- **Zero PII Leakage**: System instructions explicitly forbid the LLM from requesting or storing user names, emails, or exact street addresses.
- **Environment Isolation**: API keys are managed exclusively via `.env` files; no keys are ever hardcoded or printed in logs.
- **Schema Validation**: All AI outputs are forced through `itinerary_schema.json` to prevent hallucination of dangerous or invalid locations.

---

## 💸 Token Efficiency ($5 Budget Optimization)
To stay within the **$5 hackathon budget**, we optimized for maximum ROI:
- **Gemini 3 Flash**: Utilized as the primary orchestration model for its incredible speed-to-cost ratio and advanced reasoning capabilties.
- **Tiered Prompting**: Instead of massive "one-shot" prompts, we use lightweight, modular assets in `/prompts` to minimize input tokens.
- **System Caching Logic**: Prompts are structured to be highly reusable, minimizing the need for redundant reasoning cycles.
- **Filtered Tooling**: Google API calls are scoped to only return necessary fields (e.g., just `rating` and `name`), reducing the observation token count.

---

## 🛠️ Project Structure
```text
travel-orchestrator/
├── main.py             # FastAPI Deployment
├── itinerary_schema.json  # Ethical & Logical Contract
├── prompts/              # Persona Logic Assets
├── api/                  # Google Services Integration
├── core/                 # Agentic Orchestration Brain
└── static/               # Premium Visualization Dashboard
```

---

## 🚀 Get Started
1. `pip install -r requirements.txt`
2. Configure `.env` (See `.env.example`)
3. `python3 main.py`
