from gevent import monkey; monkey.patch_all()
import threading
import bottle
from bottle import request, response
from bottle import post, get, put, delete
from tree_allocation.helpers import *
import json
import requests
import time
_names = set()

app = application = bottle.default_app()

@get("/info")
def get_info():
    '''Returns some info on project'''
    info_text = "This is the test page for the resource manipulation API"
    response.headers['Content-Type'] = 'application/json'
    return json.dumps({"text": info_text})

@get("/resources")
def get_resources():
    '''Return the resource xml'''
    resource_xml = open("./config/res_config_5.xml").read()
    response.headers['Content-Type'] = 'text/xml'
    return resource_xml

@get("/resources2")
def get_resources():
    '''Return the resource xml'''
    resource_xml = open("./config/res_config_5.xml").read()
    response.headers['Content-Type'] = 'application/json'
    return json.dumps({"resources" :resource_xml})

@post("/allocation/")
def update_process():
    print(request.headers.raw("Cpee-Instance-Url"))
    data = request.headers.raw("Cpee-Instance-Url")
    data = data + "properties/description/"
    manipulated_process_model = allocate_process(data)
    
    event = threading.Event()
    t1 = threading.Thread(target=my_request, args=(data, manipulated_process_model, event))
    t1.daemon = True
    t1.start()
    print("returning")
    return manipulated_process_model
    
def my_request(url, xml_str, event):
    import http.client
    time.sleep(2)

    print("Back from wait")
    conn = http.client.HTTPSConnection("cpee.org")

    payload = xml_str
    print(payload)
    headers = {
        'content-id': "description",
        'content-type': "text/xml"
        }

    conn.request("PUT", "/flow/engine/17190/properties/description/", payload, headers)

    res = conn.getresponse()
    data = res.read()
    print(res.status)
    print(data.decode("utf-8"))

    headers = {
        'content-id': "description",
        'content-type': "application/x-www-form-urlencoded; charset=UTF-8"
        }
    payload = "value=running"
    conn.request("PUT", "/flow/engine/17190/properties/state/", payload, headers)
    res = conn.getresponse()
    print(res.status)

if __name__ == '__main__':
    bottle.run(host = '127.0.0.1', port = 8000, server="gevent")