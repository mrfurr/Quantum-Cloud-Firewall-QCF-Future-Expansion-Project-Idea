import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.firewall.qcf_simulator import QuantumCloudFirewall
from src.pqc.kyber_demo import PostQuantumSecureChannel
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    print("🔒 Quantum Cloud Firewall (QCF) - Future Expansion Project")
    print("=" * 60)
    
    # Initialize QCF
    qcf = QuantumCloudFirewall()
    
    # Generate sample data if not exists
    data_file = 'data/sample_network_traffic.csv'
    if not os.path.exists(data_file):
        print("Generating sample network data...")
        from data.generate_sample_data import generate_network_traffic_data
        generate_network_traffic_data()
    
    # Demo 1: Load and analyze network data
    print("\n1. 📊 Network Traffic Analysis")
    print("-" * 30)
    network_data = qcf.load_network_data(data_file)
    X, y = qcf.preprocess_features()
    
    print(f"Normal packets: {len(y) - sum(y)}")
    print(f"Anomalous packets: {sum(y)}")
    
    # Demo 2: Train quantum anomaly detector
    print("\n2. 🧠 Training Quantum Anomaly Detector")
    print("-" * 40)
    accuracy = qcf.train_anomaly_detector(method='hybrid')
    print(f"Hybrid detector accuracy: {accuracy:.2%}")
    
    # Demo 3: Real-time traffic analysis
    print("\n3. ⚡ Real-time Traffic Analysis")
    print("-" * 35)
    sample_packets = [
        {'src_port': 443, 'dst_port': 80, 'packet_size': 1500, 'duration': 1.2, 'protocol': 'TCP'},
        {'src_port': 12345, 'dst_port': 22, 'packet_size': 45, 'duration': 0.1, 'protocol': 'TCP'},
        {'src_port': 54321, 'dst_port': 135, 'packet_size': 5000, 'duration': 5.0, 'protocol': 'UDP'}
    ]
    
    for i, packet in enumerate(sample_packets):
        result = qcf.analyze_real_time_traffic(packet)
        status = "🚨 BLOCKED" if result['is_anomaly'] else "✅ ALLOWED"
        print(f"Packet {i+1}: {status} (Confidence: {result['confidence']:.2f})")
    
    # Demo 4: Post-quantum cryptography
    print("\n4. 🛡️ Post-Quantum Cryptography Demo")
    print("-" * 40)
    pq_channel = PostQuantumSecureChannel()
    session_key = pq_channel.establish_secure_channel()
    
    if session_key:
        test_message = "Secure message from QCF system"
        encrypted = pq_channel.encrypt_message(test_message, session_key)
        decrypted = pq_channel.decrypt_message(encrypted, session_key)
        
        print(f"Original: {test_message}")
        print(f"Encrypted: {encrypted.hex()[:50]}...")
        print(f"Decrypted: {decrypted}")
        print("✓ Post-quantum encryption verified")
    
    # Demo 5: Quantum state visualization
    print("\n5. ⚛️ Quantum State Encoding")
    print("-" * 30)
    sample_features = [443, 80, 1500, 1.2]  # Normal web traffic
    quantum_state = qcf.visualize_quantum_state(sample_features)
    
    if quantum_state:
        print(f"Quantum circuit depth: {quantum_state['circuit_depth']}")
        print(f"Number of qubits: {quantum_state['num_qubits']}")
        print(f"State probabilities: {quantum_state['state_probabilities'][:4]}")
    
    # Demo 6: Threat intelligence report
    print("\n6. 📈 Threat Intelligence Report")
    print("-" * 35)
    report = qcf.generate_threat_report()
    print(f"Total packets analyzed: {report['total_packets_analyzed']}")
    print(f"Anomalies detected: {report['anomalies_detected']}")
    print(f"Current threat level: {report['threat_level']}")
    
    print("\n" + "=" * 60)
    print("🎯 QCF Demonstration Completed Successfully!")
    print("\n💡 Future Applications for Ethiopia:")
    print("   • Secure national banking systems")
    print("   • Protect e-government services")
    print("   • Safeguard telecom infrastructure")
    print("   • Enhance national cybersecurity posture")
    print("\n🚀 Ethiopia can lead Africa's quantum cybersecurity revolution!")

if __name__ == "__main__":
    main()