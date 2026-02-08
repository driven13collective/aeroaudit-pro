import streamlit as st
import cv2
import tempfile
import supervision as sv
from inference import get_model

# Load model (same as before)
model = get_model(model_id="mc1620-model-auditor/1", api_key="YOUR_API_KEY")

st.title("Sponsorship Video Auditor")
video_file = st.file_uploader("Upload Race Footage", type=["mp4", "mov", "avi"])

if video_file:
    # 1. Save uploaded video to a temporary file for OpenCV to read
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(video_file.read())

    # 2. Setup video tools
    video_info = sv.VideoInfo.from_video_path(tfile.name)
    frame_generator = sv.get_video_frames_generator(source_path=tfile.name)
    fps = video_info.fps

    # 3. Create a placeholder for the live video feed
    frame_window = st.empty()
    counter_window = st.empty()

    # 4. Initialize logo frame counters
    valvoline_frames = 0
    total_frames = 0

    # 5. Loop through every frame
    for frame in frame_generator:
        # Run Audit (Inference)
        results = model.infer(frame, confidence=0.2)[0]
        detections = sv.Detections.from_inference(results)

        # Draw boxes and labels
        box_annotator = sv.BoxAnnotator()
        annotated_frame = box_annotator.annotate(scene=frame, detections=detections)

        # Count Valvoline logo appearances
        if "Valvoline" in [p.class_name for p in results.predictions]:
            valvoline_frames += 1
        total_frames += 1

        # Display the frame in Streamlit
        frame_window.image(annotated_frame, channels="BGR")

        # Display live counter
        exposure_seconds = valvoline_frames / fps if fps else 0
        counter_window.markdown(f"**Valvoline Frames:** {valvoline_frames}  ")
        counter_window.markdown(f"**Exposure Seconds:** {exposure_seconds:.2f} s")
