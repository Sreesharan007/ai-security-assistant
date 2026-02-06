import streamlit as st
import random
import time
import matplotlib.pyplot as plt
from gtts import gTTS
import tempfile
import os

# =====================================================
# PAGE CONFIG (SAFE)
# =====================================================
st.set_page_config(
    page_title="AI Security App",
    page_icon="🛡️",
    layout="wide"
)

# =====================================================
# CUSTOM CSS (CLEAN UI)
# =====================================================
st.markdown("""
<style>
.card {
    padding: 18px;
    border-radius: 14px;
    background-color: white;
    box-shadow: 0 4px 14px rgba(0,0,0,0.08);
    margin-bottom: 12px;
}
.title {
    font-size: 28px;
    font-weight: 700;
}
.subtitle {
    color: gray;
}
.center {
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# SESSION STATE
# =====================================================
if "started" not in st.session_state:
    st.session_state.started = False
if "events" not in st.session_state:
    st.session_state.events = []
if "risk" not in st.session_state:
    st.session_state.risk = []
if "chat" not in st.session_state:
    st.session_state.chat = []

# =====================================================
# TEXT → SPEECH (SAFE)
# =====================================================
def speak(text):
    try:
        tts = gTTS(text=text, lang="en")
        audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(audio.name)
        st.audio(audio.name)
    except Exception:
        pass  # never crash app due to audio

# =====================================================
# SAFE LOGO DISPLAY
# =====================================================
def show_logo(size=120):
    if os.path.exists("app_icon.png"):
        st.image("app_icon.png", width=size)
    else:
        st.markdown("### 🛡️ AI Security App")

# =====================================================
# WELCOME SCREEN
# =====================================================
if not st.session_state.started:
    st.markdown("<br><br>", unsafe_allow_html=True)
    show_logo(140)

    st.markdown("<div class='title center'>AI Security App</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='subtitle center'>Real-time AI-powered threat detection</div>",
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🚀 Start Application"):
        st.session_state.started = True
        speak("Welcome to the AI Security Application")

    st.stop()

# =====================================================
# SIDEBAR
# =====================================================
with st.sidebar:
    show_logo(80)
    st.title("AI Security App")

    page = st.radio(
        "Navigate",
        ["Live Monitoring", "Risk Analysis", "Chat Assistant", "About"]
    )

# =====================================================
# EVENT GENERATOR
# =====================================================
def generate_event():
    return random.choice([
        "normal_activity",
        "login_failed",
        "high_traffic",
        "malware_process",
        "suspicious_file_write",
        "port_scan"
    ])

# =====================================================
# DETECTION & CLASSIFICATION
# =====================================================
def detect(events):
    if events.count("malware_process") >= 2:
        return "Malware Activity", 95, 3
    if events.count("suspicious_file_write") >= 3:
        return "Ransomware-like Activity", 97, 5
    if events.count("port_scan") >= 3:
        return "Port Scanning Attack", 80, 4
    if events.count("login_failed") >= 4:
        return "Brute Force Attack", 90, 1
    if events.count("high_traffic") >= 4:
        return "DDoS-like Attack", 85, 2
    return "Normal Activity", 10, 0

# =====================================================
# BOT RESPONSE
# =====================================================
def bot_reply(attack):
    responses = {
        "Malware Activity": "Malware detected. Disconnect network and run antivirus.",
        "Ransomware-like Activity": "Suspicious file encryption detected. Backup data immediately.",
        "Port Scanning Attack": "Port scanning detected. Block the suspicious IP.",
        "Brute Force Attack": "Multiple failed logins detected. Change password and enable 2FA.",
        "DDoS-like Attack": "Traffic spike detected. Enable firewall and rate limiting.",
        "Normal Activity": "System is operating normally."
    }
    return responses[attack]

# =====================================================
# LIVE MONITORING PAGE
# =====================================================
if page == "Live Monitoring":
    st.markdown("<div class='title'>Live Monitoring</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Real-time attack detection</div>", unsafe_allow_html=True)
    st.divider()

    col1, col2, col3 = st.columns(3)

    if st.button("▶ Start Monitoring"):
        for _ in range(12):
            event = generate_event()
            st.session_state.events.append(event)

            recent = st.session_state.events[-10:]
            attack, risk, label = detect(recent)
            st.session_state.risk.append(risk)

            with col1:
                st.markdown(f"<div class='card'><b>Status</b><br>{attack}</div>", unsafe_allow_html=True)
            with col2:
                st.markdown(f"<div class='card'><b>Risk</b><br>{risk}/100</div>", unsafe_allow_html=True)
            with col3:
                st.markdown(f"<div class='card'><b>Label</b><br>{label}</div>", unsafe_allow_html=True)

            message = bot_reply(attack)
            st.session_state.chat.append(("AI", message))
            speak(message)

            time.sleep(1)

# =====================================================
# RISK ANALYSIS PAGE
# =====================================================
elif page == "Risk Analysis":
    st.markdown("<div class='title'>Risk Analysis</div>", unsafe_allow_html=True)
    st.divider()

    if len(st.session_state.risk) > 1:
        fig, ax = plt.subplots()
        ax.plot(st.session_state.risk)
        ax.set_ylim(0, 100)
        ax.set_xlabel("Time")
        ax.set_ylabel("Risk Score")
        ax.grid(True)
        st.pyplot(fig)
    else:
        st.info("Start monitoring to see risk graph")

# =====================================================
# CHAT ASSISTANT PAGE
# =====================================================
elif page == "Chat Assistant":
    st.markdown("<div class='title'>AI Chat Assistant</div>", unsafe_allow_html=True)
    st.divider()

    user = st.text_input("Ask about attacks or system status")

    if user:
        st.session_state.chat.append(("You", user))

        if "malware" in user.lower():
            answer = "Malware is detected by abnormal process and file behavior."
        elif "label" in user.lower():
            answer = "Labels: 0-Normal, 1-Brute Force, 2-DDoS, 3-Malware, 4-Port Scan, 5-Ransomware."
        else:
            answer = "I am monitoring the system in real time."

        st.session_state.chat.append(("AI", answer))
        speak(answer)

    for sender, msg in st.session_state.chat[-6:]:
        if sender == "You":
            st.info(f"You: {msg}")
        else:
            st.success(f"AI: {msg}")

# =====================================================
# ABOUT PAGE
# =====================================================
elif page == "About":
    st.markdown("<div class='title'>About</div>", unsafe_allow_html=True)
    st.divider()
    st.write("""
    **AI Security App** is a real-time AI-based security monitoring system built entirely using **Streamlit**.

    **Features**
    - Live attack detection
    - Malware & advanced threat detection
    - Risk visualization
    - Chat & voice alerts
    - Cloud-ready deployment
    """)
