import time
import json
import os
import paho.mqtt.client as mqtt
from kafka import KafkaConsumer

KAFKA_HOST = os.getenv("KAFKA_HOST")
TOPIC_CLEAN = os.getenv("TOPIC_CLEAN")
MQTT_HOST = os.getenv("MQTT_HOST")
MQTT_PORT = int(os.getenv("MQTT_PORT"))

mqtt_client = mqtt.Client()
mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)
mqtt_client.loop_start()

consumer = KafkaConsumer(
    TOPIC_CLEAN,
    bootstrap_servers=[KAFKA_HOST],
    value_deserializer=lambda x: json.loads(x.decode("utf-8")),
    auto_offset_reset="earliest",
    group_id="p3-actuator-group"
)

for msg in consumer:
    event = msg.value
    home = event["home"]
    room = event["room"]
    temp = float(event["value"])

    command = None
    if temp < 20:
        command = json.dumps({"status": "1"})
    elif temp > 25:
        command = json.dumps({"status": "0"})

    # time.sleep(1)

    if command:
        mqtt_topic = f"{home}/{room}/heatpump/set"
        mqtt_client.publish(mqtt_topic, command)
        print(f"{mqtt_topic} = {command} because temp is: {temp}º")
