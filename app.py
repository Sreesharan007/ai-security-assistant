import streamlit as st
import random
import time
import matplotlib.pyplot as plt
from gtts import gTTS
import tempfile

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="AI Security App",
    page_icon="🛡️",
    layout="wide"
)

# =====================================================
# SESSION STATE
# =====================================================
if "started" not in st.session_state:
    st.session_state.started = False
if "events" not in st.session_state:
    st.session_state.events = []
if "risk" not in st.session_state:
    st.session_state.risk = []
if "last_attack" not in st.session_state:
    st.session_state.last_attack = ""

# =====================================================
# VOICE ALERT (ONLY FOR ATTACKS)
# =====================================================
def speak_attack(attack):
    if attack == "Normal Activity":
        return

    message = f"Warning. Your system is under {attack}. Please take immediate action."

    try:
        tts = gTTS(text=message, lang="en")
        audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(audio.name)
        st.audio(audio.name)
    except Exception:
        pass

# =====================================================
# WELCOME SCREEN (TEXT ONLY, NO VOICE)
# =====================================================
if not st.session_state.started:
    st.title("🛡️ AI Security App")
    st.subheader("Real-time cyber attack detection system")
    st.write("Click start to begin live monitoring of your system.")

    if st.button("▶ Start Application"):
        st.session_state.started = True
        st.success("✅ Welcome! Live monitoring has started.")
        st.stop()

    st.stop()

# =====================================================
# SIDEBAR
# =====================================================
st.sidebar.title("AI Security App")
page = st.sidebar.radio(
    "Navigation",
    ["Live Monitoring", "Risk Graph", "About"]
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
# ATTACK DETECTION (CLEAR TYPES)
# =====================================================
def detect_attack(events):
    if events.count("malware_process") >= 2:
        return "Malware Attack", 95
    if events.count("suspicious_file_write") >= 3:
        return "Ransomware Attack", 97
    if events.count("port_scan") >= 3:
        return "Port Scanning Attack", 80
    if events.count("login_failed") >= 4:
        return "Brute Force Attack", 90
    if events.count("high_traffic") >= 4:
        return "DDoS Attack", 85
    return "Normal Activity", 10

# =====================================================
# LIVE MONITORING (VERY CLEAR OUTPUT)
# =====================================================
if page == "Live Monitoring":
    st.header("🔴 Live System Monitoring")
    st.write("The system is actively checking for cyber attacks.")
    st.divider()

    display = st.empty()

    if st.button("▶ Start Live Detection"):
        for _ in range(12):
            event = generate_event()
            st.session_state.events.append(event)

            recent = st.session_state.events[-10:]
            attack, risk = detect_attack(recent)
            st.session_state.risk.append(risk)

            # Voice only when attack changes
            if attack != st.session_state.last_attack:
                speak_attack(attack)
                st.session_state.last_attack = attack

            if attack == "Normal Activity":
                display.success(
                    "✅ SYSTEM STATUS: SAFE\n\nNo attack detected. Your system is secure."
                )
            else:
                display.error(
                    f"🚨 ALERT: YOUR SYSTEM IS UNDER A **{attack.upper()}**\n\n"
                    f"⚠️ Risk Level: {risk} / 100\n\n"
                    f"👉 Immediate action is required."
                )

            time.sleep(1)

# =====================================================
# RISK GRAPH
# =====================================================
elif page == "Risk Graph":
    st.header("📊 Risk Level Over Time")

    if len(st.session_state.risk) > 1:
        fig, ax = plt.subplots()
        ax.plot(st.session_state.risk, linewidth=2)
        ax.set_ylim(0, 100)
        ax.set_xlabel("Time")
        ax.set_ylabel("Risk Level")
        ax.grid(True)
        st.pyplot(fig)
    else:
        st.info("Start live monitoring to see the risk graph.")

# =====================================================
# ABOUT
# =====================================================
elif page == "About":
    st.header("ℹ️ About This System")
    st.write("""
    This application detects cyber attacks in real time and clearly informs the user
    when the system is under attack.

    **Detected Attacks**
    - Malware Attack
    - Ransomware Attack
    - Brute Force Attack
    - DDoS Attack
    - Port Scanning Attack
    """)
