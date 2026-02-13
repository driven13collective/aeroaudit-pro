import reflex as rx
from .state import State


def index():
    return rx.center(
        rx.vstack(
            rx.heading("AeroAudit Pro", size="9", color="#00a3e0"),
            rx.text("Industrial Infrastructure AI Auditor", color="gray"),

            # The Upload Zone (Fixed to prevent New Tab bug)
            rx.upload(
                rx.vstack(
                    rx.button("Select Aramco Video", variant="soft", color_scheme="blue"),
                    rx.text("Drag & Drop footage here"),
                ),
                id="upload_video",
                border="2px dashed #333",
                padding="4em",
                border_radius="lg",
            ),

            # The Action Button
            rx.button(
                "Run AeroVision Audit",
                on_click=State.handle_upload(rx.upload_files(upload_id="upload_video")),
                loading=State.is_processing,
                size="4",
                width="100%",
            ),

            # Results Table
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("Entity"),
                        rx.table.column_header_cell("Detection"),
                        rx.table.column_header_cell("Confidence"),
                    )
                ),
                rx.table.body(
                    rx.foreach(
                        State.audit_data,
                        lambda x: rx.table.row(
                            rx.table.cell(x["brand"]),
                            rx.table.cell(x["item"]),
                            rx.table.cell(x["confidence"]),
                        ),
                    )
                ),
                width="100%",
            ),
            spacing="6",
            width="600px",
        ),
        padding_y="5em",
    )


app = rx.App()
app.add_page(index)