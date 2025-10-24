Remote Access Face Recognition Attendance System
Overview
A web-based attendance system using YOLO for face detection, Flask for backend processing, and a web interface for live webcam feed and attendance logging.

Submitted By:
Moros, Julian Dave
Narvaez, Christian
Preclaro, Jerald James

Submitted To:
Engr. John Errol Mampusti

Setup:
Clone the Repository: 
git clone https://github.com/yanyan69/Facial_Recognition_Attendance_System.git
cd Facial_Recognition_Attendance_System

Set Up Virtual Environment:
Windows: setup.bat
macOS/Linux: ./setup.sh

Place YOLO Model:
Obtain best.pt (trained YOLO model) and place it in the project directory.

Activate Virtual Environment:
Windows: venv\Scripts\activate

Run the Web App:python app.py

Access the Interface:
Open http://127.0.0.1:5000 in a browser.

Update from GitHub
To pull updates:
git pull

Notes:
Ensure a webcam is connected to the server machine.
The best.pt model must be trained for face detection (contact team for access).
Do not run git push to avoid overwriting updates.
Dependencies: Flask, ultralytics, opencv-python, numpy, gunicorn (installed via requirements.txt).