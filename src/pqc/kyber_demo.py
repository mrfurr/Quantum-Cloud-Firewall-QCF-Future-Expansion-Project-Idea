import numpy as np
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.asymmetric import rsa, padding
import hashlib
import os

class KyberDemo:
    """Demonstration of Kyber-like key exchange mechanism"""
    
    def __init__(self, security_level=512):
        self.security_level = security_level
        
    def generate_keypair(self):
        """Generate a demonstration key pair (simplified Kyber)"""
        # In real Kyber, this would use lattice-based cryptography
        # For demonstration, we'll use a simplified approach
        
        # Simulate lattice-based key generation
        private_key = os.urandom(32)  # 256-bit private key
        public_key = hashlib.sha256(private_key).digest()  # Simplified public key
        
        return public_key, private_key
    
    def encapsulate(self, public_key):
        """Key encapsulation (simplified Kyber)"""
        # Generate random symmetric key
        symmetric_key = os.urandom(32)
        
        # "Encrypt" using public key (simplified)
        # In real Kyber, this would use lattice-based encryption
        ciphertext = self._simulate_encryption(public_key, symmetric_key)
        
        return ciphertext, symmetric_key
    
    def decapsulate(self, ciphertext, private_key):
        """Key decapsulation (simplified Kyber)"""
        # "Decrypt" using private key (simplified)
        symmetric_key = self._simulate_decryption(ciphertext, private_key)
        
        return symmetric_key
    
    def _simulate_encryption(self, public_key, data):
        """Simulate lattice-based encryption"""
        # Use the public key as a one-time pad
        # Pad the public key to match data length
        extended_key = (public_key * (len(data) // len(public_key) + 1))[:len(data)]
        encrypted = bytes(a ^ b for a, b in zip(extended_key, data))
        return encrypted
    
    def _simulate_decryption(self, ciphertext, private_key):
        """Simulate lattice-based decryption"""
        # Use the private key to derive the same extended key
        # Since public_key = hash(private_key), we need to be consistent
        public_key = hashlib.sha256(private_key).digest()
        extended_key = (public_key * (len(ciphertext) // len(public_key) + 1))[:len(ciphertext)]
        decrypted = bytes(a ^ b for a, b in zip(extended_key, ciphertext))
        return decrypted

class PostQuantumSecureChannel:
    """Demonstration of post-quantum secure communication"""
    
    def __init__(self):
        self.kyber = KyberDemo()
        
    def establish_secure_channel(self):
        """Establish a post-quantum secure channel"""
        print("Establishing post-quantum secure channel...")
        
        # Server generates key pair
        server_public, server_private = self.kyber.generate_keypair()
        print("Server key pair generated")
        
        # Client encapsulates symmetric key
        ciphertext, symmetric_key = self.kyber.encapsulate(server_public)
        print("Symmetric key encapsulated")
        
        # Server decapsulates symmetric key
        recovered_key = self.kyber.decapsulate(ciphertext, server_private)
        print("Symmetric key decapsulated")
        
        # Verify keys match
        if symmetric_key == recovered_key:
            print("✓ Secure channel established successfully!")
            return symmetric_key
        else:
            print(f"Key mismatch: original={symmetric_key.hex()[:16]}..., recovered={recovered_key.hex()[:16]}...")
            raise ValueError("Key exchange failed")
    
    def encrypt_message(self, message, key):
        """Encrypt message using established key"""
        # Simple XOR encryption for demonstration
        message_bytes = message.encode('utf-8')
        extended_key = (key * (len(message_bytes) // len(key) + 1))[:len(message_bytes)]
        encrypted = bytes(m ^ k for m, k in zip(message_bytes, extended_key))
        return encrypted
    
    def decrypt_message(self, encrypted_message, key):
        """Decrypt message using established key"""
        extended_key = (key * (len(encrypted_message) // len(key) + 1))[:len(encrypted_message)]
        decrypted = bytes(e ^ k for e, k in zip(encrypted_message, extended_key))
        return decrypted.decode('utf-8')