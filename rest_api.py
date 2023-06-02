import logging
logging.basicConfig(filename='log/myapp.log', level=logging.INFO)
logging.info('Started')

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
    resource_xml = open("./config/res_config_4.xml").read()
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
    instance_url = request.headers.raw("Cpee-Instance-Url")
    description_url = instance_url + "properties/description/"
    
    if request.forms.get("resource_url"):
        resource_url = request.forms.get("resource_url")
        print(resource_url)
        manipulated_process_model = allocate_process(description_url, resource_url=resource_url)
    else: 
        manipulated_process_model = allocate_process(description_url)

    
    event = threading.Event()
    t1 = threading.Thread(target=my_request, args=(instance_url, manipulated_process_model))
    t1.daemon = True
    t1.start()
    print("returning")
    return manipulated_process_model
    
def my_request(instance_url, xml_str):
    time.sleep(2)

    print("Back from wait")
    open("output/final_xml.xml", "wb").write(xml_str)
    description_url = instance_url + "properties/description/"
    payload = xml_str
    headers = {
        'content-id': "description",
        'content-type': "text/xml"
        }

    response = requests.request("PUT", description_url, data=payload, headers=headers)
    print(response.status_code)
    logging.info(f"PUT new process model with status code: {response.status_code}")

    headers = {
        'content-id': "description",
        'content-type': "application/x-www-form-urlencoded; charset=UTF-8"
        }
    
    status_url = instance_url + "properties/state/"
    payload = "value=running"
    response = requests.request("PUT", status_url, data=payload, headers=headers)
    print(response.status_code)
    logging.info(f"PUT state to running with status code: {response.status_code}")

if __name__ == '__main__':
    bottle.run(host = '127.0.0.1', port = 8000, server="gevent")
