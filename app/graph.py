import pandas as pd
from app.agents.triage import triage
from app.agents.solution import draft_reply
from app.agents.supervisor import supervise
from app.agents.action import act

def process_ticket(ticket: dict):
    cat = triage(ticket["subject"], ticket["body"])
    sol = draft_reply(ticket["subject"], ticket["body"])
    reply = sol.get("reply", "")
    qa = supervise(cat, reply)
    if not qa.get("approve", False):
        return {"id": ticket.get("id"), "status": "escalated", "category": cat, "reason": qa.get("reason", "uncertain")}
    action = act(str(ticket.get("id")), cat, reply)
    return {"id": ticket.get("id"), "status": "resolved", "category": cat, "reply": reply, "action": action}

def run_csv(path: str = "app/data/tickets_seed.csv"):
    df = pd.read_csv(path)
    return [process_ticket(row.to_dict()) for _, row in df.iterrows()]
