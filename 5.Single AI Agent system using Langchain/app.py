import os
import requests
import streamlit as st
import certifi
from dotenv import load_dotenv
from typing import Any, Dict, List, Union

from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain.agents import (
    create_react_agent,
    AgentExecutor
)
from langchain import hub
from langchain.callbacks.base import BaseCallbackHandler
from langchain_community.tools.tavily_search import TavilySearchResults

# ==========================================
# LOAD ENV VARIABLES
# ==========================================
os.environ["SSL_CERT_FILE"] = certifi.where()
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
WEATHERSTACK_API_KEY = os.getenv("WEATHERSTACK_API_KEY")

# ==========================================
# STREAMLIT PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Agentic AI Assistant",
    page_icon="🤖",
    layout="centered"
)

# ==========================================
# CUSTOM CSS — MODERN DARK INTELLIGENCE THEME
# ==========================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

/* ── ROOT TOKENS ── */
:root {
    --bg:          #090b10;
    --surface:     #0f1219;
    --surface-2:   #161b26;
    --border:      rgba(255,255,255,0.06);
    --border-glow: rgba(99,179,237,0.35);
    --accent:      #63b3ed;
    --accent-2:    #76e4c4;
    --accent-3:    #f6ad55;
    --text:        #e2e8f0;
    --muted:       #718096;
    --danger:      #fc8181;
    --success:     #68d391;
    --font-head:   'Syne', sans-serif;
    --font-mono:   'DM Mono', monospace;
    --radius:      14px;
    --glow:        0 0 40px rgba(99,179,237,0.12);
}

/* ── GLOBAL ── */
html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: var(--font-mono) !important;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 80% 50% at 50% -10%, rgba(99,179,237,0.07) 0%, transparent 70%),
        var(--bg) !important;
}

/* hide default streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }
.block-container { padding: 2.5rem 1.5rem 4rem !important; max-width: 820px !important; }

/* ── HEADER HERO ── */
.hero-wrap {
    text-align: center;
    padding: 3rem 0 2.4rem;
    position: relative;
}
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    font-family: var(--font-mono);
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--accent);
    background: rgba(99,179,237,0.08);
    border: 1px solid rgba(99,179,237,0.22);
    border-radius: 100px;
    padding: 5px 14px;
    margin-bottom: 1.2rem;
}
.hero-badge .dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--accent);
    box-shadow: 0 0 8px var(--accent);
    animation: pulse 2s ease-in-out infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%       { opacity: 0.4; transform: scale(0.7); }
}
.hero-title {
    font-family: var(--font-head);
    font-size: clamp(2rem, 5vw, 3rem);
    font-weight: 800;
    line-height: 1.1;
    letter-spacing: -0.03em;
    color: #fff;
    margin: 0 0 0.6rem;
}
.hero-title span {
    background: linear-gradient(135deg, var(--accent) 0%, var(--accent-2) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-sub {
    font-size: 0.88rem;
    color: var(--muted);
    letter-spacing: 0.02em;
    margin: 0;
}

/* ── CAPABILITY PILLS ── */
.caps-row {
    display: flex;
    gap: 10px;
    justify-content: center;
    flex-wrap: wrap;
    margin: 1.6rem 0 2.4rem;
}
.cap-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-family: var(--font-mono);
    font-size: 0.72rem;
    color: var(--muted);
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 100px;
    padding: 5px 13px;
}
.cap-pill .icon { font-size: 0.85rem; }

/* ── DIVIDER ── */
.section-div {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border-glow), transparent);
    margin: 2rem 0;
}

/* ── SUGGESTION CHIPS ── */
.suggest-label {
    font-family: var(--font-mono);
    font-size: 0.7rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 0.8rem;
}
.chips-row {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    margin-bottom: 1.6rem;
}
.chip {
    font-family: var(--font-mono);
    font-size: 0.75rem;
    color: var(--accent);
    background: rgba(99,179,237,0.06);
    border: 1px solid rgba(99,179,237,0.18);
    border-radius: 8px;
    padding: 6px 12px;
    cursor: default;
    transition: background 0.2s;
}

/* ── INPUT BOX OVERRIDE ── */
[data-testid="stTextInput"] input {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    color: var(--text) !important;
    font-family: var(--font-mono) !important;
    font-size: 0.92rem !important;
    padding: 0.8rem 1.1rem !important;
    transition: border-color 0.25s, box-shadow 0.25s !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(99,179,237,0.12) !important;
    outline: none !important;
}
[data-testid="stTextInput"] label {
    font-family: var(--font-mono) !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    color: var(--muted) !important;
}

/* ── BUTTON ── */
[data-testid="stButton"] > button {
    background: linear-gradient(135deg, rgba(99,179,237,0.15), rgba(118,228,196,0.1)) !important;
    border: 1px solid rgba(99,179,237,0.4) !important;
    border-radius: var(--radius) !important;
    color: var(--accent) !important;
    font-family: var(--font-head) !important;
    font-size: 0.9rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.05em !important;
    padding: 0.7rem 2rem !important;
    width: 100% !important;
    transition: all 0.25s !important;
    position: relative;
    overflow: hidden;
}
[data-testid="stButton"] > button:hover {
    background: linear-gradient(135deg, rgba(99,179,237,0.25), rgba(118,228,196,0.18)) !important;
    border-color: var(--accent) !important;
    box-shadow: 0 4px 24px rgba(99,179,237,0.2) !important;
    transform: translateY(-1px) !important;
}
[data-testid="stButton"] > button:active {
    transform: translateY(0) !important;
}

/* ── SPINNER ── */
[data-testid="stSpinner"] {
    color: var(--accent) !important;
    font-family: var(--font-mono) !important;
    font-size: 0.82rem !important;
}
.stSpinner > div { border-top-color: var(--accent) !important; }

/* ── LOG PANEL ── */
.log-panel {
    background: #07090e;
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 0;
    margin-top: 1.4rem;
    overflow: hidden;
}
.log-panel-header {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 0.75rem 1.2rem;
    background: var(--surface);
    border-bottom: 1px solid var(--border);
}
.log-panel-title {
    font-family: var(--font-head);
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--muted);
    flex: 1;
}
.log-live-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--accent-3);
    box-shadow: 0 0 7px var(--accent-3);
    animation: pulse 1.4s ease-in-out infinite;
}
.log-body {
    padding: 1rem 1.2rem;
    max-height: 320px;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 6px;
}
.log-entry {
    display: flex;
    gap: 10px;
    align-items: flex-start;
    font-family: var(--font-mono);
    font-size: 0.78rem;
    line-height: 1.55;
    animation: fadeIn 0.25s ease;
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateX(-6px); }
    to   { opacity: 1; transform: translateX(0); }
}
.log-tag {
    flex-shrink: 0;
    font-size: 0.65rem;
    font-weight: 500;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    padding: 2px 8px;
    border-radius: 4px;
    margin-top: 1px;
}
.log-tag.think  { background: rgba(99,179,237,0.12);  color: var(--accent);   border: 1px solid rgba(99,179,237,0.2); }
.log-tag.tool   { background: rgba(246,173,85,0.12);  color: var(--accent-3); border: 1px solid rgba(246,173,85,0.2); }
.log-tag.result { background: rgba(118,228,196,0.1);  color: var(--accent-2); border: 1px solid rgba(118,228,196,0.2); }
.log-tag.done   { background: rgba(104,211,145,0.1);  color: var(--success);  border: 1px solid rgba(104,211,145,0.2); }
.log-tag.error  { background: rgba(252,129,129,0.1);  color: var(--danger);   border: 1px solid rgba(252,129,129,0.2); }
.log-text { color: var(--text); flex: 1; }
.log-text .dim  { color: var(--muted); }
.log-text .hi   { color: var(--accent-3); font-weight: 500; }

/* ── RESPONSE CARD ── */
.response-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-left: 3px solid var(--accent-2);
    border-radius: var(--radius);
    padding: 1.6rem 1.8rem;
    margin-top: 1.6rem;
    box-shadow: var(--glow);
    animation: slideUp 0.4s cubic-bezier(0.16,1,0.3,1);
}
@keyframes slideUp {
    from { opacity: 0; transform: translateY(14px); }
    to   { opacity: 1; transform: translateY(0); }
}
.response-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 1.1rem;
}
.response-icon {
    width: 30px; height: 30px;
    border-radius: 50%;
    background: linear-gradient(135deg, var(--accent), var(--accent-2));
    display: flex; align-items: center; justify-content: center;
    font-size: 0.85rem;
    flex-shrink: 0;
}
.response-label {
    font-family: var(--font-head);
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--accent-2);
}
.response-body {
    font-family: var(--font-mono);
    font-size: 0.88rem;
    line-height: 1.75;
    color: var(--text);
    white-space: pre-wrap;
}

/* ── ALERT OVERRIDES ── */
[data-testid="stAlert"] {
    border-radius: var(--radius) !important;
    font-family: var(--font-mono) !important;
    font-size: 0.82rem !important;
}

/* ── STATUS BAR ── */
.status-bar {
    display: flex;
    align-items: center;
    gap: 8px;
    font-family: var(--font-mono);
    font-size: 0.72rem;
    color: var(--muted);
    margin-top: 2.5rem;
    padding-top: 1.2rem;
    border-top: 1px solid var(--border);
    justify-content: center;
}
.status-dot {
    width: 5px; height: 5px;
    border-radius: 50%;
    background: var(--accent-2);
    box-shadow: 0 0 6px var(--accent-2);
}
.status-sep { color: rgba(255,255,255,0.12); }

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--surface-2); border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# HERO HEADER
# ==========================================

st.markdown("""
<div class="hero-wrap">
    <div class="hero-badge"><span class="dot"></span>Powered by LangChain ReAct</div>
    <h1 class="hero-title">Agentic <span>AI</span> Assistant</h1>
    <p class="hero-sub">Search + Weather intelligence — powered by GPT-4o-mini &amp; Tavily</p>
</div>

<div class="caps-row">
    <div class="cap-pill"><span class="icon">🔍</span> Web Search</div>
    <div class="cap-pill"><span class="icon">🌤️</span> Live Weather</div>
    <div class="cap-pill"><span class="icon">🧠</span> ReAct Reasoning</div>
    <div class="cap-pill"><span class="icon">🤖</span> AgentExecutor</div>
</div>

<div class="section-div"></div>
""", unsafe_allow_html=True)

# ==========================================
# SEARCH TOOL
# ==========================================

search_tool = TavilySearchResults(max_results=4)

# ==========================================
# WEATHER TOOL
# ==========================================

@tool
def get_weather_data(city: str) -> str:
    """
    Fetch current weather information for a city.
    """

    url = (
        f"https://api.weatherstack.com/current?"
        f"access_key={WEATHERSTACK_API_KEY}&query={city}"
    )

    response = requests.get(url)

    data = response.json()

    if "current" not in data:
        return f"Could not fetch weather data for {city}"

    return (
        f"City: {city}\n"
        f"Temperature: {data['current']['temperature']}°C\n"
        f"Weather: {data['current']['weather_descriptions'][0]}\n"
        f"Humidity: {data['current']['humidity']}%"
    )


# ==========================================
# LLM
# ==========================================

llm = ChatOpenAI(
    model="openai/gpt-4o-mini",
    temperature=0,
    api_key=OPENAI_API_KEY,
    base_url="https://openrouter.ai/api/v1",
    max_tokens=500
)

# ==========================================
# PROMPT
# ==========================================

prompt = hub.pull("hwchase17/react")

# ==========================================
# TOOLS
# ==========================================

tools = [
    search_tool,
    get_weather_data
]

# ==========================================
# CREATE AGENT
# ==========================================

agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)

# ==========================================
# EXECUTOR
# ==========================================

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True
)

# ==========================================
# LIVE LOG CALLBACK HANDLER
# ==========================================

def _html_log(tag_class: str, tag_label: str, text: str) -> str:
    safe = text.replace("<", "&lt;").replace(">", "&gt;")
    return (
        f'<div class="log-entry">'
        f'<span class="log-tag {tag_class}">{tag_label}</span>'
        f'<span class="log-text">{safe}</span>'
        f'</div>'
    )

class StreamlitLogHandler(BaseCallbackHandler):
    """Streams agent internals into a live Streamlit placeholder."""

    def __init__(self, log_placeholder):
        self.placeholder = log_placeholder
        self.entries: List[str] = []

    def _render(self):
        body = "\n".join(self.entries)
        self.placeholder.markdown(
            f"""
            <div class="log-panel">
                <div class="log-panel-header">
                    <span class="log-live-dot"></span>
                    <span class="log-panel-title">Agent Execution Trace</span>
                </div>
                <div class="log-body">{body}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    def on_chain_start(self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs):
        q = inputs.get("input", inputs.get("query", ""))
        if q:
            self.entries.append(_html_log("think", "START", f"Agent received query: {q}"))
            self._render()

    def on_agent_action(self, action, **kwargs):
        tool_name = action.tool
        tool_input = str(action.tool_input)
        self.entries.append(_html_log("think", "THINK", f"Decided to call tool → {tool_name}"))
        self.entries.append(_html_log("tool",  "CALL",  f"{tool_name}({tool_input})"))
        self._render()

    def on_tool_start(self, serialized: Dict[str, Any], input_str: str, **kwargs):
        name = serialized.get("name", "unknown_tool")
        self.entries.append(_html_log("tool", "FETCH", f"Executing {name} with input: {input_str}"))
        self._render()

    def on_tool_end(self, output: str, **kwargs):
        preview = output[:220] + ("…" if len(output) > 220 else "")
        self.entries.append(_html_log("result", "RESULT", preview))
        self._render()

    def on_tool_error(self, error: Union[Exception, str], **kwargs):
        self.entries.append(_html_log("error", "ERROR", str(error)))
        self._render()

    def on_agent_finish(self, finish, **kwargs):
        self.entries.append(_html_log("done", "DONE", "Agent completed reasoning. Generating final response…"))
        self._render()

    def on_chain_end(self, outputs: Dict[str, Any], **kwargs):
        pass

# ==========================================
# SUGGESTION CHIPS (UI ONLY)
# ==========================================

st.markdown("""
<div class="suggest-label">Try asking</div>
<div class="chips-row">
    <div class="chip">🌦 Weather in Tokyo + latest news</div>
    <div class="chip">🏙 Capital of France &amp; current weather</div>
    <div class="chip">📈 Latest AI research trends</div>
    <div class="chip">🌡 Compare weather in NYC vs London</div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# UI INPUT
# ==========================================

user_query = st.text_input(
    "YOUR QUERY",
    placeholder="e.g.  Find the capital of India and current weather there",
    label_visibility="visible"
)

# ==========================================
# RUN AGENT
# ==========================================

if st.button("⚡  Run Agent"):

    if user_query:

        # Live log placeholder renders above the final response
        log_placeholder = st.empty()

        with st.spinner("Agent is reasoning across tools…"):

            try:
                log_handler = StreamlitLogHandler(log_placeholder)

                response = agent_executor.invoke(
                    {"input": user_query},
                    config={"callbacks": [log_handler]}
                )

                st.success("✓  Response generated successfully")

                st.markdown(f"""
                <div class="response-card">
                    <div class="response-header">
                        <div class="response-icon">✦</div>
                        <span class="response-label">Agent Response</span>
                    </div>
                    <div class="response-body">{response["output"]}</div>
                </div>
                """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"⚠  {str(e)}")

    else:
        st.warning("Please enter a query to get started.")

# ==========================================
# STATUS FOOTER
# ==========================================

st.markdown("""
<div class="status-bar">
    <span class="status-dot"></span>
    <span>GPT-4o-mini via OpenRouter</span>
    <span class="status-sep">·</span>
    <span>Tavily Search</span>
    <span class="status-sep">·</span>
    <span>Weatherstack</span>
    <span class="status-sep">·</span>
    <span>LangChain ReAct</span>
</div>
""", unsafe_allow_html=True)