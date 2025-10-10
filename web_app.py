#!/usr/bin/env python3
"""
QCF Web Service - Full Deployment Version
"""

import sys
import os
import threading
import time
import json
from datetime import datetime
from flask import Flask, render_template, jsonify, request
import pandas as pd
import numpy as np

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.firewall.qcf_simulator import QuantumCloudFirewall
from src.firewall.real_time_monitor import RealTimeNetworkMonitor
from src.firewall.advanced_rules import AdvancedFirewallRules
from src.api.qcf_api import QCFAPI

class QCFWebService:
    """Full QCF Web Service with Dashboard and API"""
    
    def __init__(self):
        self.app = Flask(__name__)
        self.qcf = QuantumCloudFirewall()
        self.monitor = RealTimeNetworkMonitor(self.qcf)
        self.rules_engine = AdvancedFirewallRules()
        self.is_running = False
        self.stats_history = []
        
        # Link components
        self.qcf.monitor = self.monitor
        self.qcf.rules_engine = self.rules_engine
        
        # Setup routes
        self.setup_routes()
        
        # Load and train model
        self.initialize_system()
    
    def initialize_system(self):
        """Initialize QCF system with training data"""
        print("🔄 Initializing QCF System...")
        
        # Load and preprocess data
        data_file = 'data/sample_network_traffic.csv'
        if not os.path.exists(data_file):
            from data.generate_sample_data import generate_network_traffic_data
            generate_network_traffic_data()
            
        self.qcf.load_network_data(data_file)
        self.qcf.preprocess_features()
        accuracy = self.qcf.train_anomaly_detector(method='hybrid')
        
        print(f"✅ QCF System Ready! Model Accuracy: {accuracy:.2%}")
    
    def setup_routes(self):
        """Setup web application routes"""
        
        @self.app.route('/')
        def dashboard():
            return render_template('dashboard.html')
        
        @self.app.route('/api/status')
        def api_status():
            return jsonify({
                'status': 'operational',
                'system': 'Quantum Cloud Firewall',
                'version': '1.0.0',
                'uptime': 'Running',
                'quantum_ready': True,
                'timestamp': datetime.now().isoformat()
            })
        
        @self.app.route('/api/stats')
        def api_stats():
            stats = self.monitor.get_monitoring_stats()
            # Add to history (keep last 50 entries)
            self.stats_history.append({
                'timestamp': datetime.now().isoformat(),
                **stats
            })
            self.stats_history = self.stats_history[-50:]
            
            return jsonify(stats)
        
        @self.app.route('/api/threats')
        def api_threats():
            report = self.qcf.generate_threat_report()
            rules_report = self.rules_engine.get_security_report()
            return jsonify({
                'threat_report': report,
                'rules_report': rules_report
            })
        
        @self.app.route('/api/analyze', methods=['POST'])
        def api_analyze():
            try:
                data = request.get_json()
                packet_data = data.get('packet', {})
                
                # Analyze packet
                result = self.qcf.analyze_real_time_traffic(packet_data)
                
                # Apply firewall rules
                rule_actions = self.rules_engine.evaluate_packet(
                    packet_data, 
                    result['confidence']
                )
                
                return jsonify({
                    'analysis': result,
                    'rule_actions': rule_actions,
                    'timestamp': datetime.now().isoformat()
                })
                
            except Exception as e:
                return jsonify({'error': str(e)}), 400
        
        @self.app.route('/api/history')
        def api_history():
            return jsonify(self.stats_history)
        
        @self.app.route('/api/start_monitoring', methods=['POST'])
        def api_start_monitoring():
            if not self.is_running:
                self.monitor.start_monitoring()
                self.is_running = True
                return jsonify({'status': 'monitoring_started'})
            return jsonify({'status': 'already_running'})
        
        @self.app.route('/api/stop_monitoring', methods=['POST'])
        def api_stop_monitoring():
            if self.is_running:
                self.monitor.stop_monitoring()
                self.is_running = False
                return jsonify({'status': 'monitoring_stopped'})
            return jsonify({'status': 'not_running'})
    
    def run(self, host='0.0.0.0', port=5000, debug=False):
        """Run the web service"""
        print(f"🚀 Starting QCF Web Service on http://{host}:{port}")
        print("📊 Dashboard available at: http://localhost:5000")
        print("🔗 API endpoints available at: /api/*")
        print("⏹️  Press Ctrl+C to stop the service")
        
        self.app.run(host=host, port=port, debug=debug)

def simulate_network_traffic(monitor):
    """Simulate background network traffic for demo"""
    import random
    import time
    
    while True:
        time.sleep(3)  # Generate traffic every 3 seconds
        
        # Simulate random packets
        packets = []
        num_packets = random.randint(1, 5)
        
        for _ in range(num_packets):
            packet = {
                'timestamp': datetime.now().isoformat(),
                'src_ip': f"192.168.1.{random.randint(1, 255)}",
                'dst_ip': f"10.0.0.{random.randint(1, 255)}",
                'src_port': random.randint(1024, 65535),
                'dst_port': random.choice([80, 443, 22, 53, 21, 135]),
                'protocol': random.choice(['TCP', 'UDP']),
                'packet_size': random.randint(64, 1500),
                'duration': random.uniform(0.1, 5.0),
                'flags': random.choice(['ACK', 'SYN', 'FIN'])
            }
            packets.append(packet)
        
        # Add packets to monitor (simulate capture)
        for packet in packets:
            monitor.packet_queue.put(packet)

if __name__ == "__main__":
    # Create and run web service
    web_service = QCFWebService()
    
    # Start background traffic simulation
    traffic_thread = threading.Thread(
        target=simulate_network_traffic, 
        args=(web_service.monitor,),
        daemon=True
    )
    traffic_thread.start()
    
    # Start monitoring
    web_service.monitor.start_monitoring()
    web_service.is_running = True
    
    # Run web service
    web_service.run()