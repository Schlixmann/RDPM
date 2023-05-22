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
from proc_manipulation.proc_resource import *
from proc_manipulation.change_pattern import *
import time 




if __name__ == "__main__":
    reslist = []
            
    try: 
        while True:
            print("create Resource")

            X = None
            
            print("Enter Resource information, enter: name, enter: \"strg+c\" for next")
            res = Resource(input())
            reslist.append(res)
    except KeyboardInterrupt:
        print("FUCK")
        time.sleep(3)

    print("create profiles")
    for resource in reslist:
        try:
            while True:
                print("please enter input in form: \"name, role, task\"")
                name, role, task = input().split(",")
                resource.create_resource_profile(name, role, task=task)
        except KeyboardInterrupt:
            print("All Profiles created")

    # Print Info of all created resources
    for res in reslist:
        print("########")
        print(res.info(), "\n", [prof.info() for prof in res.resourceProfiles], "\n" )    

    # Create change_patterns
    try: 
        while True:
            print("Create change patterns by typing: name, direction, fragment_id, anchor")
            try:
                name, direction, fragment_id, anchor = input().split(",")
                ChangePattern(name, str(direction), int(fragment_id), str(anchor))
            except ValueError as e:
                print(e)
                print("try again")

    except KeyboardInterrupt:
        print("All change patterns created")

    print("Add change_patterns to Resource Profiles")
    for resource in reslist:
        for profile in resource.resourceProfiles:
            try: 
                
                print(f"please write the names of all change_patterns you want to add to Resource {resource.name} - Profile {profile.name}, separated by ,")
                print(f"possible names are: {[cp.name for cp in ChangePattern.instances]}")
                print(f"Go to next profile with ctrl+c")
                print("Cur. Profile = ", profile)
                print("res  prof", resource, "profile: ", profile)
                cp = None
                for pattern in cp:
                    try:
                        profile.add_change_pattern(str(pattern).lower().strip())
                    
                    except ValueError as e:
                        print(e)
                        print(f"Try again... {pattern} is not an existing change pattern in {[cp.name for cp in ChangePattern.instances]}")

                for res in reslist:
                    print([x for x in res.resourceProfiles])
                    print([x.change_patterns for x in res.resourceProfiles])
            except ValueError:
                print("Pattern name not in allowed patterns - check for typo")

        print("Going to next resource")

    for resource in reslist:
        print(f"### config for resource {resource.name}" "###")
        print(resource.info())
        for profile in resource.resourceProfiles:
            print(profile.info())
        for profile in resource.resourceProfiles:
            print(f"- {profile.name} --> fragments: {[cp.name for cp in profile.change_patterns]}", "\n")


#TODO 
# parse xml als change pattern
# create allocation algorithm
# print res list during execution!



            

            
            

