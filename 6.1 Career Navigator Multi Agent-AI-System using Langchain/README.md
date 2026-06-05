<div align="center">

```
 ██████╗ █████╗ ██████╗ ███████╗███████╗██████╗     ███╗   ██╗ █████╗ ██╗   ██╗
██╔════╝██╔══██╗██╔══██╗██╔════╝██╔════╝██╔══██╗    ████╗  ██║██╔══██╗██║   ██║
██║     ███████║██████╔╝█████╗  █████╗  ██████╔╝    ██╔██╗ ██║███████║██║   ██║
██║     ██╔══██║██╔══██╗██╔══╝  ██╔══╝  ██╔══██╗    ██║╚██╗██║██╔══██║╚██╗ ██╔╝
╚██████╗██║  ██║██║  ██║███████╗███████╗██║  ██║    ██║ ╚████║██║  ██║ ╚████╔╝ 
 ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝    ╚═╝  ╚═══╝╚═╝  ╚═╝  ╚═══╝ 
```

# 💼 Career Navigator Multiagent AI
### *AI-Powered Multi-Agent Career Intelligence Platform*

---

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![LangChain](https://img.shields.io/badge/LangChain-0.2+-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)](https://langchain.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![OpenRouter](https://img.shields.io/badge/OpenRouter-GPT--4o--mini-412991?style=for-the-badge)](https://openrouter.ai)
[![Tavily](https://img.shields.io/badge/Tavily-Search_API-00B4D8?style=for-the-badge)](https://tavily.com)

---

**Six autonomous AI agents. One intelligent pipeline. Your complete career strategy — built from live market data.**

</div>

---

## 📌 Table of Contents

- [Overview](#-overview)
- [What Makes This Different](#-what-makes-this-different)
- [System Architecture](#-system-architecture)
- [Multi-Agent Pipeline](#-multi-agent-pipeline)
- [Tools](#-tools)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
  - [Conda Environment](#conda-environment)
  - [Python Virtual Environment](#python-virtual-environment)
- [Environment Variables](#-environment-variables)
- [Running the Application](#-running-the-application)
- [Streamlit Dashboard Features](#-streamlit-dashboard-features)
- [Agent Details](#-agent-details)
- [Pipeline Execution Flow](#-pipeline-execution-flow)
- [Future Improvements](#-future-improvements)
- [Author](#-author)

---

## 🧭 Overview

**Career Navigator AI** is a production-grade multi-agent career intelligence system built on **LangChain Agents**, **LCEL (LangChain Expression Language)**, and a coordinated 6-step autonomous pipeline.

Unlike static career tools, this platform operates entirely on **live external data**:

- It **searches real job postings** from the live market using the JSearch API
- It **scrapes actual job descriptions** to extract real skill requirements
- It **fetches real-time salary benchmarks** from the OpenWebNinja Salary API
- It **discovers learning resources** via Tavily web search
- It **synthesizes everything** into a structured career intelligence report

The system is built around a **shared state memory architecture** — each agent passes its output to the next through a central state dictionary, creating an interconnected, context-aware intelligence pipeline.

---

## 🔥 What Makes This Different

| Typical Career Tool | Career Navigator AI |
|---|---|
| Static dataset-based recommendations | Live job market data via JSearch API |
| Generic skill lists | Real skills extracted from actual job postings |
| Estimated salary ranges | Live salary data from OpenWebNinja Salary API |
| Pre-built course lists | Real-time learning resources via Tavily Search |
| One-size-fits-all advice | Context-aware advice synthesized across all agents |
| No state sharing | Shared state memory — all agents share context |
| Single model | GPT-4o-mini (pipeline) + GPT-5 (interactive UI) |

---

## 🏗️ System Architecture

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                              USER INPUT                                      ║
║                                                                              ║
║   Career Goal  ───────  Target Location  ──────  Years of Experience         ║
╚══════════════════════════════════════════════════════════════════════════════╝
                                    │
                                    ▼
╔══════════════════════════════════════════════════════════════════════════════╗
║                          SHARED STATE MEMORY                                 ║
║                                                                              ║
║   state["jobs"]  │  state["skills"]  │  state["salary"]  │  state["roadmap"] ║
║   state["career_advice"]  │  state["final_report"]                           ║
╚══════════════════════════════════════════════════════════════════════════════╝
          │              │              │              │              │
          ▼              ▼              ▼              ▼              ▼
    ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
    │ AGENT 1  │──▶│ AGENT 2  │──▶│ AGENT 3  │──▶│ AGENT 4  │──▶│ AGENT 5│
    │  Job     │   │  Skill   │   │  Salary  │   │ Learning │   │ Career   │
    │  Search  │   │  Extract │   │  Intel   │   │  Roadmap │   │ Advisor  │
    └──────────┘   └──────────┘   └──────────┘   └──────────┘   └──────────┘
          │              │              │              │              │
          ▼              ▼              ▼              ▼              ▼
    JSearch API    Web Scraping    Salary API     Tavily API      LLM Only
    (OpenWebNinja) (Requests +    (OpenWebNinja) (Tavily Search)  (No Tools)
                   BS4 + Traf.)
                                    │
                                    ▼
╔══════════════════════════════════════════════════════════════════════════════╗
║                     CAREER REPORT GENERATOR  (LCEL CHAIN)                    ║
║                                                                              ║
║   ChatPromptTemplate  ──▶  ChatOpenAI (GPT-4o-mini)  ──▶  StrOutputParser   ║
╚══════════════════════════════════════════════════════════════════════════════╝
                                    │
                                    ▼
                    ╔═══════════════════════════╗
                    ║   FINAL CAREER REPORT     ║
                    ║   ✓ Job Opportunities     ║
                    ║   ✓ Skills Analysis       ║
                    ║   ✓ Salary Insights       ║
                    ║   ✓ Learning Roadmap      ║
                    ║   ✓ Career Strategy       ║
                    ║   ✓ 30-60-90 Day Plan     ║
                    ╚═══════════════════════════╝
```

---

## 🤖 Multi-Agent Pipeline

### Agent 1 — Job Search Agent

```
TOOL        : search_jobs()
API         : OpenWebNinja JSearch API
PURPOSE     : Find live job opportunities for the user's career goal

INPUT       : Career goal (natural language query)

OUTPUT
├── Job Title
├── Company Name
├── Location
├── Employment Type
├── Remote Status
├── Salary (when available)
├── Apply URL
└── Job Description Summary

STORED IN   : state["jobs"]
```

---

### Agent 2 — Skill Extraction Agent

```
TOOL        : extract_skills()
STRATEGY    : Multi-layered web scraping

   1. Trafilatura          ──▶  Best for clean article-style extraction
   2. Readability-LXML     ──▶  Main content extraction fallback
   3. BeautifulSoup        ──▶  Full page fallback

INPUT       : Job posting URL (from Agent 1 results)

OUTPUT CATEGORIES
├── Technical Skills
├── Programming Languages
├── Tools & Technologies
├── Frameworks & Platforms
├── Cloud Platforms
├── Databases
├── AI / ML / GenAI Skills
├── Business Skills
├── Domain Knowledge
├── Certifications
├── Education Requirements
├── Experience Requirements
├── Soft Skills
└── Other Requirements

STORED IN   : state["skills"]
```

---

### Agent 3 — Salary Intelligence Agent

```
TOOL        : salary_research()
API         : OpenWebNinja Job Salary API
PURPOSE     : Research salary benchmarks for target role

INPUT
├── Job Title
├── Location
└── Years of Experience

OUTPUT
├── Median Salary
├── Salary Range (Min - Max)
├── Base Salary Range
├── Additional Compensation
├── Currency
├── Salary Period
├── Confidence Score
└── Source Publisher

STORED IN   : state["salary"]
```

---

### Agent 4 — Learning Roadmap Agent

```
TOOL        : find_courses()
API         : Tavily Search API
PURPOSE     : Discover learning resources aligned to required skills

INPUT       : Extracted skills from Agent 2

OUTPUT
├── Recommended Courses
├── Certifications
├── Learning Sequence (ordered steps)
├── Learning Timeline (monthly breakdown)
├── Practical Projects
├── Learning Resources (with URLs)
└── Key Recommendations

STORED IN   : state["roadmap"]
```

---

### Agent 5 — Career Advisor Agent

```
TOOLS       : None (pure LLM reasoning)
PURPOSE     : Strategic career analysis based on all previous agent outputs

INPUT
├── state["jobs"]
├── state["skills"]
├── state["salary"]
└── state["roadmap"]

OUTPUT
├── Career Recommendations
├── Skill Priority Rankings
├── Industry Insights
├── Identified Strengths
├── Skill Gaps
├── 30-60-90 Day Action Plan
└── Expected Outcomes

STORED IN   : state["career_advice"]
```

---

### Step 6 — Career Report Generator (LCEL Chain)

```
TYPE        : LangChain Expression Language (LCEL) Chain

CHAIN       : ChatPromptTemplate | ChatOpenAI | StrOutputParser

INPUT       : All state values (jobs, skills, salary, roadmap, career_advice)

SECTIONS GENERATED
├── Career Goal Summary
├── Current Job Market Opportunities
├── Most In-Demand Skills
├── Salary Intelligence
├── Recommended Learning Roadmap
├── Strengths Identified
├── Skill Gaps
├── Career Recommendations
├── 30-60-90 Day Action Plan
└── Final Verdict
```

---

## 🔧 Tools

| Tool | API / Library | Purpose |
|---|---|---|
| `search_jobs()` | OpenWebNinja JSearch API | Live job search from Google & Glassdoor Jobs |
| `extract_skills()` | Requests + BeautifulSoup + Readability-LXML + Trafilatura | Multi-strategy job posting scraper |
| `salary_research()` | OpenWebNinja Job Salary API | Salary benchmarking and market data |
| `find_courses()` | Tavily Search API | Learning resource discovery |

---

## 🛠️ Tech Stack

### AI & LLM Layer

| Component | Technology |
|---|---|
| Agent Framework | LangChain Agents (`create_agent`) |
| Chain Architecture | LCEL (LangChain Expression Language) |
| Pipeline Orchestration | Custom shared state pipeline |
| LLM — Pipeline | GPT-4o-mini via OpenRouter |
| LLM — Interactive UI | GPT-5 via OpenWebNinja |
| Prompt Management | `ChatPromptTemplate` |
| Output Parsing | `StrOutputParser` |

### APIs & Data Sources

| API | Provider | Usage |
|---|---|---|
| JSearch API | OpenWebNinja | Live job search |
| Job Salary API | OpenWebNinja | Salary intelligence |
| Search API | Tavily | Learning resource discovery |

### Web Scraping

| Library | Role |
|---|---|
| `requests` | HTTP client for URL fetching |
| `trafilatura` | Primary content extractor |
| `readability-lxml` | Secondary content extractor |
| `beautifulsoup4` | Fallback HTML parser |
| `lxml` | XML/HTML parser backend |
| `re` | Text cleaning with regex |

### Frontend & UI

| Technology | Role |
|---|---|
| Streamlit | Application framework |
| Custom CSS | Dark theme, animations, component styling |
| Plotly | Analytics charts and visualizations |

### Utilities

| Library | Role |
|---|---|
| `python-dotenv` | Environment variable management |
| `rich` | Terminal output formatting |

---

## 📂 Project Structure

```
Career-Navigator-AI/
│
├── app.py                          ← Streamlit UI + interactive features
├── main.py                         ← Terminal pipeline runner
├── requirements.txt                ← All dependencies
├── .env                            ← API keys (not committed)
├── .gitignore
├── LICENSE
│
├── src/
│   ├── __init__.py
│   │
│   ├── agents/
│   │   └── agents.py               ← All 5 agents + LCEL report chain
│   │
│   ├── tools/
│   │   └── tools.py                ← All 4 LangChain tools
│   │
│   └── pipelines/
│       └── pipeline.py             ← 6-step orchestration pipeline
│
└── README.md
```

---

## ⚙️ Installation

### Prerequisites

- Python 3.11+
- API keys for: OpenRouter, OpenWebNinja, Tavily

---

### Conda Environment

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/Career-Navigator-AI.git
cd Career-Navigator-AI

# 2. Create conda environment
conda create -n careerai python=3.11 -y

# 3. Activate environment
conda activate careerai

# 4. Install dependencies
pip install -r requirements.txt
```

---

### Python Virtual Environment

**Windows (CMD)**
```bash
# 1. Clone the repository
git clone https://github.com/yourusername/Career-Navigator-AI.git
cd Career-Navigator-AI

# 2. Create virtual environment
python -m venv venv

# 3. Activate
venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt
```

**Windows (PowerShell)**
```powershell
# Activate
.\venv\Scripts\Activate.ps1
```

**Linux / macOS**
```bash
# 2. Create virtual environment
python3 -m venv venv

# 3. Activate
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file in the project root:

```env
# OpenRouter API Key — used for GPT-4o-mini in the multi-agent pipeline
OPENAI_API_KEY=your_openrouter_api_key_here

# OpenWebNinja API Key — used for JSearch, Job Salary API, and GPT-5 chat
OPENWEBNINJA_API_KEY=your_openwebninja_api_key_here

# Tavily API Key — used for learning resource discovery
TAVILY_API_KEY=your_tavily_api_key_here
```

> ⚠️ **Never commit your `.env` file.** It is included in `.gitignore`.

| Key | Where to Get |
|---|---|
| `OPENAI_API_KEY` | [openrouter.ai/keys](https://openrouter.ai/keys) |
| `OPENWEBNINJA_API_KEY` | [openwebninja.com](https://openwebninja.com) |
| `TAVILY_API_KEY` | [app.tavily.com](https://app.tavily.com) |

---

## ▶️ Running the Application

### Terminal (Pipeline Only)

Run the full 6-agent pipeline and print the final report in the terminal:

```bash
python main.py
```

By default this runs with:
```python
goal="Generative AI Engineer"
location="Bangalore"
years_of_experience="ONE_TO_THREE"
```

To change the input, edit `main.py`:
```python
result = run_career_pipeline(
    goal="Machine Learning Engineer",
    location="Hyderabad",
    years_of_experience="THREE_TO_FIVE"
)
```

---

### Streamlit Dashboard

Launch the full interactive UI:

```bash
streamlit run app.py
```

Open in browser:
```
http://localhost:8501
```

---

## 💻 Streamlit Dashboard Features

The Streamlit app provides a full interactive career intelligence dashboard with 10 tabs:

| Tab | Feature |
|---|---|
| 💼 Jobs | Parsed live job cards with apply links |
| 🧠 Skills | Structured skill matrix across 14 categories |
| 💰 Salary | Live salary data or fallback benchmark bands |
| 📚 Roadmap | Courses, certifications, timeline, projects |
| 🎯 Strategy | Career recommendations, skill gaps, action plan |
| 📊 Analytics | Plotly charts: salary bands, skill demand, job trends, radar |
| 🤖 AI Chat | Context-aware career chat powered by GPT-5 |
| 🎤 Interview | AI-generated interview Q&A by role and type |
| 📝 Resume | ATS-optimized resume bullet generator |
| 📄 Report | Final career intelligence report with download |

### Additional UI Components

- **Live pipeline progress tracker** — 6-step visual tracker with animated step states
- **Agent status indicators** — real-time status updates during pipeline execution
- **Career Readiness Score** — AI-assessed score with strengths, gaps, and tip
- **Download options** — TXT and JSON export of all results

---

## 🔄 Pipeline Execution Flow

```
run_career_pipeline()
│
├── Step 1 ─── Job Search Agent
│               └── search_jobs(goal)
│               └── Stores → state["jobs"]
│
├── Step 2 ─── Skill Extraction Agent
│               └── extract_skills(job_url_from_step1)
│               └── Stores → state["skills"]
│
├── Step 3 ─── Salary Intelligence Agent
│               └── salary_research(goal, location, experience)
│               └── Stores → state["salary"]
│
├── Step 4 ─── Learning Roadmap Agent
│               └── find_courses(skills_from_step2)
│               └── Stores → state["roadmap"]
│
├── Step 5 ─── Career Advisor Agent
│               └── LLM reasoning over all state keys
│               └── Stores → state["career_advice"]
│
└── Step 6 ─── Career Report Generator (LCEL Chain)
                └── ChatPromptTemplate | ChatOpenAI | StrOutputParser
                └── Stores → state["final_report"]
                └── Returns complete state dict
```

---

## 📈 Experience Level Options

Use these values for `years_of_experience`:

| Value | Meaning |
|---|---|
| `ZERO_TO_ONE` | 0–1 years |
| `ONE_TO_THREE` | 1–3 years |
| `THREE_TO_FIVE` | 3–5 years |
| `FIVE_TO_SEVEN` | 5–7 years |
| `SEVEN_TO_TEN` | 7–10 years |
| `TEN_PLUS` | 10+ years |

---

## 🚀 Future Improvements

- PDF export of the full career intelligence report
- Resume file upload and AI-powered parsing
- Multi-location comparison mode
- Job bookmarking and tracking system
- Historical pipeline run comparison
- LinkedIn profile URL analysis integration
- Email delivery of final career report

---

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## 👨‍💻 Developed by

<div align="center">

**Gouthum Kharvi**



*Built with LangChain · OpenRouter · OpenWebNinja · Tavily · Streamlit · Plotly*

</div>
