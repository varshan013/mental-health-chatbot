import os
from dotenv import load_dotenv
from pathlib import Path

# Load .env from project root
env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path)

# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

print("OPENAI_API_KEY:", OPENAI_API_KEY[:12] if OPENAI_API_KEY else "MISSING")

# Pinecone
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_HOST = os.getenv("PINECONE_HOST")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
PINECONE_NAMESPACE = "mental_docs"

# RAG
TOP_K = 5

# Safety
CRISIS_MESSAGE = (
    "I'm really sorry that you're feeling this way. "
    "I’m not able to help with that, but you’re not alone.\n\n"
    "If you’re in immediate danger, please contact your local emergency number.\n"
    "India: AASRA 24x7 Helpline — 91-9820466726\n"
    "You can also reach out to a trusted person right now."
)
