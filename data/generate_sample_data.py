import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_network_traffic_data(num_samples=1000):
    """Generate synthetic network traffic data for QCF demonstration"""
    np.random.seed(42)
    
    # Generate timestamps
    start_time = datetime.now() - timedelta(days=1)
    timestamps = [start_time + timedelta(minutes=i) for i in range(num_samples)]
    
    data = []
    for i in range(num_samples):
        # Normal traffic (90% of samples)
        if i < num_samples * 0.9:
            src_port = np.random.randint(1024, 49151)
            dst_port = np.random.choice([80, 443, 22, 53])  # Common ports
            packet_size = np.random.normal(1000, 200)
            protocol = np.random.choice(['TCP', 'UDP'])
            flags = 'ACK' if protocol == 'TCP' else ''
            is_anomaly = 0
            
        # Anomalous traffic (10% of samples)
        else:
            src_port = np.random.randint(49152, 65535)
            dst_port = np.random.choice([21, 23, 135, 139, 445])  # Suspicious ports
            packet_size = np.random.normal(50, 500)  # Unusual sizes
            protocol = np.random.choice(['TCP', 'UDP', 'ICMP'])
            flags = 'SYN' if protocol == 'TCP' else 'UNKNOWN'
            is_anomaly = 1
        
        data.append({
            'timestamp': timestamps[i],
            'src_ip': f"192.168.1.{np.random.randint(1, 255)}",
            'dst_ip': f"10.0.0.{np.random.randint(1, 255)}",
            'src_port': src_port,
            'dst_port': dst_port,
            'protocol': protocol,
            'packet_size': max(64, int(packet_size)),
            'duration': np.random.exponential(2),
            'flags': flags,
            'is_anomaly': is_anomaly
        })
    
    df = pd.DataFrame(data)
    df.to_csv('data/sample_network_traffic.csv', index=False)
    print(f"Generated {num_samples} samples with {df['is_anomaly'].sum()} anomalies")
    return df

if __name__ == "__main__":
    generate_network_traffic_data() 