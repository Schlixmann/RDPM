import requests
import xml.etree.ElementTree as ET
from lxml import etree
from xml.sax.saxutils import escape

#TODO -> implement Rest API
#TODO -> implement resource definition

# Returns a list with all tasks that need allocation
def get_tasks_to_allocate(root: etree) -> list:
    to_allocate = []
    for elem in root.iter():
        if not elem.find(".//cpee1:resources", ns) == None:
            resource = elem.find(".//cpee1:resources", ns)

            if resource in elem.getchildren():
                to_allocate.append({"id": elem.get("id"), "res_profile" : [profile.text for profile in resource.getchildren()]})
            
    return to_allocate

# allocates all tasks in allocate list
# input: 
#   to_allocate: a lists with all open tasks to allocate
#   available_resources: a list with all available resource
#   xml_string: full description from cpee
def allocate_tasks(to_allocate:list, available_resources: list, xml_string):
    for task in to_allocate:
        to_manipulate: str = None

        #TODO --> implement function that finds best resource based on rule
        for res_role in task["res_profile"]:
            available_res_roles = [item for item in [resource.get_profile_list() for resource in available_resources]]
            try:
                res_role in available_res_roles
            except:
                print("no resource available")
            
            for resource in available_resources: 
                for resource_profile in resource.resourceProfiles:
                    if res_role == resource_profile["profile_name"]:
                        #trigger_change_fragment
                        print("Trigger Change Fragment:", resource_profile["change_fragment"])
                        filter = ".//cpee1:*[@id=\'" +str(task["id"]) + '\']'
                        to_manipulate = xml_string.find(filter, ns)
        
                        to_manipulate.append(resource_profile["change_fragment"])
                        to_manipulate[0] = to_manipulate[1]
                        
                        #TODO --> Remove the Original element 
                        
                        et = etree.ElementTree(xml_string)
                        et.write("xml_out.xml", pretty_print=True)
                         
                        
            #if right resource and role is available 
            # --> check for changes
            # --> add changes in xml

class Resource():
    def __init__(self):
        self.resourceProfiles:list(dict) = []
    
    def get_profile_list(self):
        profile_list = []
        for profile in self.resourceProfiles:
            profile_list.append(profile['profile_name'])
        return profile_list

    def add_resource_profile(self, profile_name:str, change_fragment:str, core_fragment:str):
        self.resourceProfiles.append({"profile_name" : profile_name, "change_fragment" : change_fragment, "core_fragment" : core_fragment})


if __name__ == "__main__":

    # api-endpoint
    cpee_url =  f"https://cpee.org/flow/engine/14567/properties/description/"
    frag_url = f"https://cpee.org/flow/engine/15344/properties/description/"
    ns = {"cpee2": "http://cpee.org/ns/properties/2.0", 
            "cpee1":"http://cpee.org/ns/description/1.0"}

    # location
    location =  "cpee felix instance"

    # send get request and save response
    r = requests.get(url = cpee_url)
    r1 = requests.get(url = frag_url)
    # parse xml:
    root = etree.fromstring(r.content)

    # create demo resources
    frag_1 = etree.fromstring(r1.content)

    # delete root ("description")
    frag_1 = etree.ElementTree(frag_1.getchildren()[0])
    frag_1 = etree.fromstring(etree.tostring(frag_1))
    
    resource_1 = Resource()
    resource_1.add_resource_profile("res1", frag_1 , "xyz")
    #resource_1.add_resource_profile("res3", f"<manipulate id=\"a10\"/>")
    #resource_1.add_resource_profile("res5", f"<manipulate id=\"a11\"/>")

    to_allocate = get_tasks_to_allocate(root)
    print(to_allocate)
    allocate_tasks(to_allocate, [resource_1], root)
