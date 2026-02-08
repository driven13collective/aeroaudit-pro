import reflex as rx
import os

class State(rx.State):
    """The app state for AeroAudit-Pro."""
    is_processing: bool = False
    video_path: str = ""

    async def handle_upload(self, files: list[rx.UploadFile]):
        """Handle the F1 video upload and trigger YOLOv8."""
        self.is_processing = True
        yield
        # Save the video to the assets folder
        for file in files:
            upload_data = await file.read()
            outfile = f"assets/{file.filename}"
            with open(outfile, "wb") as f:
                f.write(upload_data)
            self.video_path = file.filename
        # This is where we will call your YOLOv8 model later
        # process_audit(self.video_path)
        self.is_processing = False

def index() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.heading("AeroAudit-Pro", size="9"),
            rx.text("F1 Sponsorship Verification Engine"),
            rx.upload(
                rx.text("Drag and drop F1 footage or click to select"),
                border="1px dashed #ccc",
                padding="5em",
            ),
            rx.button(
                "Run Audit",
                on_click=State.handle_upload(rx.upload_files()),
                loading=State.is_processing,
            ),
            align="center",
            spacing="5",
        ),
        height="100vh",
    )

app = rx.App()
app.add_page(index)
