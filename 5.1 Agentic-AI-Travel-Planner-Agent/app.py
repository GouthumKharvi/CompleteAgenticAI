import os
import certifi
import requests
import streamlit as st
from dotenv import load_dotenv
from typing import Any, Dict, List, Union

from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain import hub
from langchain.tools import tool
from langchain.agents import create_react_agent, AgentExecutor
from langchain.callbacks.base import BaseCallbackHandler

# ==========================================
# LOAD ENV VARIABLES
# ==========================================
os.environ["SSL_CERT_FILE"] = certifi.where()
load_dotenv()

OPENAI_API_KEY        = os.getenv("OPENAI_API_KEY")
EXCHANGE_RATE_API_KEY = os.getenv("EXCHANGE_RATE_API_KEY")
TAVILY_API_KEY        = os.getenv("TAVILY_API_KEY")
WEATHERSTACK_API_KEY  = os.getenv("WEATHERSTACK_API_KEY")

# ==========================================
# PAGE CONFIG
# ==========================================
st.set_page_config(
    page_title="AI Travel Agent",
    page_icon="✈️",
    layout="centered"
)

# ==========================================
# CSS — LUXURY TRAVEL EDITORIAL THEME
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700&family=Outfit:wght@300;400;500;600&family=JetBrains+Mono:wght@300;400;500&display=swap');

:root {
    --ink:        #0a0c0f;
    --paper:      #0e1118;
    --card:       #131720;
    --card-2:     #181e2b;
    --line:       rgba(255,255,255,0.055);
    --line-gold:  rgba(201,165,91,0.4);
    --gold:       #c9a55b;
    --gold-light: #e8c97a;
    --sky:        #6eb5ff;
    --mint:       #5ee8b8;
    --rose:       #ff7f7f;
    --text:       #dde3ef;
    --muted:      #6b7590;
    --font-serif: 'Playfair Display', Georgia, serif;
    --font-sans:  'Outfit', sans-serif;
    --font-mono:  'JetBrains Mono', monospace;
    --r:          12px;
}

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stApp"] {
    background: var(--ink) !important;
    color: var(--text) !important;
    font-family: var(--font-sans) !important;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 100% 55% at 50% 0%,  rgba(201,165,91,0.06) 0%, transparent 65%),
        radial-gradient(ellipse 60%  40% at 90% 80%, rgba(110,181,255,0.04) 0%, transparent 60%),
        var(--ink) !important;
}

#MainMenu, footer, header, [data-testid="stToolbar"] { display:none !important; }
.block-container { padding: 0 1.4rem 5rem !important; max-width: 860px !important; }

/* ─── MASTHEAD ─── */
.masthead {
    text-align: center;
    padding: 3.8rem 0 0.5rem;
    position: relative;
}
.masthead-eyebrow {
    font-family: var(--font-mono);
    font-size: 0.65rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: var(--gold);
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
}
.masthead-eyebrow::before,
.masthead-eyebrow::after {
    content: '';
    height: 1px;
    width: 50px;
    background: linear-gradient(90deg, transparent, var(--gold));
}
.masthead-eyebrow::after { background: linear-gradient(90deg, var(--gold), transparent); }

.masthead h1 {
    font-family: var(--font-serif);
    font-size: clamp(2.6rem, 6vw, 4rem);
    font-weight: 900;
    line-height: 1.05;
    color: #fff;
    margin: 0 0 0.5rem;
    letter-spacing: -0.02em;
}
.masthead h1 em {
    font-style: italic;
    color: var(--gold-light);
}
.masthead-sub {
    font-family: var(--font-sans);
    font-size: 0.9rem;
    font-weight: 300;
    color: var(--muted);
    letter-spacing: 0.03em;
}

/* ─── TOOL BADGES ─── */
.tools-strip {
    display: flex;
    gap: 8px;
    justify-content: center;
    flex-wrap: wrap;
    margin: 2rem 0 0;
}
.tool-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-family: var(--font-mono);
    font-size: 0.68rem;
    letter-spacing: 0.06em;
    color: var(--muted);
    background: var(--card);
    border: 1px solid var(--line);
    border-radius: 6px;
    padding: 5px 11px;
}
.tool-badge .dot {
    width: 5px; height: 5px;
    border-radius: 50%;
    background: var(--gold);
    box-shadow: 0 0 6px var(--gold);
}

/* ─── GOLD RULE ─── */
.gold-rule {
    height: 1px;
    background: linear-gradient(90deg, transparent 0%, var(--gold) 30%, var(--gold-light) 50%, var(--gold) 70%, transparent 100%);
    margin: 2.4rem 0;
    opacity: 0.4;
}

/* ─── SAMPLE QUERIES ─── */
.sq-label {
    font-family: var(--font-mono);
    font-size: 0.62rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 0.9rem;
}
.sq-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
    margin-bottom: 1.8rem;
}
.sq-card {
    font-family: var(--font-sans);
    font-size: 0.76rem;
    font-weight: 400;
    color: var(--text);
    background: var(--card);
    border: 1px solid var(--line);
    border-radius: var(--r);
    padding: 10px 14px;
    line-height: 1.5;
    cursor: default;
    transition: border-color 0.2s;
}
.sq-card:hover { border-color: rgba(201,165,91,0.3); }
.sq-card .sq-icon { font-size: 1rem; margin-bottom: 4px; display: block; }

/* ─── INPUT ─── */
[data-testid="stTextArea"] textarea {
    background: var(--card) !important;
    border: 1px solid var(--line) !important;
    border-radius: var(--r) !important;
    color: var(--text) !important;
    font-family: var(--font-sans) !important;
    font-size: 0.9rem !important;
    font-weight: 300 !important;
    line-height: 1.7 !important;
    padding: 1rem 1.2rem !important;
    resize: none !important;
    transition: border-color 0.25s, box-shadow 0.25s !important;
}
[data-testid="stTextArea"] textarea:focus {
    border-color: var(--gold) !important;
    box-shadow: 0 0 0 3px rgba(201,165,91,0.1) !important;
    outline: none !important;
}
[data-testid="stTextArea"] label {
    font-family: var(--font-mono) !important;
    font-size: 0.62rem !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
    color: var(--muted) !important;
}

/* ─── BUTTON ─── */
[data-testid="stButton"] > button {
    background: linear-gradient(135deg, rgba(201,165,91,0.18) 0%, rgba(232,201,122,0.1) 100%) !important;
    border: 1px solid rgba(201,165,91,0.5) !important;
    border-radius: var(--r) !important;
    color: var(--gold-light) !important;
    font-family: var(--font-serif) !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.04em !important;
    padding: 0.75rem 2rem !important;
    width: 100% !important;
    transition: all 0.25s !important;
}
[data-testid="stButton"] > button:hover {
    background: linear-gradient(135deg, rgba(201,165,91,0.28) 0%, rgba(232,201,122,0.18) 100%) !important;
    box-shadow: 0 6px 30px rgba(201,165,91,0.18) !important;
    transform: translateY(-1px) !important;
    border-color: var(--gold-light) !important;
}

/* ─── SPINNER ─── */
[data-testid="stSpinner"] p {
    font-family: var(--font-mono) !important;
    font-size: 0.8rem !important;
    color: var(--muted) !important;
}

/* ─── TRACE PANEL ─── */
.trace-panel {
    background: #070a0f;
    border: 1px solid var(--line);
    border-radius: var(--r);
    overflow: hidden;
    margin-top: 1.6rem;
}
.trace-header {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 0.7rem 1.2rem;
    background: var(--card);
    border-bottom: 1px solid var(--line);
}
.trace-live {
    display: flex;
    gap: 4px;
}
.trace-live span {
    width: 8px; height: 8px;
    border-radius: 50%;
}
.trace-live .r { background: #ff5f56; }
.trace-live .y { background: #ffbd2e; }
.trace-live .g { background: #27c93f; animation: blink 1.8s ease-in-out infinite; }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.3} }
.trace-title {
    font-family: var(--font-mono);
    font-size: 0.65rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--muted);
    flex: 1;
}
.trace-counter {
    font-family: var(--font-mono);
    font-size: 0.62rem;
    color: var(--gold);
    background: rgba(201,165,91,0.08);
    border: 1px solid rgba(201,165,91,0.15);
    border-radius: 4px;
    padding: 2px 8px;
}
.trace-body {
    padding: 1rem 1.2rem;
    max-height: 350px;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 5px;
}
.trace-row {
    display: flex;
    gap: 9px;
    align-items: flex-start;
    font-family: var(--font-mono);
    font-size: 0.75rem;
    line-height: 1.55;
    animation: traceIn 0.2s ease;
}
@keyframes traceIn { from{opacity:0;transform:translateX(-8px)} to{opacity:1;transform:none} }

.tt {
    flex-shrink: 0;
    font-size: 0.6rem;
    font-weight: 600;
    letter-spacing: 0.07em;
    text-transform: uppercase;
    padding: 2px 7px;
    border-radius: 4px;
    margin-top: 1px;
    min-width: 52px;
    text-align: center;
}
.tt.start  { background:rgba(110,181,255,0.12); color:var(--sky);  border:1px solid rgba(110,181,255,0.2); }
.tt.think  { background:rgba(201,165,91,0.1);   color:var(--gold); border:1px solid rgba(201,165,91,0.2); }
.tt.call   { background:rgba(246,173,85,0.1);   color:#f6ad55;     border:1px solid rgba(246,173,85,0.2); }
.tt.fetch  { background:rgba(246,173,85,0.07);  color:#e09940;     border:1px solid rgba(246,173,85,0.15); }
.tt.result { background:rgba(94,232,184,0.08);  color:var(--mint); border:1px solid rgba(94,232,184,0.18); }
.tt.done   { background:rgba(39,201,63,0.08);   color:#27c93f;     border:1px solid rgba(39,201,63,0.18); }
.tt.error  { background:rgba(255,127,127,0.1);  color:var(--rose); border:1px solid rgba(255,127,127,0.2); }

.tr { color: var(--text); flex:1; }
.tr .dim { color: var(--muted); }
.tr .hi  { color: var(--gold-light); }

/* ─── SECTION LABEL ─── */
.section-label {
    font-family: var(--font-mono);
    font-size: 0.62rem;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: var(--muted);
    margin: 2rem 0 0.9rem;
    display: flex;
    align-items: center;
    gap: 10px;
}
.section-label::after {
    content:'';
    flex:1;
    height:1px;
    background: var(--line);
}

/* ─── RESPONSE CARD ─── */
.resp-card {
    background: var(--card);
    border: 1px solid var(--line);
    border-top: 2px solid var(--gold);
    border-radius: var(--r);
    padding: 1.8rem 2rem;
    margin-top: 0.4rem;
    box-shadow: 0 4px 40px rgba(0,0,0,0.35), 0 0 60px rgba(201,165,91,0.04);
    animation: cardIn 0.5s cubic-bezier(0.16,1,0.3,1);
}
@keyframes cardIn {
    from { opacity:0; transform:translateY(16px); }
    to   { opacity:1; transform:translateY(0); }
}
.resp-head {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 1.4rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid var(--line);
}
.resp-avatar {
    width: 34px; height: 34px;
    border-radius: 50%;
    background: linear-gradient(135deg, var(--gold) 0%, var(--gold-light) 100%);
    display: flex; align-items:center; justify-content:center;
    font-size: 1rem;
    flex-shrink:0;
}
.resp-name {
    font-family: var(--font-serif);
    font-size: 0.85rem;
    font-weight: 700;
    color: var(--gold-light);
    letter-spacing: 0.04em;
}
.resp-meta {
    font-family: var(--font-mono);
    font-size: 0.62rem;
    color: var(--muted);
    margin-top: 1px;
}
.resp-body {
    font-family: var(--font-sans);
    font-size: 0.88rem;
    font-weight: 300;
    line-height: 1.85;
    color: var(--text);
    white-space: pre-wrap;
}

/* ─── ALERTS ─── */
[data-testid="stAlert"] {
    border-radius: var(--r) !important;
    font-family: var(--font-sans) !important;
    font-size: 0.82rem !important;
    font-weight: 300 !important;
}

/* ─── FOOTER ─── */
.footer {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    flex-wrap: wrap;
    margin-top: 3rem;
    padding-top: 1.4rem;
    border-top: 1px solid var(--line);
    font-family: var(--font-mono);
    font-size: 0.62rem;
    letter-spacing: 0.08em;
    color: var(--muted);
}
.footer-dot {
    width: 4px; height: 4px;
    border-radius: 50%;
    background: var(--gold);
    box-shadow: 0 0 5px var(--gold);
}
.footer-sep { opacity: 0.2; }

/* ─── SCROLLBAR ─── */
::-webkit-scrollbar { width: 3px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--card-2); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# MASTHEAD
# ==========================================
st.markdown("""
<div class="masthead">
    <div class="masthead-eyebrow">✈ &nbsp; AI-Powered Travel Intelligence &nbsp; ✈</div>
    <h1>Your <em>Intelligent</em><br>Travel Companion</h1>
    <p class="masthead-sub">Country info · Live weather · Currency conversion · Top attractions</p>
</div>

<div class="tools-strip">
    <div class="tool-badge"><span class="dot"></span> AgentExecutor</div>
    <div class="tool-badge"><span class="dot"></span> Country Info</div>
    <div class="tool-badge"><span class="dot"></span> Exchange Rates</div>
    <div class="tool-badge"><span class="dot"></span> Live Weather</div>
    <div class="tool-badge"><span class="dot"></span> Tavily Search</div>
</div>

<div class="gold-rule"></div>
""", unsafe_allow_html=True)

# ==========================================
# TOOLS
# ==========================================

search_tool = TavilySearchResults(max_results=4)

@tool
def get_exchange_rate(currency_pair: str) -> str:
    """
    Get exchange rate between two currencies.
    Example: INR,JPY  or  USD,INR  or  EUR,JPY
    """
    from_currency, to_currency = [c.strip().upper() for c in currency_pair.split(",")]
    url = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_RATE_API_KEY}/latest/{from_currency}"
    response = requests.get(url)
    data = response.json()
    rate = data["conversion_rates"][to_currency]
    return f"1 {from_currency} = {rate} {to_currency}"

@tool
def get_weather_data(city: str) -> str:
    """Fetch current weather information for a city."""
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
        f"Humidity: {data['current']['humidity']}%\n"
        f"Wind Speed: {data['current']['wind_speed']} km/h\n"
        f"Feels Like: {data['current']['feelslike']}°C"
    )

@tool
def get_country_info(country: str) -> str:
    """
    Fetch country information including capital, currency,
    population, region, languages, flag and country codes.
    """
    url = (
        f"https://restcountries.com/v3.1/name/{country}"
        "?fields=name,capital,currencies,population,region,languages,flags,cca2,cca3"
    )
    response = requests.get(url)
    data = response.json()
    if not data or isinstance(data, dict):
        return f"Could not fetch country information for {country}"
    country_data = data[0]
    currency_code = list(country_data["currencies"].keys())[0]
    currency_name = country_data["currencies"][currency_code]["name"]
    languages = ", ".join(country_data["languages"].values())
    return (
        f"Country: {country_data['name']['common']}\n"
        f"Capital: {country_data['capital'][0]}\n"
        f"Region: {country_data['region']}\n"
        f"Population: {country_data['population']:,}\n"
        f"Currency: {currency_name} ({currency_code})\n"
        f"Languages: {languages}\n"
        f"Country Code: {country_data['cca2']} / {country_data['cca3']}\n"
        f"Flag: {country_data['flags']['png']}"
    )

tools = [search_tool, get_weather_data, get_exchange_rate, get_country_info]

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
# CREATE AGENT
# ==========================================
agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)

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
# LIVE LOG CALLBACK
# ==========================================
def _row(tag_cls: str, label: str, text: str) -> str:
    safe = (text or "").replace("<", "&lt;").replace(">", "&gt;")
    return (
        f'<div class="trace-row">'
        f'<span class="tt {tag_cls}">{label}</span>'
        f'<span class="tr">{safe}</span>'
        f'</div>'
    )

class TravelLogHandler(BaseCallbackHandler):
    def __init__(self, placeholder):
        self.ph = placeholder
        self.rows: List[str] = []
        self.steps = 0

    def _flush(self):
        body = "\n".join(self.rows)
        self.ph.markdown(
            f"""
            <div class="trace-panel">
                <div class="trace-header">
                    <div class="trace-live">
                        <span class="r"></span>
                        <span class="y"></span>
                        <span class="g"></span>
                    </div>
                    <span class="trace-title">Agent Execution Trace</span>
                    <span class="trace-counter">{self.steps} steps</span>
                </div>
                <div class="trace-body">{body}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    def on_chain_start(self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs):
        q = inputs.get("input", "")
        if q:
            self.rows.append(_row("start", "START", f"Query received → {q[:120]}{'…' if len(q)>120 else ''}"))
            self._flush()

    def on_agent_action(self, action, **kwargs):
        self.steps += 1
        self.rows.append(_row("think", "THINK", f"Decided to use → {action.tool}"))
        self.rows.append(_row("call",  "CALL",  f"{action.tool}({str(action.tool_input)})"))
        self._flush()

    def on_tool_start(self, serialized: Dict[str, Any], input_str: str, **kwargs):
        name = serialized.get("name", "tool")
        self.rows.append(_row("fetch", "FETCH", f"Executing {name} …"))
        self._flush()

    def on_tool_end(self, output: str, **kwargs):
        preview = (output or "")[:250] + ("…" if len(output or "") > 250 else "")
        self.rows.append(_row("result", "RESULT", preview))
        self._flush()

    def on_tool_error(self, error: Union[Exception, str], **kwargs):
        self.rows.append(_row("error", "ERROR", str(error)))
        self._flush()

    def on_agent_finish(self, finish, **kwargs):
        self.rows.append(_row("done", "DONE", "All tools executed. Composing final response…"))
        self._flush()

# ==========================================
# SAMPLE QUERIES
# ==========================================
st.markdown("""
<div class="sq-label">Sample queries</div>
<div class="sq-grid">
    <div class="sq-card">
        <span class="sq-icon">🇯🇵</span>
        Travelling from India to Japan. Tell me about Japan, convert 10000 INR to JPY, current weather in Tokyo & top 5 attractions.
    </div>
    <div class="sq-card">
        <span class="sq-icon">🇫🇷</span>
        Planning a trip to France. Share country info, convert 5000 INR to EUR, weather in Paris & must-see spots in Paris.
    </div>
    <div class="sq-card">
        <span class="sq-icon">🇦🇪</span>
        I'm going to Dubai. Give me UAE country info, convert 10000 INR to AED, check Dubai weather & top tourist places.
    </div>
    <div class="sq-card">
        <span class="sq-icon">🇺🇸</span>
        Trip to New York. Tell me about USA, convert 20000 INR to USD, current weather in NYC & best attractions.
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# INPUT
# ==========================================
user_query = st.text_area(
    "YOUR TRAVEL QUERY",
    placeholder=(
        "e.g.  I am travelling from India to Japan. Tell me about Japan including its capital, "
        "currency, population and languages. Convert 10000 INR to Japanese Yen. "
        "Tell me the current weather in Tokyo. Also suggest the top 5 tourist attractions in Tokyo."
    ),
    height=120,
    label_visibility="visible"
)

# ==========================================
# RUN AGENT
# ==========================================
if st.button("✈  Plan My Trip"):

    if user_query.strip():

        log_placeholder = st.empty()

        with st.spinner("Agent is gathering travel intelligence…"):
            try:
                handler = TravelLogHandler(log_placeholder)

                response = agent_executor.invoke(
                    {"input": user_query},
                    config={"callbacks": [handler]}
                )

                st.success("✓  Travel report ready")

                st.markdown('<div class="section-label">Final Response</div>', unsafe_allow_html=True)

                st.markdown(f"""
                <div class="resp-card">
                    <div class="resp-head">
                        <div class="resp-avatar">✦</div>
                        <div>
                            <div class="resp-name">Travel Intelligence Report</div>
                            <div class="resp-meta">Generated by AgentExecutor · GPT-4o-mini · ReAct Framework</div>
                        </div>
                    </div>
                    <div class="resp-body">{response["output"]}</div>
                </div>
                """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"⚠  {str(e)}")

    else:
        st.warning("Please enter your travel query above.")

# ==========================================
# FOOTER
# ==========================================
st.markdown("""
<div class="footer">
    <span class="footer-dot"></span>
    <span>GPT-4o-mini via OpenRouter</span>
    <span class="footer-sep">·</span>
    <span>Tavily Search</span>
    <span class="footer-sep">·</span>
    <span>Weatherstack</span>
    <span class="footer-sep">·</span>
    <span>ExchangeRate-API</span>
    <span class="footer-sep">·</span>
    <span>RestCountries</span>
    <span class="footer-sep">·</span>
    <span>LangChain ReAct</span>
</div>
""", unsafe_allow_html=True)