import cv2
import pandas as pd
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort

model = YOLO("runs/detect/train/weights/best.pt")
tracker = DeepSort(max_age=30)

cap = cv2.VideoCapture("race_video.mp4")

# Data structure to track logo events
logo_events = []
logo_names = {0: "Valvoline", 1: "Aramco"}
track_times = {}  # {track_id: {logo_name, start_frame, end_frame, confs}}
fps = cap.get(cv2.CAP_PROP_FPS) if cap.get(cv2.CAP_PROP_FPS) > 0 else 30
frame_num = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break
    frame_num += 1

    results = model(frame)[0]
    detections = []
    for r in results.boxes.data.tolist():
        x1, y1, x2, y2, conf, cls = r
        if conf > 0.3:
            detections.append([[x1, y1, x2-x1, y2-y1], conf, int(cls)])

    tracks = tracker.update_tracks(detections, frame=frame)
    for track in tracks:
        if not track.is_confirmed(): continue
        track_id = track.track_id
        ltrb = track.to_ltrb()
        # Find logo class for this track
        logo_cls = None
        conf = None
        for det in detections:
            if det[2] in logo_names:
                logo_cls = det[2]
                conf = det[1]
                break
        if logo_cls is not None:
            logo_name = logo_names[logo_cls]
            if track_id not in track_times:
                track_times[track_id] = {
                    "Logo_Name": logo_name,
                    "Start_Frame": frame_num,
                    "End_Frame": frame_num,
                    "Confs": [conf]
                }
            else:
                track_times[track_id]["End_Frame"] = frame_num
                track_times[track_id]["Confs"].append(conf)
        cv2.rectangle(frame, (int(ltrb[0]), int(ltrb[1])), (int(ltrb[2]), int(ltrb[3])), (0, 255, 0), 2)

    cv2.imshow("Commercial Audit", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()

# Export logo events to CSV
for track_id, info in track_times.items():
    start_time = info["Start_Frame"] / fps
    end_time = info["End_Frame"] / fps
    total_duration = end_time - start_time
    avg_conf = sum(info["Confs"]) / len(info["Confs"])
    logo_events.append({
        "Logo_Name": info["Logo_Name"],
        "Start_Time": start_time,
        "End_Time": end_time,
        "Total_Duration": total_duration,
        "Average_Confidence": avg_conf
    })

df = pd.DataFrame(logo_events)
df.to_csv("audit_report.csv", index=False)