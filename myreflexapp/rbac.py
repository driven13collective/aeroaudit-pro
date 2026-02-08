# RBAC and Audit Logging for Reflex
import reflex as rx

class User(rx.Model, table=True):
    username: str
    role: str  # e.g., 'admin', 'technician'

class AuditEntry(rx.Model, table=True):
    action: str
    user: str


def audit_log(action: str, user_id: str):
    with rx.session() as session:
        session.add(AuditEntry(action=action, user=user_id))
        session.commit()
