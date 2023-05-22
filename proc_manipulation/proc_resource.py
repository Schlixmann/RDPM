# TODO
# Add Resources in this File
import random
from .change_pattern import *

class Resource():
    def __init__(self, name):
        self.name: str = name
        self.resourceProfiles:list(ResourceProfile) = []
        self.activeRole: ResourceProfile = None

    def info(self):
        return self.__dict__
    
    def get_profile_list(self):
        return self.resourceProfiles

    #def add_resource_profile(self, profile_name:str, change_fragment:str, core_fragment:str, constraints:str, Direction:int): #TODO change to resource Profile only
        self.resourceProfiles.append({"profile_name" : profile_name, "change_fragment" : change_fragment, "core_fragment" : core_fragment})
    
    def create_resource_profile(self, name:str, role:str, **kwargs): #TODO change to resource Profile only
        res_profile = ResourceProfile(name=name, role=role, resource=self, **kwargs)
        self.resourceProfiles.append(res_profile)
        if len(self.resourceProfiles) == 1:
            self.activeRole = self.resourceProfiles[0].name

    
    

class ResourceProfile():
    def __init__(self, name,  role, resource=None,  change_pattern=[], task=str()):
        self.name:str = name
        self.role:str = role
        self.change_patterns:list() = list(change_pattern)
        self.task:str() = task
        self.resource: Resource = resource
    
    def info(self):
        return self.__dict__

    def add_change_pattern(self, name):
        cp = [cp.name for cp in ChangePattern.instances].index(name)
        self.change_patterns.append(ChangePattern.instances[cp])

if __name__ == "__main__":
    pass
