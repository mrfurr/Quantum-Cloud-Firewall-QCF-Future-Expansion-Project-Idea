import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.quantum.quantum_encoder import QuantumEncoder

class TestQuantumEncoder(unittest.TestCase):
    
    def setUp(self):
        self.encoder = QuantumEncoder(num_features=4)
    
    def test_feature_encoding(self):
        """Test that features are properly encoded into quantum circuits"""
        features = [100, 200, 1500, 2.5]
        qc = self.encoder.encode_features(features)
        
        self.assertEqual(qc.num_qubits, 4)
        self.assertGreater(qc.depth(), 0)
    
    def test_feature_normalization(self):
        """Test feature normalization to quantum range"""
        features = [0, 100, 500, 1000]
        normalized = self.encoder._normalize_features(features)
        
        self.assertEqual(len(normalized), 4)
        self.assertTrue(all(0 <= x <= 2 * 3.14159 for x in normalized))
    
    def test_quantum_feature_extraction(self):
        """Test extraction of quantum features"""
        features = [443, 80, 1500, 1.2]
        qc = self.encoder.encode_features(features)
        probabilities = self.encoder.extract_quantum_features(qc)
        
        self.assertEqual(len(probabilities), 16)  # 2^4 qubits
        self.assertAlmostEqual(sum(probabilities), 1.0, places=6)

if __name__ == '__main__':
    unittest.main()