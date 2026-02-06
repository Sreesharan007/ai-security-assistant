import streamlit as st
import random
import time
import matplotlib.pyplot as plt
from gtts import gTTS
import tempfile

# =====================================================
# PAGE CONFIG (ICON + BRANDING)
# =====================================================
st.set_page_config(
    page_title="AI Security App",
    page_icon="app_icon.png",
    layout="wide"
)

# =====================================================
# CUSTOM CSS (MODERN APP LOOK)
# =====================================================
st.markdown("""
<style>
body {
    background-color: #f4f6f9;
}

.card {
    padding: 20px;
    border-radius: 16px;
    background-color: white;
    box-shadow: 0 6px 18px rgba(0,0,0,0.08);
    margin-bottom: 15px;
}

.title {
    font-size: 30px;
    font-weight: 700;
    color: #0f172a;
}

.subtitle {
    color: #64748b;
    font-size: 15px;
}

.center {
    text-align: center;
}

button {
    border-radius: 10px !important;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# SESSION STATE
# =====================================================
for key in ["events", "risk_scores", "chat", "app_started"]:
    if key not in st.session_state:
        st.session_state[key] = False if key == "app_started" else []

# =====================================================
# VOICE FUNCTION
# =====================================================
def speak(text):
    tts = gTTS(text=text, lang="en")
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(temp.name)
    st.audio(temp.name, format="audio/mp3")

# =====================================================
# WELCOME / SPLASH SCREEN
# =====================================================
if not st.session_state.app_started:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.image("app_icon.png", width=140)
    st.markdown("<div class='title center'>AI Security App</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='subtitle center'>"
        "Real-time AI-powered threat detection & security assistant"
        "</div>",
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🚀 Enter Application"):
        st.session_state.app_started = True
        speak("Welcome to the AI Security Application. Real time monitoring is ready.")

    st.stop()

# =====================================================
# SIDEBAR (APP NAVIGATION)
# =====================================================
st.sidebar.image("app_icon.png", width=90)
st.sidebar.markdown("## AI Security App")
st.sidebar.caption("Real-time AI Protection")

page = st.sidebar.radio(
    "Navigation",
    ["📡 Live Monitoring", "📊 Risk Analysis", "💬 Chat Assistant", "ℹ️ About"]
)

# =====================================================
# EVENT GENERATOR
# =====================================================
def generate_event():
    return random.choice([
        "login_failed",
        "login_success",
        "high_traffic",
        "normal_activity",
        "malware_process",
        "suspicious_file_write",
        "port_scan"
    ])

# =====================================================
# DETECTION + CLASSIFICATION
# =====================================================
def detect_attack(window):
    if window.count("malware_process") >= 2:
        return "Malware Activity", 95, 3
    if window.count("suspicious_file_write") >= 3:
        return "Ransomware-like Activity", 97, 5
    if window.count("port_scan") >= 3:
        return "Port Scanning Attack", 80, 4
    if window.count("login_failed") >= 4:
        return "Brute Force Attack", 90, 1
    if window.count("high_traffic") >= 4:
        return "DDoS-like Attack", 85, 2
    return "Normal Activity", 10, 0

# =====================================================
# BOT RESPONSE
# =====================================================
def bot_reply(attack):
    return {
        "Malware Activity": "Critical alert. Malware behavior detected. Disconnect the network and run an antivirus scan.",
        "Ransomware-like Activity": "Critical alert. Suspicious file encryption detected. Backup your data immediately.",
        "Port Scanning Attack": "Warning. Port scanning activity detected. Block the suspicious IP.",
        "Brute Force Attack": "Warning. Multiple failed logins detected. Change passwords and enable two-factor authentication.",
        "DDoS-like Attack": "Warning. Abnormal traffic spike detected. Enable firewall and rate limiting.",
        "Normal Activity": "System is operating normally. No threats detected."
    }[attack]

# =====================================================
# 📡 LIVE MONITORING PAGE
# =====================================================
if page == "📡 Live Monitoring":
    st.markdown("<div class='title'>📡 Live Security Monitoring</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Real-time attack detection & classification</div>", unsafe_allow_html=True)
    st.divider()

    col1, col2, col3 = st.columns(3)

    start = st.button("▶ Start Monitoring")
    reset = st.button("🔄 Reset System")

    if reset:
        st.session_state.events.clear()
        st.session_state.risk_scores.clear()
        st.session_state.chat.clear()
        st.success("System reset successfully.")

    if start:
        for _ in range(15):
            event = generate_event()
            st.session_state.events.append(event)

            recent = st.session_state.events[-10:]
            attack, risk, label = detect_attack(recent)
            st.session_state.risk_scores.append(risk)

            with col1:
                st.markdown(f"<div class='card'><b>Status</b><br>{attack}</div>", unsafe_allow_html=True)
            with col2:
                st.markdown(f"<div class='card'><b>Risk Score</b><br>{risk}/100</div>", unsafe_allow_html=True)
            with col3:
                st.markdown(f"<div class='card'><b>Attack Label</b><br>{label}</div>", unsafe_allow_html=True)

            message = bot_reply(attack)
            st.session_state.chat.append(("AI Bot", message))
            speak(message)

            time.sleep(1)

# =====================================================
# 📊 RISK ANALYSIS PAGE
# =====================================================
elif page == "📊 Risk Analysis":
    st.markdown("<div class='title'>📊 Risk Analysis</div>", unsafe_allow_html=True)
    st.divider()

    if len(st.session_state.risk_scores) > 1:
        fig, ax = plt.subplots()
        ax.plot(st.session_state.risk_scores, linewidth=3)
        ax.set_ylim(0, 100)
        ax.set_xlabel("Time")
        ax.set_ylabel("Risk Score")
        ax.grid(True)
        st.pyplot(fig)
    else:
        st.info("Start monitoring to see the risk graph.")

# =====================================================
# 💬 CHAT ASSISTANT PAGE
# =====================================================
elif page == "💬 Chat Assistant":
    st.markdown("<div class='title'>💬 AI Security Assistant</div>", unsafe_allow_html=True)
    st.divider()

    user_input = st.text_input("Ask about attacks, malware, or safety")

    if user_input:
        st.session_state.chat.append(("You", user_input))

        if "label" in user_input.lower():
            answer = "Attack labels: 0-Normal, 1-Brute Force, 2-DDoS, 3-Malware, 4-Port Scan, 5-Ransomware."
        elif "malware" in user_input.lower():
            answer = "Malware is detected using abnormal process and file behavior."
        else:
            answer = "I am monitoring your system continuously in real time."

        st.session_state.chat.append(("AI Bot", answer))
        speak(answer)

    for sender, msg in st.session_state.chat[-6:]:
        if sender == "You":
            st.info(f"**You:** {msg}")
        else:
            st.success(f"**AI Bot:** {msg}")

# =====================================================
# ℹ️ ABOUT PAGE
# =====================================================
elif page == "ℹ️ About":
    st.markdown("<div class='title'>ℹ️ About This App</div>", unsafe_allow_html=True)
    st.divider()
    st.write("""
    **AI Security App** is a real-time AI-powered security monitoring system that:
    - Detects and classifies multiple cyber attacks
    - Monitors behavior continuously
    - Visualizes risk levels
    - Provides voice-based alerts
    - Runs as an installable Progressive Web App (PWA)

    Developed using **Python & Streamlit**.
    """)
