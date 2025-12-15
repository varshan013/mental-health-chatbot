from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from app.schemas import ChatRequest, ChatResponse, SourceChunk
from app.safety import is_crisis, crisis_response
from app.rag_service import retrieve_context
from app.llm_service import generate_response

app = FastAPI(title="Mental Health Chatbot")

# Serve static files (JS, CSS)
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Serve frontend UI
@app.get("/")
def serve_frontend():
    return FileResponse("frontend/index.html")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    user_message = request.message
    history = request.history or []

    # 1️⃣ Safety check
    if is_crisis(user_message):
        return ChatResponse(
            reply=crisis_response(),
            sources=[]
        )

    # 2️⃣ RAG retrieval
    contexts, sources = retrieve_context(user_message)

    # 3️⃣ LLM generation
    reply = generate_response(
        user_message=user_message,
        context_chunks=contexts,
        history=history
    )

    return ChatResponse(
        reply=reply,
        sources=[SourceChunk(**src) for src in sources]
    )
