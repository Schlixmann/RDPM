import uuid
from .node import Node

class TaskNode(Node):
    def __init__(self, task_id, label, allowed_roles=[]):
        super().__init__()
        self.task_id = task_id
        self.label = label
        self.allowed_roles = allowed_roles  
        self.node_type = "task"

    @property
    def id(self):
        return self.__id
    
    @property
    def get_name(self):
        return self.label