<div align="center">

# 🤖 GraphMind AI Chatbot
### Agentic AI Chatbot built with LangGraph, LangChain & OpenAI

<p align="center">

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![LangGraph](https://img.shields.io/badge/LangGraph-1.2.0-purple?style=for-the-badge)
![LangChain](https://img.shields.io/badge/LangChain-1.2.1-green?style=for-the-badge)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-black?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Streamlit-Web_App-red?style=for-the-badge&logo=streamlit)

</p>

A production-style **Agentic AI Chatbot** powered by **LangGraph** featuring persistent conversations, streaming responses, thread management, and modern conversational UI.

---

</div>

# 📖 Overview

GraphMind AI Chatbot demonstrates how to build an intelligent conversational AI system using **LangGraph's graph-based architecture** instead of traditional linear chains.

Unlike standard chatbots, every conversation is represented as a workflow where state is preserved between interactions, making conversations persistent and resumable.

The project demonstrates modern Agentic AI concepts including:

- Stateful AI agents
- Persistent conversation memory
- Streaming responses
- Thread management
- Graph-based execution
- Production-ready Streamlit interface

---

# ✨ Features

✅ Agentic AI Architecture

✅ LangGraph Workflow

✅ Persistent Chat Memory

✅ Thread-Based Conversations

✅ Streaming Token Response

✅ Conversation History

✅ Modern Streamlit UI

✅ OpenAI Integration

✅ Clean Modular Codebase

---

# 🏗 Project Architecture

```
                     User

                      │
                      ▼

             Streamlit Frontend

                      │
                      ▼

          LangGraph Chat Workflow

                      │
          ┌───────────┴────────────┐
          │                        │
          ▼                        ▼

    Conversation State      Checkpointer

          │                        │
          └───────────┬────────────┘
                      ▼

                 OpenAI GPT

                      │
                      ▼

                AI Response
```

---

# 📂 Project Structure

```
GraphMind-AI-Chatbot/

│

├── app_chatbot.py
├── agentic_chatbot_backend.py
├── requirements.txt
├── .env
├── README.md

```

---

# ⚙ Technologies Used

| Technology | Purpose |
|------------|----------|
| Python | Programming Language |
| LangGraph | Agent Workflow Engine |
| LangChain | LLM Integration |
| OpenAI GPT | Language Model |
| Streamlit | Frontend UI |
| dotenv | Environment Variables |

---

# 🧠 LangGraph Workflow

```
          START

             │

             ▼

      Chat Node (LLM)

             │

             ▼

            END
```

The workflow maintains conversation state throughout the session while automatically preserving message history.

---

# 💾 Persistence

This project demonstrates LangGraph Persistence.

Every conversation is stored inside a thread.

```
Thread-1

User
↓

AI

↓

User

↓

AI

↓

Saved State
```

This enables:

- Resume conversations
- Stateful interactions
- Conversation history
- Memory across requests

---

# 🚀 Installation

## Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/GraphMind-AI-Chatbot.git

cd GraphMind-AI-Chatbot
```

---

## Create Environment

```bash
conda create -n langgraph-test python=3.11

conda activate langgraph-test
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Create .env

```
OPENAI_API_KEY=your_api_key
```

---

## Run Application

```bash
streamlit run app_chatbot.py
```

---

# 💬 Example Conversation

```
👤 User

Explain LangGraph Persistence.

🤖 AI

LangGraph Persistence automatically saves the
graph state after every execution so conversations
can resume from the last checkpoint.
```

---

# 🔄 Workflow Execution

```
User Input

      │

      ▼

State Update

      │

      ▼

LangGraph

      │

      ▼

OpenAI

      │

      ▼

Response Generation

      │

      ▼

Checkpoint Saved

      │

      ▼

Display Response
```

---

# 🎯 Learning Objectives

This project demonstrates:

- LangGraph Fundamentals
- Agentic AI
- Stateful Workflows
- Persistence
- Checkpointing
- Thread Management
- Streaming
- Chatbot UI Development
- OpenAI Integration

---

# 📦 Requirements

```
langgraph==1.2.0

langchain-openai==1.2.1

python-dotenv==1.2.2

pydantic==2.10.4

streamlit==1.58.0
```

---

# 🔮 Future Improvements

- Google Gemini Support
- Anthropic Claude Support
- SQLite Checkpointer
- PostgreSQL Checkpointer
- Authentication
- User Accounts
- Chat Export
- Voice Chat
- Image Upload
- File Upload
- RAG Integration
- Long-Term Memory
- Tool Calling
- Multi-Agent Collaboration

---

# 📸 Screenshots

```
Add screenshots here

/assets/home.png

/assets/chat.png

/assets/history.png
```

---

# 👨‍💻 Author

**Gouthum Kharvi**

AI Engineer | GenAI Developer | Machine Learning Enthusiast

GitHub

https://github.com/GouthumKharvi

LinkedIn

https://linkedin.com/in/Gouthum-Kharvi-2366a6219

Portfolio

https://gouthumkharvi.github.io/Datascience_Portfolio/

---

# ⭐ Support

If you found this project helpful,

⭐ Star the repository

🍴 Fork the repository

📢 Share it with others

---

<div align="center">

## Thank You ❤️

Made with Python, LangGraph and OpenAI

</div>
