from flask import Flask, request, jsonify, render_template, Response
from ultralytics import YOLO
import cv2, csv, os, datetime
import numpy as np

# Flask config → look inside 'templates' and 'static'
app = Flask(__name__, template_folder="templates", static_folder="static")

# Load your trained YOLO model (trained on Yuan, Jerald, Yanyan)
model = YOLO("yolov8n.pt")  # make sure this is your custom trained model

# CSV log file
LOG_FILE = "attendance_log.csv"

# Insert after LOG_FILE setup
latest_detected_name = None

# Ensure CSV file exists and has headers
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["name", "action", "timestamp"])

# Helper function to log attendance to CSV
def log_to_csv(name, action, timestamp):
    with open(LOG_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, action, timestamp])

# Home route
@app.route("/")
def home():
    return render_template("index.html")

# Endpoint for Time In
@app.route("/timein", methods=["POST"])
def time_in():
    try:
        global latest_detected_name
        detected_name = latest_detected_name
        
        if detected_name:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_to_csv(detected_name, "time_in", timestamp)
            return jsonify({
                "status": "success",
                "name": detected_name,
                "action": "time_in",
                "time": timestamp
            })
        else:
            return jsonify({"status": "fail", "message": "No face detected in live feed"})
    except Exception as e:
        print("Error in /timein:", e)
        return jsonify({"status": "fail", "message": str(e)})

# Endpoint for Time Out
@app.route("/timeout", methods=["POST"])
def time_out():
    try:
        global latest_detected_name
        detected_name = latest_detected_name
        
        if detected_name:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_to_csv(detected_name, "time_out", timestamp)
            return jsonify({
                "status": "success",
                "name": detected_name,
                "action": "time_out",
                "time": timestamp
            })
        else:
            return jsonify({"status": "fail", "message": "No face detected in live feed"})
    except Exception as e:
        print("Error in /timeout:", e)
        return jsonify({"status": "fail", "message": str(e)})

# Live camera feed generator
def generate_frames():
    global latest_detected_name
    cap = cv2.VideoCapture(0)  # use default webcam (change index if needed)
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            results = model(frame)  # run YOLO
            for r in results:
                frame = r.plot()  # draw bounding boxes
                if len(r.boxes) > 0:
                    cls_idx = int(r.boxes.cls[0])  # predicted class index
                    latest_detected_name = r.names[cls_idx]
                    break  # Assume first detection
            else:
                latest_detected_name = None

            # Encode frame as JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # Yield frame in byte format for streaming
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Route for live video feed
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# Run app once
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)