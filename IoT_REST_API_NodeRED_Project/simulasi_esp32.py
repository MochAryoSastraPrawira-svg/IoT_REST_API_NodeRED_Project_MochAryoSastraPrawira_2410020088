import paho.mqtt.client as mqtt
import json
import time
import random
from datetime import datetime

BROKER = "localhost"
PORT = 1883
TOPIC_SENSOR = "iot/sensor"
TOPIC_KONTROL = "iot/kontrol"
TOPIC_ALERT = "iot/alert"

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"[MQTT] Terhubung ke broker (code: {reason_code})")
    client.subscribe(TOPIC_KONTROL)
    client.subscribe(TOPIC_ALERT)

def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    if msg.topic == TOPIC_KONTROL:
        print(f"⚡ [KONTROL DITERIMA] {payload}")
    elif msg.topic == TOPIC_ALERT:
        print(f"🚨 [PERINGATAN SUHU] {payload}")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="ESP32-Simulator")
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, 60)
client.loop_start()

print("ESP32 Simulator berjalan... Tekan Ctrl+C untuk berhenti.")

try:
    while True:
        suhu = round(random.uniform(26.0, 33.5), 1)
        kelembaban = round(random.uniform(55.0, 80.0), 1)
        data = {
            "suhu": suhu,
            "kelembaban": kelembaban,
            "timestamp": datetime.now().isoformat()
        }
        client.publish(TOPIC_SENSOR, json.dumps(data))
        print(f"→ Publish ke {TOPIC_SENSOR}: {data}")
        time.sleep(3)
except KeyboardInterrupt:
    print("\nMenghentikan simulator...")
    client.loop_stop()
    client.disconnect()
