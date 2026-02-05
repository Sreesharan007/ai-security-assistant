def security_bot_response(attack, risk):
    if attack == "No Attack":
        return "✅ System secure. No threats detected."

    tips = {
        "DDoS Attack": "🚨 Traffic spike detected. Enable firewall rules and rate limiting.",
        "Brute Force Attack": "⚠️ Multiple failed logins. Change password and enable 2FA.",
        "Malware Activity": "⚠️ Suspicious behavior detected. Run antivirus scan."
    }

    return tips.get(attack, "⚠️ Suspicious activity detected.")
