import streamlit as st
import random
import time
import matplotlib.pyplot as plt

st.set_page_config(page_title="Real-Time AI Security Assistant", layout="centered")

st.title("🛡️ Real-Time AI Security Assistant")
st.caption("Live attack detection with chatbot & risk visualization")

# -------------------------------
# Session state initialization
# -------------------------------
if "events" not in st.session_state:
    st.session_state.events = []

if "risk_scores" not in st.session_state:
    st.session_state.risk_scores = []

if "chat" not in st.session_state:
    st.session_state.chat = []

# -------------------------------
# Real-time event generator
# -------------------------------
def live_event():
    events = [
        ("login_failed", 7),
        ("login_success", 1),
        ("high_traffic", 8),
        ("normal_activity", 1)
    ]
    return random.choice(events)

# -------------------------------
# Detection logic
# -------------------------------
def detect_attack(events):
    failed = events.count("login_failed")
    traffic = events.count("high_traffic")

    if failed > 3:
        return "Brute Force Attack", 90
    if traffic > 3:
        return "DDoS-like Attack", 85
    return "Normal Activity", 10

# -------------------------------
# AI Bot response
# -------------------------------
def bot_response(attack):
    responses = {
        "Brute Force Attack":
        "🚨 Brute force attack detected.\n\n🔐 Advice:\n• Change password\n• Enable 2FA\n• Block suspicious IPs",

        "DDoS-like Attack":
        "🚨 Traffic flood detected.\n\n🌐 Advice:\n• Enable firewall\n• Apply rate limiting\n• Monitor traffic",

        "Normal Activity":
        "✅ System is stable. No threats detected."
    }
    return responses[attack]

# -------------------------------
# Start monitoring
# -------------------------------
if st.button("▶ Start Real-Time Monitoring"):
    for _ in range(15):
        event, severity = live_event()
        st.session_state.events.append(event)

        recent_events = st.session_state.events[-10:]
        attack, risk = detect_attack(recent_events)

        st.session_state.risk_scores.append(risk)
        reply = bot_response(attack)

        st.session_state.chat.append(("AI Bot", reply))

        st.subheader(f"🔍 Status: {attack}")
        st.write(f"📌 Latest Event: **{event}**")
        st.write(f"⚠️ Risk Score: **{risk}/100**")

        time.sleep(1)

# -------------------------------
# Risk graph
# -------------------------------
st.markdown("### 📊 Live Risk Level")

if len(st.session_state.risk_scores) > 1:
    fig, ax = plt.subplots()
    ax.plot(st.session_state.risk_scores)
    ax.set_xlabel("Time")
    ax.set_ylabel("Risk Score")
    ax.set_ylim(0, 100)
    st.pyplot(fig)
else:
    st.info("Risk graph will appear once monitoring starts.")

# -------------------------------
# Chatbot UI
# -------------------------------
st.markdown("### 💬 Talk to the AI Security Bot")

user_input = st.text_input("Ask something like: *What should I do now?*")

if user_input:
    st.session_state.chat.append(("You", user_input))

    if "password" in user_input.lower():
        answer = "🔐 Use a strong password with symbols, numbers, and avoid reuse."
    elif "attack" in user_input.lower():
        answer = "🚨 If an attack is detected, follow the precautions shown above immediately."
    else:
        answer = "🤖 I'm monitoring your system in real time. Let me know if you need help."

    st.session_state.chat.append(("AI Bot", answer))

# -------------------------------
# Display chat history
# -------------------------------
for sender, msg in st.session_state.chat[-6:]:
    if sender == "You":
        st.info(f"**You:** {msg}")
    else:
        st.success(f"**AI Bot:** {msg}")
