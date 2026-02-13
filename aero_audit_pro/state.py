import reflex as rx
import os
import cv2
from ultralytics import YOLO

class State(rx.State):
    # Base Vars (The "wires" the UI connects to)
    is_maintenance: bool = False
    is_processing: bool = False
    audit_data: list[dict] = []
    # This keeps track of the video name
    video_path: str = ""
    
    async def handle_upload(self, files: list[rx.UploadFile]):
        """Handle the F1 footage upload and process via AI engine."""
        self.is_processing = True
        self.audit_data = []
        yield

        upload_dir = rx.get_upload_dir()
        os.makedirs(upload_dir, exist_ok=True)

        def format_timestamp(total_seconds: float) -> str:
            minutes = int(total_seconds // 60)
            seconds = int(total_seconds % 60)
            return f"{minutes:02d}:{seconds:02d}"

        model = YOLO("best.pt")

        for file in files:
            upload_data = await file.read()
            outfile = upload_dir / file.filename

            # Save the file to your computer's temporary folder
            with open(outfile, "wb") as f:
                f.write(upload_data)

            # Update the path so the app knows where the video is
            self.video_path = file.filename

            # This is where you'd trigger your AeroVision (best.pt) audit
            print(f"Audit starting for: {self.video_path}")

            fps = 30.0
            cap = cv2.VideoCapture(str(outfile))
            if cap.isOpened():
                detected_fps = cap.get(cv2.CAP_PROP_FPS)
                if detected_fps and detected_fps > 0:
                    fps = detected_fps
            cap.release()

            results = model.predict(source=str(outfile), save=True, conf=0.5)
            for result in results:
                frame_idx = getattr(result, "frame", None)
                timestamp = "00:00"
                if frame_idx is not None:
                    timestamp = format_timestamp(frame_idx / fps if fps else 0)
                for box in result.boxes:
                    label = model.names[int(box.cls[0])]
                    conf = float(box.conf[0])
                    self.audit_data.append(
                        {
                            "timestamp": timestamp,
                            "brand": label,
                            "confidence": f"{conf * 100:.1f}%",
                        }
                    )

        self.is_processing = False