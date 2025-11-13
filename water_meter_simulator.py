import time
import json
import random
import paho.mqtt.client as mqtt
from datetime import datetime

# Replace with your AWS IoT Core endpoint
ENDPOINT = "your-endpoint-ats.iot.ap-south-1.amazonaws.com"
PORT = 8883
TOPIC = "water_meter/data"

# Paths to your downloaded certificates
CA_PATH = "AmazonRootCA1.pem"
CERT_PATH = "certificate.pem.crt"
KEY_PATH = "private.pem.key"

client = mqtt.Client()

# Enable TLS/SSL encryption
client.tls_set(ca_certs=CA_PATH, certfile=CERT_PATH, keyfile=KEY_PATH)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Connected to AWS IoT Core successfully!")
    else:
        print(f"❌ Failed to connect, return code {rc}")

client.on_connect = on_connect
client.connect(ENDPOINT, PORT, keepalive=60)
client.loop_start()

try:
    while True:
        data = {
            "device_id": "WaterMeter001",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "flow_rate_lpm": round(random.uniform(0.5, 3.0), 2)
        }
        payload = json.dumps(data)
        client.publish(TOPIC, payload)
        print("📤 Sent:", payload)
        time.sleep(5)

except KeyboardInterrupt:
    print("🛑 Stopped by user")
    client.loop_stop()
    client.disconnect()
