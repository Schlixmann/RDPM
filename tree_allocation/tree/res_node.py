
import uuid
from .node import Node

class ResourceNode(Node):
    def __init__(self, resource_obj, name, resource_profile, task, measure={}):
        super().__init__()
        self.resource_obj = resource_obj
        self.name = name
        self.resource_profile = resource_profile
        self.task = task
        self.node_type = "resource"

        self.measure = measure
        
    @property
    def get_name(self):
        return self.name