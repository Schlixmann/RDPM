
import uuid
from .node import Node

class ResourceNode(Node):
    def __init__(self, name, resource_profile, task):
        super().__init__()
        self.name = name
        self.resource_profile = resource_profile
        self.task = task
    
    @property
    def get_name(self):
        return self.name