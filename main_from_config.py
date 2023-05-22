from proc_resource import *
import time 
from lxml import etree

if __name__ == "__main__":
    reslist = []

## TODO: get tasks to allocate

    def get_all_resources(path_to_xml):
        with open(str(path_to_xml)) as f:
            root = etree.fromstring(f.read())
        
        for element in root.findall("resource"):
            print(f"Create resource with id {element.attrib['id']}")
            res = Resource(element.attrib["name"])
            for profile in element.findall("resprofile"):
                change_patterns=[]
                for cp in profile.findall("changepattern"):
                    change_patterns.append(cp)
                res.create_resource_profile(profile.attrib["name"], profile.attrib["role"], task=profile.attrib["task"], change_pattern=[change_patterns])

            reslist.append(res)
        return reslist
    
    print(get_all_resources("./config/res_config.xml"))

    #### Get Tasks to allocate ####

# TODO: create as function to get all task which need allocation
    import requests

    cpee_url =  f"https://cpee.org/flow/engine/16646/properties/description/"
    frag_url = f"https://cpee.org/flow/engine/15344/properties/description/"
    ns = {"cpee2": "http://cpee.org/ns/properties/2.0", 
            "cpee1":"http://cpee.org/ns/description/1.0"}

    # location
    location =  "cpee felix instance"

    # send get request and save response
    r = requests.get(url = cpee_url)
    r1 = requests.get(url = frag_url)
    # parse xml:
    task_root = etree.fromstring(r.content)
    path = (f".//{ns['cpee1']}/call | .//{ns['cpee1']}/call ")
    print(path)
    for task in task_root.xpath(".//cpee1:call | .//cpee1:manipulate", namespaces=ns):
        print(task.tag)
## TODO: allocation algorithm (tree)

    