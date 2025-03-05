from flask import Flask, jsonify, render_template, Response
import cv2
from ultralytics import YOLO
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import threading
import math

app = Flask(__name__)


model = YOLO("ppee.pt")


classNames = [
    'Hardhat', 'Mask', 'NO-Hardhat', 'NO-Mask', 'NO-Safety Vest',
    'Person', 'Safety Cone', 'Safety Vest', 'machinery', 'vehicle'
]


compliance_history = []


def email_alert(subject, message):
    sender_email = "eswarigeetha2005@gmail.com"
    receiver_email = "nssibiya10062007@gmail.com"
    password = "adrsfovotqhetfqm"

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

def calculate_and_send_alert():
    while True:
        time.sleep(60)  

        if compliance_history:
            
            total_workers = sum(d["total_workers"] for d in compliance_history)
            total_helmet = sum(d["helmet"] for d in compliance_history)
            total_vest = sum(d["vest"] for d in compliance_history)
            total_mask = sum(d["mask"] for d in compliance_history)

           
            email_message = f"""
            PPE Compliance Report - Last 5 Minutes:
            --------------------------------------
            Total Workers: {total_workers}
            Total Wearing Helmets: {total_helmet}
            Total Wearing Vests: {total_vest}
            Total Wearing Masks: {total_mask}
            """

            
            email_alert("PPE Compliance Alert - 5-Minute Summary", email_message)

            
            compliance_history.clear()


threading.Thread(target=calculate_and_send_alert, daemon=True).start()

def generate_frames():
    cap = cv2.VideoCapture(0)  

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)

        compliance_data = {
            "helmet": 0,
            "vest": 0,
            "mask": 0,
            "total_workers": 0
        }

        for result in results:
            boxes = result.boxes
            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = math.ceil((box.conf[0] * 100)) / 100
                cls = int(box.cls[0])
                class_name = classNames[cls]

                if class_name == "Person":
                    compliance_data["total_workers"] += 1
                elif class_name == "Hardhat":
                    compliance_data["helmet"] += 1
                elif class_name == "Safety Vest":
                    compliance_data["vest"] += 1
                elif class_name == "Mask":
                    compliance_data["mask"] += 1

                if conf > 0.5:
                    if class_name in ['NO-Hardhat', 'NO-Safety Vest', 'NO-Mask']:
                        myColor = (0, 0, 255)  
                    elif class_name in ['Hardhat', 'Safety Vest', 'Mask']:
                        myColor = (0, 255, 0)  
                    else:
                        myColor = (255, 0, 0)  

                    cv2.rectangle(frame, (x1, y1), (x2, y2), myColor, 2)
                    label = f"{class_name} {conf:.2f}"
                    t_size = cv2.getTextSize(label, 0, fontScale=1, thickness=2)[0]
                    c2 = x1 + t_size[0], y1 - t_size[1] - 3
                    cv2.rectangle(frame, (x1, y1), c2, myColor, -1, cv2.LINE_AA)
                    cv2.putText(frame, label, (x1, y1 - 2), 0, 1, [255, 255, 255], thickness=1, lineType=cv2.LINE_AA)

        compliance_history.append(compliance_data)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/compliance_data')
def get_compliance_data():
    return jsonify(compliance_history[-1] if compliance_history else {})

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)