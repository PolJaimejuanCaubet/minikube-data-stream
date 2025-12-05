import os
import paho.mqtt.client as mqtt


LOCAL_MQTT_HOST = os.getenv("LOCAL_MQTT_HOST")
LOCAL_MQTT_PORT = 1883

CLOUD_MQTT_HOST = os.getenv("CLOUD_MQTT_HOST")
CLOUD_MQTT_PORT = int(os.getenv("CLOUD_MQTT_PORT"))
CLOUD_HOME_ID = os.getenv("HOME_ID")

LOCAL_TOPIC_DATA = "+/temperature"      
CLOUD_TOPIC_CMD  = f"{CLOUD_HOME_ID}/+/heatpump/set"

print(f"GATEWAY INICIADO: Home = {CLOUD_HOME_ID}")
print(f"Local MQTT : {LOCAL_MQTT_HOST}:{LOCAL_MQTT_PORT}")
print(f"Cloud MQTT : {CLOUD_MQTT_HOST}:{CLOUD_MQTT_PORT}")

local_client = None
cloud_client = None

def local_message_to_cloud(client, userdata, msg):
    # send from local sensors to cloud
    room_id = msg.topic.split('/')[0]
    cloud_topic = f"{CLOUD_HOME_ID}/{room_id}/temperature"
    cloud_client.publish(topic=cloud_topic, payload=msg.payload)
    print(f"local->cloud {msg.topic} ({msg.payload.decode()}) → {cloud_topic}")


def cloud_commands_to_local(client, userdata, msg):
    # send cloud commands and send to local sensors
    parts = msg.topic.split('/')
    if len(parts) >= 3:
        room_id = parts[1]
        local_topic = f"{room_id}/heatpump" # modify topic
        local_client.publish(local_topic, payload=msg.payload)
        print(f"cloud->local {msg.topic} ({msg.payload.decode()}) → {local_topic}")


def main():
    global local_client, cloud_client

    local_client = mqtt.Client()
    local_client.on_message = local_message_to_cloud
    local_client.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, keepalive=60)
    local_client.subscribe(LOCAL_TOPIC_DATA)

    cloud_client = mqtt.Client()
    cloud_client.on_message = cloud_commands_to_local

    try:
        cloud_client.connect(CLOUD_MQTT_HOST, CLOUD_MQTT_PORT, keepalive=60)
        cloud_client.subscribe(CLOUD_TOPIC_CMD)
    except Exception as e:
        print(f"\nERROR\n{e}\n\n")
        return

    local_client.loop_start()
    cloud_client.loop_forever()

if __name__ == '__main__':
    main()
 

