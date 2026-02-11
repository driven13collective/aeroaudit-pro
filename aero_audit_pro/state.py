import reflex as rx
from .notifier import send_audit_log

class State(rx.State):
    # If True, everyone sees the maintenance screen
    is_maintenance: bool = True

    # Tester identity and processing flag
    tester_id: str = "Guest Auditor"
    is_busy: bool = False

    def toggle_maintenance(self):
        self.is_maintenance = not self.is_maintenance

    @rx.event(background=True)
    async def process_f1_video(self):
        async with self:
            if self.is_busy:
                return rx.window_alert("Engine is busy. Please wait.")
            self.is_busy = True

        try:
            # --- AI Processing happens here ---
            # Replace this placeholder with your YOLOv8 / ultralytics inference
            found_count = 42  # Placeholder for actual detection count

            # --- Trigger the Auto-Log ---
            # Since this event runs in the background, calling the notifier directly is acceptable.
            send_audit_log(self.tester_id, found_count)

            return rx.window_alert(f"Audit complete. Found {found_count} logos.")
        except Exception as e:
            return rx.window_alert(f"Processing error: {e}")
        finally:
            async with self:
                self.is_busy = False
