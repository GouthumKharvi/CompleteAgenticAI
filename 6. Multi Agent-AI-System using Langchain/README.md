# 🧠 ResearchMind AI

## Multi-Agent Research System using LangChain, OpenRouter, Tavily Search & Intelligent Web Scraping

<p align="center">

<img src="https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge" />

<img src="https://img.shields.io/badge/LangChain-1.3.4-green?style=for-the-badge" />

<img src="https://img.shields.io/badge/OpenRouter-GPT--4o--mini-purple?style=for-the-badge" />

<img src="https://img.shields.io/badge/Tavily-Live%20Search-orange?style=for-the-badge" />

<img src="https://img.shields.io/badge/Streamlit-Frontend-red?style=for-the-badge" />

<img src="https://img.shields.io/badge/Multi--Agent-AI%20System-cyan?style=for-the-badge" />

</p>

---

## Acess LIVE-WEB-APP : https://researchmind-ai-qq4w.onrender.com

# 🌟 Project Overview

ResearchMind AI is a Multi-Agent Research Assistant built using LangChain's modern agent framework.

Unlike a traditional AI chatbot that depends on a single model response, this system divides the research process into multiple specialized AI agents, where each agent performs a dedicated task.

The agents collaborate together to:

* Search the live internet
* Identify relevant sources
* Read and scrape webpages
* Extract meaningful information
* Generate professional research reports
* Critique and score the generated report

The entire workflow is orchestrated through a centralized state object that acts as shared memory between agents.

This project demonstrates how Agentic AI systems can be designed using LangChain's latest architecture.

---

# 🎯 Problem Statement

Traditional AI assistants usually:

* Depend only on model knowledge
* Cannot verify information
* Do not perform deep research
* Produce answers without validation

This project solves those limitations by creating a team of specialized AI agents that work together similarly to a real research organization.

Instead of:

```text
User → LLM → Answer
```

The workflow becomes:

```text
User
  ↓
Search Agent
  ↓
Reader Agent
  ↓
Writer Agent
  ↓
Critic Agent
  ↓
Final Report
```

---

# 🏗️ System Architecture

```text
                         USER QUERY
                              │
                              ▼

 ┌─────────────────────────────────────────┐
 │            SEARCH AGENT                 │
 │                                         │
 │ Tool: Tavily Search API                 │
 │ Finds live internet sources             │
 └─────────────────────────────────────────┘
                              │
                              ▼

 ┌─────────────────────────────────────────┐
 │            READER AGENT                 │
 │                                         │
 │ Tool: scrape_url()                      │
 │ Reads webpages and extracts content     │
 └─────────────────────────────────────────┘
                              │
                              ▼

                    Shared State Memory

                              │
             ┌────────────────┴───────────────┐
             ▼                                ▼

 ┌─────────────────────┐      ┌─────────────────────┐
 │    WRITER CHAIN     │      │    CRITIC CHAIN     │
 │                     │      │                     │
 │ Generates Report    │      │ Reviews Report      │
 │                     │      │ Scores Output       │
 └─────────────────────┘      └─────────────────────┘
             │                                │
             └────────────────┬───────────────┘
                              ▼

                    FINAL RESEARCH REPORT
```

---

# 🤖 Multi-Agent Design

This system contains four specialized AI components.

---

## 🔍 Agent 1 — Search Agent

### Purpose

The Search Agent is responsible for gathering information from the live internet.

### Technology Used

* LangChain Agent
* GPT-4o-mini
* Tavily Search API

### Tool

```python
web_search()
```

### Responsibilities

* Search live internet
* Retrieve recent information
* Collect URLs
* Collect snippets
* Pass findings to Reader Agent

### Output

```text
Title
URL
Snippet
```

---

## 📖 Agent 2 — Reader Agent

### Purpose

The Reader Agent performs deep content extraction.

After receiving search results from the Search Agent, it:

* Identifies the most relevant URL
* Scrapes webpage content
* Extracts meaningful text
* Removes unnecessary webpage noise

### Technology Used

* LangChain Agent
* GPT-4o-mini
* BeautifulSoup
* Readability-LXML
* Trafilatura

### Tool

```python
scrape_url()
```

### Extraction Strategy

#### Strategy 1 — Trafilatura

Used first because it performs excellent article extraction.

Best for:

* Blogs
* News articles
* Research content

---

#### Strategy 2 — Readability

If Trafilatura fails:

```python
Document(html).summary()
```

is used.

Best for:

* Content-heavy websites
* Complex HTML pages

---

#### Strategy 3 — BeautifulSoup Fallback

Final fallback method.

Removes:

```text
script
style
nav
footer
header
aside
form
```

Then extracts readable text.

### Output

```text
Clean webpage content
```

---

## ✍️ Agent 3 — Writer Chain

### Purpose

Convert collected research into a professional report.

### Technology Used

* ChatPromptTemplate
* LCEL
* GPT-4o-mini
* StrOutputParser

### Prompt Design

Writer receives:

```python
topic
research
```

and generates:

```text
Introduction

Key Findings

Conclusion

Sources
```

### Responsibilities

* Analyze collected information
* Generate structured research
* Organize findings
* Produce professional output

---

## 🧐 Agent 4 — Critic Chain

### Purpose

Evaluate report quality.

### Technology Used

* ChatPromptTemplate
* LCEL
* GPT-4o-mini
* StrOutputParser

### Responsibilities

* Review report quality
* Identify strengths
* Identify weaknesses
* Score report

### Output Format

```text
Score: X/10

Strengths:
- ...

Areas to Improve:
- ...

One line verdict:
...
```

---

# 🧰 Tools Implemented

This project contains two custom tools.

---

## Tool 1 — Web Search

```python
@tool
def web_search(query: str)
```

### Uses

* Tavily Search API

### Returns

```text
Title
URL
Snippet
```

### Purpose

Provides real-time internet information.

---

## Tool 2 — URL Scraper

```python
@tool
def scrape_url(url: str)
```

### Uses

* Requests
* BeautifulSoup
* Readability
* Trafilatura

### Purpose

Extract readable content from webpages.

### Features

* Multiple extraction strategies
* Noise removal
* Clean output
* Error handling
* Timeout handling

---

# 🧠 Shared Memory Architecture

A centralized state dictionary is used to share information across agents.

```python
state = {}
```

Stored values:

```python
state["search_results"]
state["scraped_content"]
state["report"]
state["feedback"]
```

This allows every stage of the pipeline to access previous outputs.

---

# ⚙️ Pipeline Execution Flow

The system follows four sequential stages.

---

## Step 1

Search Agent

```python
search_agent.invoke(...)
```

Output stored:

```python
state["search_results"]
```

---

## Step 2

Reader Agent

```python
reader_agent.invoke(...)
```

Output stored:

```python
state["scraped_content"]
```

---

## Step 3

Writer Chain

```python
writer_chain.invoke(...)
```

Output stored:

```python
state["report"]
```

---

## Step 4

Critic Chain

```python
critic_chain.invoke(...)
```

Output stored:

```python
state["feedback"]
```

---

# 📂 Project Structure

```text
6. Multi Agent-AI-System using Langchain
│
├── src
│   │
│   ├── agents
│   │   ├── __init__.py
│   │   └── agents.py
│   │
│   ├── pipelines
│   │   ├── __init__.py
│   │   └── pipeline.py
│   │
│   ├── tools
│   │   ├── __init__.py
│   │   └── tools.py
│   │
│   └── __init__.py
│
├── app.py
├── main.py
├── requirements.txt
├── README.md
├── .env
├── .gitignore
│
└── venv
```

---

# 💻 Frontend

Frontend built using:

```text
Streamlit
```

Features:

* Modern UI
* Multi-Agent Pipeline Visualization
* Real-Time Execution Status
* Research Topic Input
* Raw Search Results Viewer
* Raw Scraped Content Viewer
* Final Report Viewer
* Critic Feedback Viewer
* Report Download Feature

---

# 📦 Requirements

```bash
pip install -r requirements.txt
```

Dependencies used in this project:

```txt
langchain>=0.2.0
langchain-core>=0.2.0
langchain-community>=0.2.0
langchain-openai>=0.1.0

streamlit>=1.0.0

tavily-python>=0.3.0

beautifulsoup4>=4.12.0
readability-lxml
trafilatura
lxml>=5.0.0

requests>=2.31.0

python-dotenv>=1.0.0

rich>=13.7.0
```

---

# 🔧 Environment Setup

## Create Virtual Environment

```bash
python -m venv venv
```

---

## Activate Environment

Windows

```bash
venv\Scripts\activate
```

Linux / Mac

```bash
source venv/bin/activate
```

---

## Create a Conda Environment
conda create -n researchmind python=3.11 -y

Activate the environment:

conda activate researchmind

---

## Install Jupyter Kernel

```bash
pip install ipykernel
```

Register kernel:

```bash
python -m ipykernel install --user --name=researchmind
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create:

```text
.env
```

Add:

```env
OPENAI_API_KEY=YOUR_OPENROUTER_API_KEY

TAVILY_API_KEY=YOUR_TAVILY_API_KEY
```

---

# ▶️ Running Console Version

```bash
python main.py
```

Example:

```python
topic = "Impact of AI on Healthcare"
```

---

# 🌐 Running Streamlit Application

```bash
streamlit run app.py
```

Local URL:

```text
http://localhost:8501
```

---

# 🧪 Example Research Queries

```text
Impact of AI on Healthcare

Future of Quantum Computing

Best EV Cars in India 2026

Latest AI Agent Frameworks

Future of Artificial General Intelligence

Climate Technology Innovations

AI and Employment Trends
```

---

# 🎯 What This Project Demonstrates

* Agentic AI Architecture
* Multi-Agent Collaboration
* LangChain Agents(creat_agent)
* Custom Tool Creation
* Live Web Search
* Intelligent Web Scraping
* LCEL Chains
* Prompt Engineering
* State Management
* OpenRouter Integration
* Streamlit Deployment

---

# 🚀 Future Improvements

### Research Quality

* Scrape multiple URLs instead of a single URL
* Rank URLs before scraping
* Merge content from multiple sources

### Agent Architecture

* Convert to LangGraph
* Add Planner Agent
* Add Fact Checker Agent
* Add Citation Agent

### Memory

* Persistent Research History
* Vector Database Memory
* Session-Based Memory

### Reporting

* PDF Export
* DOCX Export
* Citation Formatting
* Executive Summaries

### User Experience

* Research Dashboard
* Live Agent Logs
* Research Analytics
* Source Credibility Score

### Scalability

* Async Processing
* Parallel Agent Execution
* Multi-Topic Research
* Background Tasks

---

# 👨‍💻 Author

## Gouthum Kharvi

Aspiring AI / ML Engineer

Focused on:

* Generative AI
* Agentic AI
* LangChain
* Multi-Agent Systems
* LLM Applications
* AI Product Development

---

### ⭐ If you found this project useful, consider giving it a star.

### ⭐ Feedback, suggestions, and contributions are always welcome.
