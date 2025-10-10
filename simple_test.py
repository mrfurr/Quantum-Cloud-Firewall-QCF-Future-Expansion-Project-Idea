print("🧪 Testing QCF Basic Components...")

try:
    import pandas as pd
    print("✅ pandas: OK")
except ImportError as e:
    print(f"❌ pandas: {e}")

try:
    import numpy as np
    print("✅ numpy: OK")
except ImportError as e:
    print(f"❌ numpy: {e}")

try:
    from src.quantum.quantum_encoder import QuantumEncoder
    print("✅ QuantumEncoder: OK")
    
    # Test basic functionality
    encoder = QuantumEncoder()
    features = [100, 200, 1500, 1.5]
    qc = encoder.encode_features(features)
    print(f"✅ Quantum circuit created: {qc.num_qubits} qubits")
    
except Exception as e:
    print(f"❌ QuantumEncoder: {e}")

try:
    from src.pqc.kyber_demo import PostQuantumSecureChannel
    print("✅ PostQuantumSecureChannel: OK")
except Exception as e:
    print(f"❌ PostQuantumSecureChannel: {e}")

print("\n🎯 Basic component test completed!")
