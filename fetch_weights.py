from inference import get_model
import numpy as np

# Use your specific project ID and version
model = get_model(model_id="mc1620-model-auditor/1", api_key="XnTd9tDTeh9KtywM73E9")

# Run one "fake" prediction to force the download
dummy_image = np.zeros((640, 640, 3), dtype=np.uint8)
model.infer(dummy_image)

print("Weights are now downloaded and cached locally!")
