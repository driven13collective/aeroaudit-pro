from ultralytics import YOLO
import cv2

# 1. Load your custom weights
# Since it's in the same folder, just use the filename
model = YOLO("best.pt")

# 2. Run the model on an image or video
# Replace 'test_image.jpg' with your actual file path
results = model.predict(source="test_image.jpg", save=True, conf=0.5)

# 3. Print the results (the auditor part)
for result in results:
    boxes = result.boxes
    for box in boxes:
        # Get the class name (the objects you trained it to find)
        class_id = int(box.cls[0])
        label = model.names[class_id]
        print(f"Detected: {label} with confidence {box.conf[0]:.2f}")