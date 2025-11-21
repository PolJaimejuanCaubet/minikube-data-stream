import json
import os
from datetime import datetime
from kafka import KafkaConsumer
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

KAFKA_HOST = os.getenv("KAFKA_HOST")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")

INFLUX_URL = os.getenv("INFLUX_HOST")
INFLUX_TOKEN = os.getenv("INFLUX_TOKEN")
INFLUX_ORG = os.getenv("INFLUX_ORG")
INFLUX_BUCKET = os.getenv("INFLUX_BUCKET")

influx = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
write_api = influx.write_api(write_options=SYNCHRONOUS)

consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=[KAFKA_HOST],
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    auto_offset_reset='earliest',
    group_id="p1-raw-saver-group"
)

for msg in consumer:
    event = msg.value
    
    point = (
        Point("raw_temperature")
        .tag("home_id", event["home_id"])
        .tag("room_id", event["room_id"])
        .field("value", float(event["value"]))
        .time(datetime.fromisoformat(event["timestamp"]))
    )

    write_api.write(bucket=INFLUX_BUCKET, record=point)

    print(f"[P1 RAW] guardado - {event}")
        
        
