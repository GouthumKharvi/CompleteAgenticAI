# Single AI Agent System using LangChain

A production-style AI Agent built using LangChain's ReAct framework. The agent can reason, decide which tool to use, retrieve external information, and generate responses using an LLM.

This project demonstrates how Agentic AI systems combine reasoning, tool usage, and external APIs to solve user queries beyond the knowledge available inside the LLM.

Live Website : https://websearch-and-weather-ai-agent-using.onrender.com

---

## Features

* ReAct (Reasoning + Acting) Agent Architecture
* Web Search using Tavily Search API
* Real-Time Weather Information using WeatherStack API
* OpenRouter / OpenAI Model Integration
* Terminal-Based Agent Execution (`main.py`)
* Streamlit Web Application (`app.py`)
* Environment Variable Management using `.env`
* LangChain Agent Executor
* Tool Calling and Observation Loop
* Agent Reasoning Trace (`Thought → Action → Observation → Final Answer`)

---

## Technologies Used

### AI & Agent Framework

* LangChain
* LangChain Community
* LangChain OpenAI
* ReAct Agent Pattern

### LLM

* GPT-4o Mini (via OpenRouter)

### External Tools

* Tavily Search API
* WeatherStack API

### Frontend

* Streamlit

### Python Libraries

* Requests
* Python Dotenv
* Certifi

---

## Agent Architecture

```text
User Query
     │
     ▼
┌─────────────┐
│ ReAct Agent │
└──────┬──────┘
       │
       ▼
  Thought
       │
       ▼
   Action
       │
 ┌─────┴─────┐
 │           │
 ▼           ▼
Tavily   WeatherStack
Search      API
 │           │
 └─────┬─────┘
       ▼
 Observation
       ▼
 Final Answer
```

---

## Project Structure

```text
5.Single AI Agent system using Langchain/
│
├── README.md
├── requirements.txt
├── .env
├── main.py
├── app.py
├── agent_demo.ipynb
└── 5.Single AI Agent system using Langchain.docx
```

---

## Environment Setup

### Create Virtual Environment

Navigate to the project folder:

```bash
cd "5.Single AI Agent system using Langchain"
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the environment:

### Windows

```bash
venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project directory.

```env
OPENAI_API_KEY=your_openrouter_api_key
TAVILY_API_KEY=your_tavily_api_key
WEATHERSTACK_API_KEY=your_weatherstack_api_key
GROQ_API_KEY=your_groq_api_key
```

---

## Running the Terminal Agent

Run:

```bash
python main.py
```

Example:

```text
Enter your query:
What is the weather in Bangalore today?
```

The agent will:

1. Analyze the question
2. Select the appropriate tool
3. Call Tavily Search or WeatherStack
4. Process observations
5. Generate the final answer

---

## Running the Streamlit Application

Run:

```bash
streamlit run app.py
```

Open:

```text
http://localhost:8501
```

---

## Example Agent Workflow

```text
Question:
What is the current weather in Bangalore?

Thought:
I need weather information.

Action:
get_weather_data

Action Input:
Bangalore

Observation:
Temperature: 29°C
Humidity: 65%

Thought:
I now know the answer.

Final Answer:
The current weather in Bangalore is 29°C with 65% humidity.
```

---

## Learning Outcomes

This project demonstrates:

* Agentic AI Fundamentals
* ReAct Architecture
* Tool Calling
* External API Integration
* Prompt Engineering
* Agent Executor Workflow
* LangChain Framework
* Environment Variable Management
* LLM + Tool Collaboration

---

## Future Enhancements

* Multi-Agent Systems
* Memory Integration
* LangGraph Workflows
* RAG Pipelines
* Database Integration
* Voice-Based Agent Interface

---

## Author

**Gouthum Kharvi**

GitHub:
https://github.com/GouthumKharvi

This project was built as part of an Agentic AI learning journey focused on understanding how modern AI Agents reason, use tools, and interact with external systems.
