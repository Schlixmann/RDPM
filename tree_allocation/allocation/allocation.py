from tree_allocation.tree import task_node as tn
from tree_allocation.tree import res_node as rn

from proc_resource import *
from lxml import etree
import warnings

ns = {"cpee2": "http://cpee.org/ns/properties/2.0", 
        "cpee1":"http://cpee.org/ns/description/1.0"}


def parse_tasks(xml_string:str):
    ns = {"cpee2": "http://cpee.org/ns/properties/2.0", 
        "cpee1":"http://cpee.org/ns/description/1.0"}
    #parsed = etree.fromstring(xml_string)
    parsed = xml_string
    tasks = []
    roles = []

    for task in parsed.xpath(".//cpee1:call | .//cpee1:manipulate", namespaces=ns):
        if task.tag == etree.QName(ns["cpee1"], "manipulate"):
            # TODO: add for call type: Label is stored as parameter
            task_id = task.attrib["id"]
            roles = [role.text for role in task.findall(".//cpee1:resource", ns)]
            label = task.attrib["label"]

        else: 
            task_id = task.attrib["id"]
            roles = [role.text for role in task.findall(".//cpee1:resource", ns)]
            label = task.find(".//cpee1:parameters/cpee1:label", ns).text
        tasks.append({"task_id": task_id, "label": label, "roles": roles})
    return tasks

def build_allo_tree(root, av_resources:Resource=[], excluded=[], task_parent=None, res_parent=None):
    # TODO: Multiple RP's for one resource where one RP is not possible must be created still.
    
    for resource in av_resources:
        for profile in resource.resource_profiles:
            if root.label.lower() == profile.task.lower() and (profile.role in root.allowed_roles if len(root.allowed_roles) > 0 else True): 
                root.add_child(rn.ResourceNode(resource, resource.name, profile, profile.task, profile.measure))

    if len(root.children) == 0:
        if not task_parent:
            warnings.warn("No resource for a core task")
            raise(ResourceError(root))
        # TODO Attribute error does not happen, situation is not cancelled
        task_parent.children = [task for task in task_parent.children if task.resource_profile != res_parent.resource_profile]
        if len(task_parent.children) == 0:
            warnings.warn("The task can not be allocated due to missing resource availability", ResourceWarning)
            raise(ResourceError(task_parent))
        
        return root
        
    
    for resource in root.children:
        ex_branch = excluded
        if len(resource.resource_profile.change_patterns) > 0:
            for change_patterns in resource.resource_profile.change_patterns:

                tasks = parse_tasks(change_patterns)
                #print(ex_branch , "and \n ", tasks)
                if any(x['label'].lower() in map(lambda d: d["label"].lower(), tasks) for x in ex_branch): 
                    print(f"Break reached, task {tasks} in excluded")
                    root.children.remove(resource)
                    break

                for task in tasks:
                    ex_branch = ex_branch + [task]
                    task = tn.TaskNode(task["task_id"], task["label"], allowed_roles=task["roles"])
                    resource.add_child(build_allo_tree(task, av_resources, excluded=ex_branch, task_parent=root, res_parent=resource))
                
    return root

class ResourceError(Exception):
    # Exception is raised if no sufficiant allocation for a task can be found for available resources
    
    def __init__(self, task, message=f"No valid resource allocation can be found for the given set of available resources"):
        self.task = task
        self.message = message
        super().__init__(self.message)

class ResourceWarning(UserWarning):
    pass
# TODO 
# 1. get allocation for each task. 
# 2. build change operations for this task
# 3. Integrate change operations in original RPST
# 4. Make accessible and return to CPEE
