import numpy as np
from sklearn.ensemble import IsolationForest

normal_data = np.random.normal(50, 10, (300, 3))
model = IsolationForest(contamination=0.1, random_state=42)
model.fit(normal_data)

def detect_attack(data):
    pred = model.predict([data])[0]

    if pred == -1:
        if data[0] > 80:
            return "DDoS Attack", "HIGH"
        elif data[1] > 6:
            return "Brute Force Attack", "HIGH"
        else:
            return "Malware Activity", "MEDIUM"
    return "No Attack", "LOW"
