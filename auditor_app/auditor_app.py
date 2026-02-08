import reflex as rx
from .state import State

def executive_view():
    return rx.vstack(
        rx.heading("Global Safety Insights", size="7"),
        rx.hstack(
            rx.stat(
                rx.stat_label("Compliance Rate"),
                rx.stat_number(f"{State.compliance_score}%"),
                rx.stat_help_text("↑ 2% from last month", color="green"),
            ),
            rx.stat(
                rx.stat_label("Total Audits"),
                rx.stat_number(State.total_audits),
            ),
            rx.stat(
                rx.stat_label("Active Anomalies"),
                rx.stat_number(State.anomalies_detected),
                rx.stat_help_text("Critical Priority", color="red"),
            ),
            width="100%",
            spacing="5",
        ),
        rx.recharts.area_chart(
            rx.recharts.area(data_key="safety", stroke="#8884d8", fill="#8884d8"),
            rx.recharts.x_axis(data_key="name"),
            rx.recharts.y_axis(),
            data=State.get_safety_data(),
            width="100%",
            height=300,
        ),
        padding="2em",
        bg="white",
        border_radius="xl",
        box_shadow="lg",
    )

def index() -> rx.Component:
    return rx.center(
        rx.vstack(
            executive_view(),
            rx.heading("Industrial Safety Auditor", size="9"),
            rx.text("Powered by YOLOv8 Enterprise Logic", color="gray"),
            rx.upload(
                rx.text("Drag & Drop Facility Images"),
                id="audit_images",
                border="2px dashed #2b6cb0",
                padding="5em",
            ),
            rx.button(
                "Run Compliance Audit",
                on_click=State.handle_audit(rx.upload_files(upload_id="audit_images")),
                loading=State.is_processing,
                width="100%",
                color_scheme="blue",
            ),
            rx.button(
                "Download PDF Report",
                on_click=State.generate_report,
                is_disabled=~State.has_results,
                width="100%",
                variant="outline",
                color_scheme="green",
                margin_top="1em"
            ),
            rx.divider(),
            rx.hstack(
                rx.image(src=State.output_image, width="300px"),
                rx.vstack(
                    rx.heading("Audit Trail Log", size="4"),
                    rx.foreach(State.audit_results, rx.text),
                    bg="#f7fafc",
                    padding="1em",
                    border_radius="lg",
                ),
                width="100%",
                spacing="5",
            ),
            width="80%",
            spacing="5",
        ),
        padding_top="5em",
        width="100%",
    )

app = rx.App()
app.add_page(index)
