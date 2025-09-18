import json, re
from langchain_ollama import ChatOllama  # pip install -U langchain-ollama

LLM = ChatOllama(model="llama3.1:8b", temperature=0)

REQUIRES_CITATION = {"billing", "certificate", "technical", "course_access"}  # "other" can pass without
ID_PATTERN = re.compile(r'\b(?:POL|FAQ|CRS)-[A-Z0-9\-]+\b')

def _polite_and_safe(reply: str) -> bool:
    # quick cheap checks; keep it simple
    bad = ["idiot", "shut up", "stupid", "lawsuit", "guarantee beyond policy"]
    r = reply.lower()
    return not any(b in r for b in bad)

def supervise(category: str, reply: str) -> dict:
    # 1) rule check: citations when needed
    has_id = bool(ID_PATTERN.search(reply or ""))
    if category in REQUIRES_CITATION and not has_id:
        return {"approve": False, "reason": "Missing KB citation (FAQ-*/POL-*)."}

    # 2) rule check: basic tone
    if not _polite_and_safe(reply or ""):
        return {"approve": False, "reason": "Tone/safety issue."}

    # 3) brief LLM QA (optional, but keeps you safe)
    qa_prompt = """Approve if the reply is concise, polite, fact-focused, and does not contradict typical edtech policies.
Respond JSON only: {"approve": true/false, "reason": "..."}"""
    raw = LLM.invoke(f"{qa_prompt}\n\nReply:\n{reply}\n").content
    try:
        j = json.loads(re.sub(r"```json|```", "", raw).strip())
        if isinstance(j.get("approve"), bool):
            return j
    except Exception:
        pass
    return {"approve": True, "reason": "Rule checks passed"}
