
import reflex as rx
from .state import State  # State handles the AI logic

def index():
    return rx.container(
        rx.vstack(
            rx.heading("Enterprise AI Auditor", size="9", margin_bottom="1em"),
            rx.upload(
                rx.vstack(
                    rx.button("Select File", color_scheme="blue", variant="outline"),
                    rx.text("Drag and drop or click to upload"),
                ),
                id="upload_image",
                border="1px dashed #ccc",
                padding="2em",
            ),
            rx.button(
                "Run Audit", 
                on_click=State.handle_upload(rx.upload_files(upload_id="upload_image")),
                loading=State.is_processing, # Visual indicator for the user
                width="100%",
                color_scheme="blue"
            ),
            rx.divider(),
            # Results Section
            rx.cond(
                State.has_results,
                rx.vstack(
                    rx.text("Analysis Result:", font_weight="bold"),
                    rx.text(State.audit_output),
                    rx.image(src=State.image_url, width="400px")
                ),
                rx.text("No active audit results.", color="gray")
            ),
            spacing="5",
            align="center",
        ),
        padding_top="10vh",
    )

app = rx.App()
app.add_page(index)
