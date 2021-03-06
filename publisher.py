import json
import random
import sys
import threading
from datetime import datetime

import paho.mqtt.client as mqtt

# MQTT Settings
from near_location import near_location

MQTT_Broker = "test.mosquitto.org"
MQTT_Port = 1883
Keep_Alive_Interval = 45
MQTT_Topic_Humidity = "cloud2020/gr04-3/Humidity"
MQTT_Topic_Temperature = "cloud2020/gr04-3/Temperature"
MQTT_Topic_Pollution = "cloud2020/gr04-3/Pollution"


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


def publish_To_Topic(topic, message):
    mqttc.publish(topic, message)
    print("Published: " + str(message) + " " + "on MQTT Topic: " + str(topic))
    print("")


# FAKE SENSOR
# Dummy code used as Fake Sensor to publish some random values
# to MQTT Broker

toggle = 0


def publish_Fake_Sensor_Values_to_MQTT():
    threading.Timer(3.0, publish_Fake_Sensor_Values_to_MQTT).start()
    global toggle
    if toggle == 0:
        Humidity_Fake_Value = float("{0:.2f}".format(random.uniform(50, 100)))

        Humidity_Data = {}
        Humidity_Data['Sensor_ID'] = sys.argv[1]
        Humidity_Data['Date'] = (datetime.today()).strftime("%d-%b-%Y %H:%M:%S:%f")
        Humidity_Data['Humidity'] = Humidity_Fake_Value
        Humidity_Data['Location'] = near_location(50.0646501, 19.9449799, 50)
        humidity_json_data = json.dumps(Humidity_Data)

        print("Publishing fake Humidity Value: " + str(Humidity_Fake_Value) + "...")
        publish_To_Topic(MQTT_Topic_Humidity, humidity_json_data)
        toggle = 1

    elif toggle == 1:
        Temperature_Fake_Value = float("{0:.2f}".format(random.uniform(-20, 30)))

        Temperature_Data = {}
        Temperature_Data['Sensor_ID'] = sys.argv[1]
        Temperature_Data['Date'] = (datetime.today()).strftime("%d-%b-%Y %H:%M:%S:%f")
        Temperature_Data['Temperature'] = Temperature_Fake_Value
        Temperature_Data['Location'] = near_location(50.0646501, 19.9449799, 50)
        temperature_json_data = json.dumps(Temperature_Data)

        print("Publishing fake Temperature Value: " + str(Temperature_Fake_Value) + "...")
        publish_To_Topic(MQTT_Topic_Temperature, temperature_json_data)
        toggle = 2
    else:
        Pollution_Fake_Value = float("{0:.2f}".format(random.uniform(1, 100)))
        Pollution_Data = {}
        Pollution_Data['Sensor_ID'] = sys.argv[1]
        Pollution_Data['Date'] = (datetime.today()).strftime("%d-%b-%Y %H:%M:%S:%f")
        Pollution_Data['Pollution'] = Pollution_Fake_Value
        Pollution_Data['Location'] = near_location(50.0646501, 19.9449799, 50)
        pollution_json_data = json.dumps(Pollution_Data)

        print("Publishing fake Pollution Value: " + str(Pollution_Fake_Value) + "...")
        publish_To_Topic(MQTT_Topic_Pollution, pollution_json_data)
        toggle = 0


publish_Fake_Sensor_Values_to_MQTT()
