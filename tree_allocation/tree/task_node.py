
import uuid

class TaskNode:
    def __init__(self, label):
        self.__id = str(uuid.uuid1())
        self.label = label
        self.children = []

    def add_child(self, obj):
        self.children.append(obj)

    @property
    def id(self):
        return self.__id
    
