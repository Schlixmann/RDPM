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

## TODO: allocation algorithm (tree)