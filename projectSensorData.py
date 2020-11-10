import json
import numpy as np
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


def load_image_into_numpy_array(image):
    (im_width, im_height) = image.size
    return np.array(image.getdata()).reshape(
        (im_height, im_width, 3)).astype(np.uint8)

# Functions to push Sensor Data into Database

allImages = []


def DHT22_Image_Handler(json_data):
    # Parse Data
    json_data = json_data.decode('utf-8')
    json_dict = json.loads(json_data)
    sensor_id = json_dict['Sensor_ID']
    data_and_time = json_dict['Date']
    image = json_dict['Image'] #TODO
    location = json_dict['Location']

    # print(image)
    image_np = load_image_into_numpy_array(image)#TODO
    # print(image_np)

    dbObj = DatabaseManager()
    allImages.append([sensor_id, data_and_time, image, location]) #TODO
    # allImages.append([sensor_id, data_and_time, location])
    if len(allImages) == 10:
        # FIXME uncomment database
        # dbObj.add_del_update_db_record(allImages, "Temperature")
        allImages.clear()
        del dbObj
        print("Inserted Image Data into Database.")
        print("")


# Master Function to Select DB Funtion based on MQTT Topic

def sensor_Data_Handler(Topic, jsonData):
    print("ok")
    if Topic == "cloud2020/gr04-3/Traffic":
        DHT22_Image_Handler(jsonData)
