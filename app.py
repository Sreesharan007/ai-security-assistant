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

# =====================================================
# VOICE ALERT (ONLY FOR ATTACKS)
# =====================================================
def speak_attack(attack):
    if attack == "Normal":
        return
    message = f"Warning. Your system is under {attack} attack."
    try:
        tts = gTTS(text=message, lang="en")
        audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(audio.name)
        st.audio(audio.name)
    except Exception:
        pass

# =====================================================
# CONFIDENCE SCORE
# =====================================================
def confidence_score(attack):
    ranges = {
        "Malware": (90, 98),
        "Ransomware": (92, 99),
        "Brute Force": (85, 95),
        "DDoS": (88, 96),
        "Normal": (5, 15)
    }
    low, high = ranges.get(attack, (50, 60))
    return random.randint(low, high)

# =====================================================
# SIMULATED DATA
# =====================================================
malicious_files = ["update_service.exe", "svhost32.dll", "temp_cleaner.exe"]

network_attackers = [
    {
        "ip": "192.168.1.45",
        "city": "Chennai",
        "country": "India",
        "isp": "Local Broadband ISP"
    },
    {
        "ip": "103.25.64.12",
        "city": "Mumbai",
        "country": "India",
        "isp": "FiberNet Services"
    },
    {
        "ip": "45.67.89.101",
        "city": "Bengaluru",
        "country": "India",
        "isp": "Cloud Hosting Provider"
    }
]

# =====================================================
# ATTACK DETECTION (SIMULATED)
# =====================================================
def detect_attack():
    return random.choice(["Normal", "Malware", "Brute Force", "DDoS", "Ransomware"])

# =====================================================
# SIDEBAR (NETWORK ATTACK DETAILS)
# =====================================================
st.sidebar.title("🛡️ Network Intelligence")

if st.session_state.network_info:
    info = st.session_state.network_info
    st.sidebar.error("🚨 Active Network Attack")
    st.sidebar.markdown(f"""
**Attack Type:** {info['attack']}

**Attacker IP:** {info['ip']}

**Location:** {info['city']}, {info['country']}

**ISP:** {info['isp']}
""")
    st.sidebar.info(
        "📍 Recommended Action:\n"
        "- Block the IP address\n"
        "- Preserve logs\n"
        "- Report to Cyber Crime Cell\n"
        "- https://cybercrime.gov.in"
    )
else:
    st.sidebar.success("No active network attack detected.")

# =====================================================
# UI HEADER
# =====================================================
st.title("🛡️ AI Security Assistant")
st.write("Real-time attack detection with confidence scoring")

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

# =====================================================
# MAIN LOGIC
# =====================================================
if st.session_state.scanning:
    attack = detect_attack()
    confidence = confidence_score(attack)

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
            f"No active threats detected.\n\n"
            f"🧠 Confidence Score: {confidence}%"
        )

    elif attack == "Malware":
        file = random.choice(malicious_files)
        status_box.error(
            f"🦠 MALWARE ATTACK DETECTED\n\n"
            f"Suspicious file: **{file}**\n\n"
            f"🧠 Confidence Score: **{confidence}%**"
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
            f"Affected file: **{file}**\n\n"
            f"🧠 Confidence Score: **{confidence}%**"
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
            f"Source IP: **{attacker['ip']}**\n\n"
            f"🧠 Confidence Score: **{confidence}%**"
        )

        if st.button("🚫 Block IP"):
            action_box.success(f"IP address **{attacker['ip']}** has been blocked.")

    # Log history
    st.session_state.history.append({
        "Time": timestamp,
        "Attack Type": attack,
        "Confidence (%)": confidence
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
