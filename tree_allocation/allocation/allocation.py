from tree_allocation.tree import task_node as tn
from tree_allocation.tree import res_node as rn

from proc_resource import *
from lxml import etree

ns = {"cpee2": "http://cpee.org/ns/properties/2.0", 
        "cpee1":"http://cpee.org/ns/description/1.0"}


def parse_tasks(xml_string:str):
    #parsed = etree.fromstring(xml_string)
    parsed = xml_string
    tasks = []
    roles = []
    for task in parsed.xpath(".//call | .//manipulate"):
        if task.tag == "manipulate":
            # TODO: add for call type: Label is stored as parameter
            roles = [role.text for role in task.findall(".//resource", ns)]
            label = task.attrib["label"]

        else: 
            roles = [role.text for role in task.findall(".//resource", ns)]
            label = task.find(".//parameters/label").text
        tasks.append({"label": label, "roles": roles})
    return tasks

# TODO: allowed roles for one Task

def build_allo_tree(root, av_resources:Resource=[], excluded=[], task_parent=None, res_parent=None):
    # TODO: Multiple RP's for one resource where one RP is not possible must be created still.
    for resource in av_resources:
        for profile in resource.resourceProfiles:
            if root.label.lower() == profile.task.lower() and (profile.role in root.allowed_roles if len(root.allowed_roles) > 0 else True): 
                root.add_child(rn.ResourceNode(resource.name, profile, profile.task))
    if len(root.children) == 0:
        try:
            task_parent.children = [task for task in task_parent.children if task.resource_profile != res_parent.resource_profile]
        except AttributeError:
            print("No fitting resource for core task available")
        return root
        
    
    for resource in root.children:
        if len(resource.resource_profile.change_pattern) > 0:
            for change_pattern in resource.resource_profile.change_pattern:
                #TODO check for excluded
                tasks = parse_tasks(change_pattern)
                for task in tasks:
                    task = tn.TaskNode(task["label"], allowed_roles=task["roles"])
                    resource.add_child(build_allo_tree(task, av_resources, excluded=excluded, task_parent=root, res_parent=resource))
    return root



