import reflex as rx
import os
from ultralytics import YOLO


class State(rx.State):
    video_path: str = ""
    audit_data: list[dict] = []
    is_processing: bool = False

    async def handle_upload(self, files: list[rx.UploadFile]):
        self.is_processing = True
        self.audit_data = []

        for file in files:
            upload_data = await file.read()
            # Save to the specific Reflex upload directory
            outfile = rx.get_upload_dir() / file.filename

            with open(outfile, "wb") as f:
                f.write(upload_data)

            self.video_path = file.filename

            # Run the YOLO Model
            await self.run_aero_audit(str(outfile))

        self.is_processing = False

    async def run_aero_audit(self, file_path: str):
        # Load model from assets
        model = YOLO("assets/best.pt")
        results = model(file_path)

        for r in results:
            for box in r.boxes:
                self.audit_data.append(
                    {
                        "brand": "Aramco",
                        "item": model.names[int(box.cls[0])],
                        "confidence": f"{float(box.conf[0]):.2%}",
                    }
                )