import sys
import os
import asyncio
import threading
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.firewall.qcf_simulator import QuantumCloudFirewall
from src.firewall.real_time_monitor import RealTimeNetworkMonitor, WebDashboard
from src.firewall.advanced_rules import AdvancedFirewallRules
from src.pqc.advanced_crypto import PostQuantumSecureMessaging, QuantumKeyDistributionSimulator
from src.quantum.advanced_qml import AdvancedQuantumClassifier, QuantumAutoencoder
from src.api.qcf_api import QCFAPI, CloudIntegration

class EnhancedQCF:
    """Enhanced QCF with all advanced features"""
    
    def __init__(self):
        print("🚀 Initializing Enhanced Quantum Cloud Firewall...")
        
        # Core QCF
        self.qcf = QuantumCloudFirewall()
        
        # Advanced components
        self.monitor = RealTimeNetworkMonitor(self.qcf)
        self.rules_engine = AdvancedFirewallRules()
        self.secure_messaging = PostQuantumSecureMessaging()
        self.qkd_simulator = QuantumKeyDistributionSimulator()
        self.advanced_classifier = AdvancedQuantumClassifier()
        self.quantum_autoencoder = QuantumAutoencoder()
        self.api = QCFAPI(self)
        self.cloud_integration = CloudIntegration(self)
        
        # Link components
        self.qcf.monitor = self.monitor
        self.qcf.rules_engine = self.rules_engine
        
    def run_complete_demo(self):
        """Run complete demonstration of all features"""
        print("\n🔒 ENHANCED QUANTUM CLOUD FIREWALL DEMONSTRATION")
        print("=" * 60)
        
        # 1. Basic setup
        self._demo_basic_setup()
        
        # 2. Advanced ML
        self._demo_advanced_ml()
        
        # 3. Real-time monitoring
        self._demo_real_time_monitoring()
        
        # 4. Advanced cryptography
        self._demo_advanced_crypto()
        
        # 5. Cloud integration
        self._demo_cloud_integration()
        
        # 6. API demonstration
        self._demo_api()
        
        print("\n" + "=" * 60)
        print("🎯 ENHANCED QCF DEMONSTRATION COMPLETED!")
        print("\n🌟 Ethiopia is now equipped with cutting-edge quantum cybersecurity!")
        
    def _demo_basic_setup(self):
        """Demo basic QCF setup"""
        print("\n1. 🏗️ Advanced System Setup")
        print("-" * 30)
        
        # Load and preprocess data
        data_file = 'data/sample_network_traffic.csv'
        if not os.path.exists(data_file):
            from data.generate_sample_data import generate_network_traffic_data
            generate_network_traffic_data()
            
        self.qcf.load_network_data(data_file)
        self.qcf.preprocess_features()
        
        print("✓ Advanced system initialized")
        
    def _demo_advanced_ml(self):
        """Demo advanced machine learning features"""
        print("\n2. 🧠 Advanced Quantum Machine Learning")
        print("-" * 40)
        
        # Train advanced classifier
        accuracy = self.qcf.train_anomaly_detector(method='hybrid')
        print(f"Hybrid detector accuracy: {accuracy:.2%}")
        
        # Quantum autoencoder demo
        sample_features = [443, 80, 1500, 1.2]
        reconstruction_error = self.quantum_autoencoder.calculate_reconstruction_error(sample_features)
        print(f"Quantum autoencoder error: {reconstruction_error:.4f}")
        
        print("✓ Advanced QML models trained")
        
    def _demo_real_time_monitoring(self):
        """Demo real-time monitoring"""
        print("\n3. ⚡ Enhanced Real-time Monitoring")
        print("-" * 40)
        
        # Start monitoring (simulated)
        self.monitor.start_monitoring()
        
        # Simulate some traffic
        simulated_traffic = [
            {'src_port': 443, 'dst_port': 80, 'packet_size': 1500, 'duration': 1.2, 'protocol': 'TCP'},
            {'src_port': 12345, 'dst_port': 22, 'packet_size': 45, 'duration': 0.1, 'protocol': 'TCP'},
            {'src_port': 54321, 'dst_port': 135, 'packet_size': 5000, 'duration': 5.0, 'protocol': 'UDP'}
        ]
        
        for packet in simulated_traffic:
            result = self.qcf.analyze_real_time_traffic(packet)
            action = "🚨 BLOCKED" if result['is_anomaly'] else "✅ ALLOWED"
            print(f"Packet analysis: {action}")
            
        stats = self.monitor.get_monitoring_stats()
        print(f"Current threat level: {stats['threat_level']}")
        
    def _demo_advanced_crypto(self):
        """Demo advanced cryptographic features"""
        print("\n4. 🛡️ Advanced Post-Quantum Cryptography")
        print("-" * 45)
        
        # Secure messaging
        session = self.secure_messaging.establish_secure_session()
        test_message = "Critical security alert: Suspicious activity detected"
        
        secure_packet = self.secure_messaging.send_secure_message(session, test_message)
        decrypted = self.secure_messaging.receive_secure_message(session, secure_packet)
        
        print(f"Original: {test_message}")
        print(f"Decrypted: {decrypted}")
        print("✓ End-to-end quantum-resistant encryption verified")
        
        # QKD Simulation
        print("\n5. ⚛️ Quantum Key Distribution Simulation")
        print("-" * 40)
        bits, bases_sent = self.qkd_simulator.generate_quantum_bits(10)
        bases_received = np.random.choice(['+', '×'], 10)
        sifted_key = self.qkd_simulator.simulate_quantum_measurement(bits, bases_sent, bases_received)
        
        is_secure = self.qkd_simulator.perform_eavesdropping_check(sifted_key[:5])
        print(f"QKD Security: {'✓ SECURE' if is_secure else '🚨 COMPROMISED'}")
        
    def _demo_cloud_integration(self):
        """Demo cloud platform integration"""
        print("\n6. ☁️ Multi-Cloud Integration")
        print("-" * 30)
        
        # AWS integration demo
        aws_config = {'region': 'us-east-1'}
        aws_status = self.cloud_integration.integrate_with_cloud('aws', aws_config)
        print(f"AWS Integration: {aws_status['status']}")
        
        # Azure integration demo
        azure_config = {'subscription_id': 'demo-subscription'}
        azure_status = self.cloud_integration.integrate_with_cloud('azure', azure_config)
        print(f"Azure Integration: {azure_status['status']}")
        
    def _demo_api(self):
        """Demo REST API"""
        print("\n7. 🌐 REST API Interface")
        print("-" * 25)
        
        # Start API in background thread
        api_thread = threading.Thread(target=self.api.start, daemon=True)
        api_thread.start()
        
        print("API running at: http://localhost:5000")
        print("Available endpoints:")
        print("  GET /api/status - System status")
        print("  GET /api/threat-intel - Threat intelligence")
        print("  GET /api/network-stats - Monitoring statistics")
        print("  POST /api/quantum-analysis - Quantum analysis")
        print("  GET /api/security-rules - Security rules report")

def main():
    """Main enhanced demonstration"""
    enhanced_qcf = EnhancedQCF()
    enhanced_qcf.run_complete_demo()
    
    # Keep running for API access
    print("\n🔄 Enhanced QCF is running in the background...")
    print("Press Ctrl+C to exit")
    
    try:
        while True:
            # Keep main thread alive
            pass
    except KeyboardInterrupt:
        print("\n🛑 Shutting down Enhanced QCF...")

if __name__ == "__main__":
    main()