import json

import pymongo


class DatabaseManager():
    def __init__(self):
        client = pymongo.MongoClient(
            "mongodb+srv://user1:user1@cluster0.f93zw.mongodb.net/cloud?retryWrites=true&w=majority")
        self.db = client.test

    def add_del_update_db_record(self, args=[], name=""):
        col = self.db.data
        col.insert_many([{'value': i, 'name': name} for i in args])
        return


# Functions to push Sensor Data into Database

# Function to save Temperature to DB Table
allTemperatures = []


def DHT22_Temp_Data_Handler(jsonData):
    # Parse Data
    jsonData = jsonData.decode('utf-8')
    json_Dict = json.loads(jsonData)
    SensorID = json_Dict['Sensor_ID']
    Data_and_Time = json_Dict['Date']
    Temperature = json_Dict['Temperature']
    Location = json_Dict['Location']

    dbObj = DatabaseManager()
    allTemperatures.append([SensorID, Data_and_Time, Temperature, Location])
    if len(allTemperatures) == 10:
        dbObj.add_del_update_db_record(allTemperatures, "Temperature")
        allTemperatures.clear()
        del dbObj
        print("Inserted Temperature Data into Database.")
        print("")


allHumidity = []


# Function to save Humidity to DB Table
def DHT22_Humidity_Data_Handler(jsonData):
    # Parse Data
    jsonData = jsonData.decode('utf-8')
    json_Dict = json.loads(jsonData)
    SensorID = json_Dict['Sensor_ID']
    Data_and_Time = json_Dict['Date']
    Humidity = json_Dict['Humidity']
    Location = json_Dict['Location']

    dbObj = DatabaseManager()
    allHumidity.append([SensorID, Data_and_Time, Humidity, Location])
    if len(allHumidity) == 10:
        dbObj.add_del_update_db_record(allHumidity, "Humidity")
        allHumidity.clear()
        del dbObj
        print("Inserted Humidity Data into Database.")
        print("")


# Function to save Pollution to DB Table
allPollutions = []


def DHT22_Pollution_Data_Handler(jsonData):
    # Parse Data
    jsonData = jsonData.decode('utf-8')
    json_Dict = json.loads(jsonData)
    SensorID = json_Dict['Sensor_ID']
    Data_and_Time = json_Dict['Date']
    Pollution = json_Dict['Pollution']
    Location = json_Dict['Location']

    dbObj = DatabaseManager()
    allPollutions.append([SensorID, Data_and_Time, Pollution, Location])
    if len(allPollutions) == 10:
        dbObj.add_del_update_db_record(allPollutions, "Pollution")
        allPollutions.clear()
        del dbObj
        print("Inserted Pollution Data into Database.")
        print("")


# Master Function to Select DB Funtion based on MQTT Topic

def sensor_Data_Handler(Topic, jsonData):
    if Topic == "cloud2020/gr04-3/Temperature":
        DHT22_Temp_Data_Handler(jsonData)
    elif Topic == "cloud2020/gr04-3/Humidity":
        DHT22_Humidity_Data_Handler(jsonData)
    elif Topic == "cloud2020/gr04-3/Pollution":
        DHT22_Pollution_Data_Handler(jsonData)
