# -*- coding: utf-8 -*-
import json
import sqlite3
from aiohttp import web

routes = web.RouteTableDef()

current_light = 0.0
current_distance = 0.0

def check_setup_database():
    cn = sqlite3.connect("data_stored.db")
    cr = cn.cursor()
    try:
        with open("setup_database.sql") as setup_file:
            query = setup_file.read()
            cr.executescript(query)
        
        f = open("query.json")
        query = json.load(f)
        cr.execute(query['init_data'])

        cn.commit()

    except:
        print("Database already exist!")
    
    cr.close()
    cn.close()

def database_add_sensor_value():
    cn = sqlite3.connect("data_stored.db")
    cr = cn.cursor()

    f = open("query.json")
    query = json.load(f)

    cr.execute(query['add_light_value'], [current_light])
    cr.execute(query['add_distance_value'], [current_distance])

    cn.commit()
    cr.close()
    cn.close()

@routes.get("/get_led_state")
async def get_led_state(request):
    print("/get_led_state");

    response_obj = {
        "status": True,
        "message": "Response get_led_state",
        "number_led": -1
    }
    if current_distance > 200 or current_light > 210:
        response_obj["number_led"] = 0
    else:
        response_obj["number_led"] = 3-int(current_light/70)
    
    return web.json_response(
            data=response_obj
        )


@routes.get("/get_led_state_js")
async def get_led_state_js(request):

    response_obj = {
        "status": True,
        "message": "Response get_led_state_js",
        "number_led": -1
    }

    try:
        
        token_js = await request.json()
        token = token_js["token"]
        print("\n-------get_led_state_js-------")
        print(json.dumps(token_js, indent=4))
        print("------------------------------")

        if token != "TangGiaoSu":
            response_obj["status"] = False
            return web.json_response(
                data=response_obj,
                status=401
            )

        if current_distance > 200 or current_light > 210:
            response_obj["number_led"] = 0
        else:
            response_obj["number_led"] = 3-int(current_light/70)
        
        return web.json_response(
            data=response_obj
        )

    except Exception as ex:
        print('/get_led_state_js: ERROR:', ex)
        return web.Response(
            text=f"get_led_state_js: ERROR {ex}",
            status=400
        )


@routes.post("/post_light_distance_js")
async def post_light_distance_js(request):
    global current_distance, current_light

    response_obj = {
        "status": True,
        "message": "Response post_light_distance_js" 
    }

    try:
        request_obj = await request.json()
        
        print("\n--------post_light_distance_js--------")
        print(json.dumps(request_obj, indent=4))
        print("--------------------------------------")

        token = request_obj["token"]
        if token != "TangGiaoSu":
            response_obj["status"] = False
            return web.json_response(
                data=response_obj,
                status=401
            )

        if request_obj["data"]["light"] is not None:
            if request_obj["data"]["distance"] is not None:

                current_light = request_obj["data"]["light"]
                current_distance = request_obj["data"]["distance"]
                
                database_add_sensor_value()
        
        return web.json_response(
            data=response_obj
        )

    except Exception as ex:
        print('/post_light_distance_js: ERROR:', ex)
        return web.Response(
            text=f"post_light_distance_js: ERROR {ex}",
            status=400
        )



if __name__ == '__main__':
    
    app = web.Application()
    app.add_routes(routes)

    check_setup_database()

    web.run_app(app, port=7777)