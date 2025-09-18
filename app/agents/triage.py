from langchain_ollama import ChatOllama  # pip install -U langchain-ollama

CATS = ["billing", "course_access", "technical", "certificate", "other"]
LLM = ChatOllama(model="llama3.1:8b", temperature=0)

SYSTEM = """Classify the LearnSmart support ticket into EXACTLY one of:
billing | course_access | technical | certificate | other.
Output only the label."""

FEWSHOTS = """
Examples:
Q: "Charged twice for bootcamp"
A: billing
Q: "Can't access purchased Python course"
A: course_access
Q: "Reset link expired"
A: technical
Q: "No certificate after completion"
A: certificate
Q: "Do you offer student discounts?"
A: other
"""

def triage(subject: str, body: str) -> str:
    prompt = f"{SYSTEM}\n{FEWSHOTS}\n\nSubject: {subject}\nBody: {body}\nA:"
    out = (LLM.invoke(prompt).content or "").strip().lower()
    return out if out in CATS else "other"
