import streamlit as st
import random
import time
import pandas as pd
from gtts import gTTS
import tempfile
from datetime import datetime

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
if "scanning" not in st.session_state:
    st.session_state.scanning = False
if "last_attack" not in st.session_state:
    st.session_state.last_attack = "Normal"
if "history" not in st.session_state:
    st.session_state.history = []
if "network_info" not in st.session_state:
    st.session_state.network_info = None
if "attack_memory" not in st.session_state:
    st.session_state.attack_memory = {
        "Malware": 0,
        "Ransomware": 0,
        "Brute Force": 0,
        "DDoS": 0
    }

# =====================================================
# VOICE EXPLANATION (SIMPLE + CONSEQUENCES)
# =====================================================
def speak_attack(attack):
    messages = {
        "Malware": (
            "Warning. A malware attack is detected. "
            "This means a harmful program is running on your system. "
            "If ignored, your personal files and data may be stolen or damaged."
        ),
        "Ransomware": (
            "Warning. A ransomware attack is detected. "
            "Your files may be locked and money could be demanded. "
            "If ignored, you may permanently lose access to your data."
        ),
        "Brute Force": (
            "Warning. A brute force attack is detected. "
            "Someone is trying to guess your password repeatedly. "
            "If ignored, the attacker may gain full access to your account."
        ),
        "DDoS": (
            "Warning. A denial of service attack is detected. "
            "Your system is being flooded with fake traffic. "
            "If ignored, your network may become slow or stop working completely."
        )
    }

    if attack not in messages:
        return

    try:
        tts = gTTS(text=messages[attack], lang="en")
        audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(audio.name)
        st.audio(audio.name)
    except Exception:
        pass

# =====================================================
# CONFIDENCE SCORE + ANTIBODY-LIKE LEARNING
# =====================================================
def confidence_score(attack):
    base_ranges = {
        "Malware": (85, 90),
        "Ransomware": (88, 92),
        "Brute Force": (80, 88),
        "DDoS": (82, 90),
        "Normal": (5, 15)
    }

    if attack == "Normal":
        low, high = base_ranges["Normal"]
        return random.randint(low, high), "No threat detected"

    memory = st.session_state.attack_memory.get(attack, 0)
    bonus = min(memory * 2, 10)   # max +10%

    low, high = base_ranges[attack]
    confidence = random.randint(low + bonus, high + bonus)

    explanation = (
        f"This attack pattern has been detected {memory + 1} times. "
        "The system has learned this behavior and detection reliability is improving."
    )

    return confidence, explanation

# =====================================================
# SIMULATED DATA
# =====================================================
malicious_files = ["update_service.exe", "svhost32.dll", "temp_cleaner.exe"]

network_attackers = [
    {"ip": "192.168.1.45", "city": "Chennai", "country": "India", "isp": "Local Broadband ISP"},
    {"ip": "103.25.64.12", "city": "Mumbai", "country": "India", "isp": "FiberNet Services"},
    {"ip": "45.67.89.101", "city": "Bengaluru", "country": "India", "isp": "Cloud Hosting Provider"}
]

# =====================================================
# ATTACK DETECTION (SIMULATED)
# =====================================================
def detect_attack():
    return random.choice(["Normal", "Malware", "Ransomware", "Brute Force", "DDoS"])

# =====================================================
# SIDEBAR – NETWORK ATTACK DETAILS
# =====================================================
st.sidebar.title("🌐 Network Attack Info")

if st.session_state.network_info:
    info = st.session_state.network_info
    st.sidebar.error("🚨 Network Attack Detected")
    st.sidebar.markdown(f"""
**Attack Type:** {info['attack']}  
**Attacker IP:** {info['ip']}  
**Location:** {info['city']}, {info['country']}  
**ISP:** {info['isp']}
""")
    st.sidebar.info(
        "📍 Recommended Action:\n"
        "- Block the IP address\n"
        "- Save system logs\n"
        "- Report to Cyber Crime Cell\n"
        "- https://cybercrime.gov.in"
    )
else:
    st.sidebar.success("No active network attack")

# =====================================================
# MAIN UI
# =====================================================
st.title("🛡️ AI Security Assistant")
st.write("Real-time attack detection with learning-based confidence")

col1, col2 = st.columns(2)
with col1:
    if st.button("▶ Start Scan"):
        st.session_state.scanning = True
with col2:
    if st.button("⏹ Stop Scan"):
        st.session_state.scanning = False

st.divider()

status_box = st.empty()
info_box = st.empty()
action_box = st.empty()

# =====================================================
# MAIN SCANNING LOGIC
# =====================================================
if st.session_state.scanning:
    attack = detect_attack()
    confidence, confidence_reason = confidence_score(attack)

    # Increase immune memory
    if attack in st.session_state.attack_memory:
        st.session_state.attack_memory[attack] += 1

    # Reset sidebar if not network attack
    if attack not in ["Brute Force", "DDoS"]:
        st.session_state.network_info = None

    # Speak only when attack changes
    if attack != st.session_state.last_attack:
        speak_attack(attack)
        st.session_state.last_attack = attack

    timestamp = datetime.now().strftime("%H:%M:%S")

    if attack == "Normal":
        status_box.success(
            f"✅ SYSTEM STATUS: SAFE\n\n"
            f"No active threats detected."
        )
        info_box.info(f"🧠 AI Confidence: {confidence}%")

    elif attack == "Malware":
        file = random.choice(malicious_files)
        status_box.error(
            f"🦠 MALWARE ATTACK DETECTED\n\n"
            f"Suspicious file: **{file}**"
        )
        info_box.info(
            f"🧠 AI Confidence: **{confidence}%**\n\n"
            f"🧬 Learning Status: {confidence_reason}"
        )
        if st.button("🧹 Remove Malware"):
            action_box.success(
                f"The file **{file}** has been isolated.\n"
                "Please run a full antivirus scan."
            )

    elif attack == "Ransomware":
        file = random.choice(malicious_files)
        status_box.error(
            f"🔐 RANSOMWARE ATTACK DETECTED\n\n"
            f"Affected file: **{file}**"
        )
        info_box.info(
            f"🧠 AI Confidence: **{confidence}%**\n\n"
            f"🧬 Learning Status: {confidence_reason}"
        )
        action_box.warning(
            "Disconnect the network immediately and restore from backup."
        )

    elif attack in ["Brute Force", "DDoS"]:
        attacker = random.choice(network_attackers)
        st.session_state.network_info = {
            "attack": attack,
            "ip": attacker["ip"],
            "city": attacker["city"],
            "country": attacker["country"],
            "isp": attacker["isp"]
        }

        status_box.error(
            f"🌐 {attack.upper()} ATTACK DETECTED\n\n"
            f"Source IP: **{attacker['ip']}**"
        )
        info_box.info(
            f"🧠 AI Confidence: **{confidence}%**\n\n"
            f"🧬 Learning Status: {confidence_reason}"
        )

        if st.button("🚫 Block IP"):
            action_box.success(f"IP **{attacker['ip']}** has been blocked.")

    # Log attack history
    st.session_state.history.append({
        "Time": timestamp,
        "Attack Type": attack,
        "AI Confidence (%)": confidence
    })

    time.sleep(2)

# =====================================================
# ATTACK HISTORY TABLE
# =====================================================
st.divider()
st.subheader("📜 Attack History")

if st.session_state.history:
    st.dataframe(pd.DataFrame(st.session_state.history), use_container_width=True)
else:
    st.info("No attacks recorded yet.")
