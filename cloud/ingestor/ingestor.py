import os
import json
import paho.mqtt.client as mqtt
from kafka import KafkaProducer

CLOUD_MQTT_HOST = os.getenv("MQTT_HOST")
KAFKA_HOST = os.getenv("KAFKA_HOST")
KAFKA_TOPIC = "raw_sensor_data"
# Se suscribe a CUALQUIER HOME ID (+), CUALQUIER ROOM ID (+), y al topic de temperatura
MQTT_TOPIC_SUB = "+/+/temperature" # home/#

producer = KafkaProducer(
    bootstrap_servers=[KAFKA_HOST],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def on_connect(client, userdata, flags, rc):
    client.subscribe(MQTT_TOPIC_SUB)

def on_message(client, userdata, msg):
    topic_parts = msg.topic.split('/') 
    payload = json.loads(msg.payload.decode("utf-8"))
    
    kafka_message = {
        "home": topic_parts[0],
        "room": topic_parts[1],
        "timestamp": payload["timestamp"],
        "value": payload["value"]
    }
        
    future = producer.send(KAFKA_TOPIC, value=kafka_message)
    
    metadata = future.get(timeout=10) 
    print(f"ENVIADO OK: Home={kafka_message['home']}, Room={kafka_message['room']} -> Kafka Topic={metadata.topic}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message    
client.connect(CLOUD_MQTT_HOST, 1883, 60)
client.loop_forever()
