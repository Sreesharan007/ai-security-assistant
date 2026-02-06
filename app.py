import streamlit as st
import random
import time
import matplotlib.pyplot as plt
from gtts import gTTS
import tempfile

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="AI Security App",
    page_icon="🛡️",
    layout="wide"
)

# -------------------- CUSTOM CSS --------------------
st.markdown("""
<style>
.card {
    padding: 20px;
    border-radius: 15px;
    background-color: #f9fafb;
    box-shadow: 0 4px 10px rgba(0,0,0,0.08);
    margin-bottom: 15px;
}
.title {
    font-size: 26px;
    font-weight: 700;
}
.subtitle {
    color: gray;
}
.alert-high {
    color: #d9534f;
    font-weight: bold;
}
.alert-low {
    color: #5cb85c;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# -------------------- SIDEBAR --------------------
st.sidebar.markdown("## 🛡️ AI Security App")
page = st.sidebar.radio(
    "Navigation",
    ["📡 Live Monitoring", "📊 Risk Analysis", "💬 Chat Assistant", "ℹ️ About"]
)

# -------------------- SESSION STATE --------------------
for key in ["events", "risk_scores", "chat"]:
    if key not in st.session_state:
        st.session_state[key] = []

# -------------------- VOICE FUNCTION --------------------
def speak(text):
    tts = gTTS(text=text, lang="en")
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(temp.name)
    st.audio(temp.name, format="audio/mp3")

# -------------------- EVENT GENERATOR --------------------
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

# -------------------- DETECTION + CLASSIFICATION --------------------
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

# -------------------- BOT RESPONSE --------------------
def bot_reply(attack):
    return {
        "Malware Activity": "🚨 Malware behavior detected. Disconnect network and run antivirus scan.",
        "Ransomware-like Activity": "🚨 Suspicious file encryption behavior detected. Backup data immediately.",
        "Port Scanning Attack": "⚠️ Port scanning detected. Block suspicious IPs.",
        "Brute Force Attack": "⚠️ Multiple failed logins detected. Change password and enable 2FA.",
        "DDoS-like Attack": "⚠️ Traffic spike detected. Enable firewall and rate limiting.",
        "Normal Activity": "✅ System operating normally."
    }[attack]

# ======================================================
# 📡 LIVE MONITORING PAGE
# ======================================================
if page == "📡 Live Monitoring":
    st.markdown("<div class='title'>📡 Live Security Monitoring</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Real-time threat detection & classification</div>", unsafe_allow_html=True)
    st.divider()

    col1, col2, col3 = st.columns(3)

    start = st.button("▶ Start Monitoring")
    reset = st.button("🔄 Reset")

    if reset:
        st.session_state.events.clear()
        st.session_state.risk_scores.clear()
        st.session_state.chat.clear()
        st.success("System reset successfully")

    if start:
        for _ in range(12):
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

# ======================================================
# 📊 RISK ANALYSIS PAGE
# ======================================================
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
        st.info("Start monitoring to view risk trends.")

# ======================================================
# 💬 CHAT ASSISTANT PAGE
# ======================================================
elif page == "💬 Chat Assistant":
    st.markdown("<div class='title'>💬 AI Security Assistant</div>", unsafe_allow_html=True)
    st.divider()

    user_input = st.text_input("Ask something like: Is there malware? What attack is happening?")

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

# ======================================================
# ℹ️ ABOUT PAGE
# ======================================================
elif page == "ℹ️ About":
    st.markdown("<div class='title'>ℹ️ About This App</div>", unsafe_allow_html=True)
    st.divider()
    st.write("""
    **AI Security App** is a real-time intrusion detection prototype that:
    - Detects and classifies multiple cyber attacks
    - Visualizes risk levels dynamically
    - Provides voice-based security alerts
    - Runs as an installable Progressive Web App (PWA)

    Built using **Python + Streamlit** and deployed on the cloud.
    """)
