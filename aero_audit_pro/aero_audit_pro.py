import reflex as rx
from .state import State


def index() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.heading("AeroAudit Pro", size="9"),
            rx.text("Industrial AI Auditor for Aramco Infrastructure"),

            # Upload Zone
            rx.upload(
                rx.vstack(
                    rx.button("Select Video", color_scheme="blue"),
                    rx.text("Drag Aramco footage here"),
                ),
                id="upload_video",
                border="2px dashed #333",
                padding="3em",
            ),

            # Audit Button
            rx.button(
                "Run AeroVision Audit",
                on_click=State.handle_upload(
                    rx.upload_files(upload_id="upload_video")
                ),
                loading=State.is_processing,
                width="100%",
            ),

            # Results Table
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("Brand"),
                        rx.table.column_header_cell("Item"),
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
            spacing="5",
        ),
        padding_top="10%",
    )

app = rx.App()
app.add_page(index)