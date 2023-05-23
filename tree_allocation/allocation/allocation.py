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
    tasklist = []
    for task in parsed.xpath(".//call | .//manipulate"):
        # TODO: add for call type: Label is stored as parameter
        tasklist.append(task.attrib["label"])

    return tasklist

def get_allocation(root, av_resources:Resource=[], excluded=[], task_parent=None, res_parent=None):
    # TODO: Multiple RP's for one resource where one RP is not possible must be created still.
    for resource in av_resources:
        for profile in resource.resourceProfiles:
            if root.label.lower() == profile.task.lower():
                root.add_child(rn.ResourceNode(resource.name, profile, profile.task))
    if len(root.children) == 0:
        root.label = "to_delete"
        task_parent.children.remove(res_parent)
        return root
        
    
    for resource in root.children:
        #TODO: change_pattern is list of lists but should be list
        #resource.resource_profile.change_pattern = resource.resource_profile.change_pattern[0]
        if len(resource.resource_profile.change_pattern) > 0:
            for change_pattern in resource.resource_profile.change_pattern:
                #TODO check for excluded
                tasks = parse_tasks(change_pattern)
                for task in tasks:
                    task = tn.TaskNode(task)
                    resource.add_child(get_allocation(task, av_resources, excluded=excluded, task_parent=root, res_parent=resource))
    return root



