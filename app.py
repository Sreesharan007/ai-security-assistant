import streamlit as st
import random
import time
import pandas as pd
from gtts import gTTS
import tempfile
from datetime import datetime

st.set_page_config(page_title="AI Security App", page_icon="🛡️", layout="wide")

# ---------------- SESSION STATE ----------------
if "scanning" not in st.session_state:
    st.session_state.scanning = False
if "last_attack" not in st.session_state:
    st.session_state.last_attack = "Normal"
if "history" not in st.session_state:
    st.session_state.history = []

# ---------------- VOICE ALERT ----------------
def speak(msg):
    try:
        tts = gTTS(text=msg, lang="en")
        audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(audio.name)
        st.audio(audio.name)
    except:
        pass

# ---------------- SIMULATION DATA ----------------
malicious_files = ["update_service.exe", "svhost32.dll", "temp_cleaner.exe"]
attacker_ips = ["192.168.1.45", "103.25.64.12", "45.67.89.101"]

# ---------------- ATTACK DETECTION ----------------
def detect_attack():
    attacks = ["Normal", "Malware", "Brute Force", "DDoS"]
    return random.choice(attacks)

# ---------------- UI ----------------
st.title("🛡️ AI Security Assistant")
st.write("Real-time protection and guided response system")

col1, col2 = st.columns(2)
with col1:
    if st.button("▶ Start Scan"):
        st.session_state.scanning = True
with col2:
    if st.button("⏹ Stop Scan"):
        st.session_state.scanning = False

st.divider()

status_box = st.empty()
action_box = st.empty()

# ---------------- MAIN LOGIC ----------------
if st.session_state.scanning:
    attack = detect_attack()

    if attack != st.session_state.last_attack:
        if attack == "Malware":
            speak("Warning. Your system is under a malware attack.")
        elif attack == "Brute Force":
            speak("Warning. A brute force attack is detected.")
        elif attack == "DDoS":
            speak("Warning. A denial of service attack is detected.")

        st.session_state.last_attack = attack

    if attack == "Normal":
        status_box.success("✅ System is safe. No threats detected.")

    elif attack == "Malware":
        file = random.choice(malicious_files)
        status_box.error(
            f"🦠 MALWARE ATTACK DETECTED\n\n"
            f"Suspicious file identified: **{file}**"
        )

        if st.button("🧹 Remove Malware"):
            action_box.success(
                f"The file **{file}** has been isolated.\n\n"
                "Please run a full antivirus scan."
            )

    elif attack == "Brute Force":
        ip = random.choice(attacker_ips)
        status_box.error(
            f"🔐 BRUTE FORCE ATTACK DETECTED\n\n"
            f"Attacking IP address: **{ip}**"
        )

        if st.button("🚫 Block IP"):
            action_box.success(f"IP address **{ip}** has been blocked.")

        st.info(
            "📍 Please report this incident to your nearest Cyber Crime Police Station\n"
            "or visit: https://cybercrime.gov.in"
        )

    elif attack == "DDoS":
        ip = random.choice(attacker_ips)
        status_box.error(
            f"🌐 DDoS ATTACK DETECTED\n\n"
            f"Source IP: **{ip}**"
        )

        st.info(
            "📍 This is a serious network attack.\n"
            "Please report it to the nearest Cyber Crime Cell or at:\n"
            "https://cybercrime.gov.in"
        )

    st.session_state.history.append({
        "Time": datetime.now().strftime("%H:%M:%S"),
        "Attack": attack
    })

    time.sleep(2)

# ---------------- ATTACK HISTORY ----------------
st.divider()
st.subheader("📜 Attack History")

if st.session_state.history:
    st.dataframe(pd.DataFrame(st.session_state.history))
else:
    st.info("No attacks recorded yet.")
