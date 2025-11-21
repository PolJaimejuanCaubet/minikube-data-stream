import json
import os
from datetime import datetime
from kafka import KafkaConsumer
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

KAFKA_HOST = os.getenv('KAFKA_HOST')
TOPIC_CLEAN = os.getenv('TOPIC_CLEAN')
INFLUX_URL = os.getenv('INFLUX_URL') 
INFLUX_TOKEN = os.getenv('INFLUX_TOKEN')
INFLUX_ORG = os.getenv('INFLUX_ORG')
INFLUX_BUCKET = os.getenv('INFLUX_BUCKET')

client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
write_api = client.write_api(write_options=SYNCHRONOUS)

consumer = KafkaConsumer(
    TOPIC_CLEAN,
    bootstrap_servers=KAFKA_HOST,
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    auto_offset_reset="earliest",
    group_id="p4-aggregator-group"
)

home_data = {}

for msg in consumer:
    event = msg.value
    
    home = event["home"]
    room = event["room"]
    value = float(event["value"])
    timestamp = event["timestamp"]

    if home not in home_data:
        home_data[home] = {}

    home_data[home][room] = value
    rooms = home_data[home]

    if len(rooms) < 5:   
        continue

    avg_temp = sum(rooms.values()) / len(rooms)

    print(f"{home} -> average temp = {avg_temp}")

    point = Point("home_avg_temperature") \
        .tag("home", home) \
        .field("avg_temp", avg_temp) \
        .time(datetime.fromisoformat(timestamp))

    write_api.write(bucket=INFLUX_BUCKET, record=point)
