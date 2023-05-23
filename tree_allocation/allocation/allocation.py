from tree_allocation.tree import task_node as tn
from tree_allocation.tree import res_node as rn

from proc_resource import *
from lxml import etree

ns = {"cpee2": "http://cpee.org/ns/properties/2.0", 
        "cpee1":"http://cpee.org/ns/description/1.0"}
        # send get request and save response
def parse_tasks(xml_string:str):
    #parsed = etree.fromstring(xml_string)
    parsed = xml_string
    for i in parsed.xpath(".//call | .//manipulate"):
        print(i)
    tasklist = []
    for task in parsed.xpath(".//call | .//manipulate"):
        # TODO: add for call type: Label is stored as parameter
        tasklist.append(task.attrib["label"])

    return tasklist

def get_allocation(task, av_resources:Resource=[], excluded=[]):
    root = tn.TaskNode(task)
    #excluded = excluded.append(root)

    for resource in av_resources:
        for profile in resource.resourceProfiles:
            if task.lower() == profile.task.lower():
                root.add_child(rn.ResourceNode(resource.name, profile, profile.task))
    if len(root.children) == 0:
        return root
    
    for resource in root.children:
        #TODO: change_pattern is list of lists but should be list
        #resource.resource_profile.change_pattern = resource.resource_profile.change_pattern[0]
        if len(resource.resource_profile.change_pattern) > 0:
            for change_pattern in resource.resource_profile.change_pattern:
                #TODO check for excluded
                tasks = parse_tasks(change_pattern)
                for task in tasks:
                    resource.add_child(get_allocation(task, av_resources, excluded=excluded))
        else:
            return root

