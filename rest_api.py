import requests
import xml.etree.ElementTree as ET
from lxml import etree

# Returns a list with all tasks that need allocation
def get_tasks_to_allocate(root: etree) -> list:
    to_allocate = []
    for elem in root.iter():
        if not elem.find(".//cpee1:resources", ns) == None:
            resource = elem.find(".//cpee1:resources", ns)

            if resource in elem.getchildren():
                to_allocate.append({"id": elem.get("id"), "res_profile" : [profile.text for profile in resource.getchildren()]})
            
    return to_allocate

def allocate_tasks(to_allocate:list, available_resources: list, xml_string):
    for task in to_allocate:
        for res_role in task["roles"]:
            available_res_roles = [item for item in [resource.get_profile_list() for resource in available_resources]]
            try:
                res_role in available_res_roles
            except:
                print("no resource available")
            
            for resource in available_resources: 
                for resource_profile in resource.resourceProfiles:
                    if res_role == resource_profile["profileName"]:
                        #trigger_change_fragment
                        print("Trigger Change Fragment:", resource_profile["changeFragment"])
            #if right resource and role is available 
            # --> check for changes
            # --> add changes in xml

class Resource():
    def __init__(self):
        self.resourceProfiles:list(dict) = []
    
    def get_profile_list(self):
        profile_list = []
        for profile in self.resourceProfiles:
            profile_list.append(profile['profileName'])
        return profile_list

    def add_resource_profile(self, profileName:str, changeFragment:str, coreFragment:str):
        self.resourceProfiles.append({"profileName" : profileName, "changeFragment" : changeFragment, "coreFragment" : coreFragment})


if __name__ == "__main__":

    # api-endpoint
    cpee_url =  f"https://cpee.org/flow/engine/14567/properties/description/"

    ns = {"cpee2": "http://cpee.org/ns/properties/2.0", 
            "cpee1":"http://cpee.org/ns/description/1.0"}

    # location
    location =  "cpee felix instance"

    # send get request and save response
    r = requests.get(url = cpee_url)

    # parse xml:
    root = etree.fromstring(r.content)

    # create demo resources
    resource_1 = Resource()
    resource_1.add_resource_profile("res1", f"<manipulate id=\"a9\"/>", "xyz")
    #resource_1.add_resource_profile("res3", f"<manipulate id=\"a10\"/>")
    #resource_1.add_resource_profile("res5", f"<manipulate id=\"a11\"/>")

    to_allocate = get_tasks_to_allocate(root)
    print(to_allocate)
    allocate_tasks(to_allocate, [resource_1], root)
