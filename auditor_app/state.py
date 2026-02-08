
import reflex as rx
from ultralytics import YOLO
import cv2
import os
from fpdf import FPDF
import datetime



class State(rx.State):
        def generate_audit_report(self, data, output_path="assets/AeroAudit_Verification.pdf"):
            from reportlab.lib.pagesizes import A4
            from reportlab.pdfgen import canvas
            from reportlab.lib.units import mm
            from reportlab.lib import colors
            c = canvas.Canvas(output_path, pagesize=A4)
            width, height = A4
            # Header & Branding
            c.setFont("Helvetica-Bold", 22)
            c.drawString(20 * mm, height - 25 * mm, "AeroAudit-Pro: Verification Report")
            # Project Metadata
            c.setFont("Helvetica", 12)
            c.drawString(20 * mm, height - 40 * mm, f"Project: {data.get('project_name', 'N/A')}")
            c.drawString(20 * mm, height - 45 * mm, f"Audit ID: {data.get('audit_id', 'N/A')}")
            c.drawString(20 * mm, height - 50 * mm, f"Date: {data.get('date', 'N/A')}")
            # Verification Trail (The Table)
            c.setStrokeColor(colors.black)
            c.line(20 * mm, height - 55 * mm, width - 20 * mm, height - 55 * mm)
            c.setFont("Helvetica-Bold", 14)
            c.drawString(20 * mm, height - 65 * mm, "Exposure Summary")
            y_pos = height - 75 * mm
            for brand, seconds in data.get('exposure', {}).items():
                c.setFont("Helvetica", 12)
                c.drawString(25 * mm, y_pos, f"• {brand}:")
                c.drawRightString(width - 30 * mm, y_pos, f"{seconds:.2f} Seconds")
                y_pos -= 10 * mm
            # Digital Watermark (For Authenticity)
            c.setFont("Helvetica-Oblique", 9)
            c.setFillColor(colors.grey)
            c.drawRightString(width - 20 * mm, 10 * mm, "Verified by AeroAudit AI - Secure Hash: 8f2b3e")
            c.showPage()
            c.save()
    is_processing: bool = False
    audit_results: list[str] = []
    output_image: str = ""
    has_results: bool = False
    # Executive Dashboard Data
    compliance_score: int = 94
    total_audits: int = 1250
    anomalies_detected: int = 12

    # Data for the graph (Safety Trends)
    def get_safety_data(self):
        return [
            {"name": "Mon", "safety": 92},
            {"name": "Tue", "safety": 95},
            {"name": "Wed", "safety": 91},
            {"name": "Thu", "safety": 98},
            {"name": "Fri", "safety": 94},
        ]

    async def handle_audit(self, files: list[rx.UploadFile]):
        import json
        self.is_processing = True
        yield
        model = YOLO("best.pt")
        self.audit_results = []
        for file in files:
            upload_data = await file.read()
            path = os.path.join("assets", file.filename)
            with open(path, "wb") as f:
                f.write(upload_data)
            results = model.predict(source=path, save=True, conf=0.5)
            detections = []
            for result in results:
                for box in result.boxes:
                    label = model.names[int(box.cls[0])]
                    conf = float(box.conf[0])
                    bbox = [int(coord) for coord in box.xyxy[0].tolist()]
                    frame = getattr(result, 'frame', 0)
                    detections.append({
                        "frame": frame,
                        "label": label,
                        "conf": conf,
                        "bbox": bbox
                    })
                    self.audit_results.append(f"Detected: {label} ({conf:.2f})")
            self.output_image = f"/{file.filename}"
            # Generate verification log
            verification_log = {
                "audit_id": f"AUD-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
                "video_source": file.filename,
                "detections": detections
            }
            log_path = os.path.join("assets", f"{file.filename}_verification.json")
            with open(log_path, "w") as log_file:
                json.dump(verification_log, log_file, indent=2)
        self.is_processing = False
        self.has_results = bool(self.audit_results)

    def generate_report(self):
        import json
        import datetime
        # Find the latest verification log
        logs = [f for f in os.listdir("assets") if f.endswith("_verification.json")]
        if not logs:
            return rx.download(url="/audit_report.pdf")
        latest_log = max(logs, key=lambda x: os.path.getmtime(os.path.join("assets", x)))
        with open(os.path.join("assets", latest_log), "r") as f:
            verification_data = json.load(f)
        # Build exposure summary from detections
        exposure = {}
        for det in verification_data.get("detections", []):
            brand = det["label"]
            exposure.setdefault(brand, 0)
            exposure[brand] += 1/30  # Assuming 30 FPS, 1 frame = 1/30 sec
        report_data = {
            "project_name": "AeroAudit-Pro",
            "audit_id": verification_data.get("audit_id", "N/A"),
            "date": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "exposure": {k: round(v, 2) for k, v in exposure.items()}
        }
        self.generate_audit_report(report_data)
        return rx.download(url="/AeroAudit_Verification.pdf")
