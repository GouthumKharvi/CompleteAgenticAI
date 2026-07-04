<div align="center">

# 🤖 GraphMind
### ⚡ Agentic AI Chatbot powered by LangGraph + OpenRouter + Streamlit

<img src="assets/demo.gif" width="900"/>

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![LangGraph](https://img.shields.io/badge/LangGraph-Agentic%20AI-purple?style=for-the-badge)
![OpenRouter](https://img.shields.io/badge/OpenRouter-GPT--4o--Mini-green?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Streamlit-Web%20App-red?style=for-the-badge&logo=streamlit)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

</div>

---

# 🌟 Overview

GraphMind is an **Agentic AI Chatbot** built using **LangGraph**.

Unlike a traditional chatbot, GraphMind uses **graph-based execution**, **persistent conversation threads**, **streaming responses**, and **memory management** to provide an intelligent conversational experience similar to ChatGPT.

The application provides:

- 💬 Multi-thread conversations
- 🧠 Persistent memory
- ⚡ Live streaming responses
- 🔄 LangGraph workflow execution
- 🎨 Beautiful glassmorphism Streamlit UI
- 🚀 OpenRouter GPT-4o Mini integration

---

# 🎥 Demo

> Replace with your GIF

```
assets/demo.gif
```

---

# ✨ Features

## 🤖 Intelligent Chatbot

- Natural conversations
- GPT-4o Mini responses
- Context-aware replies

---

## 🧠 Persistent Memory

Each conversation gets its own Thread ID.

This allows the chatbot to remember previous messages.

```
Conversation A
    │
Thread ID A
    │
Memory A

Conversation B
    │
Thread ID B
    │
Memory B
```

---

## ⚡ Streaming Responses

Instead of waiting for the entire response...

```
Generating...

Hello...
How...
Are...
You...
Today...
```

Users receive responses token-by-token.

---

## 🔀 LangGraph Workflow

```
            START
               │
               ▼
        Chat Node (LLM)
               │
               ▼
              END
```

Workflow execution is handled by LangGraph.

---

## 💾 Memory Checkpointing

The chatbot uses

```
MemorySaver()
```

which stores conversation history for every thread.

---

## 🎨 Modern User Interface

Features include

- Glassmorphism
- Animated Background
- Floating Effects
- Sidebar Threads
- Beautiful Chat UI
- Responsive Design

---

# 🏗️ Project Structure

```
GraphMind
│
├── app_chatbot.py
├── agentic_chatbot_backend.py
├── requirements.txt
│
├── assets
│     ├── demo.gif
│     ├── architecture.png
│     └── ui.png
│
└── README.md
```

---

# ⚙️ Architecture

```
             User
               │
               ▼
        Streamlit Frontend
               │
               ▼
        LangGraph Workflow
               │
               ▼
         Chat Node (LLM)
               │
               ▼
      GPT-4o Mini (OpenRouter)
               │
               ▼
        AI Response
               │
               ▼
     MemorySaver Checkpoint
               │
               ▼
        Streamlit UI
```

---

# 🔄 Workflow

```
START

↓

User Message

↓

LangGraph State

↓

Chat Node

↓

GPT-4o Mini

↓

MemorySaver

↓

Stream Response

↓

END
```

---

# 🧠 State Definition

```python
class ChatState(TypedDict):

    messages: Annotated[
        list[BaseMessage],
        add_messages
    ]
```

The state stores the complete chat history for every thread.

---

# 💡 Technologies Used

| Technology | Purpose |
|------------|----------|
| Python | Backend |
| LangGraph | Workflow Engine |
| LangChain OpenAI | LLM Wrapper |
| OpenRouter | AI Model Provider |
| GPT-4o Mini | Language Model |
| Streamlit | Frontend |
| MemorySaver | Persistence |
| dotenv | Environment Variables |

---

# 📦 Installation

Clone repository

```bash
git clone https://github.com/yourusername/GraphMind.git
```

Move into project

```bash
cd GraphMind
```

Create environment

```bash
conda create -n graphmind python=3.11
```

Activate

```bash
conda activate graphmind
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a

```
.env
```

file

```env
OPENAI_API_KEY=your_openrouter_api_key
OPENAI_BASE_URL=https://openrouter.ai/api/v1
```

---

# ▶️ Run Backend

```bash
python agentic_chatbot_backend.py
```

---

# ▶️ Run Streamlit App

```bash
streamlit run app_chatbot.py
```

---

# 🖥️ User Interface

| Home | Chat |
|------|------|
| Modern Sidebar | Streaming Responses |
| Thread Management | Persistent Memory |
| Beautiful Animations | ChatGPT Style |

---

# 🧩 Conversation Threads

Each chat gets a unique Thread ID.

```
Thread 1

Hello

↓

Memory

↓

Next Message

↓

Previous Context Available
```

Another thread starts fresh.

```
Thread 2

Hello

↓

New Memory
```

---

# 🚀 Future Improvements

- Vector Database
- RAG
- Long-Term Memory
- Tool Calling
- Function Calling
- Image Generation
- Voice Chat
- Multi-Agent Support
- Authentication
- Database Persistence
- File Upload
- PDF Chat
- Internet Search

---

# 📊 Tech Stack

```
Frontend

Streamlit

↓

LangGraph

↓

OpenRouter

↓

GPT-4o Mini

↓

MemorySaver
```

---

# ⭐ Why LangGraph?

✔ Graph-based execution

✔ Persistent memory

✔ Streaming

✔ Agent workflows

✔ Thread management

✔ Human-in-the-loop support

✔ Production-ready architecture

---

# 🙌 Acknowledgements

- LangGraph
- LangChain
- OpenRouter
- Streamlit
- OpenAI

---

<div align="center">

### ⭐ If you like this project, don't forget to star the repository!

Made with ❤️ using LangGraph

</div>
