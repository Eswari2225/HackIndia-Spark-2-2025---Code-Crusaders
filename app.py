from flask import Flask, jsonify, render_template, Response
import cv2
from ultralytics import YOLO
import threading
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests

app = Flask(__name__)

# Load the pre-trained YOLOv8 model
model = YOLO("yolov8n.pt")  # Replace with your custom-trained model if available

# Global variable to store compliance data
compliance_data = {
    "helmet": 0,
    "vest": 0,
    "mask": 0,
    "total_workers": 0
}

# Function to send email alerts
def send_email_alert(subject, message):
    sender_email = "eswarigeetha2005@gmail.com"
    receiver_email = "aruldassdharsh@gmail.com"
    password = "Eswari2005"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("Email alert sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Function to send Telegram alerts
def send_telegram_alert(message):
    bot_token = "your_bot_token"
    chat_id = "your_chat_id"

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("Telegram alert sent successfully!")
        else:
            print(f"Failed to send Telegram alert: {response.text}")
    except Exception as e:
        print(f"Failed to send Telegram alert: {e}")

# Function to generate video frames
def generate_frames():
    cap = cv2.VideoCapture(0)  # Use 0 for webcam, or provide a video file path

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Perform object detection using YOLOv8
        results = model(frame)

        # Reset compliance data for each frame
        compliance_data = {
            "helmet": 0,
            "vest": 0,
            "mask": 0,
            "total_workers": 0
        }

        # Extract detection results
        for result in results:
            boxes = result.boxes
            for box in boxes:
                class_id = int(box.cls)
                label = model.names[class_id]

                # Update compliance data based on detected labels
                if label == "person":
                    compliance_data["total_workers"] += 1
                elif label == "helmet":
                    compliance_data["helmet"] += 1
                elif label == "vest":
                    compliance_data["vest"] += 1
                elif label == "mask":
                    compliance_data["mask"] += 1

        # Send alert if workers are not wearing PPE
        if compliance_data["total_workers"] > 0:
            if compliance_data["helmet"] < compliance_data["total_workers"] or \
               compliance_data["vest"] < compliance_data["total_workers"] or \
               compliance_data["mask"] < compliance_data["total_workers"]:
                alert_message = "ALERT: Workers detected without proper PPE!"
                send_email_alert("PPE Compliance Alert", alert_message)  # Use email
                # send_telegram_alert(alert_message)  # Use Telegram

        # Draw bounding boxes and labels on the frame
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            label = model.names[int(box.cls)]
            confidence = float(box.conf)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"{label} {confidence:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        # Convert the frame to JPEG format
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # Yield the frame in byte format
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()

# Route to stream video
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# API endpoint to get compliance data
@app.route('/compliance_data')
def get_compliance_data():
    return jsonify(compliance_data)

# Route to render the dashboard
@app.route('/')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)