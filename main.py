# TODO
# create a Testbench with multiple test cases on smaller Processes first
# 1. Sequential with recursive insertion
#   -> Some resource combinations should breach constrain

# 2. Parallel with recoursive insertion
#   -> Some resource combinations should brach availability

# 3. Parallel in a higher level than insertion.
#   -> check if parallel is identified in smallest fragment

# 4. Insert a high ranked parallel into cpee tree
#   -> Is it possible and can it breach?
from proc_resource import *
import time 

if __name__ == "__main__":
    reslist = []
            
    try: 
        while True:
            print("create Resource")

            X = None
            
            print("Enter Resource information, enter: name, enter: \"X\" for next")
            res = Resource(input())
            reslist.append(res)
    except KeyboardInterrupt:
        print("FUCK")
        time.sleep(3)

    print("create profiles")
    for resource in reslist:
        try:
            while True:
                print("please enter input in form: \"name, role, change_pattern, task\"")
                name, role, change_pattern, task = input().split(",")
                resource.create_resource_profile(name, role, change_pattern=change_pattern, task=task)
        except KeyboardInterrupt:
            print("All Profiles created")

    for res in reslist:
        print(res.info(), [prof.info() for prof in res.resourceProfiles] )    

#TODO 
# parse xml als change pattern
# create allocation algorithm
# print res list during execution!



            

            
            

