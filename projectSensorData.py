import json

import cv2
import numpy as np
import pymongo


class DatabaseManager():
    def __init__(self):
        client = pymongo.MongoClient(
            "mongodb://user1:user1@cluster0-shard-00-00.f93zw.mongodb.net:27017,cluster0-shard-00-01.f93zw.mongodb.net:27017,cluster0-shard-00-02.f93zw.mongodb.net:27017/cloud?ssl=true&replicaSet=atlas-z3y6rw-shard-0&authSource=admin&retryWrites=true&w=majority")
        self.db = client.test

    def add_del_update_db_record(self, args=[], name=""):
        col = self.db.traffic
        col.insert_many([{'value': i, 'name': name} for i in args])
        return


def load_image_into_numpy_array(image):
    (im_width, im_height) = image.size
    return np.array(image.getdata()).reshape(
        (im_height, im_width, 3)).astype(np.uint8)


allImages = []


def detect(file):
    img = cv2.imread(file)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    light_color = None
    # color range
    lower_red1 = np.array([0, 100, 100])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([160, 100, 100])
    upper_red2 = np.array([180, 255, 255])
    lower_green = np.array([40, 50, 50])
    upper_green = np.array([90, 255, 255])
    lower_yellow = np.array([15, 150, 150])
    upper_yellow = np.array([35, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    maskg = cv2.inRange(hsv, lower_green, upper_green)
    masky = cv2.inRange(hsv, lower_yellow, upper_yellow)
    maskr = cv2.add(mask1, mask2)

    size = img.shape
    # print size

    # hough circle detect
    r_circles = cv2.HoughCircles(maskr, cv2.HOUGH_GRADIENT, 1, 80,
                                 param1=50, param2=10, minRadius=0, maxRadius=30)

    g_circles = cv2.HoughCircles(maskg, cv2.HOUGH_GRADIENT, 1, 60,
                                 param1=50, param2=10, minRadius=0, maxRadius=30)

    y_circles = cv2.HoughCircles(masky, cv2.HOUGH_GRADIENT, 1, 30,
                                 param1=50, param2=5, minRadius=0, maxRadius=30)

    # traffic light detect
    r = 5
    bound = 4.0 / 10
    if r_circles is not None:
        r_circles = np.uint16(np.around(r_circles))

        for i in r_circles[0, :]:
            if i[0] > size[1] or i[1] > size[0] or i[1] > size[0] * bound:
                continue

            h, s = 0.0, 0.0
            for m in range(-r, r):
                for n in range(-r, r):

                    if (i[1] + m) >= size[0] or (i[0] + n) >= size[1]:
                        continue
                    h += maskr[i[1] + m, i[0] + n]
                    s += 1
            if h / s > 50:
                light_color = 'RED'

    if g_circles is not None:
        g_circles = np.uint16(np.around(g_circles))

        for i in g_circles[0, :]:
            if i[0] > size[1] or i[1] > size[0] or i[1] > size[0] * bound:
                continue

            h, s = 0.0, 0.0
            for m in range(-r, r):
                for n in range(-r, r):

                    if (i[1] + m) >= size[0] or (i[0] + n) >= size[1]:
                        continue
                    h += maskg[i[1] + m, i[0] + n]
                    s += 1
            if h / s > 100:
                light_color = 'GREEN'

    if y_circles is not None:
        y_circles = np.uint16(np.around(y_circles))

        for i in y_circles[0, :]:
            if i[0] > size[1] or i[1] > size[0] or i[1] > size[0] * bound:
                continue

            h, s = 0.0, 0.0
            for m in range(-r, r):
                for n in range(-r, r):

                    if (i[1] + m) >= size[0] or (i[0] + n) >= size[1]:
                        continue
                    h += masky[i[1] + m, i[0] + n]
                    s += 1
            if h / s > 50:
                light_color = 'YELLOW'

    return light_color


def DHT22_Image_Handler(json_data):
    # Parse Data
    json_data = json_data.decode('utf-8')
    json_dict = json.loads(json_data)
    sensor_id = json_dict['Sensor_ID']
    data_and_time = json_dict['Date']
    image_path = json_dict['Image']
    location = json_dict['Location']

    light_color = detect(image_path)
    print(light_color)

    if light_color is not None:
        dbObj = DatabaseManager()
        allImages.append(
            {"sensor_id": sensor_id, "date": data_and_time, "location": location, "light_color": light_color})
        if len(allImages) == 10:
            dbObj.add_del_update_db_record(allImages)
            allImages.clear()
            del dbObj
            print("Inserted Image Data into Database.")
            print("")


# Master Function to Select DB Funtion based on MQTT Topic

def sensor_Data_Handler(Topic, jsonData):
    if Topic == "cloud2020/gr04-3/Traffic":
        DHT22_Image_Handler(jsonData)
