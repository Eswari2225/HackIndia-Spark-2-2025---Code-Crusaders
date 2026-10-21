import base64
import os
import smtplib
import threading
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import cv2
from flask import Flask, jsonify, render_template, request
import numpy as np
import requests
from ultralytics import YOLO

app = Flask(__name__)

# Load the pre-trained YOLOv8 model
model = YOLO("yolov8n.pt")

# Function to send email alerts in a separate background thread
def send_email_alert(subject, message):
    sender_email = "eswarigeetha2005@gmail.com"
    receiver_email = "aruldassdharsh@gmail.com"
    password = os.getenv("EMAIL_PASSWORD", "Eswari2005")

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

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/process_frame', methods=['POST'])
def process_frame():
    try:
        data = request.get_json()
        image_data = data['image'].split(',')[1]
        
        # Decode base64 image string to OpenCV image array
        nparr = np.frombuffer(base64.b64decode(image_data), np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Run inference using YOLO model
        results = model(frame)

        compliance_data = {
            "helmet": 0,
            "vest": 0,
            "mask": 0,
            "total_workers": 0
        }

        # Process detections
        for result in results:
            boxes = result.boxes
            for box in boxes:
                class_id = int(box.cls)
                label = model.names[class_id]
                confidence = float(box.conf)
                x1, y1, x2, y2 = map(int, box.xyxy[0])

                # Draw bounding box and detection text on the frame
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f"{label} {confidence:.2f}", (x1, max(y1 - 10, 20)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

                # Update compliance stats
                if label == "person":
                    compliance_data["total_workers"] += 1
                elif label == "helmet":
                    compliance_data["helmet"] += 1
                elif label == "vest":
                    compliance_data["vest"] += 1
                elif label == "mask":
                    compliance_data["mask"] += 1

        # Check for non-compliance and trigger email alert in a non-blocking background thread
        if compliance_data["total_workers"] > 0:
            if (compliance_data["helmet"] < compliance_data["total_workers"] or
                compliance_data["vest"] < compliance_data["total_workers"] or
                compliance_data["mask"] < compliance_data["total_workers"]):
                alert_message = "ALERT: Workers detected without proper PPE!"
                threading.Thread(target=send_email_alert, args=("PPE Compliance Alert", alert_message)).start()

        # Encode annotated image back to base64
        _, buffer = cv2.imencode('.jpg', frame)
        encoded_image = base64.b64encode(buffer).decode('utf-8')

        return jsonify({
            "processed_image": f"data:image/jpeg;base64,{encoded_image}",
            "compliance_data": compliance_data
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
