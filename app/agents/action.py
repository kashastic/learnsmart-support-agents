# app/agents/action.py
from app.tools import crm

def act(ticket_id: str, category: str, reply: str):
    """
    Decide and trigger a simulated business action based on the
    ticket category and the drafted reply text.
    """
    text = (reply or "").lower()

    if category == "billing" and (
        "refund" in text or "duplicate" in text or "charged twice" in text
    ):
        return crm.refund(ticket_id)

    if category == "technical" and (
        "password" in text or "reset link" in text
    ):
        return crm.resend_reset(ticket_id)

    if category == "course_access" and (
        "unlock" in text or "access" in text or "cannot access" in text
    ):
        return crm.unlock_course(ticket_id)

    # default: we sent a response but no special action needed
    return crm.resolve(ticket_id, note="response sent")
