import base64
import json
import os
import random
import threading
from datetime import datetime

import numpy as np
import paho.mqtt.client as mqtt
from PIL import Image

# MQTT Settings
from near_location import near_location

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
    # print("Published: " + str(message) + " " + "on MQTT Topic: " + str(topic))
    print("Published: " + "on MQTT Topic: " + str(topic))
    print("")


def load_image_into_numpy_array(image):
    (im_width, im_height) = image.size
    return np.array(image.getdata()).reshape(
        (im_height, im_width, 3)).astype(np.uint8)


def publish_random_sensor_values_to_mqtt():
    num_images = 17
    image_number = random.randrange(1, num_images)

    images_directory = "./frames"

    image_path = os.path.join(images_directory, 'img_{}.jpg'.format(image_number))
    print(image_path)

    image = Image.open(image_path)
    (im_width, im_height) = image.size
    image_np = np.array(image.getdata()).reshape(
        (im_height, im_width, 3)).astype(np.uint8)
    # image_np = np.array(image.getdata()).reshape(
    #     (im_height, im_width, 3)).tolist()
    image_np_expanded = np.expand_dims(image_np, axis=0).tolist()



    # image = Image.open(image_path)
    # image_np = np.array(image).tolist()

    # FIXME bytes
    # with open(image_path, mode='rb') as file:
    #     img = file.read()
    # image_np = base64.encodebytes(img).decode("utf-8")

    threading.Timer(3.0, publish_random_sensor_values_to_mqtt).start()

    humidity_data = {}
    # humidity_data['Sensor_ID'] = sys.argv[1]
    humidity_data['Sensor_ID'] = "1"
    humidity_data['Date'] = (datetime.today()).strftime("%d-%b-%Y %H:%M:%S:%f")
    humidity_data['Image'] = image_np_expanded
    humidity_data['Location'] = near_location(50.0646501, 19.9449799, 50)
    humidity_json_data = json.dumps(humidity_data)

    print(humidity_json_data)

    publish_to_topic(MQTT_Topic_Traffic, humidity_json_data)


publish_random_sensor_values_to_mqtt()
