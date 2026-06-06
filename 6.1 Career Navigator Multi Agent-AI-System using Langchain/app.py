import streamlit as st
import json
import re
import os
import requests
import markdown
from dotenv import load_dotenv
from src.pipelines.pipeline import run_career_pipeline

# ─────────────────────────────────────────────────────────────
# ENV + AI CLIENT (OpenWebNinja → GPT-5)
# ─────────────────────────────────────────────────────────────
load_dotenv()
OWN_KEY   = os.getenv("OPENWEBNINJA_API_KEY")
OWN_URL   = "https://api.openwebninja.com/chatgpt/chat"
OWN_MODEL = "gpt-5"

def own_chat(system: str, messages: list, max_tokens: int = 1024) -> str:
    try:
        prompt = f"System Instructions:\n{system}\n\n"

        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            prompt += f"{role.upper()}: {content}\n\n"

        payload = {
            "message": prompt,
            "markdown": True
        }

        resp = requests.post(
            OWN_URL,
            headers={
                "X-API-Key": OWN_KEY,
                "Content-Type": "application/json"
            },
            json=payload,
            timeout=60
        )

        print("Status:", resp.status_code)
        print("Response:", resp.text)

        data = resp.json()

        if data.get("status") == "OK":
            return data["data"]["reply_text"]

        return f"API Error: {data}"

    except Exception as e:
        return f"API Error: {str(e)}"

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Career Navigator AI",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');

*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html,body,[class*="css"]{font-family:'Inter',sans-serif!important;background:#09090f!important;color:#e2e8f0!important}
.main{background:#09090f!important}
.block-container{padding:1.5rem 2rem 2rem!important;max-width:1400px!important}
::-webkit-scrollbar{width:5px;height:5px}
::-webkit-scrollbar-track{background:#0d0d1a}
::-webkit-scrollbar-thumb{background:#4f8ef7;border-radius:10px}

body::before{content:'';position:fixed;inset:0;z-index:-1;
  background:radial-gradient(ellipse 80% 60% at 10% 10%,rgba(79,142,247,.08) 0%,transparent 60%),
             radial-gradient(ellipse 60% 50% at 90% 80%,rgba(139,92,246,.07) 0%,transparent 60%),#09090f;
  animation:meshShift 14s ease-in-out infinite alternate}
@keyframes meshShift{from{opacity:.8}to{opacity:1}}

/* Sidebar */
[data-testid="stSidebar"]{background:#0b0b18!important;border-right:1px solid rgba(79,142,247,.15)!important}
[data-testid="stSidebar"] *{color:#cbd5e1!important;font-family:'Inter',sans-serif!important}
[data-testid="stSidebar"] .stTextInput>div>div>input{background:#111122!important;border:1px solid rgba(79,142,247,.28)!important;border-radius:10px!important;color:#e2e8f0!important;padding:10px 14px!important;font-size:.875rem!important}
[data-testid="stSidebar"] .stTextInput>div>div>input:focus{border-color:#4f8ef7!important;box-shadow:0 0 0 3px rgba(79,142,247,.13)!important}
[data-testid="stSidebar"] label{font-size:.71rem!important;font-weight:700!important;letter-spacing:1.5px!important;text-transform:uppercase!important;color:#64748b!important}
[data-testid="stSidebar"] .stSelectbox>div>div{background:#111122!important;border:1px solid rgba(79,142,247,.28)!important;border-radius:10px!important;color:#e2e8f0!important}

.sidebar-brand{background:linear-gradient(135deg,#1a1a38,#0f1628);border-bottom:1px solid rgba(79,142,247,.18);padding:28px 20px 22px;margin-bottom:24px}
.sidebar-logo{font-family:'Space Grotesk',sans-serif;font-size:1.15rem;font-weight:700;background:linear-gradient(90deg,#4f8ef7,#a78bfa);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.sidebar-tag{font-size:.68rem;color:#475569!important;letter-spacing:2px;margin-top:5px;text-transform:uppercase}

/* Buttons */
.stButton>button{background:linear-gradient(135deg,#4f8ef7,#7c3aed)!important;border:none!important;border-radius:12px!important;color:#fff!important;font-family:'Space Grotesk',sans-serif!important;font-weight:700!important;font-size:.88rem!important;letter-spacing:.8px!important;padding:13px 22px!important;transition:transform .2s,box-shadow .2s!important;box-shadow:0 4px 24px rgba(79,142,247,.3)!important}
.stButton>button:hover{transform:translateY(-2px)!important;box-shadow:0 8px 32px rgba(79,142,247,.52)!important}

/* Progress */
.stProgress>div>div{background:#131324!important;border-radius:99px!important;height:6px!important}
.stProgress>div>div>div{background:linear-gradient(90deg,#4f8ef7,#a78bfa,#f5c842)!important;border-radius:99px!important;box-shadow:0 0 14px rgba(79,142,247,.55)!important;transition:width .4s ease!important}

/* Hero */
.hero-wrap{background:linear-gradient(135deg,#0f1628,#13132a 55%,#0d1a1a);border:1px solid rgba(79,142,247,.17);border-radius:22px;padding:52px 52px 44px;margin-bottom:28px;position:relative;overflow:hidden;box-shadow:0 8px 56px rgba(0,0,0,.45),inset 0 1px 0 rgba(255,255,255,.05)}
.hero-wrap::before{content:'';position:absolute;top:-70px;right:-70px;width:360px;height:360px;background:radial-gradient(circle,rgba(79,142,247,.13),transparent 70%);border-radius:50%;animation:orb1 9s ease-in-out infinite alternate}
.hero-wrap::after{content:'';position:absolute;bottom:-50px;left:38%;width:280px;height:280px;background:radial-gradient(circle,rgba(167,139,250,.09),transparent 70%);border-radius:50%;animation:orb2 11s ease-in-out infinite alternate}
@keyframes orb1{from{transform:translate(0,0)}to{transform:translate(-22px,22px)}}
@keyframes orb2{from{transform:translate(0,0)}to{transform:translate(22px,-18px)}}
.hero-eyebrow{font-size:.68rem;font-weight:700;letter-spacing:3.5px;text-transform:uppercase;color:#4f8ef7;margin-bottom:14px;display:flex;align-items:center;gap:10px}
.hero-eyebrow::before{content:'';width:26px;height:2px;background:linear-gradient(90deg,#4f8ef7,#a78bfa);border-radius:2px}
.hero-title{font-family:'Space Grotesk',sans-serif;font-size:3.1rem;font-weight:800;line-height:1.08;background:linear-gradient(135deg,#fff 25%,#c4b5fd 65%,#4f8ef7);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:14px;letter-spacing:-1.5px}
.hero-sub{font-size:1rem;color:#94a3b8;line-height:1.65;max-width:620px;margin-bottom:28px}
.hero-badges{display:flex;flex-wrap:wrap;gap:8px}
.hero-badge{background:rgba(79,142,247,.1);border:1px solid rgba(79,142,247,.22);color:#93c5fd;padding:6px 15px;border-radius:99px;font-size:.72rem;font-weight:500;transition:all .25s;cursor:default}
.hero-badge:hover{background:rgba(79,142,247,.2);border-color:rgba(79,142,247,.5);box-shadow:0 0 14px rgba(79,142,247,.25)}

/* Pipeline */
.pipeline-wrap{background:#0b0b18;border:1px solid rgba(79,142,247,.11);border-radius:16px;padding:20px 28px;margin:18px 0 26px;display:flex;align-items:center;justify-content:space-between;gap:6px;flex-wrap:wrap;box-shadow:0 4px 28px rgba(0,0,0,.3)}
.p-step{display:flex;flex-direction:column;align-items:center;gap:7px;flex:1;min-width:68px}
.p-icon{width:44px;height:44px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:1.1rem;background:#111122;border:1px solid rgba(255,255,255,.06);transition:all .4s}
.p-icon.done{background:linear-gradient(135deg,#1e3a5f,#1e1b4b);border-color:#4f8ef7;box-shadow:0 0 18px rgba(79,142,247,.35)}
.p-icon.active{background:linear-gradient(135deg,#1e3a5f,#2d1b69);border-color:#a78bfa;animation:stepPulse 1.2s ease-in-out infinite alternate}
@keyframes stepPulse{from{box-shadow:0 0 8px rgba(167,139,250,.3);transform:scale(1)}to{box-shadow:0 0 24px rgba(167,139,250,.75);transform:scale(1.06)}}
.p-label{font-size:.58rem;font-weight:700;letter-spacing:1px;text-align:center;color:#334155;text-transform:uppercase}
.p-label.done{color:#93c5fd}.p-label.active{color:#c4b5fd}
.p-connector{flex:.4;height:1px;background:rgba(255,255,255,.05);margin-bottom:22px;position:relative;overflow:hidden}
.p-connector.done{background:linear-gradient(90deg,#4f8ef7,#a78bfa);box-shadow:0 0 6px rgba(79,142,247,.4)}
.p-connector.active::after{content:'';position:absolute;top:0;left:-100%;width:100%;height:100%;background:linear-gradient(90deg,transparent,#a78bfa,transparent);animation:connFlow 1.5s linear infinite}
@keyframes connFlow{to{left:100%}}

/* Agent status */
.agent-status{background:linear-gradient(135deg,#0f1628,#13132a);border:1px solid rgba(79,142,247,.22);border-left:3px solid #4f8ef7;border-radius:10px;padding:13px 20px;font-size:.875rem;color:#93c5fd;font-weight:500;margin:10px 0;display:flex;align-items:center;gap:12px;animation:statusIn .35s cubic-bezier(.34,1.56,.64,1)}
.agent-status::before{content:'';width:8px;height:8px;background:#4f8ef7;border-radius:50%;box-shadow:0 0 8px #4f8ef7;flex-shrink:0;animation:pulseDot 1s infinite}
@keyframes pulseDot{0%,100%{opacity:1;transform:scale(1)}50%{opacity:.4;transform:scale(.65)}}
@keyframes statusIn{from{opacity:0;transform:translateX(-18px) scale(.97)}to{opacity:1;transform:translateX(0) scale(1)}}

/* Metrics */
[data-testid="metric-container"]{background:#0d0d1a!important;border:1px solid rgba(79,142,247,.12)!important;border-radius:14px!important;padding:20px!important;box-shadow:0 2px 18px rgba(0,0,0,.25)!important;transition:transform .2s,box-shadow .2s}
[data-testid="metric-container"]:hover{transform:translateY(-2px);box-shadow:0 8px 26px rgba(79,142,247,.1)!important}
[data-testid="stMetricLabel"]>div{font-size:.67rem!important;font-weight:700!important;letter-spacing:2px!important;text-transform:uppercase!important;color:#475569!important}
[data-testid="stMetricValue"]>div{font-family:'Space Grotesk',sans-serif!important;font-size:1.2rem!important;font-weight:700!important;color:#e2e8f0!important}

/* Tabs */
.stTabs [data-baseweb="tab-list"]{background:transparent!important;border-bottom:1px solid rgba(255,255,255,.07)!important;gap:3px}
.stTabs [data-baseweb="tab"]{background:transparent!important;color:#475569!important;border:none!important;border-radius:10px 10px 0 0!important;font-family:'Inter',sans-serif!important;font-size:.8rem!important;font-weight:600!important;padding:10px 16px!important;transition:all .2s}
.stTabs [data-baseweb="tab"]:hover{color:#94a3b8!important;background:rgba(255,255,255,.03)!important}
.stTabs [aria-selected="true"]{background:rgba(79,142,247,.1)!important;color:#93c5fd!important;border-bottom:2px solid #4f8ef7!important}

/* Section headers */
.sec-header{font-family:'Space Grotesk',sans-serif;font-size:1.05rem;font-weight:700;color:#e2e8f0;padding:18px 0 14px;display:flex;align-items:center;gap:10px}
.sec-header::after{content:'';flex:1;height:1px;background:linear-gradient(90deg,rgba(79,142,247,.3),transparent)}
.sec-dot{width:8px;height:8px;border-radius:50%;background:linear-gradient(135deg,#4f8ef7,#a78bfa);box-shadow:0 0 8px rgba(79,142,247,.5);flex-shrink:0}

/* Cards */
.content-card{background:#0d0d1a;border:1px solid rgba(255,255,255,.07);border-radius:16px;padding:24px;margin-bottom:16px;box-shadow:0 4px 24px rgba(0,0,0,.25);transition:border-color .2s,box-shadow .2s;animation:cardIn .4s ease-out}
.content-card:hover{border-color:rgba(79,142,247,.2);box-shadow:0 8px 32px rgba(79,142,247,.07)}
@keyframes cardIn{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:translateY(0)}}

/* Job card */
.job-card{background:#0d0d1a;border:1px solid rgba(255,255,255,.07);border-radius:14px;padding:22px 24px;margin-bottom:14px;transition:all .25s;animation:cardIn .4s ease-out;position:relative;overflow:hidden}
.job-card::before{content:'';position:absolute;left:0;top:0;bottom:0;width:3px;background:linear-gradient(180deg,#4f8ef7,#a78bfa)}
.job-card:hover{border-color:rgba(79,142,247,.3);box-shadow:0 8px 28px rgba(79,142,247,.1);transform:translateX(4px)}
.job-title{font-family:'Space Grotesk',sans-serif;font-size:1rem;font-weight:700;color:#e2e8f0;margin-bottom:6px}
.job-company{font-size:.82rem;color:#4f8ef7;font-weight:600;margin-bottom:4px}
.job-meta{display:flex;flex-wrap:wrap;gap:8px;margin:10px 0}
.job-chip{background:rgba(79,142,247,.08);border:1px solid rgba(79,142,247,.18);color:#93c5fd;padding:3px 12px;border-radius:99px;font-size:.72rem;font-weight:500}
.job-chip.salary{background:rgba(245,200,66,.08);border-color:rgba(245,200,66,.25);color:#f5c842}
.job-chip.loc{background:rgba(34,197,94,.06);border-color:rgba(34,197,94,.2);color:#86efac}
.job-summary{font-size:.84rem;color:#94a3b8;line-height:1.65;margin-top:8px}
.job-apply{display:inline-flex;align-items:center;gap:6px;background:linear-gradient(135deg,#4f8ef7,#7c3aed);color:#fff!important;padding:7px 16px;border-radius:8px;font-size:.75rem;font-weight:700;text-decoration:none!important;margin-top:12px;transition:all .2s}
.job-apply:hover{opacity:.85;transform:translateY(-1px)}

/* Skill cards */
.skill-card{background:#0d0d1a;border:1px solid rgba(255,255,255,.07);border-radius:14px;padding:18px 20px;margin-bottom:14px;transition:all .2s;animation:cardIn .4s ease-out}
.skill-card:hover{border-color:rgba(79,142,247,.22);box-shadow:0 6px 24px rgba(79,142,247,.07);transform:translateY(-2px)}
.skill-tags{display:flex;flex-wrap:wrap;gap:6px}
.skill-tag{background:rgba(79,142,247,.08);border:1px solid rgba(79,142,247,.2);color:#93c5fd;padding:4px 13px;border-radius:99px;font-size:.74rem;font-weight:500;transition:all .2s}
.skill-tag:hover{background:rgba(79,142,247,.18);border-color:rgba(79,142,247,.5)}

/* Salary card */
.salary-band{background:#0d0d1a;border:1px solid rgba(245,200,66,.14);border-top:2px solid #f5c842;border-radius:12px;padding:18px;text-align:center;margin-bottom:12px;animation:cardIn .4s ease-out}
.salary-exp{font-size:.63rem;color:#475569;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:6px}
.salary-val{font-family:'Space Grotesk',sans-serif;font-size:1.15rem;font-weight:800;color:#f5c842;margin-bottom:4px}
.salary-lvl{font-size:.7rem;color:#64748b}

/* Roadmap */
.roadmap-section{background:#0d0d1a;border:1px solid rgba(255,255,255,.07);border-radius:14px;padding:20px 24px;margin-bottom:14px;animation:cardIn .4s ease-out}
.roadmap-section:hover{border-color:rgba(79,142,247,.2);box-shadow:0 4px 20px rgba(79,142,247,.06)}
.roadmap-title{font-family:'Space Grotesk',sans-serif;font-size:.82rem;font-weight:700;color:#e2e8f0;margin-bottom:12px;display:flex;align-items:center;gap:8px}
.roadmap-title-icon{width:28px;height:28px;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:.85rem;flex-shrink:0}
.course-item{background:rgba(79,142,247,.05);border:1px solid rgba(79,142,247,.12);border-radius:10px;padding:12px 16px;margin-bottom:8px;display:flex;align-items:center;justify-content:space-between;gap:10px;transition:all .2s}
.course-item:hover{background:rgba(79,142,247,.1);border-color:rgba(79,142,247,.3)}
.course-name{font-size:.83rem;font-weight:600;color:#e2e8f0}
.course-provider{font-size:.72rem;color:#64748b;margin-top:2px}
.course-link{background:linear-gradient(135deg,#4f8ef7,#7c3aed);color:#fff!important;padding:5px 12px;border-radius:7px;font-size:.7rem;font-weight:700;text-decoration:none!important;white-space:nowrap;transition:opacity .2s}
.course-link:hover{opacity:.8}
.cert-item{background:rgba(245,200,66,.05);border:1px solid rgba(245,200,66,.15);border-radius:10px;padding:10px 16px;margin-bottom:8px;display:flex;align-items:center;justify-content:space-between;gap:10px}
.cert-name{font-size:.83rem;font-weight:600;color:#f5c842}
.cert-link{color:#f5c842!important;font-size:.72rem;font-weight:600;text-decoration:none!important;border:1px solid rgba(245,200,66,.3);padding:4px 10px;border-radius:6px;transition:all .2s}
.cert-link:hover{background:rgba(245,200,66,.1)}
.timeline-month{background:rgba(167,139,250,.06);border:1px solid rgba(167,139,250,.15);border-left:3px solid #a78bfa;border-radius:10px;padding:14px 18px;margin-bottom:10px}
.timeline-month-title{font-family:'Space Grotesk',sans-serif;font-size:.82rem;font-weight:700;color:#c4b5fd;margin-bottom:8px}
.seq-step{display:flex;align-items:flex-start;gap:10px;padding:8px 0;border-bottom:1px solid rgba(255,255,255,.05)}
.seq-step:last-child{border-bottom:none}
.seq-num{width:22px;height:22px;border-radius:6px;background:linear-gradient(135deg,#4f8ef7,#7c3aed);color:#fff;display:flex;align-items:center;justify-content:center;font-size:.65rem;font-weight:800;flex-shrink:0;margin-top:1px}
.seq-text{font-size:.83rem;color:#94a3b8;line-height:1.55}
.project-item{display:flex;align-items:flex-start;gap:10px;padding:10px 0;border-bottom:1px solid rgba(255,255,255,.05)}
.project-item:last-child{border-bottom:none}
.project-dot{width:8px;height:8px;border-radius:50%;background:#22c55e;box-shadow:0 0 6px rgba(34,197,94,.5);flex-shrink:0;margin-top:5px}
.project-text{font-size:.83rem;color:#94a3b8;line-height:1.55}

/* Strategy */
.strategy-card{background:#0d0d1a;border:1px solid rgba(255,255,255,.07);border-radius:14px;padding:20px 24px;margin-bottom:14px;animation:cardIn .4s ease-out;transition:all .2s}
.strategy-card:hover{border-color:rgba(79,142,247,.2);box-shadow:0 4px 20px rgba(79,142,247,.06)}
.strategy-title{font-family:'Space Grotesk',sans-serif;font-size:.82rem;font-weight:700;margin-bottom:12px;display:flex;align-items:center;gap:8px}
.strategy-item{display:flex;align-items:flex-start;gap:10px;padding:8px 0;border-bottom:1px solid rgba(255,255,255,.05)}
.strategy-item:last-child{border-bottom:none}
.strategy-bullet{width:6px;height:6px;border-radius:50%;background:#4f8ef7;flex-shrink:0;margin-top:6px}
.strategy-text{font-size:.84rem;color:#94a3b8;line-height:1.6}
.action-day{background:rgba(79,142,247,.05);border:1px solid rgba(79,142,247,.15);border-left:3px solid #4f8ef7;border-radius:10px;padding:14px 18px;margin-bottom:10px}
.action-day-title{font-family:'Space Grotesk',sans-serif;font-size:.8rem;font-weight:700;color:#93c5fd;margin-bottom:8px}

/* Chat */
.chat-shell{background:#0d0d1a;border:1px solid rgba(79,142,247,.17);border-radius:20px;overflow:hidden;box-shadow:0 8px 52px rgba(0,0,0,.4)}
.chat-topbar{background:linear-gradient(135deg,#0f1628,#13132a);border-bottom:1px solid rgba(79,142,247,.14);padding:15px 22px;display:flex;align-items:center;gap:12px}
.chat-avatar{width:36px;height:36px;border-radius:10px;background:linear-gradient(135deg,#4f8ef7,#7c3aed);display:flex;align-items:center;justify-content:center;font-size:1rem;box-shadow:0 0 14px rgba(79,142,247,.4)}
.chat-name{font-family:'Space Grotesk',sans-serif;font-size:.88rem;font-weight:700;color:#e2e8f0}
.chat-online{font-size:.68rem;color:#22c55e;display:flex;align-items:center;gap:5px}
.online-dot{width:6px;height:6px;border-radius:50%;background:#22c55e;box-shadow:0 0 6px #22c55e;animation:pulseDot 1.5s infinite}
.chat-msgs{padding:18px 18px 6px;min-height:280px;max-height:370px;overflow-y:auto;display:flex;flex-direction:column;gap:12px}
.msg-u{align-self:flex-end;background:linear-gradient(135deg,#1e3a5f,#1e1b4b);border:1px solid rgba(79,142,247,.25);color:#e2e8f0;padding:11px 16px;border-radius:16px 16px 4px 16px;max-width:78%;font-size:.87rem;line-height:1.55;animation:msgIn .25s ease-out}
.msg-ai{align-self:flex-start;background:#111122;border:1px solid rgba(255,255,255,.07);border-left:3px solid #f5c842;color:#cbd5e1;padding:11px 16px;border-radius:4px 16px 16px 16px;max-width:86%;font-size:.87rem;line-height:1.65;animation:msgIn .25s ease-out}
@keyframes msgIn{from{opacity:0;transform:translateY(9px)}to{opacity:1;transform:translateY(0)}}

/* Q&A */
.qa-card{background:#0d0d1a;border:1px solid rgba(255,255,255,.07);border-radius:14px;padding:20px 22px;margin-bottom:13px;animation:cardIn .4s ease-out;transition:all .2s}
.qa-card:hover{border-color:rgba(245,200,66,.2);box-shadow:0 4px 20px rgba(245,200,66,.05)}
.qa-q{font-family:'Space Grotesk',sans-serif;font-size:.9rem;font-weight:700;color:#e2e8f0;margin-bottom:10px;display:flex;gap:10px;align-items:flex-start}
.qa-num{background:linear-gradient(135deg,#4f8ef7,#7c3aed);color:#fff;width:24px;height:24px;border-radius:6px;display:flex;align-items:center;justify-content:center;font-size:.68rem;font-weight:800;flex-shrink:0;margin-top:1px}
.qa-a{font-size:.83rem;color:#94a3b8;line-height:1.72;margin-left:34px;border-left:2px solid rgba(245,200,66,.28);padding-left:14px}

/* Resume */
.resume-bullet{background:#0d0d1a;border:1px solid rgba(167,139,250,.14);border-left:3px solid #a78bfa;border-radius:10px;padding:14px 18px;margin-bottom:10px;font-size:.875rem;color:#cbd5e1;line-height:1.65;transition:all .2s;animation:cardIn .3s ease-out}
.resume-bullet:hover{border-color:rgba(167,139,250,.3);background:#111122;box-shadow:0 4px 18px rgba(167,139,250,.07)}

/* Score */
.score-wrap{background:#0d0d1a;border:1px solid rgba(255,255,255,.07);border-radius:16px;padding:28px;text-align:center}

/* Chart */
.chart-card{background:#0d0d1a;border:1px solid rgba(255,255,255,.07);border-radius:16px;padding:20px 20px 8px;box-shadow:0 4px 24px rgba(0,0,0,.25);transition:all .2s;animation:cardIn .4s ease-out;margin-bottom:18px}
.chart-card:hover{border-color:rgba(79,142,247,.2);box-shadow:0 8px 32px rgba(79,142,247,.07)}
.chart-label{font-size:.67rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#4f8ef7;margin-bottom:4px}
.chart-title-text{font-family:'Space Grotesk',sans-serif;font-size:.93rem;font-weight:700;color:#e2e8f0;margin-bottom:14px}

/* Misc */
.stMarkdown h1,.stMarkdown h2,.stMarkdown h3,.stMarkdown h4{font-family:'Space Grotesk',sans-serif!important;color:#e2e8f0!important;font-weight:700!important}
.stMarkdown p,.stMarkdown li{color:#94a3b8!important;line-height:1.72!important}
.stMarkdown strong{color:#e2e8f0!important}
.stMarkdown a{color:#4f8ef7!important}
.stMarkdown code{background:rgba(79,142,247,.1)!important;color:#93c5fd!important;border-radius:4px!important;padding:2px 6px!important}
.stAlert{background:rgba(79,142,247,.08)!important;border:1px solid rgba(79,142,247,.2)!important;border-radius:12px!important}
.stDownloadButton>button{background:rgba(245,200,66,.09)!important;border:1px solid rgba(245,200,66,.28)!important;color:#f5c842!important;border-radius:10px!important;font-weight:600!important;transition:all .2s!important}
.stDownloadButton>button:hover{background:rgba(245,200,66,.18)!important;box-shadow:0 4px 20px rgba(245,200,66,.2)!important;transform:translateY(-1px)!important}
hr{border-color:rgba(255,255,255,.07)!important;margin:22px 0!important}
.stTextInput>div>div>input{background:#111122!important;border:1px solid rgba(79,142,247,.2)!important;border-radius:10px!important;color:#e2e8f0!important}
.stTextInput>div>div>input:focus{border-color:#4f8ef7!important;box-shadow:0 0 0 3px rgba(79,142,247,.1)!important}
.footer{text-align:center;padding:40px 0 24px;border-top:1px solid rgba(255,255,255,.06);margin-top:48px}
.ai-badge{display:inline-flex;align-items:center;gap:6px;background:rgba(79,142,247,.08);border:1px solid rgba(79,142,247,.22);color:#93c5fd;padding:4px 12px;border-radius:99px;font-size:.7rem;font-weight:600;letter-spacing:.5px}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────
DEFAULTS = dict(result=None, chat_history=[], pipeline_step=0,
                interview_qa=[], resume_tips="", readiness_score=None)
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─────────────────────────────────────────────────────────────
# STRUCTURED RENDERERS
# ─────────────────────────────────────────────────────────────
SKILL_META = {
    "Technical Skills":        ("🔧","#4f8ef7"),
    "Programming Languages":   ("💻","#a78bfa"),
    "Tools & Technologies":    ("🛠️","#22c55e"),
    "Frameworks & Platforms":  ("⚙️","#f97316"),
    "Cloud Platforms":         ("☁️","#06b6d4"),
    "Databases":               ("🗄️","#f5c842"),
    "AI / ML / GenAI Skills":  ("🤖","#ec4899"),
    "Business Skills":         ("📊","#4f8ef7"),
    "Domain Knowledge":        ("🌐","#a78bfa"),
    "Certifications":          ("🏅","#f5c842"),
    "Education Requirements":  ("🎓","#22c55e"),
    "Experience Requirements": ("📅","#f97316"),
    "Soft Skills":             ("🤝","#06b6d4"),
    "Other Requirements":      ("📋","#94a3b8"),
}

def parse_json_safe(raw: str):
    try:
        cleaned = re.sub(r"```(?:json)?", "", raw).replace("```","").strip()
        s = cleaned.find("{"); e = cleaned.rfind("}")
        if s == -1 or e == -1: return None
        return json.loads(cleaned[s:e+1])
    except Exception:
        return None

# ── Jobs renderer ──
def render_jobs(raw: str):
    # Parse structured job blocks from markdown text
    blocks = re.split(r'\n(?=\d+\.\s|\*\*Job Title)', raw.strip())
    if len(blocks) < 2:
        blocks = re.split(r'\n\n+', raw.strip())

    rendered = 0
    for block in blocks:
        block = block.strip()
        if not block or len(block) < 30: continue

        title    = re.search(r'\*{0,2}Job Title\*{0,2}[:\s]+(.+?)(?:\n|\*\*|$)', block)
        company  = re.search(r'\*{0,2}Company\*{0,2}[:\s]+(.+?)(?:\n|\*\*|$)', block)
        location = re.search(r'\*{0,2}Location\*{0,2}[:\s]+(.+?)(?:\n|\*\*|$)', block)
        salary   = re.search(r'\*{0,2}Salary\*{0,2}[:\s]+(.+?)(?:\n|\*\*|$)', block)
        summary  = re.search(r'\*{0,2}(?:Short Job Summary|Summary)\*{0,2}[:\s]+(.+?)(?:\n\n|$)', block, re.DOTALL)
        url_m    = re.search(r'\[Apply Here\]\(([^)]+)\)', block)

        if not title: continue

        t  = title.group(1).strip().rstrip("*").strip()
        co = company.group(1).strip().rstrip("*").strip() if company else "N/A"
        lo = location.group(1).strip().rstrip("*").strip() if location else "N/A"
        sa = salary.group(1).strip().rstrip("*").strip() if salary else "Not Available"
        su = summary.group(1).strip().replace("\n"," ") if summary else ""
        url= url_m.group(1) if url_m else "#"

        sal_na = sa.lower() in ("not available","n/a","not specified","")
        sal_chip = f'<span class="job-chip salary">💰 {sa}</span>' if not sal_na else ""

        st.markdown(f"""
        <div class="job-card">
          <div class="job-title">{t}</div>
          <div class="job-company">{co}</div>
          <div class="job-meta">
            <span class="job-chip loc">📍 {lo}</span>
            {sal_chip}
          </div>
          {f'<div class="job-summary">{su}</div>' if su else ''}
          <a href="{url}" target="_blank" class="job-apply">Apply Now →</a>
        </div>""", unsafe_allow_html=True)
        rendered += 1

    if rendered == 0:
        st.markdown(f'<div class="content-card">{raw}</div>', unsafe_allow_html=True)

# ── Skills renderer ──
def render_skills(raw: str):
    data = parse_json_safe(raw)
    if not data:
        st.markdown(f'<div class="content-card">{raw}</div>', unsafe_allow_html=True)
        return
    filtered = {
        k: [str(i) for i in v if str(i).strip().lower() not in ("not mentioned","none","n/a","")]
        for k, v in data.items() if isinstance(v, list)
    }
    filtered = {k: v for k, v in filtered.items() if v}
    keys = list(filtered.keys())
    for i in range(0, len(keys), 2):
        cols = st.columns(2)
        for col, key in zip(cols, keys[i:i+2]):
            icon, color = SKILL_META.get(key, ("📌","#4f8ef7"))
            tags = "".join(f'<span class="skill-tag">{item}</span>' for item in filtered[key])
            with col:
                st.markdown(f"""
                <div class="skill-card" style="border-top:2px solid {color};">
                  <div style="display:flex;align-items:center;gap:8px;margin-bottom:12px;">
                    <span style="font-size:1.05rem;">{icon}</span>
                    <span style="font-family:'Space Grotesk',sans-serif;font-size:.82rem;font-weight:700;color:#e2e8f0;">{key}</span>
                    <span style="margin-left:auto;background:rgba(79,142,247,.11);color:#4f8ef7;font-size:.63rem;font-weight:700;padding:2px 9px;border-radius:99px;">{len(filtered[key])}</span>
                  </div>
                  <div class="skill-tags">{tags}</div>
                </div>""", unsafe_allow_html=True)

# ── Salary renderer ──
def render_salary(raw: str):
    BAD = ["unable to retrieve","temporary issue","try again","error","failed","unavailable","cannot"]
    is_bad = any(p in raw.lower() for p in BAD) or len(raw.strip()) < 40

    if not is_bad:
        # Try to render structured salary from text
        lines = [l.strip() for l in raw.split("\n") if l.strip()]
        # Show as nicely formatted content card
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown(raw)
        st.markdown('</div>', unsafe_allow_html=True)
        return

    st.markdown("""
    <div style="background:rgba(245,200,66,.06);border:1px solid rgba(245,200,66,.24);
    border-left:3px solid #f5c842;border-radius:14px;padding:22px 26px;margin-bottom:20px;">
      <div style="display:flex;align-items:center;gap:10px;margin-bottom:7px;">
        <span style="font-size:1.2rem;">⚠️</span>
        <span style="font-family:'Space Grotesk',sans-serif;font-weight:700;color:#f5c842;">Salary API Temporarily Unavailable</span>
      </div>
      <p style="color:#94a3b8;font-size:.87rem;line-height:1.6;margin:0;">
        Re-run the analysis to fetch live data. Estimated benchmarks shown below.
      </p>
    </div>""", unsafe_allow_html=True)

    bands = [("0–1 yr","₹4L – ₹7L","Entry Level"),("1–3 yrs","₹7L – ₹14L","Junior"),
             ("3–5 yrs","₹14L – ₹22L","Mid Level"),("5–7 yrs","₹22L – ₹32L","Senior"),
             ("7–10 yrs","₹32L – ₹45L","Lead / Staff"),("10+ yrs","₹45L – ₹80L","Principal")]
    c1,c2,c3 = st.columns(3)
    for idx,(exp,sal,lvl) in enumerate(bands):
        with [c1,c2,c3][idx%3]:
            st.markdown(f"""
            <div class="salary-band">
              <div class="salary-exp">{exp}</div>
              <div class="salary-val">{sal}</div>
              <div class="salary-lvl">{lvl}</div>
            </div>""", unsafe_allow_html=True)

# ── Roadmap renderer ──
def render_roadmap(raw: str):
    # Parse courses
    courses = re.findall(
        r'[-•*]\s*([^\[\n]+?)\s*[-–]\s*([^\[\n]+?)\s*\[(?:Link|link)\]\(([^)]+)\)',
        raw)
    # Parse certs
    certs = re.findall(
        r'(?:NVIDIA|AWS|Azure|Google|Microsoft|CompTIA|PMI)[^\[\n]+\[(?:Link|link)\]\(([^)]+)\)',
        raw)
    cert_names = re.findall(
        r'\*\s*((?:NVIDIA|AWS|Azure|Google|Microsoft|CompTIA|PMI)[^\[\n*]+)',
        raw)
    # Parse sequence steps
    seq_steps = re.findall(r'\d+\.\s+(.+?)(?:\n|$)', raw)
    seq_steps = [s for s in seq_steps if len(s) > 10 and not s.startswith("Complete") or True]
    # Parse months
    months = re.findall(r'(Month \d+|Month\s+\w+):\s*\n((?:[-*•].+\n?)+)', raw, re.IGNORECASE)
    # Parse projects
    projects = re.findall(r'[-*•]\s+(Build|Create|Develop|Implement|Deploy|Design).+', raw)
    # Parse key recs
    recs = re.findall(r'[-*•]\s+(Focus|Engage|Consider|Pursue|Ensure|Learn|Master|Stay|Practice|Work|Collaborate).+', raw)

    col_a, col_b = st.columns(2)

    with col_a:
        if courses:
            st.markdown("""
            <div class="roadmap-section">
              <div class="roadmap-title">
                <div class="roadmap-title-icon" style="background:rgba(79,142,247,.12);">📚</div>
                Recommended Courses
              </div>""", unsafe_allow_html=True)
            for name, provider, link in courses[:8]:
                st.markdown(f"""
                <div class="course-item">
                  <div>
                    <div class="course-name">{name.strip()}</div>
                    <div class="course-provider">{provider.strip()}</div>
                  </div>
                  <a href="{link}" target="_blank" class="course-link">Enroll →</a>
                </div>""", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        if cert_names:
            st.markdown("""
            <div class="roadmap-section">
              <div class="roadmap-title">
                <div class="roadmap-title-icon" style="background:rgba(245,200,66,.1);">🏅</div>
                Certifications
              </div>""", unsafe_allow_html=True)
            for i, name in enumerate(cert_names[:5]):
                link = certs[i] if i < len(certs) else "#"
                st.markdown(f"""
                <div class="cert-item">
                  <div class="cert-name">🏅 {name.strip()}</div>
                  <a href="{link}" target="_blank" class="cert-link">View →</a>
                </div>""", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    with col_b:
        if seq_steps:
            seq_display = [s for s in seq_steps if len(s) > 15][:10]
            if seq_display:
                st.markdown("""
                <div class="roadmap-section">
                  <div class="roadmap-title">
                    <div class="roadmap-title-icon" style="background:rgba(167,139,250,.1);">🗺️</div>
                    Learning Sequence
                  </div>""", unsafe_allow_html=True)
                for i, step in enumerate(seq_display):
                    st.markdown(f"""
                    <div class="seq-step">
                      <div class="seq-num">{i+1}</div>
                      <div class="seq-text">{step.strip()}</div>
                    </div>""", unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

        if projects:
            st.markdown("""
            <div class="roadmap-section">
              <div class="roadmap-title">
                <div class="roadmap-title-icon" style="background:rgba(34,197,94,.1);">🔨</div>
                Practical Projects
              </div>""", unsafe_allow_html=True)
            for p in projects[:5]:
                st.markdown(f"""
                <div class="project-item">
                  <div class="project-dot"></div>
                  <div class="project-text">{p.strip()}</div>
                </div>""", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # Timeline full width
    if months:
        st.markdown("""
        <div class="roadmap-section">
          <div class="roadmap-title">
            <div class="roadmap-title-icon" style="background:rgba(6,182,212,.1);">📅</div>
            Learning Timeline
          </div>""", unsafe_allow_html=True)
        mc = st.columns(min(len(months), 3))
        for i, (month, content) in enumerate(months[:3]):
            items = re.findall(r'[-*•]\s*(.+)', content)
            with mc[i]:
                items_html = "".join(f'<div style="font-size:.8rem;color:#94a3b8;padding:4px 0;border-bottom:1px solid rgba(255,255,255,.04);">• {it.strip()}</div>' for it in items)
                st.markdown(f"""
                <div class="timeline-month">
                  <div class="timeline-month-title">📅 {month}</div>
                  {items_html}
                </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Key Recs
    if recs:
        st.markdown("""
        <div class="roadmap-section">
          <div class="roadmap-title">
            <div class="roadmap-title-icon" style="background:rgba(245,200,66,.08);">💡</div>
            Key Recommendations
          </div>""", unsafe_allow_html=True)
        for r in recs[:5]:
            st.markdown(f"""
            <div class="strategy-item">
              <div class="strategy-bullet"></div>
              <div class="strategy-text">{r.strip()}</div>
            </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    if not courses and not cert_names and not seq_steps:
        st.markdown(f'<div class="content-card">{raw}</div>', unsafe_allow_html=True)

# ── Strategy renderer ──
def render_strategy(raw: str):
    sections = {
        "Career Recommendations": (re.findall(r'[-*•]\s*(Pursue|Target|Engage|Build|Focus|Develop|Network|Apply|Consider|Create).+', raw), "🎯","#4f8ef7"),
        "Skill Priorities":       (re.findall(r'\d+\.\s+(.+?)(?:\n|$)', raw)[:8], "🧠","#a78bfa"),
        "Industry Insights":      (re.findall(r'[-*•]\s*(The demand|Companies|Security|Organizations|AI|Market|Trend).+', raw), "📈","#22c55e"),
        "Strengths Identified":   (re.findall(r'[-*•]\s*(Strong|Experience|Ability|Skilled|Proven|Deep|Expert).+', raw), "✅","#22c55e"),
        "Potential Skill Gaps":   (re.findall(r'[-*•]\s*(Limited|Need|Lack|Gap|Missing|Require|Without).+', raw), "⚠️","#f97316"),
    }
    action_blocks = re.findall(r'(30|60|90)\s*Days?[:\s]+([\s\S]+?)(?=(?:30|60|90)\s*Days?|Expected|Final|$)', raw, re.IGNORECASE)
    outcome = re.search(r'Expected Outcome[:\s]+([\s\S]+?)(?=Final|$)', raw, re.IGNORECASE)
    final_rec = re.search(r'Final Recommendation[:\s]+([\s\S]+?)$', raw, re.IGNORECASE)

    rendered = 0
    col_a, col_b = st.columns(2)
    sec_list = list(sections.items())
    for idx, (title, (items, icon, color)) in enumerate(sec_list):
        if not items: continue
        col = col_a if idx % 2 == 0 else col_b
        with col:
            items_html = "".join(
                f'<div class="strategy-item"><div class="strategy-bullet" style="background:{color};"></div><div class="strategy-text">{it.strip()}</div></div>'
                for it in items[:6]
            )
            st.markdown(f"""
            <div class="strategy-card" style="border-top:2px solid {color};">
              <div class="strategy-title" style="color:{color};">{icon} {title}</div>
              {items_html}
            </div>""", unsafe_allow_html=True)
            rendered += 1

    if action_blocks:
        st.markdown("""
        <div class="strategy-card">
          <div class="strategy-title" style="color:#4f8ef7;">📅 30-60-90 Day Action Plan</div>""", unsafe_allow_html=True)
        ac = st.columns(len(action_blocks))
        for i, (days, content) in enumerate(action_blocks):
            items = re.findall(r'[-*•]\s*(.+)', content)
            with ac[i]:
                items_html = "".join(f'<div style="font-size:.8rem;color:#94a3b8;padding:5px 0;border-bottom:1px solid rgba(255,255,255,.04);">• {it.strip()}</div>' for it in items[:5])
                st.markdown(f"""
                <div class="action-day">
                  <div class="action-day-title">Day {days}</div>
                  {items_html}
                </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    if outcome:
        items = re.findall(r'[-*•]\s*(.+)', outcome.group(1))
        if items:
            items_html = "".join(f'<div class="strategy-item"><div class="strategy-bullet" style="background:#22c55e;"></div><div class="strategy-text">{it.strip()}</div></div>' for it in items[:4])
            st.markdown(f"""
            <div class="strategy-card" style="border-top:2px solid #22c55e;">
              <div class="strategy-title" style="color:#22c55e;">🏆 Expected Outcomes</div>
              {items_html}
            </div>""", unsafe_allow_html=True)

    if rendered == 0 and not action_blocks:
        st.markdown(f'<div class="content-card">{raw}</div>', unsafe_allow_html=True)

# ── Report renderer ──
def render_report(raw: str):
    # Split into sections by ## or # headers
    sections = re.split(r'\n(?=#{1,3}\s)', raw.strip())
    if len(sections) < 2:
        # Try splitting by bold headers
        sections = re.split(r'\n(?=[A-Z][a-z].*\n[-=]+)', raw.strip())

    if len(sections) >= 2:
        for section in sections:
            section = section.strip()
            if not section: continue
            header_m = re.match(r'^(#{1,3})\s+(.+)', section)
            header   = header_m.group(2) if header_m else None
            body     = section[header_m.end():].strip() if header_m else section

            if header:
                st.markdown(f"""
                <div style="font-family:'Space Grotesk',sans-serif;font-size:.95rem;font-weight:700;
                color:#e2e8f0;padding:16px 0 8px;border-bottom:1px solid rgba(79,142,247,.15);
                margin-bottom:12px;">{header}</div>""", unsafe_allow_html=True)

            if body:
                # Parse bullet items
                items = re.findall(r'[-*•]\s+(.+?)(?:\n|$)', body)
                num_items = re.findall(r'\d+\.\s+(.+?)(?:\n|$)', body)
                plain = re.sub(r'[-*•]\s+.+?\n?', '', body).strip()
                plain = re.sub(r'\d+\.\s+.+?\n?', '', plain).strip()

                if plain and len(plain) > 20:
                    st.markdown(f'<p style="color:#94a3b8;font-size:.875rem;line-height:1.7;margin-bottom:10px;">{plain}</p>', unsafe_allow_html=True)
                for it in items[:8]:
                    st.markdown(f'<div style="display:flex;gap:8px;padding:5px 0;"><span style="color:#4f8ef7;font-size:.75rem;margin-top:3px;">▸</span><span style="color:#94a3b8;font-size:.84rem;line-height:1.6;">{it.strip()}</span></div>', unsafe_allow_html=True)
                for i, it in enumerate(num_items[:8]):
                    st.markdown(f'<div style="display:flex;gap:8px;padding:5px 0;"><span style="background:linear-gradient(135deg,#4f8ef7,#7c3aed);color:#fff;width:20px;height:20px;border-radius:5px;display:inline-flex;align-items:center;justify-content:center;font-size:.62rem;font-weight:800;flex-shrink:0;">{i+1}</span><span style="color:#94a3b8;font-size:.84rem;line-height:1.6;">{it.strip()}</span></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="content-card">{raw}</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# PIPELINE TRACKER
# ─────────────────────────────────────────────────────────────
STEPS    = [("🔍","Job Search"),("🧠","Skills"),("💰","Salary"),
            ("📚","Roadmap"),("🎯","Advisor"),("📄","Report")]
STEP_MAP = {10:1,20:1,30:2,40:2,50:3,60:3,70:4,80:4,85:5,95:5,100:6}

def render_tracker(active=0):
    html = '<div class="pipeline-wrap">'
    for i,(icon,label) in enumerate(STEPS):
        done = i < active; act = i == active
        ic = "done" if done else ("active" if act else "")
        lc = "done" if done else ("active" if act else "")
        html += f'<div class="p-step"><div class="p-icon {ic}">{icon}</div><div class="p-label {lc}">{label}</div></div>'
        if i < len(STEPS)-1:
            cc = "done" if done else ("active" if act else "")
            html += f'<div class="p-connector {cc}"></div>'
    return html + '</div>'

# ─────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
      <div class="sidebar-logo">💼 Career Navigator</div>
      <div class="sidebar-tag">Intelligence Platform · v4.0</div>
      <div style="margin-top:10px;"><span class="ai-badge">✨ GPT-5 via OpenWebNinja</span></div>
    </div>""", unsafe_allow_html=True)

    goal                = st.text_input("Career Goal",     value="Generative AI Engineer")
    location            = st.text_input("Target Location", value="Bangalore")
    years_of_experience = st.selectbox("Experience Level", [
        "ZERO_TO_ONE","ONE_TO_THREE","THREE_TO_FIVE",
        "FIVE_TO_SEVEN","SEVEN_TO_TEN","TEN_PLUS"
    ])
    st.markdown("<br>", unsafe_allow_html=True)
    run_button = st.button("🚀 Launch Analysis", use_container_width=True)

    st.markdown("""
    <div style="margin-top:26px;padding:15px;background:rgba(79,142,247,.05);border:1px solid rgba(79,142,247,.1);border-radius:12px;">
      <div style="font-size:.63rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#475569;margin-bottom:10px;">System Status</div>
      <div style="display:flex;flex-direction:column;gap:7px;font-size:.75rem;">
        <div style="display:flex;justify-content:space-between;"><span style="color:#64748b;">Agents</span><span style="color:#22c55e;font-weight:600;">6/6 Ready</span></div>
        <div style="display:flex;justify-content:space-between;"><span style="color:#64748b;">AI Model</span><span style="color:#a78bfa;font-weight:600;">GPT-5</span></div>
        <div style="display:flex;justify-content:space-between;"><span style="color:#64748b;">Provider</span><span style="color:#93c5fd;font-weight:600;">OpenWebNinja</span></div>
        <div style="display:flex;justify-content:space-between;"><span style="color:#64748b;">Data</span><span style="color:#22c55e;font-weight:600;">Live</span></div>
      </div>
    </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# HERO
# ─────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero-wrap">
  <div class="hero-eyebrow">AI-Powered Career Intelligence</div>
  <div class="hero-title">Your Career,<br>Intelligently Mapped.</div>
  <div class="hero-sub">Six specialized AI agents surface job opportunities, decode skill requirements,
  benchmark salaries, and chart your fastest path to
  <strong style="color:#e2e8f0;">{goal}</strong>. All AI features powered by GPT-5 via OpenWebNinja.</div>
  <div class="hero-badges">
    <span class="hero-badge">🔍 Job Search</span>
    <span class="hero-badge">🧠 Skill Intelligence</span>
    <span class="hero-badge">💰 Salary Benchmarking</span>
    <span class="hero-badge">📚 Learning Roadmap</span>
    <span class="hero-badge">🎯 Career Strategy</span>
    <span class="hero-badge">📊 Analytics</span>
    <span class="hero-badge">🤖 AI Chat</span>
    <span class="hero-badge">🎤 Interview Prep</span>
    <span class="hero-badge">📝 Resume Tips</span>
    <span class="hero-badge">✨ GPT-5 Powered</span>
  </div>
</div>""", unsafe_allow_html=True)

tracker_ph = st.empty()
tracker_ph.markdown(render_tracker(0), unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# PIPELINE
# ─────────────────────────────────────────────────────────────
if run_button:
    prog = st.progress(0)
    s_ph = st.empty()

    def update_status(msg, pct):
        prog.progress(pct)
        s_ph.markdown(f'<div class="agent-status">{msg}</div>', unsafe_allow_html=True)
        st.session_state.pipeline_step = STEP_MAP.get(pct, st.session_state.pipeline_step)
        tracker_ph.markdown(render_tracker(st.session_state.pipeline_step), unsafe_allow_html=True)

    with st.spinner("Running career intelligence pipeline..."):
        result = run_career_pipeline(
            goal=goal, location=location,
            years_of_experience=years_of_experience,
            callback=update_status
        )
    for k in ("chat_history","interview_qa"): st.session_state[k] = []
    for k in ("resume_tips",): st.session_state[k] = ""
    st.session_state.readiness_score = None
    st.session_state.result = result
    tracker_ph.markdown(render_tracker(6), unsafe_allow_html=True)
    prog.progress(100)
    s_ph.success("✅ Career Intelligence Report Generated Successfully")

# ─────────────────────────────────────────────────────────────
# RESULTS
# ─────────────────────────────────────────────────────────────
if st.session_state.result:
    res = st.session_state.result

    st.markdown('<div class="sec-header"><div class="sec-dot"></div>Analysis Overview</div>', unsafe_allow_html=True)
    c1,c2,c3,c4 = st.columns(4)
    with c1: st.metric("Career Goal",  goal)
    with c2: st.metric("Location",     location)
    with c3: st.metric("Experience",   years_of_experience.replace("_"," "))
    with c4: st.metric("Agents Run",   "6 / 6 ✓")
    st.markdown("<br>", unsafe_allow_html=True)

    tabs = st.tabs(["💼 Jobs","🧠 Skills","💰 Salary","📚 Roadmap",
                    "🎯 Strategy","📊 Analytics","🤖 AI Chat",
                    "🎤 Interview","📝 Resume","📄 Report"])

    # JOBS
    with tabs[0]:
        st.markdown('<div class="sec-header"><div class="sec-dot"></div>Live Job Opportunities</div>', unsafe_allow_html=True)
        render_jobs(res["jobs"])

    # SKILLS
    with tabs[1]:
        st.markdown('<div class="sec-header"><div class="sec-dot"></div>Skills Intelligence Matrix</div>', unsafe_allow_html=True)
        render_skills(res["skills"])

    # SALARY
    with tabs[2]:
        st.markdown('<div class="sec-header"><div class="sec-dot"></div>Salary Intelligence</div>', unsafe_allow_html=True)
        render_salary(res["salary"])

    # ROADMAP
    with tabs[3]:
        st.markdown('<div class="sec-header"><div class="sec-dot"></div>Learning Roadmap</div>', unsafe_allow_html=True)
        render_roadmap(res["roadmap"])

    # STRATEGY
    with tabs[4]:
        st.markdown('<div class="sec-header"><div class="sec-dot"></div>Career Strategy</div>', unsafe_allow_html=True)
        render_strategy(res["career_advice"])

    # ANALYTICS
    with tabs[5]:
        st.markdown('<div class="sec-header"><div class="sec-dot"></div>Job Market Analytics</div>', unsafe_allow_html=True)
        try:
            import plotly.graph_objects as go
            BG=("#0d0d1a"); GRID="rgba(255,255,255,.05)"
            B="#4f8ef7"; P="#a78bfa"; G="#f5c842"
            PAL=[B,P,G,"#22c55e","#f97316","#ec4899","#06b6d4"]
            BL=dict(paper_bgcolor=BG,plot_bgcolor=BG,font=dict(family="Inter,sans-serif",color="#94a3b8",size=11),
                    title_font=dict(family="Space Grotesk,sans-serif",color="#e2e8f0",size=13),
                    margin=dict(l=12,r=12,t=44,b=12),
                    xaxis=dict(gridcolor=GRID,color="#475569",linecolor=GRID,zeroline=False),
                    yaxis=dict(gridcolor=GRID,color="#475569",linecolor=GRID,zeroline=False))
            CFG=dict(displayModeBar=False)
            NOAX={k:v for k,v in BL.items() if k not in ("xaxis","yaxis")}

            r1a,r1b=st.columns(2)
            with r1a:
                st.markdown('<div class="chart-card"><div class="chart-label">Compensation</div><div class="chart-title-text">Salary Range by Experience</div>',unsafe_allow_html=True)
                exp=["0-1yr","1-3yrs","3-5yrs","5-7yrs","7-10yrs","10+yrs"]
                lo=[4,6,10,15,22,32];hi=[7,10,16,24,35,55];mid=[(a+b)/2 for a,b in zip(lo,hi)]
                fig=go.Figure()
                fig.add_trace(go.Bar(x=exp,y=[b-a for a,b in zip(lo,hi)],base=lo,marker=dict(color=PAL[:6],opacity=.85,line=dict(width=0)),name="Range",hovertemplate="<b>%{x}</b><br>₹%{base}L–₹%{y}L<extra></extra>"))
                fig.add_trace(go.Scatter(x=exp,y=mid,mode="lines+markers",line=dict(color="#fff",width=1.5,dash="dot"),marker=dict(size=5,color="#fff"),name="Median"))
                fig.update_layout(**BL,title="Annual Salary (₹ Lakhs)",legend=dict(bgcolor="rgba(0,0,0,0)",font=dict(size=10)))
                st.plotly_chart(fig,use_container_width=True,config=CFG)
                st.markdown('</div>',unsafe_allow_html=True)
            with r1b:
                st.markdown('<div class="chart-card"><div class="chart-label">Skills</div><div class="chart-title-text">Top In-Demand Skills</div>',unsafe_allow_html=True)
                sk=["Python","LLMs/GenAI","LangChain","Vector DBs","Cloud","MLOps","FastAPI","SQL"]
                val=[95,92,87,82,80,75,70,65]
                fig2=go.Figure(go.Bar(x=val,y=sk,orientation="h",marker=dict(color=val,colorscale=[[0,"#111122"],[.5,B],[1,P]],line=dict(width=0)),hovertemplate="<b>%{y}</b>: %{x}%<extra></extra>"))
                fig2.update_layout(**BL,title="Demand Index (%)");fig2.update_xaxes(range=[0,100])
                st.plotly_chart(fig2,use_container_width=True,config=CFG)
                st.markdown('</div>',unsafe_allow_html=True)

            r2a,r2b=st.columns(2)
            with r2a:
                st.markdown('<div class="chart-card"><div class="chart-label">Companies</div><div class="chart-title-text">Top Hiring Companies</div>',unsafe_allow_html=True)
                fig3=go.Figure(go.Pie(labels=["Google","Amazon","Microsoft","Infosys","TCS","Wipro","Startups"],values=[18,15,14,12,11,9,21],hole=.58,marker=dict(colors=PAL,line=dict(color=BG,width=2)),hovertemplate="<b>%{label}</b>: %{percent}<extra></extra>"))
                fig3.update_layout(**NOAX,title="Hiring Distribution",legend=dict(bgcolor="rgba(0,0,0,0)",font=dict(size=10)),annotations=[dict(text="HIRING",x=.5,y=.5,showarrow=False,font=dict(family="Space Grotesk,sans-serif",size=10,color=B))])
                st.plotly_chart(fig3,use_container_width=True,config=CFG)
                st.markdown('</div>',unsafe_allow_html=True)
            with r2b:
                st.markdown('<div class="chart-card"><div class="chart-label">Skill Gap</div><div class="chart-title-text">Required vs Your Level</div>',unsafe_allow_html=True)
                cats=["Python","Cloud","MLOps","GenAI","Databases","APIs","Soft Skills","Python"]
                req=[95,80,75,92,70,78,65,95];you=[70,55,40,60,65,72,80,70]
                fig4=go.Figure()
                fig4.add_trace(go.Scatterpolar(r=req,theta=cats,fill="toself",name="Required",line=dict(color=B,width=2),fillcolor="rgba(79,142,247,.1)"))
                fig4.add_trace(go.Scatterpolar(r=you,theta=cats,fill="toself",name="Your Level",line=dict(color=G,width=1.5,dash="dot"),fillcolor="rgba(245,200,66,.06)"))
                fig4.update_layout(**NOAX,title="Skill Gap Radar",polar=dict(bgcolor=BG,radialaxis=dict(visible=True,range=[0,100],color="#475569",gridcolor=GRID),angularaxis=dict(color="#94a3b8",gridcolor=GRID)),legend=dict(bgcolor="rgba(0,0,0,0)",font=dict(size=10)))
                st.plotly_chart(fig4,use_container_width=True,config=CFG)
                st.markdown('</div>',unsafe_allow_html=True)

            st.markdown('<div class="chart-card"><div class="chart-label">Market Trend</div><div class="chart-title-text">Job Postings & Avg Salary — Last 12 Months</div>',unsafe_allow_html=True)
            months=["Jul'24","Aug","Sep","Oct","Nov","Dec","Jan'25","Feb","Mar","Apr","May","Jun"]
            postings=[820,910,880,1050,1200,980,1350,1480,1600,1720,1850,1980]
            avgs=[14.2,14.5,14.8,15.0,15.4,15.1,15.8,16.2,16.8,17.1,17.6,18.0]
            fig5=go.Figure()
            fig5.add_trace(go.Scatter(x=months,y=postings,mode="lines+markers",name="Job Postings",line=dict(color=B,width=2.5),marker=dict(size=6,color=B),fill="tozeroy",fillcolor="rgba(79,142,247,.06)",hovertemplate="<b>%{x}</b><br>%{y:,}<extra></extra>"))
            fig5.add_trace(go.Scatter(x=months,y=avgs,mode="lines+markers",name="Avg Salary (₹L)",line=dict(color=G,width=1.5,dash="dot"),marker=dict(size=5,color=G),yaxis="y2",hovertemplate="₹%{y}L<extra></extra>"))
            fig5.update_layout(**BL,yaxis2=dict(overlaying="y",side="right",color=G,gridcolor=GRID),legend=dict(bgcolor="rgba(0,0,0,0)",font=dict(size=10)),hovermode="x unified")
            st.plotly_chart(fig5,use_container_width=True,config=CFG)
            st.markdown('</div>',unsafe_allow_html=True)

            r3a,r3b=st.columns(2)
            with r3a:
                st.markdown('<div class="chart-card"><div class="chart-label">Work Mode</div><div class="chart-title-text">Remote vs Hybrid vs On-site</div>',unsafe_allow_html=True)
                fig6=go.Figure(go.Bar(x=["Remote","Hybrid","On-site"],y=[35,42,23],marker=dict(color=[B,P,G],line=dict(width=0)),text=["35%","42%","23%"],textposition="auto",textfont=dict(color="#fff",family="Space Grotesk,sans-serif",size=12),hovertemplate="%{x}: %{y}%<extra></extra>"))
                fig6.update_layout(**BL,title="Work Mode Split")
                st.plotly_chart(fig6,use_container_width=True,config=CFG)
                st.markdown('</div>',unsafe_allow_html=True)
            with r3b:
                st.markdown('<div class="chart-card"><div class="chart-label">Experience</div><div class="chart-title-text">Jobs by Experience Level</div>',unsafe_allow_html=True)
                fig7=go.Figure(go.Bar(x=["0-1yr","1-3yrs","3-5yrs","5-7yrs","7+yrs"],y=[8,28,35,18,11],marker=dict(color=PAL[:5],line=dict(width=0)),text=["8%","28%","35%","18%","11%"],textposition="auto",textfont=dict(color="#fff",family="Space Grotesk,sans-serif",size=12),hovertemplate="%{x}: %{y}%<extra></extra>"))
                fig7.update_layout(**BL,title="Experience Distribution")
                st.plotly_chart(fig7,use_container_width=True,config=CFG)
                st.markdown('</div>',unsafe_allow_html=True)
        except ImportError:
            st.error("Run: `pip install plotly`")

    # AI CHAT
    with tabs[6]:
        st.markdown('<div class="sec-header"><div class="sec-dot"></div>AI Career Advisor Chat</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="chat-shell">
          <div class="chat-topbar">
            <div class="chat-avatar">🤖</div>
            <div>
              <div class="chat-name">Career Advisor AI</div>
              <div class="chat-online"><div class="online-dot"></div>Online · GPT-5 via OpenWebNinja · Context-aware</div>
            </div>
          </div>""", unsafe_allow_html=True)
        msgs_html = ""
        if not st.session_state.chat_history:
            msgs_html = '<div class="msg-ai">👋 Hello! I\'ve fully reviewed your career intelligence report and I\'m running on GPT-5 via OpenWebNinja.<br><br>Ask me anything — skill gaps, salary negotiation, target companies, or your action plan.</div>'
        else:
            for m in st.session_state.chat_history:
                cls = "msg-u" if m["role"]=="user" else "msg-ai"
                msgs_html += f'<div class="{cls}">{m["content"].replace(chr(10),"<br>")}</div>'
        st.markdown(f'<div class="chat-msgs">{msgs_html}</div>', unsafe_allow_html=True)
        st.markdown('</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<p style="font-size:.68rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#475569;margin-bottom:8px;">Quick Prompts</p>', unsafe_allow_html=True)
        qc1,qc2,qc3,qc4=st.columns(4)
        with qc1: q1=st.button("🔍 Skill gaps?",  key="q1")
        with qc2: q2=st.button("🏢 Best company?",key="q2")
        with qc3: q3=st.button("💰 Salary tips?", key="q3")
        with qc4: q4=st.button("📅 90-day plan?", key="q4")
        chosen=None
        if q1: chosen="What skills am I missing and how do I close the gap fast?"
        if q2: chosen="Which company from the job results should I prioritize and why?"
        if q3: chosen="How can I negotiate a higher salary for this role?"
        if q4: chosen="Give me a focused 90-day action plan to land this role."

        ic,bc=st.columns([5,1])
        with ic:
            user_input=st.text_input("Message",placeholder="Ask anything about your career analysis...",label_visibility="collapsed",key="chat_field")
        with bc:
            send=st.button("Send →",use_container_width=True)

        final=chosen or (user_input if send and user_input else None)
        if final:
            sys_ctx=f"""You are an expert AI Career Advisor with deep tech industry knowledge.
The user's full career analysis:
GOAL: {goal} | LOCATION: {location} | EXP: {years_of_experience}
JOBS:\n{res['jobs'][:700]}
SKILLS:\n{res['skills'][:700]}
SALARY:\n{res['salary'][:500]}
ROADMAP:\n{res['roadmap'][:700]}
STRATEGY:\n{res['career_advice'][:700]}
Be sharp, direct, specific. Use bullet points. Tone: senior mentor."""
            hist=[{"role":m["role"],"content":m["content"]} for m in st.session_state.chat_history[-8:]]
            hist.append({"role":"user","content":final})
            with st.spinner("✨ GPT-5 is thinking..."):
                reply=own_chat(sys_ctx,hist)
            st.session_state.chat_history.append({"role":"user","content":final})
            st.session_state.chat_history.append({"role":"assistant","content":reply})
            st.rerun()

    # INTERVIEW
    with tabs[7]:
        st.markdown('<div class="sec-header"><div class="sec-dot"></div>Interview Preparation</div>', unsafe_allow_html=True)
        st.markdown("""
        <div style="background:rgba(79,142,247,.06);border:1px solid rgba(79,142,247,.15);border-radius:14px;padding:20px 24px;margin-bottom:20px;">
          <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px;">
            <span style="font-size:1.1rem;">🎤</span>
            <span style="font-family:'Space Grotesk',sans-serif;font-size:.95rem;font-weight:700;color:#e2e8f0;">AI Interview Coach</span>
            <span class="ai-badge" style="margin-left:auto;">✨ GPT-5 via OpenWebNinja</span>
          </div>
          <p style="font-size:.85rem;color:#94a3b8;margin:0;">Role-specific questions with model answers, generated from your actual job analysis.</p>
        </div>""", unsafe_allow_html=True)
        ic1,ic2=st.columns([2,1])
        with ic1:
            itype=st.selectbox("Interview Type",["Technical Deep-Dive","Behavioral / HR","System Design","Case Study","Mixed (All Rounds)"],key="itype")
        with ic2:
            numq=st.selectbox("Questions",[5,8,10,15],key="numq")
        if st.button("🎯 Generate Interview Questions",key="gen_iv"):
            with st.spinner("✨ GPT-5 generating questions..."):
                prompt=f"""Generate {numq} {itype} interview questions for a {goal} role.
Required skills: {res['skills'][:600]}
Job context: {res['jobs'][:400]}
For each provide a strong model answer (3-5 sentences).
Return ONLY valid JSON array, no markdown:
[{{"question":"...","answer":"..."}}]"""
                raw=own_chat("You are an expert technical interviewer. Return only valid JSON arrays.",
                             [{"role":"user","content":prompt}],max_tokens=2000)
                try:
                    s=raw.find("[");e=raw.rfind("]")
                    st.session_state.interview_qa=json.loads(raw[s:e+1]) if s!=-1 else []
                except Exception:
                    st.session_state.interview_qa=[]
                    st.error("Could not parse. Try again.")
        if st.session_state.interview_qa:
            st.markdown(f'<div style="font-size:.72rem;color:#475569;font-weight:700;letter-spacing:1px;text-transform:uppercase;margin:16px 0 12px;">{len(st.session_state.interview_qa)} Questions Generated</div>',unsafe_allow_html=True)
            for idx,qa in enumerate(st.session_state.interview_qa):
                

                answer_html = markdown.markdown(
                    qa.get("answer", "")
                )
                st.markdown(f"""
                <div class="qa-card">
                <div class="qa-q">
                    <div class="qa-num">{idx+1}</div>
                    <div>{qa.get("question","")}</div>
                </div>
                <div class="qa-a">
                    {answer_html}
                </div>
                </div>
                """, unsafe_allow_html=True)
            qa_text="\n\n".join([f"Q{i+1}: {q['question']}\n\nA: {q['answer']}" for i,q in enumerate(st.session_state.interview_qa)])
            st.download_button("📥 Download Q&A Sheet",data=qa_text,file_name=f"interview_{goal.replace(' ','_').lower()}.txt",mime="text/plain",use_container_width=True)

    # RESUME
    with tabs[8]:
        st.markdown('<div class="sec-header"><div class="sec-dot"></div>Resume Optimizer</div>', unsafe_allow_html=True)
        st.markdown("""
        <div style="background:rgba(167,139,250,.06);border:1px solid rgba(167,139,250,.15);border-radius:14px;padding:20px 24px;margin-bottom:20px;">
          <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px;">
            <span style="font-size:1.1rem;">📝</span>
            <span style="font-family:'Space Grotesk',sans-serif;font-size:.95rem;font-weight:700;color:#e2e8f0;">AI Resume Bullet Generator</span>
            <span class="ai-badge" style="margin-left:auto;">✨ GPT-5 via OpenWebNinja</span>
          </div>
          <p style="font-size:.85rem;color:#94a3b8;margin:0;">ATS-optimized bullets tailored to the exact keywords employers are scanning for.</p>
        </div>""", unsafe_allow_html=True)
        rc1,rc2=st.columns(2)
        with rc1: curr_role=st.text_input("Current / Last Role",placeholder="e.g. ML Engineer at TCS",key="curr_role")
        with rc2: exp_yr=st.text_input("Years in that Role",placeholder="e.g. 2",key="exp_yr")
        if st.button("✨ Generate Resume Bullets",key="gen_res"):
            with st.spinner("✨ GPT-5 crafting bullets..."):
                prompt=f"""Write 8-10 powerful ATS-optimized resume bullet points for someone targeting {goal}.
Background: {curr_role}, {exp_yr} years.
Required skills: {res['skills'][:500]}
Context: {res['jobs'][:300]}
Rules: Strong action verbs, realistic metrics (X%, $Xk), weave in keywords, 1-2 lines each.
Return a plain numbered list only."""
                st.session_state.resume_tips=own_chat(
                    "You are an expert tech resume writer.",
                    [{"role":"user","content":prompt}],max_tokens=1200)
        if st.session_state.resume_tips:
            lines=[l.strip() for l in st.session_state.resume_tips.strip().split("\n") if l.strip()]
            for line in lines:
                clean=re.sub(r"^\d+[\.\)]\s*","",line)
                if clean:
                    st.markdown(f'<div class="resume-bullet"><span style="color:#a78bfa;font-weight:700;margin-right:8px;">▸</span>{clean}</div>',unsafe_allow_html=True)
            st.markdown("<br>",unsafe_allow_html=True)
            st.download_button("📥 Download Resume Bullets",data=st.session_state.resume_tips,file_name=f"resume_{goal.replace(' ','_').lower()}.txt",mime="text/plain",use_container_width=True)

            st.markdown('<div class="sec-header" style="margin-top:24px;"><div class="sec-dot"></div>Career Readiness Score</div>',unsafe_allow_html=True)
            if st.button("📊 Calculate Readiness Score",key="calc_score"):
                with st.spinner("✨ Analyzing with GPT-5..."):
                    p2=f"""Analyze career readiness for {goal}.
Skills required: {res['skills'][:400]}
User: {curr_role}, {exp_yr} years.
Return ONLY valid JSON (no markdown):
{{"score":72,"level":"Strong Candidate","strengths":["Python","ML"],"gaps":["LangChain","MLOps"],"tip":"One actionable sentence."}}"""
                    raw2=own_chat("Return only valid JSON.",
                                  [{"role":"user","content":p2}],max_tokens=400)
                    try:
                        s2=raw2.find("{");e2=raw2.rfind("}")
                        st.session_state.readiness_score=json.loads(raw2[s2:e2+1]) if s2!=-1 else None
                    except Exception:
                        st.session_state.readiness_score=None
            if st.session_state.readiness_score:
                sc=st.session_state.readiness_score
                val=sc.get("score",0)
                col="#22c55e" if val>=75 else ("#f5c842" if val>=50 else "#f97316")
                sc1,sc2,sc3=st.columns(3)
                with sc1:
                    st.markdown(f"""<div class="score-wrap">
                      <div style="font-size:.67rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#475569;margin-bottom:6px;">Readiness Score</div>
                      <div style="font-family:'Space Grotesk',sans-serif;font-size:3.6rem;font-weight:800;background:linear-gradient(135deg,{col},{col}88);-webkit-background-clip:text;-webkit-text-fill-color:transparent;line-height:1;">{val}%</div>
                      <div style="font-size:.8rem;color:#64748b;margin-top:6px;">{sc.get("level","")}</div>
                    </div>""",unsafe_allow_html=True)
                with sc2:
                    stags="".join(f'<span class="skill-tag" style="border-color:rgba(34,197,94,.3);color:#86efac;">{s}</span>' for s in sc.get("strengths",[]))
                    st.markdown(f'<div class="content-card" style="border-top:2px solid #22c55e;"><div style="font-family:Space Grotesk,sans-serif;font-size:.8rem;font-weight:700;color:#22c55e;margin-bottom:10px;">✅ Strengths</div><div class="skill-tags">{stags}</div></div>',unsafe_allow_html=True)
                with sc3:
                    gtags="".join(f'<span class="skill-tag" style="border-color:rgba(249,115,22,.3);color:#fdba74;">{g}</span>' for g in sc.get("gaps",[]))
                    st.markdown(f'<div class="content-card" style="border-top:2px solid #f97316;"><div style="font-family:Space Grotesk,sans-serif;font-size:.8rem;font-weight:700;color:#f97316;margin-bottom:10px;">🎯 Gaps</div><div class="skill-tags">{gtags}</div></div>',unsafe_allow_html=True)
                if sc.get("tip"):
                    st.markdown(f'<div style="background:rgba(79,142,247,.06);border:1px solid rgba(79,142,247,.2);border-radius:12px;padding:16px 20px;margin-top:14px;display:flex;gap:12px;align-items:flex-start;"><span style="font-size:1.1rem;">💡</span><span style="font-size:.875rem;color:#93c5fd;line-height:1.65;">{sc["tip"]}</span></div>',unsafe_allow_html=True)

    # REPORT
    with tabs[9]:
        st.markdown('<div class="sec-header"><div class="sec-dot"></div>Final Career Intelligence Report</div>', unsafe_allow_html=True)
        render_report(res["final_report"])
        st.markdown("<br>", unsafe_allow_html=True)
        d1,d2,_=st.columns([2,2,3])
        with d1:
            st.download_button("📥 Download TXT",data=res["final_report"],file_name=f"career_{goal.replace(' ','_').lower()}.txt",mime="text/plain",use_container_width=True)
        with d2:
            st.download_button("📦 Export JSON",data=json.dumps({k:str(v) for k,v in res.items()},indent=2),file_name=f"career_data_{goal.replace(' ','_').lower()}.json",mime="application/json",use_container_width=True)

# ─────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
  <div style="font-family:'Space Grotesk',sans-serif;font-size:.8rem;font-weight:700;color:#475569;letter-spacing:2px;">CAREER NAVIGATOR AI · EXECUTIVE DARK v4.0</div>
  <div style="margin-top:8px;"><span class="ai-badge">✨ AI powered by GPT-5 via OpenWebNinja</span></div>
  <div style="font-size:.7rem;color:#334155;margin-top:10px;letter-spacing:1px;">LangChain · OpenRouter · Tavily · OpenWebNinja · Plotly · Streamlit</div>
  <div style="font-size:.62rem;color:#1e293b;margin-top:6px;">© 2026 Career Navigator AI. All rights reserved.</div>
</div>""", unsafe_allow_html=True)
