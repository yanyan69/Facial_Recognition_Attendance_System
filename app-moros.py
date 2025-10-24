#python code na gawa ni yuan
from flask import Flask, request, jsonify
from ultralytics import YOLO
import cv2
import numpy as np
import datetime
import csv
import os

app = Flask(__name__)

# Load your trained YOLO model (trained on Yuan, Jerald, Yanyan)
model = YOLO("best.pt")  # make sure this is your custom trained model

# CSV log file
LOG_FILE = "attendance_log.csv"

# Ensure CSV file exists and has headers
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["name", "action", "timestamp"])

# Helper function to read uploaded image
def read_image_file(file):
    npimg = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    return img

# Helper function to log attendance to CSV
def log_to_csv(name, action, timestamp):
    with open(LOG_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, action, timestamp])

# Helper function to detect a face and return the predicted name
def detect_name(img):
    results = model.predict(img)
    for result in results:
        if len(result.boxes) > 0:
            # Use cls to get the correct predicted class index
            cls_idx = int(result.boxes.cls[0])
            detected_name = result.names[cls_idx]
            return detected_name
    return None

# Endpoint for Time In
@app.route("/timein", methods=["POST"])
def time_in():
    try:
        if 'file' not in request.files:
            return jsonify({"status": "fail", "message": "No file uploaded"})
        
        file = request.files['file']
        img = read_image_file(file)
        
        detected_name = detect_name(img)
        
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
            return jsonify({"status": "fail", "message": "No face detected"})
    except Exception as e:
        print("Error in /timein:", e)
        return jsonify({"status": "fail", "message": str(e)})

# Endpoint for Time Out
@app.route("/timeout", methods=["POST"])
def time_out():
    try:
        if 'file' not in request.files:
            return jsonify({"status": "fail", "message": "No file uploaded"})
        
        file = request.files['file']
        img = read_image_file(file)
        
        detected_name = detect_name(img)
        
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
            return jsonify({"status": "fail", "message": "No face detected"})
    except Exception as e:
        print("Error in /timeout:", e)
        return jsonify({"status": "fail", "message": str(e)})

if __name__ == "_main_":
    app.run(host="0.0.0.0", port=5000)