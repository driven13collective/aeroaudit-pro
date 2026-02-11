import reflex as rx
import os

# Lightning AI automatically assigns a unique URL to your Studio
# This code dynamically detects it so your link never breaks.
studio_id = os.getenv("LIGHTNING_CLOUDSPACE_ID", "default")
user_name = os.getenv("LIGHTNING_USER_NAME", "user")
base_url = f"{studio_id}.cloudspaces.litng.ai"

config = rx.Config(
    app_name="aero_audit_pro",
    # Port 8000 is the standard Reflex backend port
    api_url=f"https://8000-{base_url}",
    # Port 3000 is your website's public front door
    deploy_url=f"https://3000-{base_url}",
    db_url="sqlite:///reflex.db", # Enterprise Step 3: Local DB for audit logs
)