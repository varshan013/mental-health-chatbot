from openai import OpenAI
from app.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

MAX_HISTORY = 6

SYSTEM_PROMPT = """
You are a supportive mental health assistant.
Your role is to provide empathetic, non-judgmental emotional support.

Rules:
- Do NOT diagnose medical or mental conditions
- Do NOT suggest medication
- Do NOT encourage harmful behavior
- If the user sounds distressed, respond calmly and empathetically
- Encourage healthy coping strategies
- Gently suggest professional help when appropriate
"""

def generate_response(user_message: str, context_chunks: list, history: list):
    context_text = "\n\n".join(context_chunks)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

    # Add conversation history
    for msg in history[-MAX_HISTORY:]:
        messages.append({
            "role": msg.role,
            "content": msg.content
        })


    # Inject RAG context
    messages.append({
        "role": "system",
        "content": f"Relevant information:\n{context_text}"
    })

    messages.append({
        "role": "user",
        "content": user_message
    })

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.7
    )

    return response.choices[0].message.content
