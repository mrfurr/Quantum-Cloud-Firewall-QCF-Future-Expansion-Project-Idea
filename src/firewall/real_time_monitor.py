import asyncio
import websockets
import json
import time
from datetime import datetime
from threading import Thread
from queue import Queue
import warnings
warnings.filterwarnings('ignore')

class RealTimeNetworkMonitor:
    """Real-time network traffic monitoring and analysis"""
     
    def __init__(self, qcf_firewall, interface='eth0'):
        self.qcf_firewall = qcf_firewall
        self.interface = interface
        self.packet_queue = Queue()
        self.is_monitoring = False
        self.anomaly_count = 0
        self.normal_count = 0
        self.threat_level = "LOW"
        
    def start_monitoring(self):
        """Start real-time network monitoring"""
        print(f"Starting real-time monitoring on interface {self.interface}...")
        self.is_monitoring = True
        
        # Start packet capture in separate thread
        capture_thread = Thread(target=self._packet_capture)
        capture_thread.daemon = True
        capture_thread.start()
        
        # Start analysis in separate thread
        analysis_thread = Thread(target=self._analyze_packets)
        analysis_thread.daemon = True
        analysis_thread.start()
        
        print("Real-time monitoring started!")
        
    def stop_monitoring(self):
        """Stop monitoring"""
        self.is_monitoring = False
        print("Monitoring stopped")
        
    def _packet_capture(self):
        """Capture network packets (simulated)"""
        try:
            while self.is_monitoring:
                # Simulate packet generation
                simulated_packets = self._generate_simulated_packets()
                for packet in simulated_packets:
                    if self.is_monitoring:
                        self.packet_queue.put(packet)
                time.sleep(2)  # Generate packets every 2 seconds
                
        except Exception as e:
            print(f"Packet capture error: {e}")
            
    def _generate_simulated_packets(self):
        """Generate simulated network packets for demonstration"""
        packets = []
        
        # Generate 3-5 random packets
        num_packets = np.random.randint(3, 6)
        
        for _ in range(num_packets):
            # 80% normal traffic, 20% anomalous
            is_anomalous = np.random.random() < 0.2
            
            if is_anomalous:
                packet = {
                    'timestamp': datetime.now().isoformat(),
                    'src_ip': f"203.0.113.{np.random.randint(1, 255)}",  # Suspicious IP range
                    'dst_ip': f"10.0.0.{np.random.randint(1, 255)}",
                    'src_port': np.random.randint(49152, 65535),
                    'dst_port': np.random.choice([21, 23, 135, 139, 445]),  # Suspicious ports
                    'protocol': np.random.choice(['TCP', 'UDP', 'ICMP']),
                    'packet_size': np.random.randint(40, 100),  # Small suspicious packets
                    'duration': np.random.exponential(0.1),
                    'flags': 'SYN' if np.random.random() > 0.5 else 'UNKNOWN'
                }
            else:
                packet = {
                    'timestamp': datetime.now().isoformat(),
                    'src_ip': f"192.168.1.{np.random.randint(1, 255)}",
                    'dst_ip': f"10.0.0.{np.random.randint(1, 255)}",
                    'src_port': np.random.randint(1024, 49151),
                    'dst_port': np.random.choice([80, 443, 22, 53]),  # Common ports
                    'protocol': np.random.choice(['TCP', 'UDP']),
                    'packet_size': np.random.randint(500, 1500),
                    'duration': np.random.exponential(1.0),
                    'flags': 'ACK'
                }
                
            packets.append(packet)
            
        return packets
            
    def _analyze_packets(self):
        """Analyze captured packets for anomalies"""
        while self.is_monitoring:
            if not self.packet_queue.empty():
                packet_data = self.packet_queue.get()
                
                # Analyze packet using QCF
                analysis_result = self.qcf_firewall.analyze_real_time_traffic(packet_data)
                
                # Update statistics
                if analysis_result['is_anomaly']:
                    self.anomaly_count += 1
                    print(f"🚨 ANOMALY DETECTED: {packet_data['src_ip']}:{packet_data['src_port']} -> {packet_data['dst_ip']}:{packet_data['dst_port']}")
                else:
                    self.normal_count += 1
                    
                # Update threat level
                self._update_threat_level()
                
            time.sleep(0.1)  # Prevent CPU overload
            
    def _update_threat_level(self):
        """Update threat level based on anomaly ratio"""
        total_packets = self.anomaly_count + self.normal_count
        if total_packets == 0:
            return
            
        anomaly_ratio = self.anomaly_count / total_packets
        
        if anomaly_ratio > 0.1:
            self.threat_level = "CRITICAL"
        elif anomaly_ratio > 0.05:
            self.threat_level = "HIGH"
        elif anomaly_ratio > 0.02:
            self.threat_level = "MEDIUM"
        else:
            self.threat_level = "LOW"
            
    def get_monitoring_stats(self):
        """Get current monitoring statistics"""
        total = self.anomaly_count + self.normal_count
        return {
            'threat_level': self.threat_level,
            'anomalies_detected': self.anomaly_count,
            'normal_packets': self.normal_count,
            'total_packets': total,
            'anomaly_ratio': self.anomaly_count / total if total > 0 else 0
        }

class WebDashboard:
    """Web-based dashboard for real-time monitoring"""
    
    def __init__(self, monitor, port=8080):
        self.monitor = monitor
        self.port = port
        self.connections = set()
        
    async def start_server(self):
        """Start WebSocket server for real-time updates"""
        print(f"Starting WebSocket dashboard on port {self.port}...")
        start_server = websockets.serve(self.handler, "localhost", self.port)
        await start_server
        
    async def handler(self, websocket, path):
        """Handle WebSocket connections"""
        self.connections.add(websocket)
        try:
            # Send periodic updates
            while True:
                stats = self.monitor.get_monitoring_stats()
                await websocket.send(json.dumps(stats))
                await asyncio.sleep(2)  # Update every 2 seconds
        finally:
            self.connections.remove(websocket)