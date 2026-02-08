
from ultralytics import YOLO

def process_audit(image_path: str):
    model = YOLO("best.pt")
    results = model.predict(source=image_path, save=True, conf=0.5)
    output = []
    for result in results:
        boxes = result.boxes
        for box in boxes:
            class_id = int(box.cls[0])
            label = model.names[class_id]
            output.append(f"Detected: {label} with confidence {box.conf[0]:.2f}")
    # Find the saved image path
    result_img_path = image_path  # Or update if model.save=True changes path
    return "\n".join(output), result_img_path
