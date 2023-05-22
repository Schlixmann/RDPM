# TODO 
# Implement change pattern as in paper
from enum import Enum
import requests
from lxml import etree

class Direction(Enum):

    before = "before"
    after = "after"
    parallel = "parallel"

        


class ChangePattern():
    instances = []


    def __init__(self, name, direction:Direction, fragment = None, anchor:str = None, constraint:str = None, type:str = None ):
        self.name: str = name
        self.type: str 
        self.fragment: list(etree.Element) = self._get_change_fragment(fragment) if fragment != None else None
        self.anchor: str = anchor
        self.constraint: str
        try:
            self.direction: Direction = self.data_type_check(str(direction).lower().strip())
        except ValueError:
            print("Wrong value, please enter a value out of  [before, after, parallel]")
        if self.name in self.instances:
            print("Name already in use, please use different name for change_pattern")
            raise ValueError
        else: 
            ChangePattern.instances.append(self)
           

    @staticmethod
    def data_type_check(value):
        return Direction(value)
    
    def _get_change_fragment(self, instance_id):
        ns = {"cpee2": "http://cpee.org/ns/properties/2.0", 
        "cpee1":"http://cpee.org/ns/description/1.0"}
        try: 
            url = f"https://cpee.org/flow/engine/" + str(instance_id) + f"/properties/description/"
            req1 = requests.get(url)
            fragment = etree.fromstring(req1.content)
            fragment = fragment.xpath("*", namespaces=ns)

            try: 
                if len(fragment) == 0:
                    raise ValueError
                else: 
                    return fragment

            except ValueError:
                print("Cannot fetch fragment model under url: " + url)
        except TypeError:
            print(f"\"Fragment\" should be of type str or int but is type {type(fragment)}") 
        except:
            print("Error during Fragment fetch. Please check instance Id")
    
    def info(self):
        return self.__dict__
    