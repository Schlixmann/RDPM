from ..tree.node import *
from lxml import etree
from ..helpers import *


    
    
def create_change_operation(allocated_branch: Node, process_model: str):
    print("Operations of allocated_branch: ", allocated_branch.get_all_nodes(key="task"))
    # define namespaces
    ns = {"cpee2": "http://cpee.org/ns/properties/2.0", 
            "cpee1":"http://cpee.org/ns/description/1.0"}
    resources = allocated_branch.get_all_nodes(key="resource")
    process_model = etree.fromstring(process_model)
    
 
    rp = (next(rp for rp in resources[0].resource_obj.resource_profiles if rp == resources[0].resource_profile))
    #TODO maybe for multiple change patterns
    #print([x for x in rp.change_patterns[0].iter()])
    
    for x in allocated_branch.get_all_nodes(key="task"):
        # find element to manipulate:
        task_id = x.id


        with open("process2.xml", "wb") as f:
            f.write(etree.tostring(process_model))
        #try:
        elem_to_manipulate = process_model.xpath(f".//cpee1:*[@id='{task_id}']", namespaces=ns)[0]
        #except:
        #    elem_to_manipulate = process_model.xpath(f".//*[@id='{task_id}']", namespaces=ns)[0]    

        for child in x.children:
            if len(child.resource_profile.change_patterns) > 0:
                for pattern in child.resource_profile.change_patterns:
                    a = pattern.attrib["type"]
                    match a:
                        case "replace":
                            to_insert = pattern.findall(f".//cpee1:description/", ns)
                            
                            for change in to_insert[::-1]:
                                
                                process_model.find(f".//cpee1:*[@id='{task_id}']", ns).addnext(change)
                            process_model.remove(elem_to_manipulate)
                            with open("process1.xml", "wb") as f:
                                f.write(etree.tostring(process_model))

            else:
                    
                # BaseCase to allocate an element
                # allocate element:
                allocation_attrib = elem_to_manipulate.find(f".//cpee1:resources", ns).attrib["allocated_to"] 
                if allocation_attrib != "not_allocated":
                    allocation_attrib = allocation_attrib + " & " + str(child.get_name) + " rp:" + str(child.resource_profile.name)
                    elem_to_manipulate.find(f".//cpee1:resources", ns).attrib["allocated_to"] = allocation_attrib
                else:
                    elem_to_manipulate.find(f".//cpee1:resources", ns).attrib["allocated_to"]  = str(child.get_name) + " rp:" + str(child.resource_profile.name)



                
    return process_model
    


#TODO show that task is allocated and which resource
# test with insert and conditions
# realize rest api 
# test with different settings! 

if __name__ == "__main__":
    pass
