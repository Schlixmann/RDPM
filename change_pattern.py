# TODO 
# Implement change pattern as in paper
from enum import Enum

class Direction(Enum):
    before = "before"
    after = "after"
    parallel = "parallel"

class ChangePattern():

    def __init__(self, name, direction:Direction, **kwargs):
        self.name: str = name
        self.type: str 
        self.fragment: str
        self.anchor: str
        self.constraint: str
        self.direction: Direction = self.data_type_check(direction)

    @staticmethod
    def data_type_check(value):
        return Direction(value)
    
    def info(self):
        return self.__dict__
    