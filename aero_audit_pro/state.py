import reflex as rx

class State(rx.State):
    # Base Vars (The "wires" the UI connects to)
    is_maintenance: bool = False
    is_processing: bool = False
    audit_data: list[dict] = []
    
    def handle_upload(self, files: list[rx.UploadFile]):
        """Handle the F1 footage upload and process via AI engine."""
        self.is_processing = True
        yield
        # This is where your AI logic would populate the list
        self.audit_data = [
            {"timestamp": "00:12", "brand": "Aramco", "confidence": "98%"},
            {"timestamp": "00:45", "brand": "Pirelli", "confidence": "94%"},
        ]
        self.is_processing = False