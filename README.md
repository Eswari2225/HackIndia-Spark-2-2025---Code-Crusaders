# 🦺 Guardian Eyes — AI-Powered Safety Monitoring System

\<div align="center">



\


**AI-powered safety monitoring using computer vision and object detection.**

[View Repository](https://github.com/Eswari2225/HackIndia-Spark-2-2025---Code-Crusaders)

\</div>

---

## 📌 About the Project

**Guardian Eyes** is a computer vision project developed by Team Code Crusaders for HackIndia Spark 2 – 2025.

The project aims to support safety monitoring by using the YOLOv8 object detection model to analyze visual input and identify safety-related conditions. The application includes a Python backend, a web dashboard, and an alert module.

## 🎯 Problem Statement

Monitoring safety compliance manually can be time-consuming and difficult in environments where protective equipment is required.

Guardian Eyes explores how computer vision can assist in detecting safety-related violations and help improve monitoring efficiency.

## 💡 Proposed Solution

The system combines object detection with a web-based interface to present detection results and support alerts for identified violations.

## ✨ Key Features

- 🤖 **AI-Based Detection:** Uses the YOLOv8 model for object detection.
- 🦺 **Safety Monitoring:** Designed for safety-equipment monitoring, such as helmet detection, depending on the implemented model classes.
- 🌐 **Web Dashboard:** Provides a browser-based interface using HTML templates.
- 🚨 **Alert Module:** Includes Python alert functionality for safety-related events.
- 🖼️ **Detection Outputs:** Includes sample output images showing project results.
- ⚙️ **Python Backend:** Organizes application functionality through Python scripts.

## 🛠️ Tech Stack

- **Programming Language:** Python
- **Computer Vision:** YOLOv8, Ultralytics
- **Web Framework:** Flask, if used by `app.py`
- **Frontend:** HTML, JavaScript, JSON
- **Model Weights:** `yolov8n.pt`
- **Dependency Management:** pip and `requirements.txt`

## 📂 Project Structure

```text
HackIndia-Spark-2-2025---Code-Crusaders/
│
├── templates/
│   ├── dashboard.html
│   ├── js.js
│   └── json.json
│
├── GE output.png
├── GE2output.png
├── GE3.png
│
├── alert.py
├── app.py
├── sample.py
├── requirements.txt
├── yolov8n.pt
└── README.md
```

### 📄 File Descriptions

| File                       | Description                         |
| -------------------------- | ----------------------------------- |
| `app.py`                   | Main Python application entry point |
| `alert.py`                 | Alert-related functionality         |
| `sample.py`                | Sample or testing script            |
| `requirements.txt`         | Python dependencies                 |
| `yolov8n.pt`               | YOLOv8 nano model weights           |
| `templates/dashboard.html` | Dashboard interface                 |
| `templates/js.js`          | JavaScript functionality            |
| `templates/json.json`      | JSON data or configuration          |
| `GE output.png`            | Sample project output               |
| `GE2output.png`            | Additional output image             |
| `GE3.png`                  | Additional project image            |

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Eswari2225/HackIndia-Spark-2-2025---Code-Crusaders.git
```

### 2. Navigate to the project directory

```bash
cd HackIndia-Spark-2-2025---Code-Crusaders
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

**Windows**

```bash
venv\Scripts\activate
```

**macOS / Linux**

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

If the Ultralytics package is not included in your requirements, install it with:

```bash
pip install ultralytics
```

### 5. Run the application

```bash
python app.py
```

If `app.py` starts a Flask development server, open the local URL displayed in the terminal, commonly:

```text
http://127.0.0.1:5000/
```

*The exact setup and launch commands depend on how the application is implemented.*

## 🚀 Future Enhancements

- Improve detection accuracy in different lighting conditions.
- Expand safety-equipment detection capabilities.
- Improve alert delivery and event logging.
- Enhance the dashboard with detection statistics.
- Evaluate real-time monitoring and deployment options.

## 👥 Team

**Team Code Crusaders**
HackIndia Spark 2 – 2025

Update this section with the names and roles of all team members.

## 🏆 Hackathon Project

Developed as part of **HackIndia Spark 2 – 2025**, this project explores the use of artificial intelligence and computer vision to support safety monitoring.

## 🤝 Contributing

Contributions and suggestions are welcome.

1. Fork this repository.
2. Create a feature branch.
3. Commit your changes.
4. Open a pull request.

---

\<div align="center">

**Built with Python, AI, and teamwork. 💙**

⭐ If you find this project interesting, consider starring the repository!

\</div>
