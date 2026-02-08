import reflex as rx

config = rx.Config(
    app_name="auditor_app",
    db_url="sqlite:///reflex.db", # Enterprise Step 3: Local DB for audit logs
)