import unittest
from proc_manipulation.change_pattern import * 

class TestEvent(unittest.TestCase):
    def test_changePattern(self):
        cp1 = ChangePattern("test", "after")
        print(cp1.info())
        
        try:
            cp2 = ChangePattern("failure_test", "titatata")
            
        except:
            print("Wrong Value for cp2")
    
    def test_direction(self):
        print(Direction("after"))

    def test_changePattern_url(self):
        cp1 = ChangePattern("test", "after", fragment= 15344)
        print(cp1.info())

    
        