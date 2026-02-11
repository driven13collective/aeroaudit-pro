import reflex as rx

config = rx.Config(
    app_name="aero_audit_pro",
    api_url="http://localhost:8000",
    # This line stops the warning message
    disable_plugins=['reflex.plugins.sitemap.SitemapPlugin'],
)