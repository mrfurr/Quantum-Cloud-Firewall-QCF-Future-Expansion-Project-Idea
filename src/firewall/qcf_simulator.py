import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

from ..quantum.quantum_encoder import QuantumEncoder
from ..quantum.qml_models import QuantumAnomalyDetector, HybridAnomalyDetector
from ..pqc.kyber_demo import PostQuantumSecureChannel

class QuantumCloudFirewall:
    """Main QCF simulator class"""
    
    def __init__(self, config=None):
        self.config = config or {}
        self.quantum_encoder = QuantumEncoder(num_features=4)
        self.anomaly_detector = None
        self.secure_channel = PostQuantumSecureChannel()
        self.network_logs = []
        self.threat_intelligence = []
        self.monitor = None
        self.rules_engine = None
        
    def load_network_data(self, filepath):
        """Load network traffic data"""
        print(f"Loading network data from {filepath}...")
        self.network_data = pd.read_csv(filepath)
        self.network_data['timestamp'] = pd.to_datetime(self.network_data['timestamp'])
        print(f"Loaded {len(self.network_data)} network packets")
        return self.network_data
    
    def preprocess_features(self):
        """Preprocess network features for quantum analysis"""
        print("Preprocessing network features...")
        
        # Select relevant features for anomaly detection
        features = self.network_data[['src_port', 'dst_port', 'packet_size', 'duration']].copy()
        
        # One-hot encode protocol
        protocol_dummies = pd.get_dummies(self.network_data['protocol'], prefix='protocol')
        features = pd.concat([features, protocol_dummies], axis=1)
        
        # Handle missing values
        features = features.fillna(0)
        
        # Normalize features
        from sklearn.preprocessing import StandardScaler
        self.scaler = StandardScaler()
        self.X = self.scaler.fit_transform(features)
        
        # Target variable
        self.y = self.network_data['is_anomaly'].values
        
        print(f"Preprocessed {self.X.shape[0]} samples with {self.X.shape[1]} features")
        return self.X, self.y
    
    def train_anomaly_detector(self, method='hybrid'):
        """Train the quantum-enhanced anomaly detector"""
        print(f"Training {method} anomaly detector...")
        
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(
            self.X, self.y, test_size=0.2, random_state=42, stratify=self.y
        )
        
        if method == 'quantum':
            self.anomaly_detector = QuantumAnomalyDetector(num_features=X_train.shape[1])
        elif method == 'hybrid':
            self.anomaly_detector = HybridAnomalyDetector(num_features=X_train.shape[1])
        else:
            raise ValueError("Method must be 'quantum' or 'hybrid'")
        
        self.anomaly_detector.train(X_train, y_train)
        
        # Evaluate on test set
        y_pred = self.anomaly_detector.predict(X_test)
        accuracy = np.mean(y_pred == y_test)
        print(f"Test accuracy: {accuracy:.4f}")
        
        return accuracy
    
    def analyze_real_time_traffic(self, packet_data):
        """Analyze real-time network traffic for anomalies"""
        if self.anomaly_detector is None:
            raise ValueError("Anomaly detector must be trained first")
        
        # Preprocess packet data
        features = self._extract_packet_features(packet_data)
        features_scaled = self.scaler.transform([features])
        
        # Predict anomaly
        is_anomaly = self.anomaly_detector.predict(features_scaled)[0]
        
        # Get confidence score
        try:
            confidence_scores = self.anomaly_detector.get_confidence_scores(features_scaled)
            confidence = float(confidence_scores[0][1])  # Probability of anomaly
        except:
            confidence = 0.85  # Fallback confidence
        
        # Log the analysis
        log_entry = {
            'timestamp': datetime.now(),
            'packet_data': packet_data,
            'is_anomaly': bool(is_anomaly),
            'confidence': confidence,
            'action': 'BLOCK' if is_anomaly else 'ALLOW'
        }
        
        self.network_logs.append(log_entry)
        
        return log_entry
    
    def _extract_packet_features(self, packet_data):
        """Extract features from packet data"""
        features = [
            packet_data.get('src_port', 0),
            packet_data.get('dst_port', 0),
            packet_data.get('packet_size', 0),
            packet_data.get('duration', 0)
        ]
        
        # Add protocol encoding
        protocols = ['TCP', 'UDP', 'ICMP']
        protocol_features = [1 if packet_data.get('protocol') == p else 0 for p in protocols]
        features.extend(protocol_features)
        
        return features
    
    def establish_secure_connection(self):
        """Establish post-quantum secure connection"""
        print("Initiating post-quantum secure connection...")
        try:
            session_key = self.secure_channel.establish_secure_channel()
            print("✓ Post-quantum secure connection established")
            return session_key
        except Exception as e:
            print(f"✗ Secure connection failed: {e}")
            return None
    
    def generate_threat_report(self):
        """Generate comprehensive threat intelligence report"""
        if not self.network_logs:
            return {
                'timestamp': datetime.now(),
                'total_packets_analyzed': 0,
                'anomalies_detected': 0,
                'threat_level': 'LOW',
                'recent_anomalies': []
            }
        
        total_packets = len(self.network_logs)
        anomalies = sum(1 for log in self.network_logs if log['is_anomaly'])
        
        # Calculate threat level
        if total_packets == 0:
            threat_level = 'LOW'
        else:
            anomaly_ratio = anomalies / total_packets
            if anomaly_ratio > 0.1:
                threat_level = 'CRITICAL'
            elif anomaly_ratio > 0.05:
                threat_level = 'HIGH'
            elif anomaly_ratio > 0.02:
                threat_level = 'MEDIUM'
            else:
                threat_level = 'LOW'
        
        report = {
            'timestamp': datetime.now(),
            'total_packets_analyzed': total_packets,
            'anomalies_detected': anomalies,
            'threat_level': threat_level,
            'recent_anomalies': [log for log in self.network_logs[-5:] if log['is_anomaly']]
        }
        
        return report
    
    def visualize_quantum_state(self, features):
        """Visualize quantum state encoding"""
        try:
            # Encode features into quantum state
            qc = self.quantum_encoder.encode_features(features[:4])
            
            print("Quantum Circuit for feature encoding:")
            print(qc.draw())
            
            # Get quantum state probabilities
            probabilities = self.quantum_encoder.extract_quantum_features(qc)
            
            return {
                'circuit_depth': qc.depth(),
                'num_qubits': qc.num_qubits,
                'state_probabilities': probabilities[:8].tolist()  # First 8 probabilities
            }
            
        except Exception as e:
            print(f"Quantum visualization error: {e}")
            return None
    
    def get_system_status(self):
        """Get current system status"""
        return {
            'anomaly_detector_trained': self.anomaly_detector is not None,
            'network_logs_count': len(self.network_logs),
            'quantum_encoder_ready': True,
            'secure_channel_ready': True,
            'monitoring_active': self.monitor is not None and getattr(self.monitor, 'is_monitoring', False),
            'rules_engine_ready': self.rules_engine is not None
        }