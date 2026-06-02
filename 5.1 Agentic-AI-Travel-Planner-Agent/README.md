<div align="center">



<h1 align="center">🌍 AI Travel Planner Agent</h1>

<p align="center">
<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=22&duration=2000&pause=700&color=00C853&center=true&vCenter=true&width=1000&lines=User+%E2%86%92+AI+Agent;AI+Agent+%E2%86%92+Country+API;AI+Agent+%E2%86%92+Weather+API;AI+Agent+%E2%86%92+Exchange+Rate+API;AI+Agent+%E2%86%92+Tavily+Search;Generating+Personalized+Travel+Plan+%E2%9C%88%EF%B8%8F" />
</p>

#Access Live wen app : https://ai-travel-planner-agent-3yni.onrender.com
<br/>

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-ReAct-1C3C3C?style=for-the-badge&logo=chainlink&logoColor=white)
![OpenAI](https://img.shields.io/badge/GPT--4o--mini-OpenRouter-412991?style=for-the-badge&logo=openai&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)

<br/>

> **An intelligent travel planning agent that reasons across multiple real-world APIs to give you country info, live weather, currency conversion, and top tourist attractions — all in one query.**

<br/>

![-----](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

</div>

<br/>

## 🗺️ What It Does

You type one travel query. The agent **thinks**, **plans**, and **calls the right tools** automatically — no manual API wrangling needed.

```
"I'm travelling from India to Japan. Tell me about Japan, convert 10000 INR to JPY,
 check the weather in Tokyo, and suggest the top 5 tourist attractions."
```

The agent will:
1. 🌏 Fetch **country info** — capital, currency, population, languages, flag
2. 💱 Convert **INR → JPY** in real time
3. 🌤️ Pull **live weather** for Tokyo
4. 🔍 **Search the web** for top tourist attractions
5. ✦ Synthesise everything into a **single coherent response**

<br/>

![-----](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/solar.png)

## 🧠 Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     User Query (natural language)           │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│              LangChain ReAct Agent (GPT-4o-mini)            │
│                                                             │
│   Thought → Action → Observation → Thought → ... → Answer  │
└──────┬──────────┬──────────┬──────────┬────────────────────┘
       │          │          │          │
       ▼          ▼          ▼          ▼
  🌍 Country   💱 Exchange  🌤️ Weather  🔍 Tavily
  RestCountries  Rate API   Weatherstack  Search
```

<br/>

![-----](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/solar.png)

## 🛠️ Tools & APIs

| Tool | API | What It Does |
|------|-----|-------------|
| `get_country_info` | [RestCountries](https://restcountries.com) | Capital, currency, population, languages, flag |
| `get_exchange_rate` | [ExchangeRate-API](https://exchangerate-api.com) | Real-time currency conversion (INR → JPY, USD, EUR...) |
| `get_weather_data` | [Weatherstack](https://weatherstack.com) | Live temperature, humidity, wind speed, feels-like |
| `tavily_search` | [Tavily](https://tavily.com) | AI-optimised web search for attractions, visa info, tips |

<br/>

![-----](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/solar.png)

## 🚀 Quick Start

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/ai-travel-agent.git
cd ai-travel-agent
```

### 2. Create a virtual environment 

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openrouter_key_here
TAVILY_API_KEY=your_tavily_key_here
WEATHERSTACK_API_KEY=your_weatherstack_key_here
EXCHANGE_RATE_API_KEY=your_exchangerate_key_here
```

### 5. Run

```bash
# Streamlit Web App
streamlit run app.py

# CLI (Terminal)
python main.py
```

<br/>

![-----](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/solar.png)

## 📁 Project Structure

```
5.1 Agentic-AI-Travel-Planner-Agent/
│
├── 📓 travel_agent_demo.ipynb           # Jupyter notebook — exploration & testing
├── 🌐 app.py                            # Streamlit web app (luxury dark UI)
├── 💻 main.py                           # CLI version — runs in terminal
├── 📄 .env                              # API keys (never commit this!)
├── 📋 requirements.txt                  # All dependencies
├── 📑 AI_Agentic_Projects_Documentation.pdf  # Full project documentation
├── 📖 README.md
└── 📁 venv/                             # Virtual environment (not committed)
```

<br/>

![-----](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/solar.png)

## 💬 Sample Queries

<details>
<summary><b>🇯🇵 India → Japan (uses all 4 tools)</b></summary>

```
I am travelling from India to Japan. Tell me about Japan including its capital,
currency, population and languages. Convert 10000 INR to Japanese Yen.
Tell me the current weather in Tokyo. Also suggest the top 5 tourist attractions in Tokyo.
```
</details>

<details>
<summary><b>🇫🇷 India → France</b></summary>

```
Planning a trip to France. Share country info, convert 5000 INR to EUR,
check the weather in Paris, and suggest must-see spots.
```
</details>

<details>
<summary><b>🇦🇪 India → Dubai</b></summary>

```
I am going to Dubai. Give me UAE country info, convert 10000 INR to AED,
check Dubai weather and top tourist places.
```
</details>

<details>
<summary><b>💱 Currency only</b></summary>

```
Convert 50000 INR to Japanese Yen, Euro, and US Dollar.
```
</details>

<details>
<summary><b>🌤️ Weather only</b></summary>

```
What is the current weather in London, Tokyo and Sydney?
```
</details>

<br/>

![-----](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/solar.png)

## ⚙️ How the ReAct Agent Works

The agent follows a **Thought → Action → Observation** loop until it has enough information to answer:

```
Thought:   "I need country info about Japan first."
Action:    get_country_info
Input:     Japan
Observation: Country: Japan | Capital: Tokyo | Currency: JPY ...

Thought:   "Now I need the exchange rate."
Action:    get_exchange_rate
Input:     INR,JPY
Observation: 1 INR = 1.68 JPY

Thought:   "Now weather in Tokyo."
Action:    get_weather_data
Input:     Tokyo
Observation: Temperature: 20°C | Humidity: 69% ...

Thought:   "Now search for top attractions."
Action:    tavily_search_results_json
Input:     top tourist attractions in Tokyo
Observation: [Senso-ji, Ueno Park, Akihabara, Tokyo Skytree, Meiji Jingu ...]

Thought:   "I have all the information needed."
Final Answer: ...
```

<br/>

![-----](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/solar.png)

## 🖥️ Two Interfaces

### 🌐 Streamlit Web App (`app.py`)

- Luxury dark editorial UI — Playfair Display + Outfit + JetBrains Mono fonts
- Live **Agent Execution Trace** panel with macOS-style header and step counter
- 4 sample query cards for instant testing
- Animated final response card with gold top border
- Real-time streaming via custom `BaseCallbackHandler`

### 💻 CLI Terminal App (`main.py`)

- Interactive `You:` prompt loop — ask multiple queries without restarting
- Full verbose agent trace printed to terminal automatically
- Clean `FINAL ANSWER` block after the trace
- `exit` / `quit` / `Ctrl+C` to stop

<br/>

![-----](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/solar.png)

## 📦 Requirements

```txt
langchain==0.1.16
langchain-community==0.0.32
langchain-core==0.1.42
langchain-openai==0.1.3
requests==2.31.0
tavily-python
python-dotenv
langchainhub
streamlit
```

Install all at once:

```bash
pip install langchain==0.1.16 langchain-community==0.0.32 langchain-core==0.1.42 langchain-openai==0.1.3 requests==2.31.0 tavily-python python-dotenv langchainhub streamlit openai certifi
```

<br/>

![-----](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/solar.png)

## 🔑 API Keys — Where to Get Them

| Service | URL | Free Tier |
|---------|-----|-----------|
| OpenRouter (GPT-4o-mini) | [openrouter.ai](https://openrouter.ai) | Pay per token, very cheap |
| Tavily Search | [app.tavily.com](https://app.tavily.com) | 1,000 searches/month free |
| Weatherstack | [weatherstack.com](https://weatherstack.com) | 250 calls/month free |
| ExchangeRate-API | [exchangerate-api.com](https://exchangerate-api.com) | 1,500 calls/month free |
| RestCountries | [restcountries.com](https://restcountries.com) | Completely free, no key needed |

<br/>

![-----](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/solar.png)

## 🐛 Common Issues

| Problem | Fix |
|---------|-----|
| `SSL Certificate Error` | Already handled — `certifi` is set in code |
| `API key not found (None)` | Check `.env` is in the same folder you run the script from |
| `Agent stuck in loop` | Add `max_iterations=10` to `AgentExecutor` |
| `Weatherstack error` | Free tier uses HTTP only — check your key at weatherstack.com |
| `Tavily no results` | Free tier monthly limit hit — check usage at app.tavily.com |

<br/>

![-----](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/solar.png)

## 🧩 Tech Stack

<div align="center">

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=flat-square&logo=chainlink&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=flat-square&logo=openai&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=flat-square&logo=jupyter&logoColor=white)
![dotenv](https://img.shields.io/badge/.env-ECD53F?style=flat-square&logo=dotenv&logoColor=black)

</div>

<br/>

![-----](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

<div align="center">

**Built with ❤️ using LangChain ReAct · GPT-4o-mini · Real-world APIs**
**Developed By Gouthum_Kharvi"

*Part of the Complete Agentic AI Coursework*

</div>
