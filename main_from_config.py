from proc_resource import *
import time 
from lxml import etree
from tree_allocation.helpers import *
from tree_allocation.allocation.allocation import *
from PrettyPrint import PrettyPrintTree
from tree_allocation.allocation.change_operations import *



def print_allo_tree(node, indent=""):
   # Print the tree
   try:
    if type(node) == tn.TaskNode:
        print(indent , node.label)
    else: 
         print(indent, node.name)
    for child in node.children:
        print_allo_tree(child, indent + "  ")
   except Exception as e:
       print(e)

def allocate_process(cpee_url, resource_url="http://127.0.0.1:8000/resources"):
    #resources = get_all_resources("./config/res_config_5.xml")
    resources = get_all_resources(resource_url)
    tasklabels = []
    for task in get_all_tasks(cpee_url):
        try:
            tasklabels.append({"task_id": task.attrib["id"] ,"label": task.attrib["label"]})
            
        except:
            try:
                attrib = task.find(".//cpee1:parameters", ns)
                if not attrib.find(".//cpee1:label", ns).text:
                     raise Exception("Task {} has no label.".format(task.attrib["id"]))
                else:
                     tasklabels.append({"task_id": task.attrib["id"], "label": attrib.find(".//cpee1:label", ns).text })
            except Exception as e:
                print(e)
                continue
    print(tasklabels)
    print(resources)

    
    changed_model = None
    i = 0
    for task in tasklabels:
        print(f"Start Allocation of {task}")
        root = tn.TaskNode(task["task_id"], task["label"])
        try:
            build_allo_tree(root, resources)
            #print_allo_tree(root)

            pt = PrettyPrintTree(lambda x: x.children, lambda x: "task:" + str(x.label) + " " + str(x.id) if type(x) == tn.TaskNode else "res:" + str(x.name) + " rp:" + str(x.resource_profile.name))
            pt(root)

            print(root.get_best_branch(measure="expected_time", operator=max))
            best_branch, options, value, best_node = root.get_best_branch(measure="expected_time", operator=max)
        
            pt(best_node)
            # TODO: create change operation

            all_resources = best_node.get_all_nodes()
            print([resource.get_name for resource in all_resources])

            if tasklabels.index(task) == 0:
                process_model_xml, process_model_etree = get_process_model(cpee_url)
            else: 
                process_model_xml = changed_model_xml

            changed_model_xml, changed_model_etree = create_change_operation(best_node, process_model_xml)
            
            with open(f"./output/out_{str(i)}.xml", "wb") as f:
                f.write((changed_model_xml))
        except ResourceError as e:
            e.add_note(f"No allocation possible, the task: {task} is skipped")
            print("Task not allocatable:", e.task.get_name, ", Message:", e.message)

        i += 1
        
        
    with open("./output/test.xml", "wb") as f:
        f.write((changed_model_xml))
    return changed_model_xml

if __name__ == "__main__":


    cpee_url =  f"https://cpee.org/flow/engine/16646/properties/description/"
    frag_url = f"https://cpee.org/flow/engine/15344/properties/description/"
    resource_url = f"http://127.0.0.1:8000/resources"
    ns = {"cpee2": "http://cpee.org/ns/properties/2.0", 
            "cpee1":"http://cpee.org/ns/description/1.0"}       
    
    allocate_process(cpee_url, resource_url=resource_url)
    """
    resources = get_all_resources("./config/res_config_5.xml")
    tasklabels = []
    for task in get_all_tasks(cpee_url):
        try:
            tasklabels.append({"task_id": task.attrib["id"] ,"label": task.attrib["label"]})
            
        except:
            try:
                attrib = task.find(".//cpee1:parameters", ns)
                if not attrib.find(".//cpee1:label", ns).text:
                     raise Exception("Task {} has no label.".format(task.attrib["id"]))
                else:
                     tasklabels.append({"task_id": task.attrib["id"], "label": attrib.find(".//cpee1:label", ns).text })
            except Exception as e:
                print(e)
                continue
    print(tasklabels)
    print(resources)
    from tree_allocation.allocation.allocation import *
    from PrettyPrint import PrettyPrintTree
    from tree_allocation.allocation.change_operations import *
    
    changed_model = None
    i = 0
    for task in tasklabels:
        print(f"Start Allocation of {task}")
        root = tn.TaskNode(task["task_id"], task["label"])
        try:
            build_allo_tree(root, resources)
            #print_allo_tree(root)

            pt = PrettyPrintTree(lambda x: x.children, lambda x: "task:" + str(x.label) + " " + str(x.id) if type(x) == tn.TaskNode else "res:" + str(x.name) + " rp:" + str(x.resource_profile.name))
            pt(root)

            print(root.get_best_branch(measure="expected_time", operator=max))
            best_branch, options, value, best_node = root.get_best_branch(measure="expected_time", operator=max)
        
            pt(best_node)
            # TODO: create change operation

            all_resources = best_node.get_all_nodes()
            print([resource.get_name for resource in all_resources])

            if tasklabels.index(task) == 0:
                process_model_xml, process_model_etree = get_process_model(cpee_url)
            else: 
                process_model_xml = changed_model_xml

            changed_model_xml, changed_model_etree = create_change_operation(best_node, process_model_xml)
            
            with open(f"./output/out_{str(i)}.xml", "wb") as f:
                f.write((changed_model_xml))
        except ResourceError as e:
            e.add_note(f"No allocation possible, the task: {task} is skipped")
            print("Task not allocatable:", e.task.get_name, ", Message:", e.message)

        i += 1
        
        
    with open("./output/test.xml", "wb") as f:
        f.write((changed_model_xml))


## TODO: access via Rest Service

    """