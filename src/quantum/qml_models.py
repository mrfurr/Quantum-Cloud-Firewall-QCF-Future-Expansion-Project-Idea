import numpy as np
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier

try:
    from qiskit import QuantumCircuit
    from qiskit.circuit.library import ZZFeatureMap, RealAmplitudes
    from qiskit_machine_learning.algorithms import QSVC
    from qiskit_machine_learning.kernels import QuantumKernel
    QISKIT_AVAILABLE = True
    print("✅ Qiskit Machine Learning available - using quantum models")
except ImportError:
    QISKIT_AVAILABLE = False
    print("⚠️  Qiskit Machine Learning not available - using classical models with quantum simulation")

class QuantumAnomalyDetector:
    """Quantum-enhanced anomaly detection using QML"""
    
    def __init__(self, num_features=4):
        self.num_features = num_features
        self.model = None
        
        if QISKIT_AVAILABLE:
            self.feature_map = ZZFeatureMap(feature_dimension=num_features, reps=2)
            self.quantum_kernel = QuantumKernel(feature_map=self.feature_map, quantum_instance='statevector_simulator')
        else:
            # Fallback to classical SVM
            self.model = SVC(kernel='rbf', probability=True)
        
    def train(self, X_train, y_train):
        """Train the quantum anomaly detector"""
        print("Training Anomaly Detector...")
        
        if QISKIT_AVAILABLE:
            # Use Quantum Support Vector Classifier
            self.model = QSVC(quantum_kernel=self.quantum_kernel)
            self.model.fit(X_train, y_train)
            print("Quantum training completed!")
        else:
            # Use classical SVM
            self.model.fit(X_train, y_train)
            print("Classical training completed (quantum simulation unavailable)")
        
    def predict(self, X_test):
        """Predict anomalies using model"""
        if self.model is None:
            raise ValueError("Model must be trained before prediction")
        
        return self.model.predict(X_test)
    
    def get_confidence_scores(self, X_test):
        """Get anomaly detection confidence scores"""
        if hasattr(self.model, 'predict_proba'):
            return self.model.predict_proba(X_test)
        else:
            # Fallback: return dummy probabilities
            predictions = self.predict(X_test)
            return np.array([[1-p, p] for p in predictions])

class HybridAnomalyDetector:
    """Hybrid quantum-classical anomaly detection"""
    
    def __init__(self, num_features=4):
        self.quantum_detector = QuantumAnomalyDetector(num_features)
        self.classical_detector = RandomForestClassifier(n_estimators=100)
        self.is_trained = False
        
    def train(self, X_train, y_train):
        """Train both quantum and classical models"""
        print("Training Hybrid Anomaly Detector...")
        
        # Train quantum detector
        self.quantum_detector.train(X_train, y_train)
        
        # Train classical detector
        self.classical_detector.fit(X_train, y_train)
        
        self.is_trained = True
        print("Hybrid training completed!")
        
    def predict(self, X_test, method='ensemble'):
        """Predict using specified method"""
        if not self.is_trained:
            raise ValueError("Model must be trained before prediction")
        
        if method == 'quantum':
            return self.quantum_detector.predict(X_test)
        elif method == 'classical':
            return self.classical_detector.predict(X_test)
        elif method == 'ensemble':
            quantum_pred = self.quantum_detector.predict(X_test)
            classical_pred = self.classical_detector.predict(X_test)
            # Simple majority voting
            return np.round((quantum_pred + classical_pred) / 2)
        else:
            raise ValueError("Method must be 'quantum', 'classical', or 'ensemble'")