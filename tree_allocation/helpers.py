from proc_resource import *
from lxml import etree
import requests

def get_all_resources(path_to_xml):
        reslist = []
        with open(str(path_to_xml)) as f:
            root = etree.fromstring(f.read())
        
        for element in root.findall("resource"):
            print(f"Create resource with id {element.attrib['id']}")
            res = Resource(element.attrib["name"])
            for profile in element.findall("resprofile"):
                change_patterns=[]
                for cp in profile.findall("changepattern"):
                    change_patterns.append(cp)
                res.create_resource_profile(profile.attrib["name"], profile.attrib["role"], task=profile.attrib["task"], change_patterns=change_patterns)

            reslist.append(res)
        return reslist


def get_all_tasks(cpee_url):
        # define namespaces
        ns = {"cpee2": "http://cpee.org/ns/properties/2.0", 
            "cpee1":"http://cpee.org/ns/description/1.0"}
        # send get request and save response
        r = requests.get(url = cpee_url)

        # parse xml:
        root = etree.fromstring(r.content)
        tasks = []
        for task in root.xpath(".//cpee1:call | .//cpee1:manipulate", namespaces=ns):
            tasks.append(task)
        
        return tasks

def get_process_model(cpee_url):
        # define namespaces
        ns = {"cpee2": "http://cpee.org/ns/properties/2.0", 
            "cpee1":"http://cpee.org/ns/description/1.0"}
        # send get request and save response
        r = requests.get(url = cpee_url)

        # parse xml:
        root = etree.fromstring(r.content)
        xml_string = r.content
        with open("./config/xml_model.xml", "wb") as f:
            f.write(xml_string)
        return xml_string, root