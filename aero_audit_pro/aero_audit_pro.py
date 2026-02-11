import reflex as rx
from .state import State  # Removed the dot to fix import errors

def index() -> rx.Component:
    return rx.cond(
        State.is_maintenance,
        rx.vstack(
            rx.heading("AeroAudit-Pro", size="9"),
            rx.text("🏎️ Our AI engine is currently being tuned for the next race."),
            rx.badge("Status: Under Maintenance", color_scheme="orange"),
            height="100vh", justify_content="center",
        ),
        rx.vstack(
            rx.heading("AeroAudit-Pro Dashboard"),
            rx.text("Welcome, Auditor. Upload your F1 footage below."),
            
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("Time"),
                        rx.table.column_header_cell("Brand"),
                        rx.table.column_header_cell("Confidence"),
                    ),
                ),
                rx.table.body(
                    rx.foreach(
                        State.audit_data,
                        lambda item: rx.table.row(
                            rx.table.cell(item["timestamp"]),
                            rx.table.cell(item["brand"]),
                            rx.table.cell(item["confidence"]),
                        ),
                    ),
                ),
                width="100%",
            ),
            rx.upload(
                rx.text("Drag and drop F1 footage or click to select"),
                id="upload1",
                border="1px dashed #ccc",
                padding="5em",
            ),
            rx.button(
                "Run Audit",
                on_click=State.handle_upload(rx.upload_files(upload_id="upload1")),
                loading=State.is_processing,
            ),
            rx.button("Export Verification Report (PDF)", color_scheme="green"),
            align="center",
            spacing="5",
        ),
    )

app = rx.App()
app.add_page(index)