import streamlit as st
import random
import time
import matplotlib.pyplot as plt
from gtts import gTTS
import tempfile

# ----------------------------------
# Page configuration
# ----------------------------------
st.set_page_config(
    page_title="AI Security Assistant",
    page_icon="🛡️",
    layout="centered"
)

# ----------------------------------
# Header UI
# ----------------------------------
st.markdown(
    """
    <h1 style='text-align:center;'>🛡️ AI Security Assistant</h1>
    <p style='text-align:center; color:gray;'>
    Real-time attack detection • Risk visualization • Voice alerts
    </p>
    """,
    unsafe_allow_html=True
)

st.divider()

# ----------------------------------
# Session state
# ----------------------------------
if "events" not in st.session_state:
    st.session_state.events = []

if "risk_scores" not in st.session_state:
    st.session_state.risk_scores = []

if "chat" not in st.session_state:
    st.session_state.chat = []

# ----------------------------------
# Voice function (Text → Speech)
# ----------------------------------
def speak(text):
    tts = gTTS(text=text, lang="en")
    temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(temp_audio.name)
    st.audio(temp_audio.name, format="audio/mp3")

# ----------------------------------
# Real-time event generator
# ----------------------------------
def generate_event():
    events = [
        ("login_failed", 8),
        ("login_success", 1),
        ("high_traffic", 9),
        ("normal_activity", 1)
    ]
    return random.choice(events)

# ----------------------------------
# Detection logic
# ----------------------------------
def detect_attack(event_window):
    failed = event_window.count("login_failed")
    traffic = event_window.count("high_traffic")

    if failed >= 4:
        return "Brute Force Attack", 90
    elif traffic >= 4:
        return "DDoS-like Attack", 85
    else:
        return "Normal Activity", 10

# ----------------------------------
# AI Bot response
# ----------------------------------
def bot_response(attack):
    responses = {
        "Brute Force Attack":
        "Alert. Multiple failed login attempts detected. "
        "Please change your password, enable two-factor authentication, "
        "and block suspicious IP addresses.",

        "DDoS-like Attack":
        "Warning. Abnormal traffic spike detected. "
        "Enable firewall protection, apply rate limiting, "
        "and monitor incoming network requests.",

        "Normal Activity":
        "System is operating normally. No threats detected."
    }
    return responses[attack]

# ----------------------------------
# Control panel
# ----------------------------------
st.subheader("🎛️ Control Panel")

col1, col2 = st.columns(2)

with col1:
    start = st.button("▶ Start Real-Time Monitoring")

with col2:
    reset = st.button("🔄 Reset System")

if reset:
    st.session_state.events.clear()
    st.session_state.risk_scores.clear()
    st.session_state.chat.clear()
    st.success("System reset successfully.")

st.divider()

# ----------------------------------
# Real-time monitoring loop
# ----------------------------------
if start:
    for _ in range(15):
        event, severity = generate_event()
        st.session_state.events.append(event)

        recent_events = st.session_state.events[-10:]
        attack, risk = detect_attack(recent_events)

        st.session_state.risk_scores.append(risk)

        response = bot_response(attack)
        st.session_state.chat.append(("AI Bot", response))

        # Status UI
        if attack == "Normal Activity":
            st.success(f"✅ {attack}")
        else:
            st.error(f"🚨 {attack}")

        st.write(f"📌 Latest Event: **{event}**")
        st.write(f"⚠️ Risk Level: **{risk} / 100**")

        speak(response)
        time.sleep(1)

st.divider()

# ----------------------------------
# Risk Graph
# ----------------------------------
st.subheader("📊 Live Risk Level Graph")

if len(st.session_state.risk_scores) > 1:
    fig, ax = plt.subplots()
    ax.plot(st.session_state.risk_scores, linewidth=2)
    ax.set_ylim(0, 100)
    ax.set_xlabel("Time")
    ax.set_ylabel("Risk Score")
    ax.grid(True)
    st.pyplot(fig)
else:
    st.info("Start monitoring to view risk graph.")

st.divider()

# ----------------------------------
# Chat Interface
# ----------------------------------
st.subheader("💬 Talk to the AI Security Bot")

user_input = st.text_input(
    "Ask something like: *What should I do now?* or *Is my system safe?*"
)

if user_input:
    st.session_state.chat.append(("You", user_input))

    if "safe" in user_input.lower():
        answer = "I am continuously monitoring your system. Currently, no critical threat is detected."
    elif "attack" in user_input.lower():
        answer = "If an attack is detected, follow the recommended security actions immediately."
    elif "password" in user_input.lower():
        answer = "Use a strong password with uppercase, lowercase, numbers, and symbols. Avoid reuse."
    else:
        answer = "I am here to help. Please ask about security status or precautions."

    st.session_state.chat.append(("AI Bot", answer))
    speak(answer)

# ----------------------------------
# Display chat history
# ----------------------------------
for sender, message in st.session_state.chat[-8:]:
    if sender == "You":
        st.info(f"**You:** {message}")
    else:
        st.success(f"**AI Bot:** {message}")
