
import uuid
class ResourceNode:
    def __init__(self, name, resource_profile, task):
        self.__id = str(uuid.uuid1())
        self.name = name
        self.resource_profile = resource_profile
        self.task = task
        self.children = []

    def add_child(self, obj):
        self.children.append(obj)

    @property
    def id(self):
        return self.__id