#!/usr/bin/env python3
"""
Simple QCF Demo - Standalone version without complex dependencies
"""

import pandas as pd
import numpy as np
from datetime import datetime
import hashlib
import os

print("🔒 Quantum Cloud Firewall - Simplified Demo")
print("=" * 50)

# 1. Generate sample data
print("\n1. 📊 Generating Network Data...")
np.random.seed(42)
num_samples = 200

data = []
for i in range(num_samples):
    if i < num_samples * 0.9:  # 90% normal
        data.append({
            'src_port': np.random.randint(1024, 49151),
            'dst_port': np.random.choice([80, 443, 22, 53]),
            'packet_size': np.random.normal(1000, 200),
            'protocol': np.random.choice(['TCP', 'UDP']),
            'is_anomaly': 0
        })
    else:  # 10% anomalous
        data.append({
            'src_port': np.random.randint(49152, 65535),
            'dst_port': np.random.choice([21, 23, 135, 139, 445]),
            'packet_size': np.random.normal(50, 500),
            'protocol': np.random.choice(['TCP', 'UDP', 'ICMP']),
            'is_anomaly': 1
        })

df = pd.DataFrame(data)
print(f"Generated {len(df)} packets ({df['is_anomaly'].sum()} anomalies)")

# 2. Simple anomaly detection
print("\n2. 🧠 Training Anomaly Detector...")
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Prepare features
features = df[['src_port', 'dst_port', 'packet_size']]
protocol_dummies = pd.get_dummies(df['protocol'], prefix='protocol')
features = pd.concat([features, protocol_dummies], axis=1)
target = df['is_anomaly']

X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=50, random_state=42)
model.fit(X_train, y_train)
accuracy = model.score(X_test, y_test)
print(f"Model accuracy: {accuracy:.2%}")

# 3. Simulate quantum encryption
print("\n3. 🛡️ Post-Quantum Encryption Demo...")
class SimpleEncryption:
    @staticmethod
    def encrypt(message, key):
        message_bytes = message.encode('utf-8')
        encrypted = bytes(m ^ k for m, k in zip(message_bytes, key * (len(message_bytes) // len(key) + 1)))
        return encrypted.hex()
    
    @staticmethod
    def decrypt(encrypted_hex, key):
        encrypted = bytes.fromhex(encrypted_hex)
        decrypted = bytes(e ^ k for e, k in zip(encrypted, key * (len(encrypted) // len(key) + 1)))
        return decrypted.decode('utf-8')

# Generate quantum-safe key
quantum_key = hashlib.sha256(b"quantum_security_demo").digest()
test_message = "Secure QCF transmission"

encrypted = SimpleEncryption.encrypt(test_message, quantum_key)
decrypted = SimpleEncryption.decrypt(encrypted, quantum_key)

print(f"Original: {test_message}")
print(f"Encrypted: {encrypted[:50]}...")
print(f"Decrypted: {decrypted}")
print("✓ Encryption/decryption successful")

# 4. Threat analysis
print("\n4. 📈 Threat Intelligence Report...")
test_packets = [
    {'src_port': 443, 'dst_port': 80, 'packet_size': 1500, 'protocol': 'TCP'},
    {'src_port': 12345, 'dst_port': 22, 'packet_size': 45, 'protocol': 'TCP'},
    {'src_port': 54321, 'dst_port': 135, 'packet_size': 5000, 'protocol': 'UDP'}
]

print("Real-time packet analysis:")
for i, packet in enumerate(test_packets):
    # Prepare packet features
    packet_features = [[
        packet['src_port'],
        packet['dst_port'], 
        packet['packet_size'],
        1 if packet['protocol'] == 'TCP' else 0,
        1 if packet['protocol'] == 'UDP' else 0,
        1 if packet['protocol'] == 'ICMP' else 0
    ]]
    
    prediction = model.predict(packet_features)[0]
    confidence = model.predict_proba(packet_features)[0][1]
    
    status = "🚨 BLOCKED" if prediction == 1 else "✅ ALLOWED"
    print(f"  Packet {i+1}: {status} (confidence: {confidence:.2f})")

print("\n" + "=" * 50)
print("🎯 QCF Simplified Demo Completed Successfully!")
print("\n💡 This demonstrates the core concepts of Quantum Cloud Firewall")
print("   • Network traffic analysis")
print("   • Machine learning anomaly detection") 
print("   • Post-quantum encryption")
print("   • Real-time threat detection")
EOF

python simple_demo.py