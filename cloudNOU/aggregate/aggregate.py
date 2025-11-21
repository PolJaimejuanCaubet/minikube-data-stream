
import json
import os
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
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# Buffer simple para agregación en memoria
# Estructura: { "home1": [20.5, 21.0, ...], "home2": [...] }
home_temps = {}

print("P4 Aggregator Iniciado...")

for msg in consumer:
    event = msg.value
    home_id = event.get('home_id')
    value = float(event.get('value', 0))
    
    if home_id not in home_temps:
        home_temps[home_id] = []

    home_temps[home_id].append(value)

    # Lógica simple de agregación:
    # Cada 5 lecturas de una misma casa, calculamos media y guardamos.
    # (En un entorno real usaríamos Kafka Streams o Time Windows)
    if len(home_temps[home_id]) >= 5:
        avg_temp = sum(home_temps[home_id]) / len(home_temps[home_id])
        
        print(f"Agregando {home_id}: Media {avg_temp:.2f}")

        # Guardar en InfluxDB [cite: 79]
        point = Point("home_avg_temperature") \
            .tag("home", home_id) \
            .field("avg_value", avg_temp)
        write_api.write(bucket=INFLUX_BUCKET, record=point)

        # Resetear buffer
        home_temps[home_id] = []