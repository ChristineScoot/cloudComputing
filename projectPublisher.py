import json
import os
import random
import threading
from datetime import datetime

import paho.mqtt.client as mqtt

# MQTT Settings

MQTT_Broker = "test.mosquitto.org"
MQTT_Port = 1883
Keep_Alive_Interval = 45
MQTT_Topic_Traffic = "cloud2020/gr04-3/Traffic"


def on_connect(client, userdata, rc):
    if rc != 0:
        pass
        print("Unable to connect to MQTT Broker...")
    else:
        print("Connected with MQTT Broker: " + str(MQTT_Broker))


def on_publish(client, userdata, mid):
    pass


def on_disconnect(client, userdata, rc):
    if rc != 0:
        pass


mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_disconnect = on_disconnect
mqttc.on_publish = on_publish
mqttc.connect(MQTT_Broker, int(MQTT_Port), int(Keep_Alive_Interval))


def publish_to_topic(topic, message):
    mqttc.publish(topic, message)
    print("Published: " + message + " on MQTT Topic: " + str(topic))
    print("")


def publish_random_sensor_values_to_mqtt():
    num_images = 12
    image_number = random.randrange(1, num_images)

    images_directory = "./frames"
    image_path = os.path.join(images_directory, 'img_{}.jpg'.format(image_number))
    print(image_path)

    threading.Timer(3.0, publish_random_sensor_values_to_mqtt).start()

    date = (datetime.today()).strftime("%d-%b-%Y %H:%M:%S:%f")
    # location = near_location(50.0646501, 19.9449799, 500)
    locations = [[50.06458920751176, 19.94521232796986],
                 [50.062331900722626, 19.941672997556896],
                 [50.06531621494584, 19.94691840311032],
                 [50.067899497949895, 19.943737310452978],
                 [50.06182888519117, 19.942573341602063],
                 [50.06171616360789, 19.944906618659157],
                 [50.064723729369675, 19.944031683425237],
                 [50.063002019715256, 19.94818279057535]]
    location = locations[random.randrange(0, 7)]

    data = {"Image": image_path, "Sensor_ID": "1", "Date": date, "Location": location}
    publish_to_topic(MQTT_Topic_Traffic, json.JSONEncoder().encode(data))


publish_random_sensor_values_to_mqtt()
