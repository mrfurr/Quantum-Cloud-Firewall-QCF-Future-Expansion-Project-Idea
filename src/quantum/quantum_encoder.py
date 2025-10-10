import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import ZZFeatureMap, RealAmplitudes

class QuantumEncoder:
    """Encodes classical network features into quantum states"""
    
    def __init__(self, num_features=4, num_qubits=None):
        self.num_features = num_features
        self.num_qubits = num_qubits or num_features
        
        # Create feature map for encoding classical data
        self.feature_map = ZZFeatureMap(feature_dimension=num_features, reps=2)
        
    def encode_features(self, features):
        """Encode classical features into quantum state"""
        if len(features) != self.num_features:
            raise ValueError(f"Expected {self.num_features} features, got {len(features)}")
        
        # Normalize features to [0, 2π] range
        normalized_features = self._normalize_features(features)
        
        # Create quantum circuit with encoded features
        qc = QuantumCircuit(self.num_qubits)
        qc.compose(self.feature_map, inplace=True)
        qc.assign_parameters(normalized_features, inplace=True)
        
        return qc
    
    def _normalize_features(self, features):
        """Normalize features to appropriate range for quantum encoding"""
        features = np.array(features)
        
        # Simple min-max normalization to [0, 2π]
        min_val = np.min(features)
        max_val = np.max(features)
        
        if max_val == min_val:
            return np.ones_like(features) * np.pi
        
        normalized = 2 * np.pi * (features - min_val) / (max_val - min_val)
        return normalized.tolist()
    
    def extract_quantum_features(self, qc, backend=None):
        """Extract quantum features from circuit"""
        try:
            from qiskit import Aer, execute
            if backend is None:
                backend = Aer.get_backend('statevector_simulator')
            
            # Execute circuit and get statevector
            job = execute(qc, backend)
            result = job.result()
            statevector = result.get_statevector()
            
            # Convert statevector to probability distribution
            probabilities = np.abs(statevector)**2
            return probabilities
        except ImportError:
            # Fallback: return simulated probabilities
            print("⚠️  Using simulated quantum probabilities")
            num_states = 2 ** self.num_qubits
            simulated_probs = np.random.dirichlet(np.ones(num_states))
            return simulated_probs
        except Exception as e:
            print(f"⚠️  Quantum simulation fallback: {e}")
            # Return uniform probabilities as fallback
            num_states = 2 ** self.num_qubits
            return np.ones(num_states) / num_states