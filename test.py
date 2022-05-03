# -*- coding: utf-8 -*-
import requests
import json
import time
import sqlite3

def database_show():
    cn = sqlite3.connect("data_stored.db")
    cr = cn.cursor()

    f = open("query.json")
    query = json.load(f)

    print("\n___________SENSOR__________")
    for row in cr.execute(query['list_sensor']):
        print(row)
    print("___________________________")
    print("\n__________VALUE___________")
    for row in cr.execute(query['show_all_value']):
        print(row)
    print("__________________________")

    cn.commit()
    cr.close()
    cn.close()

get_js = {
    "token": "TangGiaoSu",
    "message": "Request get_led_state_js",
}

post_js = {
    "token": "TangGiaoSu",
    "message": "Request post_light_distance_js",
    "data": {
        "light": 90,
        "distance": 90
    }
}

response1 = requests.post("http://52.77.238.126:7777/post_light_distance_js", json=post_js)
time.sleep(2)
response = requests.get("http://52.77.238.126:7777/get_led_state_js", json=get_js)
time.sleep(2)
response2 = requests.get("http://52.77.238.126:7777/get_led_state")

print("\nPOST")
print(json.dumps(response1.json(), indent=4))
print(response1.headers)

print("\nGET")
print(json.dumps(response.json(), indent=4))
print(response.headers)

print("\nGET")
print(response.content)

database_show()

