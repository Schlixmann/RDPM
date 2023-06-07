from proc_resource import *
from tree_allocation.allocation.allocation import *
from tree_allocation.allocation.change_operations import * 
from PrettyPrint import PrettyPrintTree
from pptree import *
from lxml import etree
import requests
import logging
logger = logging.getLogger(__name__)

def get_all_resources(resource_url):

        r = requests.get(url = resource_url)
        print("Resource status_code: ", r.status_code)
        root = etree.fromstring(r.content)
        reslist = []
        init_measure_dict = dict(map(lambda e: (e.tag, 0), root.xpath("//measures/*")))
        print(f"Dict of Measures: ", init_measure_dict)
        
        for element in root.xpath("//resource"):
            print(f"Create resource with id {element.attrib['id']}")
            res = Resource(element.attrib["name"])
            
            for profile in element.xpath("resprofile"):
                change_patterns = [] + profile.xpath("changepattern")
                measure_dict = init_measure_dict | dict(map(lambda e: (e.tag, float(e.text)), profile.xpath("measures/*")))
                
                logger.debug(f"init_measure_dict of {element} : {profile}: {measure_dict}")
                logger.debug(f"check_init_measure: {init_measure_dict}")
                
                res.create_resource_profile(profile.attrib["name"], profile.attrib["role"], task=profile.attrib["task"], change_patterns=change_patterns, measure=measure_dict)

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
        tasks = root.xpath(".//cpee1:call | .//cpee1:manipulate", namespaces=ns)
        
        return tasks

def get_process_model(cpee_url):
        # send get request and save response
        r = requests.get(url = cpee_url)

        # parse xml:
        root = etree.fromstring(r.content)
        xml_string = r.content
        with open("./config/xml_model.xml", "wb") as f:
            f.write(xml_string)
        return xml_string, root

def allocate_process(cpee_url, resource_url="http://127.0.0.1:8000/resources", measure=None, operator=min):
    #resources = get_all_resources("./config/res_config_5.xml")
    resources = get_all_resources(resource_url)
    logger.info(f"Test logging from module {[r.name for r in resources]}")
    process_model_xml, process_model_etree = get_process_model(cpee_url)
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
    print("Tasklabels: ", tasklabels)
    print("Resource: ", resources)

    
    
    i = 0
    for task in tasklabels:
        print(f"Start Allocation of {task}")
        root = tn.TaskNode(task["task_id"], task["label"])
        try:
            build_allo_tree(root, resources)
            #print_allo_tree(root)

            pt = PrettyPrintTree(lambda x: x.children, lambda x: "task:" + str(x.label) + " " + str(x.id) if type(x) == tn.TaskNode else "res:" + str(x.name) + " rp:" + str(x.resource_profile.name) + f"\n {str(measure)}: "  + str(x.measure[measure]))
            pt(root)

            
            best_branch, branch_measure, value, best_node = root.get_best_branch(measure=measure, operator=operator)
            print("Best_branch", f"All branch measures: {branch_measure}, best measure: {value}")
            pt(best_node)
            # TODO: create change operation

            all_resources = best_node.get_all_nodes()
            print([resource.get_name for resource in all_resources])

            process_model_xml, changed_model_etree = create_change_operation(best_node, process_model_xml)
            
            with open(f"./output/out_{str(i)}.xml", "wb") as f:
                f.write((process_model_xml))

            logger.info(f"Task successfully allocate: {root.get_name}")
        except ResourceError as e:
            e.add_note(f"No allocation possible, the task: {task} is skipped")
            print("Task not allocatable:", e.task.get_name, ", Message:", e.message)
            
        #except Exception as e:
        #    print("Allocation Failed")
        #    print(e)
            
        i += 1
        
        
    with open("./output/test.xml", "wb") as f:
        f.write((process_model_xml))
    return process_model_xml
