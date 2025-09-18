import json, re
from typing import List
from langchain_ollama import ChatOllama  # pip install -U langchain-ollama
from app.services.rag import retrieve

LLM = ChatOllama(model="llama3.1:8b", temperature=0)

SYSTEM = """You are a LearnSmart support agent.
Use ONLY the retrieved company KB to answer.
ALWAYS cite at least one KB ID when relevant (e.g., POL-REFUND-001, FAQ-BILL-001, FAQ-ACCESS-001).
If the KB does not contain the answer, say you will escalate to human support.
Return STRICT JSON with keys: reply (string), cited_ids (array of strings). No extra text.
"""

def _extract_ids(text: str) -> List[str]:
    ids = re.findall(r'\b(?:POL|FAQ|CRS)-[A-Z0-9\-]+', text)
    return sorted(set(ids))

def draft_reply(subject: str, body: str):
    hits = retrieve(subject + "\n" + body, k=4)
    context = "\n\n".join(h.page_content for h in hits)

    prompt = f"""{SYSTEM}

# Retrieved KB
{context}

# Ticket
Subject: {subject}
Body: {body}

Respond as JSON:
{{
  "reply": "... one-paragraph grounded answer with IDs in-line like (POL-REFUND-001) ...",
  "cited_ids": ["ID1","ID2"]
}}"""

    raw = LLM.invoke(prompt).content
    try:
        data = json.loads(re.sub(r"```json|```", "", raw).strip())
    except Exception:
        # fallback: salvage reply, synthesize IDs
        ids = _extract_ids(raw)
        data = {"reply": raw, "cited_ids": ids}
    # final safety: if no ids but the context had IDs, try to pull them
    if not data.get("cited_ids"):
        data["cited_ids"] = _extract_ids(context)
    return data
