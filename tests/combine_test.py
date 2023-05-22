import unittest
from proc_manipulation.proc_resource import *
from proc_manipulation.change_pattern import *

class TestEvent(unittest.TestCase):
    def test_combinations(self):
        r1 = Resource("r1")
        r2 = Resource("r2")

        r1.create_resource_profile("p1", "doc", task="a1")
        r1.create_resource_profile("p2", "nurse", task="a1")

        r2.create_resource_profile("p1", "doc", task="a1")
        r2.create_resource_profile("p2", "nurse", task="a2")

        cp1 = ChangePattern("cp1", "after", "15344" "a1")
        cp2 = ChangePattern("cp2", "after", "15344" ,"a2")
        cp3 = ChangePattern("cp3", "before", "15344" ,"a3")

        r1.resourceProfiles[0].add_change_pattern("cp1")
        r1.resourceProfiles[0].add_change_pattern("cp3")
        r1.resourceProfiles[1].add_change_pattern("cp2")
        r1.resourceProfiles[1].add_change_pattern("cp3")#

        r2.resourceProfiles[0].add_change_pattern("cp2")
        r2.resourceProfiles[1].add_change_pattern("cp3")

        for i in [r1,r2]:
            print("Resource Name. ", i.name)
            for profile in i.resourceProfiles:
                print("Profile.name: ",  profile.name)
                print(profile.change_patterns[0].fragment)
    