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
                return [[self]]

        return [
             [self] + path for child in self.children for path in child.tree_paths()
        ]

    def get_branch_depth(self):
        print([[len(branch), branch[-1].get_name ]for branch in self.tree_paths()])
    
    def get_shortest_leaf(self):
        leaves = ([{ "depth": len(branch),"name": branch[-1] }for branch in self.tree_paths()])
        leaf_depths = [depth["depth"] for depth in leaves]
        return (leaves[leaf_depths.index(min(leaf_depths))]["name"])
    # TODO: Find Shortest Path in Tree

    def min_depth(self, leaf = None):
         if len(self.children) == 0:
              return 1
         
         return min([child.min_depth()+1 for child in self.children])

    def get_min_branch(self):
        x = (([child.min_depth() for child in self.children]))
        x = x.index(min(x))
        return self.children[x].get_name


    