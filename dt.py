import sys
import math

# sys.argv[1] will be the csv name

#test1 = [['yes']]
#test2 = [['yes'],['no']]
#test3 = [['yes'],['yes'],['no'], ['no']]
#test4 = [['yes'],['yes'],['yes']]
class Node:

    def __init__(self):
        self.attribute = None
        self.leaves = {}
        self.nodes = {} 

    def set_attribute(self, attribute):
        self.attribute = attribute

    def add_yes_leaf(self, attr_value):
        self.leaves[attr_value] = True
        
    def add_no_leaf(self, attr_value):
        self.leaves[attr_value] = False

    def add_node(self, attr_value, node):
        self.nodes[attr_value] = node


def entropy(fold):
    size = len(fold)
    yes_count = sum(1 if 'yes' in row else 0 for row in fold)
    no_count = size - yes_count
    p_yes, p_no  = yes_count/size , no_count/size
    entropy = -p_yes * (math.log2(p_yes) if p_yes > 0 else p_yes) - p_no*(math.log2(p_no) if p_no > 0 else p_no)

    return entropy

