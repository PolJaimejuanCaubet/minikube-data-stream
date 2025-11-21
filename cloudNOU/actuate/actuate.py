import json
import os
import time
import paho.mqtt.client as mqtt
from kafka import KafkaConsumer

KAFKA_HOST = os.getenv("KAFKA_HOST")
TOPIC_CLEAN = os.getenv("TOPIC_CLEAN")
MQTT_HOST = os.getenv("MQTT_HOST")
MQTT_PORT = int(os.getenv("MQTT_PORT"))

mqtt_client = mqtt.Client()
mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)

print(f"ESTE ES EL TOPIC {TOPIC_CLEAN}, {type(TOPIC_CLEAN)}")
consumer = KafkaConsumer(
    TOPIC_CLEAN,
    bootstrap_servers=[KAFKA_HOST],
    value_deserializer=lambda x: json.loads(x.decode("utf-8")),
    auto_offset_reset="earliest",
    group_id="p3-actuator-group"
)


for msg in consumer:
    event = msg.value
    home = event["home_id"]
    room = event["room_id"]
    temp = float(event["value"])
    print(f"La temperatura es -> {temp}")
    print(f"Tipo de la variable temp -> {type(temp)}")

    if temp < 20:
        command = "start"
    elif temp > 25:
        command = "stop"
    else:
        print(f"[P3] {home}/{room} -> Temp={temp} - No action")
        continue

    mqtt_topic = f"{home}/{room}/heatpump/set"

    
    time.sleep(1)

    mqtt_client.publish(mqtt_topic, command)
    print(f"[P3] ACTUATION SENT → {mqtt_topic} = {command}")
