# app/tools/crm.py
from datetime import datetime
LOG = []
def _log(entry): entry["ts"] = datetime.utcnow().isoformat(); LOG.append(entry); return entry
def refund(ticket_id, note="duplicate charge"): return _log({"ticket_id": ticket_id, "action": "refund_initiated", "note": note})
def resend_reset(ticket_id): return _log({"ticket_id": ticket_id, "action": "password_reset_sent"})
def unlock_course(ticket_id, course="unknown"): return _log({"ticket_id": ticket_id, "action": "course_unlocked", "course": course})
def resolve(ticket_id, note="response sent"): return _log({"ticket_id": ticket_id, "action": "resolved", "note": note})
def get_log(): return LOG
