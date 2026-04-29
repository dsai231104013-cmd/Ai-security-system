from email.mime.base import MIMEBase
from email import encoders
import pywhatkit as kit
import time
import streamlit as st
import cv2
import numpy as np
from ultralytics import YOLO
from PIL import Image
import tempfile
import datetime
import pandas as pd
import os
import winsound
import matplotlib.pyplot as plt
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pickle


persons_count = 0
confidence_value = 0.0

# ---------------- LOGIN (JET BLACK CYBER THEME) ----------------

import streamlit as st

USER = "sawera maqsood"
PASS = "lilly112233#"

# 🎨 JET BLACK CYBER UI
st.markdown("""
<style>

/* Main background */
.stApp {
    background: radial-gradient(circle at top, #0a0a0a, #000000);
    color: #ffffff;
    font-family: "Arial";
}

/* Login container */
.login-box {
    background: rgba(255, 255, 255, 0.05);
    padding: 35px;
    border-radius: 18px;
    width: 380px;
    margin: auto;
    margin-top: 120px;
    box-shadow: 0px 0px 25px rgba(0, 255, 200, 0.15);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(0, 255, 200, 0.2);
}

/* Title */
.title {
    text-align: center;
    font-size: 28px;
    font-weight: bold;
    color: #00ffd5;
    margin-bottom: 20px;
    letter-spacing: 2px;
}

/* Input fields */
input {
    background-color: rgba(0,0,0,0.6) !important;
    color: white !important;
    border: 1px solid #00ffd5 !important;
    border-radius: 8px !important;
}

/* Button */
.stButton > button {
    width: 100%;
    background: linear-gradient(90deg, #00ffd5, #0066ff);
    color: black;
    font-weight: bold;
    border-radius: 8px;
    transition: 0.3s;
}

.stButton > button:hover {
    transform: scale(1.03);
    box-shadow: 0px 0px 15px #00ffd5;
}

</style>
""", unsafe_allow_html=True)

# ---------------- SESSION ----------------
if "login" not in st.session_state:
    st.session_state.login = False

# ---------------- LOGIN SCREEN ----------------
if not st.session_state.login:

    st.markdown("<div class='login-box'>", unsafe_allow_html=True)

    st.markdown("<div class='title'>🛡 AI SECURITY ACCESS</div>", unsafe_allow_html=True)

    u = st.text_input("USERNAME")
    p = st.text_input("PASSWORD", type="password")

    if st.button("LOGIN"):
        if u == USER and p == PASS:
            st.success("ACCESS GRANTED ✔")
            st.session_state.login = True
            st.rerun()
        else:
            st.error("ACCESS DENIED ❌")

    st.markdown("</div>", unsafe_allow_html=True)

    st.stop()
# ---------------- EMAIL (UPGRADED PROFESSIONAL ALERT SYSTEM) ----------------

EMAIL_SENDER = "starlightspark000@gmail.com"
EMAIL_PASSWORD = "mckg gxve fkvi rmsr"
EMAIL_RECEIVER = "sawraarana@gmail.com"

def send_email(msg_text, frame_path=None):
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER
        msg["Subject"] = "🚨 AI SECURITY ALERT - UNKNOWN PERSON DETECTED"

        body = f"""
AI Security System Alert 🚨

Status: UNKNOWN PERSON DETECTED
Time: {datetime.datetime.now()}

Details:
{msg_text}

⚠️ Please check your security system immediately.
"""
        msg.attach(MIMEText(body, "plain"))

        # 📎 ATTACH IMAGE (FIXED INDENTATION)
        if frame_path and os.path.exists(frame_path):
            with open(frame_path, "rb") as f:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(f.read())

            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename={os.path.basename(frame_path)}"
            )

            msg.attach(part)

        # SMTP SERVER
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()

    except Exception as e:
        print("Email error:", e)
# ---------------- ALERT CONTROL ----------------

last_alert_time = 0

def trigger_alert():
    global last_alert_time

    current_time = time.time()

    # 10 sec cooldown (no spam emails)
    if current_time - last_alert_time > 10:
        send_email("Unknown person detected in your system!")
        last_alert_time = current_time

# ---------------- WHATSAPP ----------------
def send_whatsapp():
    try:
        kit.sendwhatmsg_instantly(
            "+92XXXXXXXXXX",
            "🚨 ALERT: Unknown person detected in AI Security System!"
        )
    except:
        pass

# ---------------- UI (PROFESSIONAL DARK MODE) ----------------

st.set_page_config(page_title="AI Security Pro+", layout="wide")

st.markdown(
    """
    <style>
    /* Main background */
    .stApp {
        background-color: #000000;
        color: #ffffff;
    }

    /* Title styling */
    h1 {
        color: #00ffcc;
        text-align: center;
        font-size: 42px;
        font-weight: 800;
        letter-spacing: 2px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #0a0a0a;
    }

    /* Buttons */
    .stButton>button {
        background-color: #00ffcc;
        color: black;
        font-weight: bold;
        border-radius: 10px;
        padding: 10px;
        transition: 0.3s;
    }

    .stButton>button:hover {
        background-color: #00bfa6;
        color: white;
    }

    /* Input fields */
    input {
        background-color: #111111 !important;
        color: white !important;
        border: 1px solid #00ffcc !important;
    }

    /* Slider */
    .stSlider {
        color: #00ffcc;
    }

    /* File uploader */
    .stFileUploader {
        background-color: #111111;
        border-radius: 10px;
        padding: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

st.title("🛡️ AI SECURITY SYSTEM")
# ---------------- YOLO MODEL ----------------
@st.cache_resource
def load_model():
    return YOLO("yolov8n.pt")

model = load_model()

# ---------------- SETTINGS ----------------
conf = st.sidebar.slider("Confidence", 0.1, 1.0, 0.5)
alarm = st.sidebar.checkbox("🔔 Alarm", True)

mode = st.sidebar.radio("Mode", ["📷 Image", "🎥 Video", "📡 Live"])
# ---------------- FILES ----------------
log_file = "log.csv"
img_dir = "intruder_images"
face_dir = "faces"

last_alert_time = 0

os.makedirs(img_dir, exist_ok=True)
os.makedirs(face_dir, exist_ok=True)

if not os.path.exists(log_file):
    pd.DataFrame(columns=["Time", "Persons"]).to_csv(log_file, index=False)

# ---------------- ALARM ----------------
def beep():
    if alarm:
        try:
            for _ in range(5):
                winsound.Beep(2500, 300)
                winsound.Beep(1200, 300)
        except:
            pass
# ---------------- SAVE ----------------
def save_intruder(frame):
    filename = datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + ".jpg"
    path = os.path.join(img_dir, filename)
    cv2.imwrite(path, frame)
    return path
def update_analytics(p, c_list):
    global persons_count, confidence_value

    persons_count = p

    if len(c_list) > 0:
        confidence_value = (sum(c_list) / len(c_list)) * 100
    else:
        confidence_value = 0

# =====================================================
# FACE SYSTEM
# =====================================================

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

recognizer = cv2.face.LBPHFaceRecognizer_create()

model_file = "face_model.yml"
label_file = "labels.pkl"

if os.path.exists(model_file):
    recognizer.read(model_file)

if os.path.exists(label_file):
    with open(label_file, "rb") as f:
        labels = pickle.load(f)
else:
    labels = {}

def detect_faces(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    results = []

    for (x, y, w, h) in faces:
        roi = gray[y:y+h, x:x+w]

        name = "UNKNOWN"

        try:
            label, conf_val = recognizer.predict(roi)

            if conf_val < 60:
                name = labels.get(label, "KNOWN")
        except:
            pass

        results.append((x, y, w, h, name))

    return results

# ---------------- TRAIN ----------------
def train_model():
    faces = []
    ids = []
    label_map = {}
    id_counter = 0

    for person in os.listdir(face_dir):
        person_path = os.path.join(face_dir, person)

        label_map[id_counter] = person

        for img in os.listdir(person_path):
            img_path = os.path.join(person_path, img)
            gray = cv2.imread(img_path, 0)

            faces.append(gray)
            ids.append(id_counter)

        id_counter += 1

    if len(faces) > 0:
        recognizer.train(faces, np.array(ids))
        recognizer.save(model_file)

        with open(label_file, "wb") as f:
            pickle.dump(label_map, f)

# =====================================================
# IMAGE MODE
# =====================================================
if mode == "📷 Image":
    file = st.file_uploader("Upload Image")

    if file:
        img = np.array(Image.open(file))

        results = model(img, conf=conf)[0]

        persons = sum(1 for b in results.boxes
                      if model.names[int(b.cls[0])] == "person")

        confidences = [float(b.conf[0]) for b in results.boxes
                       if model.names[int(b.cls[0])] == "person"]

        update_analytics(persons, confidences)
        faces = detect_faces(img)

        for (x, y, w, h, name) in faces:
            color = (0,255,0) if name != "UNKNOWN" else (0,0,255)

            cv2.rectangle(img, (x,y), (x+w,y+h), color, 2)
            cv2.putText(img, name, (x,y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

            # ✅ FIXED ALERT BLOCK
            if name == "UNKNOWN":
                current_time = time.time()

                if current_time - last_alert_time > 10:
                    beep()
                    img_path = save_intruder(img)
                    send_email("UNKNOWN FACE DETECTED", img_path)
                    send_whatsapp()
                    last_alert_time = current_time

        st.image(img)

# =====================================================
# VIDEO MODE
elif mode == "🎥 Video":
    video_file = st.file_uploader("Upload Video", type=["mp4", "avi", "mov"])

    if video_file is not None:
        tfile = open("temp_video.mp4", "wb")
        tfile.write(video_file.read())

        cap = cv2.VideoCapture("temp_video.mp4")
        frame_box = st.image([])

        unknown_counter = 0   # ✅ OUTSIDE LOOP

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            faces = detect_faces(frame)

            results = model(frame, conf=conf)[0]

            persons = sum(1 for b in results.boxes
                          if model.names[int(b.cls[0])] == "person")

            confidences = [float(b.conf[0]) for b in results.boxes
                           if model.names[int(b.cls[0])] == "person"]

            for (x, y, w, h, name) in faces:
                color = (0,255,0) if name != "UNKNOWN" else (0,0,255)

                cv2.rectangle(frame, (x,y), (x+w,y+h), color, 2)
                cv2.putText(frame, name, (x,y-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

                # ✅ ONLY COUNT
                if name == "UNKNOWN":
                    unknown_counter += 1
                else:
                    unknown_counter = 0

            # ✅ ALERT LOGIC (OUTSIDE FOR LOOP)
            if unknown_counter >= 5:
                current_time = time.time()

                if current_time - last_alert_time > 10:
                    beep()
                    img_path = save_intruder(frame)
                    send_email("UNKNOWN FACE DETECTED", img_path)
                    send_whatsapp()
                    last_alert_time = current_time

                unknown_counter = 0

            frame_box.image(frame, channels="BGR")
            update_analytics(persons, confidences)

        cap.release()
# =====================================================
# LIVE MODE
# =====================================================
elif mode == "📡 Live":
    run = st.checkbox("Start Camera")
    cap = cv2.VideoCapture(0)

    frame_box = st.image([])
    unknown_counter = 0

    while run:
        ret, frame = cap.read()
        if not ret:
            break

        faces = detect_faces(frame)

        results = model(frame, conf=conf)[0]

        persons = sum(1 for b in results.boxes
                      if model.names[int(b.cls[0])] == "person")

        confidences = [float(b.conf[0]) for b in results.boxes
                       if model.names[int(b.cls[0])] == "person"]

        for (x, y, w, h, name) in faces:
            color = (0,255,0) if name != "UNKNOWN" else (0,0,255)

            cv2.rectangle(frame, (x,y), (x+w,y+h), color, 2)
            cv2.putText(frame, name, (x,y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

            # ✅ FIXED ALERT BLOCK
            if name == "UNKNOWN":
                unknown_counter += 1
            else:
                unknown_counter = 0
                # ✅ ALERT LOGIC (INSIDE WHILE, OUTSIDE FOR LOOP)
        if unknown_counter >= 5:
            current_time = time.time()

            if current_time - last_alert_time > 10:
                beep()
                img_path = save_intruder(frame)
                send_email("UNKNOWN FACE DETECTED", img_path)
                send_whatsapp()
                last_alert_time = current_time

            unknown_counter = 0

        frame_box.image(frame, channels="BGR")
        update_analytics(persons, confidences)

    cap.release()
# ---------------- SIDEBAR ----------------

st.sidebar.markdown("## 📊 LIVE ANALYTICS")

st.sidebar.markdown("### 👥 Persons Detected")
st.sidebar.success(str(persons_count))

st.sidebar.markdown("### 📊 Confidence Level")
st.sidebar.info(f"{confidence_value:.2f}%")

# ---------------- DASHBOARD ----------------
st.sidebar.subheader("📊 Analytics")

if st.sidebar.button("Show Graph"):
    df = pd.read_csv(log_file)
    plt.plot(df["Persons"])
    st.pyplot(plt)

# ---------------- GALLERY ----------------
st.sidebar.subheader("📸 Gallery")

if st.sidebar.button("Show Images"):
    for img in os.listdir(img_dir):
        st.image(os.path.join(img_dir, img))