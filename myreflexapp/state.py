
import reflex as rx
from auditor_core import process_audit

class State(rx.State):
    is_processing: bool = False
    audit_output: str = ""
    image_url: str = ""
    has_results: bool = False

    async def handle_upload(self, files: list[rx.UploadFile]):
        self.is_processing = True
        yield # Trigger UI update to show loading spinner
        # 1. Save file locally
        file = files[0]
        file_path = f"uploads/{file.name}"
        with open(file_path, "wb") as f:
            f.write(await file.read())
        # 2. Call your logic from auditor_core.py
        result_text, result_img_path = process_audit(file_path)
        self.audit_output = result_text
        self.image_url = result_img_path
        self.has_results = True
        self.is_processing = False
