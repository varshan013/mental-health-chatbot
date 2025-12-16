# 🧠 Mental Health Chatbot (LLM + RAG)

An end to end Mental Health Chatbot built using Large Language Models (LLMs) with Retrieval Augmented Generation (RAG).  
The chatbot provides empathetic, grounded responses using curated mental-health resources, includes conversational memory, and is deployed live.

---

## 🚀 Features

- 💬 LLM-powered Chat
- 📚 RAG with Pinecone(context-aware answers from mental health resources)
- 🛡️ Safety Layer
  - Crisis detection
  - Supportive & non-harmful responses
- 🧠 Conversation Memory
- ⚡ FastAPI Backend
- 🌐 Simple Web UI
- ☁️ Deployed on Render
---

## 🏗️ Tech Stack

| Layer        | Technology |
|-------------|-----------|
| LLM         | OpenAI API |
| Vector DB   | Pinecone |
| Backend     | FastAPI |
| Frontend   | HTML, CSS, JavaScript |
| Deployment | Render |
| Language   | Python |

---

## 📂 Project Structure

mental-health-chatbot/
│
├── app/
│ ├── main.py # FastAPI app entry point
│ ├── config.py # Environment configuration
│ ├── llm_service.py # OpenAI interaction
│ ├── rag_service.py # Pinecone retrieval logic
│ ├── safety.py # Crisis & safety checks
│ └── schemas.py # Pydantic models
│
├── ingest/
│ └── ingest_texts.py # Text ingestion into Pinecone
│
├── data/
│ └── texts/ # Mental health knowledge files
│
├── frontend/
│ ├── index.html
│ └── script.js
│
├── requirements.txt
├── Dockerfile
├── README.md
└── .gitignore


---

## 🔄 How It Works

1. User sends a message via the Web UI
2. Relevant mental-health context is retrieved from Pinecone
3. Safety checks are applied
4. LLM generates a grounded, empathetic response
5. Conversation history is maintained for memory

---


## Deployment

Deployed using Render

Backend runs via:

uvicorn app.main:app --host 0.0.0.0 --port 10000


Environment variables managed securely via Render dashboard
