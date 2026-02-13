import reflex as rx
import os
from ultralytics import YOLO


class State(rx.State):
    video_path: str = ""
    audit_data: list[dict] = []
    is_processing: bool = False

    async def handle_upload(self, files: list[rx.UploadFile]):
        self.is_processing = True
        yield

        upload_dir = rx.get_upload_dir()
        os.makedirs(upload_dir, exist_ok=True)

        for file in files:
            upload_data = await file.read()
            outfile = upload_dir / file.filename

            # 1. Save File
            with open(outfile, "wb") as f:
                f.write(upload_data)
            self.video_path = file.filename

            # 2. Trigger AeroVision Audit (Hooked to best.pt)
            await self.run_audit(str(outfile))

        self.is_processing = False

    async def run_audit(self, file_path: str):
        # This hooks the audit pipeline into the handler
        model_path = os.path.join("assets", "best.pt")
        model = YOLO(model_path)
        results = model(file_path)

        # 3. Repopulate audit_data
        self.audit_data = []
        for r in results:
            for box in r.boxes:
                self.audit_data.append(
                    {
                        "brand": "Aramco",
                        "confidence": f"{float(box.conf[0]):.2%}",
                        "item": model.names[int(box.cls[0])],
                    }
                )