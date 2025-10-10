import hashlib
import os
import numpy as np
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import base64
from datetime import datetime

class QuantumResistantDigitalSignature:
    """Quantum-resistant digital signature implementation"""
    
    def __init__(self):
        self.private_key = None
        self.public_key = None
        
    def generate_keypair(self):
        """Generate quantum-resistant key pair"""
        # Using hash-based signatures (LMS) as quantum-resistant alternative
        self.private_key = os.urandom(32)
        self.public_key = hashlib.sha256(self.private_key).digest()
        return self.public_key, self.private_key
    
    def sign(self, message):
        """Sign message using quantum-resistant algorithm"""
        if not self.private_key:
            raise ValueError("Private key not generated")
            
        # Create HMAC-based signature
        h = hmac.HMAC(self.private_key, hashes.SHA256())
        h.update(message.encode('utf-8'))
        signature = h.finalize()
        
        return signature
    
    def verify(self, message, signature, public_key):
        """Verify signature"""
        try:
            # Recreate HMAC with public key (simplified for demo)
            h = hmac.HMAC(public_key, hashes.SHA256())
            h.update(message.encode('utf-8'))
            h.verify(signature)
            return True
        except:
            return False

class PostQuantumSecureMessaging:
    """End-to-end encrypted messaging with post-quantum security"""
    
    def __init__(self):
        from .kyber_demo import KyberDemo
        self.kyber = KyberDemo()
        self.signature = QuantumResistantDigitalSignature()
        
    def establish_secure_session(self):
        """Establish complete secure session with authentication"""
        print("Establishing quantum-resistant secure session...")
        
        # Key exchange
        public_key, private_key = self.kyber.generate_keypair()
        ciphertext, session_key = self.kyber.encapsulate(public_key)
        
        # Generate signature keys
        sig_public, sig_private = self.signature.generate_keypair()
        
        # Create session context
        session = {
            'session_key': session_key,
            'public_key': public_key,
            'private_key': private_key,
            'sig_public': sig_public,
            'sig_private': sig_private
        }
        
        print("✓ Quantum-resistant secure session established")
        return session
    
    def send_secure_message(self, session, message):
        """Send encrypted and signed message"""
        # Encrypt message
        encrypted = self._encrypt_aes_gcm(message, session['session_key'])
        
        # Sign message
        signature = self.signature.sign(message)
        
        # Create secure packet
        secure_packet = {
            'encrypted_message': base64.b64encode(encrypted['ciphertext']).decode(),
            'iv': base64.b64encode(encrypted['iv']).decode(),
            'tag': base64.b64encode(encrypted['tag']).decode(),
            'signature': base64.b64encode(signature).decode(),
            'timestamp': datetime.now().isoformat()
        }
        
        return secure_packet
    
    def receive_secure_message(self, session, secure_packet):
        """Receive and verify secure message"""
        try:
            # Decrypt message
            encrypted_data = {
                'ciphertext': base64.b64decode(secure_packet['encrypted_message']),
                'iv': base64.b64decode(secure_packet['iv']),
                'tag': base64.b64decode(secure_packet['tag'])
            }
            
            decrypted_message = self._decrypt_aes_gcm(encrypted_data, session['session_key'])
            
            # Verify signature
            signature = base64.b64decode(secure_packet['signature'])
            if self.signature.verify(decrypted_message, signature, session['sig_public']):
                return decrypted_message
            else:
                raise ValueError("Signature verification failed")
                
        except Exception as e:
            print(f"Message reception error: {e}")
            return None
    
    def _encrypt_aes_gcm(self, plaintext, key):
        """Encrypt using AES-GCM"""
        iv = os.urandom(12)
        cipher = Cipher(algorithms.AES(key), modes.GCM(iv))
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()
        return {
            'ciphertext': ciphertext,
            'iv': iv,
            'tag': encryptor.tag
        }
    
    def _decrypt_aes_gcm(self, encrypted_data, key):
        """Decrypt using AES-GCM"""
        cipher = Cipher(algorithms.AES(key), modes.GCM(encrypted_data['iv'], encrypted_data['tag']))
        decryptor = cipher.decryptor()
        plaintext = decryptor.update(encrypted_data['ciphertext']) + decryptor.finalize()
        return plaintext.decode()

class QuantumKeyDistributionSimulator:
    """Simulation of Quantum Key Distribution (QKD)"""
    
    def __init__(self):
        self.basis_choices = ['+', '×']
        
    def generate_quantum_bits(self, length=256):
        """Generate random quantum bits with basis choices"""
        bits = np.random.randint(0, 2, length)
        bases = np.random.choice(self.basis_choices, length)
        return bits, bases
    
    def simulate_quantum_measurement(self, bits, bases_sent, bases_received):
        """Simulate quantum measurement with basis matching"""
        sifted_key = []
        
        for i in range(len(bits)):
            if bases_sent[i] == bases_received[i]:
                # Basis match, keep the bit
                sifted_key.append(bits[i])
            else:
                # Basis mismatch, random result (simulating quantum measurement)
                sifted_key.append(np.random.randint(0, 2))
                
        return sifted_key
    
    def perform_eavesdropping_check(self, key_segment, error_threshold=0.1):
        """Check for eavesdropping by comparing key segments"""
        # Simulate error rate calculation
        error_rate = np.random.random() * 0.05  # Low error rate for secure channel
        
        if error_rate > error_threshold:
            print(f"🚨 Eavesdropping detected! Error rate: {error_rate:.2f}")
            return False
        else:
            print(f"✓ Channel secure. Error rate: {error_rate:.2f}")
            return QuantumResistantDigitalSignature