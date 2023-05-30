import uuid

class Node:
    def __init__(self):
        self.__id = str(uuid.uuid1())
        self.children = []
        self.expected_time = 0

    def add_child(self, obj):
        self.children.append(obj)

    @property
    def id(self):
        return self.__id

    def tree_paths(self, stack = [], i=0):
        if len(self.children) == 0:
                return [self]
        if self.node_type == "task":   
            # TODO decide on best resource based on measurement 
            # current decision: first in line [0]
            return [self] + [path for child in self.children for path in child.tree_paths()]
        else: 
            return [self] + [child.tree_paths() for child in self.children]
        

    def count_branch_steps(self, branch, measure=None):
        # TODO Change so different measures work
        if measure == None:
            finished_step = len([step for step in branch if type(step) != list])
        else:
            step_list = [getattr(step, measure) for step in branch if type(step) != list]
            finished_step = sum(step_list)
        open_step = [step for step in branch if type(step) == list]
        open_step = [step for sublist in open_step for step in sublist]
        if len(open_step) == 0: return finished_step
        return finished_step + self.count_branch_steps(open_step, measure=measure)

    def clean_best_branch_node(self, measure, operator):
        if len(self.children) == 0:
            return self 
        if self.node_type == "resource":
            for child in self.children:
                return child.clean_best_branch_node(measure, operator)
        else:
            if not measure:
                self.children = [self.children[0]]
            else: 
                child_compare = [getattr(child, measure) for child in self.children]
                best_child_index = child_compare.index(operator(child_compare))
                self.children = [self.children[best_child_index]]

            for child in self.children:
                return child.clean_best_branch_node(measure, operator)    

    def get_best_branch(self, measure=None, operator=None):
        # TODO should return all indices not just first. 
        #       
        all_branches = [child.tree_paths() for child in self.children]
        #print(all_branches)
        branch_measure = [self.count_branch_steps(branch, measure=measure) for branch in all_branches]#[len(branch) for branch in all_branches]
        if not operator:
            value = min(branch_measure)
        else:
            value = operator(branch_measure)
        index = branch_measure.index(value)

        best_branch = all_branches[index]       
        
        # clean node:
        best_node = best_branch[0]
        best_node.clean_best_branch_node(measure, operator)
        
        
        return best_branch, branch_measure, value, best_node

    def filter_nested_list(self, nested_list, node_type="resource"):
        open_list = [element for element in nested_list if type(element) == list]
        finished_list = [element for element in nested_list if (type(element) != list) and (getattr(element, "node_type") == node_type)]
        open_list = [step for sublist in open_list for step in sublist]
        if len(open_list) == 0:
            return finished_list
        return finished_list + self.filter_nested_list(open_list, node_type=node_type)
    
    def get_all_nodes(self, key="resource"):
        # if len(self.children) == 0:
        #     return [self]
        # for child in self.children:
        #     if self.node_type == key:
        #         return [self] + child.get_all_resource_nodes()
        #     else:
        #         return child.get_all_resource_nodes()
        nodes = self.tree_paths()
        nodes = self.filter_nested_list(nodes, node_type="resource")
        return nodes
    # TODO 
    # create method "get_best_branch" based on different optimization types (e.g. min/max/avg)
    #  -> different values from Resource Profile (sum of rp expected values)
    