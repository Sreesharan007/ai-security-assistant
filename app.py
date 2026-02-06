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
# BASIC STYLING
# =====================================================
st.markdown("""
<style>
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
# TEXT TO SPEECH (SAFE)
# =====================================================
def speak(text):
    try:
        tts = gTTS(text=text, lang="en")
        audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(audio.name)
        st.audio(audio.name)
    except Exception:
        pass

# =====================================================
# WELCOME SCREEN
# =====================================================
if not st.session_state.started:
    st.markdown("<br><br>", unsafe_allow_html=True)

    if os.path.exists("app_icon.png"):
        st.image("app_icon.png", width=120)
    else:
        st.markdown("## 🛡️ AI Security App")

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
# SIDEBAR NAVIGATION
# =====================================================
st.sidebar.title("🛡️ AI Security App")

page = st.sidebar.radio(
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
        "Malware Activity": "Malware detected. Disconnect the network and run antivirus.",
        "Ransomware-like Activity": "Suspicious file encryption detected. Backup data immediately.",
        "Port Scanning Attack": "Port scanning detected. Block suspicious IPs.",
        "Brute Force Attack": "Multiple failed logins detected. Change passwords and enable 2FA.",
        "DDoS-like Attack": "Traffic spike detected. Enable firewall and rate limiting.",
        "Normal Activity": "System is operating normally."
    }
    return responses[attack]

# =====================================================
# LIVE MONITORING (SENTENCE-BASED)
# =====================================================
if page == "Live Monitoring":
    st.markdown("<div class='title'>Live Monitoring</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Real-time attack detection</div>", unsafe_allow_html=True)
    st.divider()

    output = st.empty()

    if st.button("▶ Start Monitoring"):
        for _ in range(12):
            event = generate_event()
            st.session_state.events.append(event)

            recent = st.session_state.events[-10:]
            attack, risk, label = detect(recent)
            st.session_state.risk.append(risk)

            message = bot_reply(attack)
            st.session_state.chat.append(("AI", message))
            speak(message)

            output.markdown(f"""
### 🔴 Live Security Status

- 🔍 **Detected Activity:** `{attack}`
- ⚠️ **Risk Score:** `{risk} / 100`
- 🏷️ **Attack Label:** `{label}`
- 📌 **Latest Event:** `{event}`

🕒 *Monitoring system behavior in real time...*
""")

            time.sleep(1)

# =====================================================
# RISK ANALYSIS
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
        st.info("Start monitoring to view the risk graph.")

# =====================================================
# CHAT ASSISTANT
# =====================================================
elif page == "Chat Assistant":
    st.markdown("<div class='title'>AI Chat Assistant</div>", unsafe_allow_html=True)
    st.divider()

    user = st.text_input("Ask about attacks, malware, or system status")

    if user:
        st.session_state.chat.append(("You", user))

        if "malware" in user.lower():
            answer = "Malware is detected using abnormal process and file behavior."
        elif "label" in user.lower():
            answer = "Labels: 0-Normal, 1-Brute Force, 2-DDoS, 3-Malware, 4-Port Scan, 5-Ransomware."
        else:
            answer = "I am monitoring the system continuously in real time."

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
    **AI Security App** is a real-time security monitoring application built using **Streamlit**.

    **Features**
    - Real-time attack detection
    - Malware and advanced threat detection
    - Risk visualization
    - Chat and voice alerts
    - Cloud-ready deployment
    """)
