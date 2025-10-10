import re
import ipaddress
from datetime import datetime, timedelta
import json
import numpy as np

class AdvancedFirewallRules:
    """Advanced firewall rules with quantum-enhanced decision making"""
    
    def __init__(self):
        self.rules = self._load_default_rules()
        self.quantum_threshold = 0.7
        self.suspicious_activities = []
        
    def _load_default_rules(self):
        """Load default firewall rules"""
        return [
            {
                'name': 'Port Scan Detection',
                'condition': self._detect_port_scan,
                'action': 'BLOCK',
                'priority': 'HIGH'
            },
            {
                'name': 'DDoS Protection',
                'condition': self._detect_ddos,
                'action': 'RATE_LIMIT',
                'priority': 'CRITICAL'
            },
            {
                'name': 'Suspicious Protocol',
                'condition': self._detect_suspicious_protocol,
                'action': 'ALERT',
                'priority': 'MEDIUM'
            },
            {
                'name': 'Geolocation Filter',
                'condition': self._check_geolocation,
                'action': 'BLOCK',
                'priority': 'MEDIUM'
            },
            {
                'name': 'Quantum Anomaly Rule',
                'condition': self._quantum_anomaly_check,
                'action': 'QUARANTINE',
                'priority': 'HIGH'
            }
        ]
    
    def evaluate_packet(self, packet_data, quantum_confidence):
        """Evaluate packet against all rules"""
        actions = []
        
        for rule in self.rules:
            if rule['condition'](packet_data, quantum_confidence):
                actions.append({
                    'rule': rule['name'],
                    'action': rule['action'],
                    'priority': rule['priority'],
                    'timestamp': datetime.now()
                })
                
        return actions
    
    def _detect_port_scan(self, packet_data, quantum_confidence):
        """Detect port scanning activity"""
        # Check for multiple connection attempts to different ports
        suspicious_ports = [21, 23, 135, 139, 445, 1433, 3389]
        
        if (packet_data.get('dst_port', 0) in suspicious_ports and
            packet_data.get('packet_size', 0) < 100):
            self._log_suspicious_activity('Port Scan', packet_data)
            return True
        return False
    
    def _detect_ddos(self, packet_data, quantum_confidence):
        """Detect DDoS attack patterns"""
        # Simplified DDoS detection
        recent_packets = [p for p in self.suspicious_activities 
                         if datetime.now() - p['timestamp'] < timedelta(seconds=10)]
        
        if len(recent_packets) > 100:  # High packet rate
            self._log_suspicious_activity('DDoS Attack', packet_data)
            return True
        return False
    
    def _detect_suspicious_protocol(self, packet_data, quantum_confidence):
        """Detect suspicious protocol usage"""
        suspicious_protocols = ['ICMP', 'IGMP', 'GRE']
        
        if packet_data.get('protocol') in suspicious_protocols:
            if packet_data.get('packet_size', 0) > 1500:  # Large ICMP packets
                self._log_suspicious_activity('Suspicious Protocol', packet_data)
                return True
        return False
    
    def _check_geolocation(self, packet_data, quantum_confidence):
        """Check if traffic originates from suspicious locations"""
        suspicious_ranges = [
            '192.168.0.0/16',
            '10.0.0.0/8',
            '172.16.0.0/12'
        ]
        
        src_ip = packet_data.get('src_ip', '')
        try:
            ip = ipaddress.ip_address(src_ip)
            for range_str in suspicious_ranges:
                if ip in ipaddress.ip_network(range_str):
                    return False  # Allow internal traffic
                    
            # Block specific external IP ranges (example)
            if src_ip.startswith('203.0.113.'):  # Example block range
                self._log_suspicious_activity('Suspicious Geolocation', packet_data)
                return True
                
        except ValueError:
            pass
            
        return False
    
    def _quantum_anomaly_check(self, packet_data, quantum_confidence):
        """Use quantum confidence score for decision making"""
        if quantum_confidence > self.quantum_threshold:
            self._log_suspicious_activity('Quantum Anomaly', packet_data)
            return True
        return False
    
    def _log_suspicious_activity(self, activity_type, packet_data):
        """Log suspicious activities for analysis"""
        activity = {
            'type': activity_type,
            'timestamp': datetime.now(),
            'packet_data': packet_data,
            'action_taken': 'Logged'
        }
        self.suspicious_activities.append(activity)
        
        # Keep only recent activities (last hour)
        one_hour_ago = datetime.now() - timedelta(hours=1)
        self.suspicious_activities = [
            act for act in self.suspicious_activities 
            if act['timestamp'] > one_hour_ago
        ]
    
    def get_security_report(self):
        """Generate security report based on rule violations"""
        report = {
            'total_activities': len(self.suspicious_activities),
            'recent_activities': [],
            'threat_categories': {}
        }
        
        # Get activities from last 15 minutes
        fifteen_min_ago = datetime.now() - timedelta(minutes=15)
        recent = [act for act in self.suspicious_activities 
                 if act['timestamp'] > fifteen_min_ago]
        
        report['recent_activities'] = recent[-10:]  # Last 10 activities
        
        # Count by type
        for activity in recent:
            activity_type = activity['type']
            report['threat_categories'][activity_type] = \
                report['threat_categories'].get(activity_type, 0) + 1
        
        return report  