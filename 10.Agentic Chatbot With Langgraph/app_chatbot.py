import uuid
from datetime import datetime

import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage

from agentic_chatbot_backend import chatbot

# ──────────────────────────────────────────────────────────────────────────
# Page config
# ──────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="GraphMind",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────────────────────────────
# Design system — glassmorphism + motion
# ──────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

:root{
    --bg:        #06080d;
    --panel:     rgba(18,22,32,0.72);
    --panel-2:   rgba(24,29,42,0.85);
    --panel-3:   rgba(32,38,54,0.9);
    --border:    rgba(255,255,255,0.08);
    --border-2:  rgba(255,255,255,0.14);
    --accent:    #8b5cf6;
    --accent-2:  #22d3ee;
    --accent-3:  #f472b6;
    --text:      #f1f2f7;
    --muted:     #8891a5;
    --muted-2:   #5c6579;
    --good:      #34d399;
}

html, body, [class*="css"]{ font-family:'Inter', sans-serif; color:var(--text); }
::-webkit-scrollbar{ width:8px; height:8px; }
::-webkit-scrollbar-track{ background:transparent; }
::-webkit-scrollbar-thumb{ background:var(--border-2); border-radius:8px; }
::-webkit-scrollbar-thumb:hover{ background:#454f66; }

/* ── Animated ambient background ─────────────────────────────────── */
.stApp{ background: var(--bg); overflow-x:hidden; }
.stApp::before, .stApp::after{
    content:""; position:fixed; z-index:0; border-radius:50%;
    filter: blur(90px); pointer-events:none;
}
.stApp::before{
    width:520px; height:520px; top:-160px; left:-120px;
    background: radial-gradient(circle, rgba(139,92,246,0.30), transparent 70%);
    animation: drift1 16s ease-in-out infinite;
}
.stApp::after{
    width:480px; height:480px; bottom:-160px; right:-100px;
    background: radial-gradient(circle, rgba(34,211,238,0.22), transparent 70%);
    animation: drift2 18s ease-in-out infinite;
}
@keyframes drift1{
    0%,100%{ transform: translate(0,0) scale(1); }
    50%{ transform: translate(60px,40px) scale(1.15); }
}
@keyframes drift2{
    0%,100%{ transform: translate(0,0) scale(1); }
    50%{ transform: translate(-50px,-30px) scale(1.1); }
}

section[data-testid="stSidebar"], .main .block-container{ position:relative; z-index:1; }

/* ── Sidebar ─────────────────────────────────────────────────────── */
section[data-testid="stSidebar"]{
    background: var(--panel);
    backdrop-filter: blur(20px);
    border-right: 1px solid var(--border);
    min-width: 300px !important;
}
section[data-testid="stSidebar"] .block-container{ padding: 1.3rem 1rem 1rem; }

.brand{ display:flex; align-items:center; gap:12px; margin-bottom:24px; }
.brand-mark{
    width:36px; height:36px; border-radius:11px; flex-shrink:0; position:relative;
    background: conic-gradient(from 0deg, var(--accent), var(--accent-2), var(--accent-3), var(--accent));
    display:flex; align-items:center; justify-content:center;
    animation: spin 6s linear infinite;
    box-shadow: 0 0 28px rgba(139,92,246,0.45);
}
.brand-mark::after{
    content:"🤖"; font-size:16px; background:#0b0e15; width:28px; height:28px;
    border-radius:8px; display:flex; align-items:center; justify-content:center;
}
@keyframes spin{ from{ transform:rotate(0deg); } to{ transform:rotate(360deg); } }
.brand-text{ line-height:1.15; }
.brand-title{ font-family:'Space Grotesk', sans-serif; font-weight:700; font-size:1.15rem;
    background: linear-gradient(120deg, #fff, var(--accent-2));
    -webkit-background-clip:text; background-clip:text; -webkit-text-fill-color:transparent; }
.brand-tag{ font-family:'JetBrains Mono', monospace; font-size:0.66rem; color:var(--muted); letter-spacing:.02em; }

div[data-testid="stSidebar"] div[data-testid="stButton"] > button{
    text-align:left; justify-content:flex-start;
    border-radius:10px !important;
    font-size:0.85rem;
    transition: all .18s ease;
}
div[data-testid="stSidebar"] button[kind="primary"]{
    background: linear-gradient(135deg, var(--accent), #6d3ce0);
    border:none; font-weight:600;
    box-shadow: 0 4px 20px rgba(139,92,246,0.35);
}
div[data-testid="stSidebar"] button[kind="primary"]:hover{ transform: translateY(-1px); box-shadow: 0 6px 26px rgba(139,92,246,0.5); }
div[data-testid="stSidebar"] button[kind="secondary"]{
    background: transparent; border:1px solid transparent; color:var(--muted);
}
div[data-testid="stSidebar"] button[kind="secondary"]:hover{
    background: var(--panel-3); border-color:var(--border-2); color:var(--text); transform: translateX(2px);
}

.section-label{
    font-size:0.66rem; text-transform:uppercase; letter-spacing:.14em;
    color:var(--muted-2); margin:22px 2px 8px; font-weight:600;
}

.thread-row{ display:flex; align-items:center; gap:4px; margin-bottom:2px; }
.thread-row div[data-testid="stButton"]{ flex:1; }
.thread-row div[data-testid="stButton"]:last-child{ flex:0 0 auto; }

.stack-grid{ display:grid; grid-template-columns:1fr 1fr; gap:8px; margin-top:20px; }
.stack-card{
    background: var(--panel-2); border:1px solid var(--border);
    border-radius:12px; padding:10px 12px;
}
.stack-card .k{ font-size:0.64rem; text-transform:uppercase; letter-spacing:.08em; color:var(--muted-2); margin-bottom:3px; }
.stack-card .v{ font-family:'JetBrains Mono', monospace; font-size:0.78rem; color:var(--text); display:flex; align-items:center; gap:6px; }

.sidebar-footer{ margin-top:18px; padding-top:14px; border-top:1px solid var(--border); }
.status-pill{
    display:flex; align-items:center; gap:6px;
    font-family:'JetBrains Mono', monospace; font-size:0.68rem; color:var(--muted);
}
.status-dot{
    width:6px; height:6px; border-radius:50%; background:var(--good);
    box-shadow: 0 0 8px rgba(52,211,153,0.7);
    animation: blink 2s ease-in-out infinite;
}
@keyframes blink{ 0%,100%{ opacity:1; } 50%{ opacity:0.35; } }

/* ── Top bar ─────────────────────────────────────────────────────── */
.main .block-container{ padding-top: 1.4rem; padding-bottom: 6rem; max-width: 920px; }

.topbar{
    padding-bottom:16px; margin-bottom:22px;
    border-bottom:1px solid var(--border);
}
.topbar-row{ display:flex; align-items:center; justify-content:space-between; margin-bottom:12px; }
.topbar .title{
    font-family:'Space Grotesk', sans-serif; font-weight:600; font-size:1.15rem;
    display:flex; align-items:center; gap:10px;
}
.topbar .thread-id{
    font-family:'JetBrains Mono', monospace; font-size:0.7rem; color:var(--muted);
    padding:4px 11px; border-radius:999px; border:1px solid var(--border-2); background:var(--panel-2);
}
.tech-badges{ display:flex; gap:8px; flex-wrap:wrap; }
.tech-badge{
    display:flex; align-items:center; gap:6px;
    font-family:'JetBrains Mono', monospace; font-size:0.7rem;
    padding:5px 12px; border-radius:999px;
    border:1px solid var(--border-2); color:var(--text);
    background: var(--panel-2);
}
.tech-badge .dot{ width:6px; height:6px; border-radius:50%; }
.tech-badge.lg .dot{ background:var(--accent); box-shadow:0 0 6px var(--accent); }
.tech-badge.pr .dot{ background:var(--accent-2); box-shadow:0 0 6px var(--accent-2); }
.tech-badge.st .dot{ background:var(--good); box-shadow:0 0 6px var(--good); }
.tech-badge.th .dot{ background:var(--accent-3); box-shadow:0 0 6px var(--accent-3); }

/* ── Messages ────────────────────────────────────────────────────── */
[data-testid="stChatMessage"]{
    background: transparent; border:none; padding: 7px 0;
    animation: fadeInUp .35s ease both;
}
@keyframes fadeInUp{
    from{ opacity:0; transform: translateY(10px); }
    to{ opacity:1; transform: translateY(0); }
}

[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) [data-testid="stChatMessageContent"]{
    background: var(--panel-2);
    border: 1px solid var(--border);
    border-radius: 16px 16px 4px 16px;
    padding: 13px 17px;
}
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) [data-testid="stChatMessageContent"]{
    background: linear-gradient(180deg, rgba(139,92,246,0.10), rgba(139,92,246,0.02));
    border: 1px solid rgba(139,92,246,0.24);
    border-radius: 16px 16px 16px 4px;
    padding: 13px 17px;
}
[data-testid="stChatMessageAvatarUser"], [data-testid="stChatMessageAvatarAssistant"]{
    border-radius:10px !important;
}

.empty-state{
    display:flex; flex-direction:column; align-items:center; justify-content:center;
    padding: 90px 20px 50px; text-align:center;
}
.empty-node{
    width:60px; height:60px; border-radius:18px;
    background: conic-gradient(from 0deg, var(--accent), var(--accent-2), var(--accent-3), var(--accent));
    display:flex; align-items:center; justify-content:center;
    font-size:26px; margin-bottom:20px;
    animation: spin 8s linear infinite, floaty 3.2s ease-in-out infinite;
}
@keyframes floaty{ 0%,100%{ transform:translateY(0) rotate(0); } 50%{ transform:translateY(-8px); } }
.empty-state h3{ font-family:'Space Grotesk', sans-serif; font-weight:600; margin-bottom:6px; font-size:1.2rem; }
.empty-state p{ color:var(--muted); font-size:0.9rem; max-width:400px; }

/* ── Input ───────────────────────────────────────────────────────── */
[data-testid="stChatInput"]{
    border-radius: 16px;
    border: 1px solid var(--border-2) !important;
    background: var(--panel-2) !important;
    backdrop-filter: blur(16px);
    box-shadow: 0 4px 28px rgba(0,0,0,0.4);
    transition: box-shadow .2s ease, border-color .2s ease;
}
[data-testid="stChatInput"]:focus-within{
    border-color: rgba(139,92,246,0.6) !important;
    box-shadow: 0 0 0 3px rgba(139,92,246,0.16);
}

#MainMenu, footer, header{ visibility:hidden; }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────
# Session state — thread registry
# ──────────────────────────────────────────────────────────────────────────
def new_thread_id() -> str:
    return str(uuid.uuid4())


def _blank_thread():
    return {"title": "New chat", "created": datetime.now().strftime("%H:%M")}


if "threads" not in st.session_state:
    first_id = new_thread_id()
    st.session_state.threads = {first_id: _blank_thread()}
    st.session_state.thread_order = [first_id]
    st.session_state.current_thread = first_id


def load_history(thread_id: str):
    """Pull message history for a thread straight from the LangGraph checkpointer."""
    config = {"configurable": {"thread_id": thread_id}}
    state = chatbot.get_state(config)
    return state.values.get("messages", []) if state and state.values else []


def switch_thread(thread_id: str):
    st.session_state.current_thread = thread_id


def start_new_chat():
    tid = new_thread_id()
    st.session_state.threads[tid] = _blank_thread()
    st.session_state.thread_order.insert(0, tid)
    st.session_state.current_thread = tid


def delete_thread(thread_id: str):
    st.session_state.thread_order.remove(thread_id)
    del st.session_state.threads[thread_id]
    if not st.session_state.thread_order:
        start_new_chat()
    elif st.session_state.current_thread == thread_id:
        st.session_state.current_thread = st.session_state.thread_order[0]


# ──────────────────────────────────────────────────────────────────────────
# Sidebar
# ──────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
        <div class="brand">
            <div class="brand-mark"></div>
            <div class="brand-text">
                <div class="brand-title">GraphMind</div>
                <div class="brand-tag">agentic chat runtime</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.button("＋  New chat", type="primary", use_container_width=True, on_click=start_new_chat)

    st.markdown(f'<div class="section-label">Conversations · {len(st.session_state.thread_order)}</div>', unsafe_allow_html=True)

    for tid in st.session_state.thread_order:
        meta = st.session_state.threads[tid]
        is_active = tid == st.session_state.current_thread

        st.markdown('<div class="thread-row">', unsafe_allow_html=True)
        c1, c2 = st.columns([6, 1])
        with c1:
            st.button(
                meta["title"],
                key=f"thread_{tid}",
                use_container_width=True,
                type="primary" if is_active else "secondary",
                on_click=switch_thread,
                args=(tid,),
            )
        with c2:
            st.button(
                "✕",
                key=f"del_{tid}",
                use_container_width=True,
                type="secondary",
                on_click=delete_thread,
                args=(tid,),
                help="Delete thread",
            )
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
        <div class="section-label">Tech stack</div>
        <div class="stack-grid">
            <div class="stack-card"><div class="k">Framework</div><div class="v">🔗 LangGraph</div></div>
            <div class="stack-card"><div class="k">Model</div><div class="v">🤖 gpt-4o-mini</div></div>
            <div class="stack-card"><div class="k">Persistence</div><div class="v">💾 MemorySaver</div></div>
            <div class="stack-card"><div class="k">Response mode</div><div class="v">⚡ Streaming</div></div>
        </div>
        <div class="sidebar-footer">
            <div class="status-pill"><div class="status-dot"></div>runtime online</div>
        </div>
    """, unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────
# Main chat area
# ──────────────────────────────────────────────────────────────────────────
current_id = st.session_state.current_thread
current_meta = st.session_state.threads[current_id]

st.markdown(f"""
    <div class="topbar">
        <div class="topbar-row">
            <div class="title">🤖 {current_meta['title']}</div>
            <div class="thread-id">thread · {current_id[:8]}</div>
        </div>
        <div class="tech-badges">
            <div class="tech-badge lg"><div class="dot"></div>LangGraph</div>
            <div class="tech-badge th"><div class="dot"></div>Multi-thread</div>
            <div class="tech-badge pr"><div class="dot"></div>Persistent memory</div>
            <div class="tech-badge st"><div class="dot"></div>Live streaming</div>
        </div>
    </div>
""", unsafe_allow_html=True)

history = load_history(current_id)

if not history:
    st.markdown("""
        <div class="empty-state">
            <div class="empty-node">🤖</div>
            <h3>Ready when you are</h3>
            <p>Every reply streams token by token. Each thread keeps its own memory through LangGraph's checkpointer, just like separate ChatGPT conversations.</p>
        </div>
    """, unsafe_allow_html=True)
else:
    for msg in history:
        role = "user" if isinstance(msg, HumanMessage) else "assistant"
        avatar = "🧑" if role == "user" else "🤖"
        with st.chat_message(role, avatar=avatar):
            st.markdown(msg.content)

# ──────────────────────────────────────────────────────────────────────────
# Streaming generator
# ──────────────────────────────────────────────────────────────────────────
def stream_reply(user_input: str, thread_id: str):
    config = {"configurable": {"thread_id": thread_id}}
    for message_chunk, metadata in chatbot.stream(
        {"messages": [HumanMessage(content=user_input)]},
        config=config,
        stream_mode="messages",
    ):
        if isinstance(message_chunk, AIMessage) or hasattr(message_chunk, "content"):
            if message_chunk.content:
                yield message_chunk.content


# ──────────────────────────────────────────────────────────────────────────
# Chat input
# ──────────────────────────────────────────────────────────────────────────
user_input = st.chat_input("Message GraphMind…")

if user_input:
    if current_meta["title"] == "New chat":
        st.session_state.threads[current_id]["title"] = (
            user_input[:38] + "…" if len(user_input) > 38 else user_input
        )

    with st.chat_message("user", avatar="🧑"):
        st.markdown(user_input)

    with st.chat_message("assistant", avatar="🤖"):
        st.write_stream(stream_reply(user_input, current_id))

    st.rerun()