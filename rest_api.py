import logging
logging.basicConfig(filename='log/myapp.log', level=logging.DEBUG)
logging.info('Started')

from gevent import monkey; monkey.patch_all()
import threading
import bottle
from bottle import request, response, static_file
from bottle import post, get, put, delete, route
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
    resource_xml = open("./config/res_config_cost2.xml").read()
    response.headers['Content-Type'] = 'text/xml'  
    return resource_xml

@post("/allocation/")
def update_process():
    # Get measure and Operator from form
    try:
        measure = request.forms.get("measure").lower().strip()
    except:
        measure = None

    try: 
        operator = request.forms.get("operator")
        match operator:
            case "min":
                operator = min
            case "max":
                operator = max
    except:
        operator = None

    # Get URLs from Header
    print("CPEE-Instance URL: ", request.headers.raw("Cpee-Instance-Url"))
    instance_url = request.headers.raw("Cpee-Instance-Url")
    description_url = instance_url + "properties/description/"

    # Get Resource URL from form
    if request.forms.get("resource_url"):
        resource_url = request.forms.get("resource_url")
        print("Resource config File URL", resource_url)
        manipulated_process_model = allocate_process(description_url, resource_url=resource_url, measure=measure, operator=operator)
    else: 
        manipulated_process_model = allocate_process(description_url, measure=measure, operator=operator)

    # Start allocation task
    event = threading.Event()
    t1 = threading.Thread(target=my_request, args=(instance_url, manipulated_process_model))
    t1.daemon = True
    t1.start()

    # Send response 400 to stop CPEE
    print("returning")
    response.status = 400
    print(response.status_line)
    return response
    
def my_request(instance_url, xml_str):
    ns = {"cpee2": "http://cpee.org/ns/properties/2.0", 
        "cpee1":"http://cpee.org/ns/description/1.0"}
    time.sleep(2)

    print("Back from wait")
    open("output/final_xml.xml", "wb").write(xml_str)

    process_model = etree.fromstring(xml_str)
    position = process_model.xpath(".//cpee1:*[@id]", namespaces=ns)[1].attrib["id"]
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
        'content-id': "positions",
        'content-type': "text/xml; charset=UTF-8"
        }
    
    status_url = instance_url + "properties/positions/"
    payload = f"<?xml version=\"1.0\"?><positions xmlns=\"http://cpee.org/ns/properties/2.0\"><{position}>at</{position}></positions>"
    response = requests.request("PUT", status_url, data=payload, headers=headers)
    print(response.status_code)
    headers = {
        'content-id': "description",
        'content-type': "application/x-www-form-urlencoded; charset=UTF-8"
        }
    status_url = instance_url + "properties/state/"
    payload = "value=running"
    response = requests.request("PUT", status_url, data=payload, headers=headers)
    print(response.status_code)
    logging.info(f"PUT state to running with status code: {response.status_code}")


# Try to generate an Editor for resource specification file
@post("/edit/add_resprofile/")
def edit_resources():
    print(request.body)
    """Return HTML to edit resources"""
    response.status = 201
    return response


@route("/edit/resources/")
def edit_resources():
    """Return HTML to edit resources"""

    return static_file("res_editor.html", root="frontend/")



if __name__ == '__main__':
    bottle.run(host = '127.0.0.1', port = 8000, server="gevent")
