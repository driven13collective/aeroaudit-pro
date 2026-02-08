from ultralytics import YOLO

# Load your model (update the path to your actual .pt file)
model = YOLO("best.pt")

# Run hyperparameter tuning
model.tune(
    data="data.yaml",
    epochs=30,
    iterations=10,
    use_ray=True,
    optimizer="AdamW",
    plots=True
)