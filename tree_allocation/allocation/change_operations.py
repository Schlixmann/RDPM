from ..tree.node import *
from lxml import etree
from ..helpers import *

def get_all_resource_nodes(node:Node):
    pass


def create_change_operation(allocated_branch: Node, process_model: str):

    # define namespaces
    ns = {"cpee2": "http://cpee.org/ns/properties/2.0", 
            "cpee1":"http://cpee.org/ns/description/1.0"}
    resources = allocated_branch.get_all_nodes(key="resource")

    task_id = allocated_branch.task_id
    process_model = etree.fromstring(process_model)

    elem_to_manipulate = process_model.xpath(f".//cpee1:*[@id='{task_id}']", namespaces=ns)


    
    rp = (next(rp for rp in resources[0].resource_obj.resource_profiles if rp == resources[0].resource_profile))
    #TODO maybe for multiple change patterns
    #print([x for x in rp.change_patterns[0].iter()])
    a = rp.change_patterns[0].xpath(f"//changepattern[@type]", namespaces=ns)[0].attrib["type"] 
    match a:
        case "replace":
            to_insert = rp.change_patterns[0].findall(f".//description/", ns)
            for change in to_insert[::-1]:
                process_model.find(f".//cpee1:*[@id='{task_id}']", ns).addnext(change)
            process_model.remove(elem_to_manipulate[0])

    
    return process_model
        
#TODO show that task is allocated and which resource
# test with insert and conditions
# realize rest api 
# test with different settings! 

if __name__ == "__main__":
    pass


