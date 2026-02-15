import os

import reflex as rx

# Detect if we are running on Railway or locally
host = os.environ.get("HOST", "0.0.0.0")
port = int(os.environ.get("PORT", "8000"))

# Prefer Railway's dynamic public domain, then API_URL, then a host/port fallback
public_domain = os.environ.get("RAILWAY_PUBLIC_DOMAIN")
api_url = os.environ.get("API_URL")
if public_domain:
    api_url = f"https://{public_domain}"
elif not api_url:
    api_url = f"http://{host}:{port}"

config = rx.Config(
    app_name="aeroaudit_pro",
    # Crucial for Railway: Bind to all interfaces (0.0.0.0)
    backend_port=port,
    backend_host=host,
    api_url=api_url,
    # Enable CORS for production
    cors_allowed_origins=["*"],
)