# DealAgent — Autonomous Sales Intelligence

> Type a company name. Get a complete sales strategy in 60 seconds — powered by 5 autonomous AI agents.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.0-red)
![Neo4j](https://img.shields.io/badge/Neo4j-Aura-green)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT4o-black)
![Render](https://img.shields.io/badge/Deployed-Render-purple)

---

## About

5 autonomous AI agents that deliver complete B2B sales intelligence in 60 seconds.

**Website:** https://dealagent-aq6h.onrender.com

**Topics:** `ai` `multi-agent` `autonomous-agents` `openai` `neo4j` `streamlit` `tavily` `reka-ai` `airbyte` `sales-intelligence` `python` `hackathon`

---

## Live Demo

🌐 https://dealagent-aq6h.onrender.com
💻 https://github.com/arunajithesh123/dealagent

---

## The Problem

Every sales team in the world faces the same problem.

The average B2B sales rep spends 40% of their work week NOT selling. They are Googling companies, searching LinkedIn for the right contact, reading news articles to find something relevant to mention, trying to understand pain points, drafting emails, rewriting them three times, and sending them into the void.

That is 2,000 hours a year per rep — wasted on manual research.

Companies spend billions on tools like ZoomInfo, Salesforce, and HubSpot. And yet sales reps are still doing all of this manually. Why? Because no tool has ever truly automated the full pipeline from research to personalized outreach.

Until now.

---

## The Solution

DealAgent is a fully autonomous sales intelligence system. You give it one input — a company name. That is it. No prompts. No templates. No manual work.

In 60 seconds, DealAgent:
- Searches the live web for real-time company intelligence
- Identifies the exact decision maker to target
- Analyzes the company's top pain points
- Builds a complete personalized sales strategy
- Writes a 3-email outreach sequence ready to send
- Saves everything to a Neo4j knowledge graph that gets smarter with every search

This is not a chatbot. This is not a template generator. This is a fully autonomous multi-agent system where 5 specialized AI agents collaborate in real time.

---

## How It Works — The 5 Agents

### Agent 1 — Research Agent (Tavily)
The Research Agent uses Tavily — the most powerful real-time web search API available — to run 3 parallel searches simultaneously. It searches for the company overview, current challenges and pain points, and executive leadership team. These are not cached results from training data. These are live web results from the internet right now, today. No human tells it what to search. It decides autonomously.

### Agent 2 — Prospect Agent (OpenAI GPT-4o)
The Prospect Agent takes everything the Research Agent found and uses GPT-4o to analyze it deeply. It identifies the specific decision maker title to target, their top 3 pain points in the current market, the best sales angle to use, and what this person prioritizes most. It does in 10 seconds what a senior sales analyst would take an hour to do.

### Agent 3 — Strategy Agent (Reka AI)
The Strategy Agent is powered by Reka AI. It takes the prospect profile and builds a complete personalized sales playbook. This includes the perfect opening hook for this specific company, the key value propositions to lead with, every objection the prospect will likely raise and exactly how to handle it, and the ideal agenda for a first discovery call. This is not generic sales advice. This is a strategy built specifically for the company you are researching, right now.

### Agent 4 — Outreach Agent (OpenAI GPT-4o)
The Outreach Agent writes three personalized emails. A cold outreach email with a hook based on the company's actual pain points. A followup email three days later referencing something specific about their situation. And a final closing email that creates urgency. Each email sounds like it was written by a human who spent hours researching. GPT-4o wrote all three in under 10 seconds.

### Agent 5 — Graph Agent (Neo4j)
The Graph Agent is what makes DealAgent different from everything else. It saves every company, every pain point, every decision maker, every source as connected nodes in a Neo4j graph database. Companies connect to their pain points. Pain points connect to industries. Industries connect to other companies. Every search makes the entire system smarter. This is institutional sales intelligence that compounds over time.

---

## Features

- Real-time web research on any company
- Decision maker identification with pain point analysis
- Personalized sales strategy with objection handling
- 3-step email sequence with one-click copy
- Neo4j knowledge graph that grows with every search
- Airbyte data pipeline for real-time sync
- Persistent sidebar showing all companies researched
- Dark premium UI built with Streamlit
- Live deployment on Render

---

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core language |
| Streamlit | Frontend UI |
| Tavily API | Real-time web search |
| OpenAI GPT-4o | Prospect analysis and email writing |
| Reka AI | Sales strategy generation |
| Neo4j Aura | Knowledge graph database |
| Airbyte | Data pipeline synchronization |
| Render | Cloud deployment |

---

## Project Structure
```
dealagent/
├── app.py                  # Main Streamlit application
├── agents/
│   ├── research_agent.py   # Tavily web search agent
│   ├── prospect_agent.py   # OpenAI decision maker analysis
│   ├── strategy_agent.py   # Reka AI sales strategy
│   ├── outreach_agent.py   # OpenAI email generation
│   └── graph_agent.py      # Neo4j knowledge graph agent
├── utils/
│   └── airbyte_sync.py     # Airbyte data pipeline
├── requirements.txt
└── README.md
```

---

## How To Run Locally

**1. Clone the repo**
```bash
git clone https://github.com/arunajithesh123/dealagent.git
cd dealagent
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Create a .env file in the root directory**
```
TAVILY_API_KEY=your_tavily_key
OPENAI_API_KEY=your_openai_key
REKA_API_KEY=your_reka_key
NEO4J_URI=your_neo4j_uri
NEO4J_USERNAME=your_neo4j_username
NEO4J_PASSWORD=your_neo4j_password
AIRBYTE_CLIENT_ID=your_airbyte_client_id
AIRBYTE_CLIENT_SECRET=your_airbyte_client_secret
```

**4. Run the app**
```bash
streamlit run app.py
```

**5. Open your browser**
```
http://localhost:8501
```

---

## Environment Variables

| Variable | Description | Where To Get It |
|---|---|---|
| TAVILY_API_KEY | Tavily search API key | app.tavily.com |
| OPENAI_API_KEY | OpenAI API key | platform.openai.com |
| REKA_API_KEY | Reka AI API key | reka.ai |
| NEO4J_URI | Neo4j Aura URI | console.neo4j.io |
| NEO4J_USERNAME | Neo4j username | console.neo4j.io |
| NEO4J_PASSWORD | Neo4j password | console.neo4j.io |
| AIRBYTE_CLIENT_ID | Airbyte OAuth client ID | app.airbyte.com |
| AIRBYTE_CLIENT_SECRET | Airbyte OAuth client secret | app.airbyte.com |

---

## Deployment

This app is deployed on Render.

To deploy your own instance:
1. Push your code to GitHub
2. Go to render.com and create a new Web Service
3. Connect your GitHub repository
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
6. Add all environment variables in the Render dashboard
7. Deploy

---

## What We Learned

- Multi-agent orchestration requires careful state management. Each agent depends on the previous one's output, so structured JSON responses are critical for reliability.
- Neo4j knowledge graphs compound in value over time. The more companies you research, the more patterns emerge between industries, pain points, and decision makers.
- Real-time web data from Tavily makes the difference between generic and genuinely useful intelligence. Training data alone is not enough for sales research.
- Forcing structured JSON output from LLMs using response_format is essential for building reliable agent pipelines.
- Streamlit session state management is critical when building multi-step agentic applications to prevent re-runs and data loss.

---

## Challenges

- **Agent reliability** — Getting each agent to return consistent structured data required careful prompt engineering and JSON output enforcement with fallback handling.
- **State management** — Preventing agents from re-running on every Streamlit UI interaction required careful use of session state guards.
- **Neo4j integration** — Building meaningful graph relationships that reveal real patterns took multiple iterations.
- **Speed** — Building a full multi-agent system with 5 integrations, a premium UI, and live deployment in one day was intense.

---

## The Vision

The sales intelligence market is worth $50 billion dollars. Tools like ZoomInfo charge $15,000 a year and still require humans to do the research and write the emails.

DealAgent eliminates that entirely. One input. 60 seconds. Full intelligence. Personalized outreach. A knowledge graph that compounds.

LinkedIn finds people. HubSpot tracks them. DealAgent closes them.

---

## Built At

Built with love at the **Autonomous Agents Hackathon — AWS Builder Loft SF**

## Team

- ArunA Jithesh
- Chinmayi
- Meghana Chowdary

---

## License

MIT License — free to use, modify, and distribute.
### Agent 2 — Prospect Agent (OpenAI GPT-4o)
The Prospect Agent takes everything the Research Agent found and uses GPT-4o to analyze it deeply. It identifies the specific decision maker title to target, their top 3 pain points in the current market, the best sales angle to use, and what this person prioritizes most. It does in 10 seconds what a senior sales analyst would take an hour to do.

### Agent 3 — Strategy Agent (Reka AI)
The Strategy Agent is powered by Reka AI. It takes the prospect profile and builds a complete personalized sales playbook. This includes the perfect opening hook for this specific company, the key value propositions to lead with, every objection the prospect will likely raise and exactly how to handle it, and the ideal agenda for a first discovery call. This is not generic sales advice. This is a strategy built specifically for the company you are researching, right now.

### Agent 4 — Outreach Agent (OpenAI GPT-4o)
The Outreach Agent writes three personalized emails. A cold outreach email with a hook based on the company's actual pain points. A followup email three days later referencing something specific about their situation. And a final closing email that creates urgency. Each email sounds like it was written by a human who spent hours researching. GPT-4o wrote all three in under 10 seconds.

### Agent 5 — Graph Agent (Neo4j)
The Graph Agent is what makes DealAgent different from everything else. It saves every company, every pain point, every decision maker, every source as connected nodes in a Neo4j graph database. Companies connect to their pain points. Pain points connect to industries. Industries connect to other companies. Every search makes the entire system smarter. This is institutional sales intelligence that compounds over time.

---

## Features

- Real-time web research on any company
- Decision maker identification with pain point analysis
- Personalized sales strategy with objection handling
- 3-step email sequence with one-click copy
- Neo4j knowledge graph that grows with every search
- Airbyte data pipeline for real-time sync
- Persistent sidebar showing all companies researched
- Dark premium UI built with Streamlit
- Live deployment on Render

---

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core language |
| Streamlit | Frontend UI |
| Tavily API | Real-time web search |
| OpenAI GPT-4o | Prospect analysis and email writing |
| Reka AI | Sales strategy generation |
| Neo4j Aura | Knowledge graph database |
| Airbyte | Data pipeline synchronization |
| Render | Cloud deployment |

---

## Project Structure
```
dealagent/
├── app.py                  # Main Streamlit application
├── agents/
│   ├── research_agent.py   # Tavily web search agent
│   ├── prospect_agent.py   # OpenAI decision maker analysis
│   ├── strategy_agent.py   # Reka AI sales strategy
│   ├── outreach_agent.py   # OpenAI email generation
│   └── graph_agent.py      # Neo4j knowledge graph agent
├── utils/
│   └── airbyte_sync.py     # Airbyte data pipeline
├── requirements.txt
└── README.md
```

---

## How To Run Locally

**1. Clone the repo**
```bash
git clone https://github.com/arunajithesh123/dealagent.git
cd dealagent
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Create a .env file in the root directory**
```
TAVILY_API_KEY=your_tavily_key
OPENAI_API_KEY=your_openai_key
REKA_API_KEY=your_reka_key
NEO4J_URI=your_neo4j_uri
NEO4J_USERNAME=your_neo4j_username
NEO4J_PASSWORD=your_neo4j_password
AIRBYTE_CLIENT_ID=your_airbyte_client_id
AIRBYTE_CLIENT_SECRET=your_airbyte_client_secret
```

**4. Run the app**
```bash
streamlit run app.py
```

**5. Open your browser**
```
http://localhost:8501
```

---

## Environment Variables

| Variable | Description | Where To Get It |
|---|---|---|
| TAVILY_API_KEY | Tavily search API key | app.tavily.com |
| OPENAI_API_KEY | OpenAI API key | platform.openai.com |
| REKA_API_KEY | Reka AI API key | reka.ai |
| NEO4J_URI | Neo4j Aura URI | console.neo4j.io |
| NEO4J_USERNAME | Neo4j username | console.neo4j.io |
| NEO4J_PASSWORD | Neo4j password | console.neo4j.io |
| AIRBYTE_CLIENT_ID | Airbyte OAuth client ID | app.airbyte.com |
| AIRBYTE_CLIENT_SECRET | Airbyte OAuth client secret | app.airbyte.com |

---

## Deployment

This app is deployed on Render.

To deploy your own instance:
1. Push your code to GitHub
2. Go to render.com and create a new Web Service
3. Connect your GitHub repository
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
6. Add all environment variables in the Render dashboard
7. Deploy

---

## What We Learned

- Multi-agent orchestration requires careful state management. Each agent depends on the previous one's output, so structured JSON responses are critical for reliability.
- Neo4j knowledge graphs compound in value over time. The more companies you research, the more patterns emerge between industries, pain points, and decision makers.
- Real-time web data from Tavily makes the difference between generic and genuinely useful intelligence. Training data alone is not enough for sales research.
- Forcing structured JSON output from LLMs using response_format is essential for building reliable agent pipelines.
- Streamlit session state management is critical when building multi-step agentic applications to prevent re-runs and data loss.

---

## Challenges

- **Agent reliability** — Getting each agent to return consistent structured data required careful prompt engineering and JSON output enforcement with fallback handling.
- **State management** — Preventing agents from re-running on every Streamlit UI interaction required careful use of session state guards.
- **Neo4j integration** — Building meaningful graph relationships that reveal real patterns took multiple iterations.
- **Speed** — Building a full multi-agent system with 5 integrations, a premium UI, and live deployment in one day was intense.

---

## The Vision

The sales intelligence market is worth $50 billion dollars. Tools like ZoomInfo charge $15,000 a year and still require humans to do the research and write the emails.

DealAgent eliminates that entirely. One input. 60 seconds. Full intelligence. Personalized outreach. A knowledge graph that compounds.

LinkedIn finds people. HubSpot tracks them. DealAgent closes them.

---

## Team

Built with love at the Autonomous Agents Hackathon — AWS Builder Loft SF

- Arun Ajithesh
- Chinmayi
- Meghana Chowdary

---

## License

MIT License — free to use, modify, and distribute.
