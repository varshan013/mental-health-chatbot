import re
from app.config import CRISIS_MESSAGE

# Simple but effective keyword-based detection
CRISIS_PATTERNS = [
    r"\bkill myself\b",
    r"\bwant to die\b",
    r"\bend my life\b",
    r"\bsuicide\b",
    r"\bself harm\b",
    r"\bhurt myself\b",
    r"\bno reason to live\b",
]

def is_crisis(message: str) -> bool:
    msg = message.lower()
    return any(re.search(pattern, msg) for pattern in CRISIS_PATTERNS)


def crisis_response() -> str:
    return CRISIS_MESSAGE
