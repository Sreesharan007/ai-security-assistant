import streamlit as st
import numpy as np
import time
from detector import detect_attack
from security_bot import security_bot_response

st.set_page_config(page_title="AI Security Assistant")

st.title("🛡️ AI Security Assistant")
st.write("Real-time attack detection and advisory bot")

if "chat" not in st.session_state:
    st.session_state.chat = []

if st.button("Start Monitoring"):
    for _ in range(8):
        traffic = np.random.randint(30, 100)
        failed = np.random.randint(0, 10)
        cpu = np.random.randint(20, 90)

        attack, risk = detect_attack([traffic, failed, cpu])
        reply = security_bot_response(attack, risk)

        st.session_state.chat.append(reply)

        st.write(f"📡 Traffic: {traffic}")
        st.write(f"🔐 Failed Logins: {failed}")
        st.write(f"💻 CPU Usage: {cpu}%")
        st.subheader(f"Status: {attack} (Risk: {risk})")
        time.sleep(2)

st.subheader("AI Bot Messages")
for msg in st.session_state.chat:
    st.success(msg)
