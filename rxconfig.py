import reflex as rx

config = rx.Config(
    app_name="aero_audit_pro",
    # 0.0.0.0 is required for Railway to find the app
    api_url="0.0.0.0:8000",
)