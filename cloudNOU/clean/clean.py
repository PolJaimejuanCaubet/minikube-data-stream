import datetime
import json
import os
from kafka import KafkaConsumer, KafkaProducer
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS


KAFKA_HOST = os.getenv("KAFKA_HOST")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")
TOPIC_CLEAN = os.getenv("TOPIC_CLEAN")

INFLUX_URL = os.getenv('INFLUX_URL')
INFLUX_TOKEN = os.getenv('INFLUX_TOKEN')
INFLUX_ORG = os.getenv('INFLUX_ORG')
INFLUX_BUCKET = os.getenv("INFLUX_BUCKET")

print(f"ESTE ES EL TOPIC {KAFKA_TOPIC}, {type(KAFKA_TOPIC)}")

consumer = KafkaConsumer(
    KAFKA_TOPIC, 
    bootstrap_servers=KAFKA_HOST,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

producer = KafkaProducer(
    bootstrap_servers=KAFKA_HOST,
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
write_api = client.write_api(write_options=SYNCHRONOUS)


for msg in consumer:
    event = msg.value
    value = float(event.get('value', 0))
    
    
    if value == 100.0:
        print(f"Dato descartado pq es == 100: {value}")
        continue

    point = Point("temperature_clean") \
        .tag("home", event['home_id']) \
        .tag("room", event['room_id']) \
        .field("value", value) \
        .time(datetime.fromisoformat(event["timestamp"]))
        
    write_api.write(bucket=INFLUX_BUCKET, record=point)

    producer.send(TOPIC_CLEAN, value=event)
    print(f"Dato limpio y reenviado: {value}")




















