import json, re
from app.services.rag import retrieve

# OLD:
# from langchain_openai import ChatOpenAI
# llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# NEW:
from langchain_community.chat_models import ChatOllama
llm = ChatOllama(model="llama3.1:8b", temperature=0)
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.


SYSTEM = """You are a LearnSmart support agent.
Answer ONLY using the retrieved company KB.
Always cite at least one Policy or FAQ ID when relevant (e.g., POL-REFUND-001, FAQ-BILL-001).
Be concise, polite, and provide clear next steps.
If no KB entry is relevant, say 'I will escalate this case to human support.'
"""

def draft_reply(subject: str, body: str):
    hits = retrieve(subject + "\n" + body, k=4)
    context = "\n\n---\n\n".join(d.page_content for d in hits)
    prompt = f"""{SYSTEM}

Retrieved context:
{context}

Ticket:
Subject: {subject}
Body: {body}

Return JSON with keys:
- reply (string)
- cited_ids (array of strings if any)
"""
    raw = llm.invoke(prompt).content
    try:
        data = json.loads(re.sub(r"```json|```", "", raw).strip())
    except Exception:
        data = {"reply": raw, "cited_ids": []}
    return data




