import reflex as rx

config = rx.Config(
    app_name="aero_audit_pro",
    api_url="http://localhost:8000",
    db_url="sqlite:///reflex.db", # Enterprise Step 3: Local DB for audit logs
)