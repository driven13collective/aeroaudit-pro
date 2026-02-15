import threading

import reflex as rx
from ultralytics import YOLO  # If this is Line 2, the error is likely the OpenCV/libxcb issue again
import os

# 1. Global placeholder for the model
model = None


def load_model_background() -> None:
    """Load YOLO in a background thread so the server doesn't time out."""
    global model
    print("AI Engine: Starting model load...")
    model = YOLO("assets/best.pt")
    print("AI Engine: Ready for audits.")


# Start the background loader
threading.Thread(target=load_model_background, daemon=True).start()


class State(rx.State):
    audit_data: list[dict] = []
    is_processing: bool = False

    @rx.var
    def model_status(self) -> str:
        return "System Online" if model is not None else "AI Engine Loading..."

    async def handle_upload(self, files: list[rx.UploadFile]):
        self.is_processing = True
        self.audit_data = []

        if model is None:
            self.is_processing = False
            return

        for file in files:
            upload_data = await file.read()
            outfile = rx.get_upload_dir() / file.filename

            with open(outfile, "wb") as f:
                f.write(upload_data)

            results = model(str(outfile))

            for r in results:
                for box in r.boxes:
                    self.audit_data.append(
                        {
                            "brand": "Aramco",
                            "item": model.names[int(box.cls[0])],
                            "confidence": f"{float(box.conf[0]):.2%}",
                        }
                    )

        self.is_processing = False


def index():
    return rx.center(
        rx.vstack(
            rx.heading("AeroAudit Pro", size="9", color="#00a3e0"),
            rx.text("Industrial Infrastructure AI Auditor", color="gray"),
            rx.text(f"Status: {State.model_status}"),
            rx.upload(
                rx.vstack(
                    rx.button("Select Aramco Video", variant="soft"),
                    rx.text("Drag & Drop footage here"),
                ),
                id="upload_video",
                border="2px dashed #333",
                padding="4em",
            ),
            rx.button(
                "Run AeroVision Audit",
                on_click=State.handle_upload(rx.upload_files(upload_id="upload_video")),
                loading=State.is_processing,
                width="100%",
            ),
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


# 2. Add a dedicated Health Check Page for Railway
def health():
    return rx.text("Alive")


app = rx.App()
app.add_page(index)
app.add_page(health, route="/health")
