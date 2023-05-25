import uuid

class Node:
    def __init__(self):
        self.__id = str(uuid.uuid1())
        self.children = []

    def add_child(self, obj):
        self.children.append(obj)

    @property
    def id(self):
        return self.__id

    def tree_paths(self, stack = [], i=0):
        if len(self.children) == 0:
                return [[self.get_name]]
        if self.node_type == "task":   
            # TODO decide on best resource based on measurement 
            # current decision: first in line
            return [
                [self.get_name] + [path for child in self.children for path in child.tree_paths()][0]
            ]
        else: 
            return [
            [self.get_name] + [child.tree_paths() for child in self.children]
        ]

    def count_branch_steps(self, branch):
        # TODO Change so different measures work
        finished_step = len([step for step in branch if type(step) != list])
        open_step = [step for step in branch if type(step) == list]
        open_step = [step for sublist in open_step for step in sublist]
        if len(open_step) == 0: return finished_step
        return finished_step + self.count_branch_steps(open_step)

    def get_branch_depth(self):
        print([[len(branch), branch[-1]] for branch in self.tree_paths()])
    
    def get_shortest_leaf(self):
        leaves = ([{ "depth": len(branch),"name": branch }for branch in self.tree_paths()])
        leaf_depths = [depth["depth"] for depth in leaves]
        return (leaves[leaf_depths.index(max(leaf_depths))]["name"])
    # TODO: Find Shortest Path in Tree

    def get_best_branch(self, measure=None, operator=None):
        # TODO should return all indices not just first. 
        #       
        all_branches = [(branch)for branch in self.tree_paths()]
        branch_measure = [self.count_branch_steps(branch) for branch in all_branches]#[len(branch) for branch in all_branches]
        value = max(branch_measure)
        index = branch_measure.index(value)
        
        return all_branches[index], branch_measure

    def min_depth(self, leaf = None):
         if len(self.children) == 0:
              return 1
         
         return min([child.min_depth()+1 for child in self.children])

    def get_min_branch(self):
        x = (([child.min_depth() for child in self.children]))
        x = x.index(min(x))
        return self.children[x]


    # TODO 
    # create method "get_best_branch" based on different optimization types (e.g. min/max/avg)
    #  -> different values from Resource Profile (sum of rp expected values)
    