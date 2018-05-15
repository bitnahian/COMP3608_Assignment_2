import csv
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


def entropy_T1(data):
    size = len(data)
    yes_count = sum(1 if 'yes' in row else 0 for row in data)
    no_count = size - yes_count
    p_yes, p_no  = yes_count/size , no_count/size
    entropy = -p_yes * (math.log2(p_yes) if p_yes > 0 else p_yes) - p_no*(math.log2(p_no) if p_no > 0 else p_no)

    return entropy

# attribute is actually the index which represents the column
def entropy_T2(data, attribute):
    # Add to attr_vals as you find more attribute_values
    attr_values = {} # These will be the keys so make sure to return them every time
    for row in data:
        # For the particular value of the attribute
        attr_val = row[attribute]
        # Add to the dictionary if it doesn't exit
        if attr_val not in attr_values:
            attr_values[attr_val] = { 'size': 0, 'yes': 0 }
        # Increment the yes counter if it yields yes
        if 'yes' in row:
            attr_values[attr_val]['yes'] += 1
        # Always increment the size
        attr_values[attr_val]['size'] += 1
    
    return attr_values


if __name__ in "__main__":
    # Read the data in first
    csvfile = sys.argv[1]
    data = []
    with open(csvfile, "r") as myfile:
        reader = csv.reader(myfile, delimiter = ',')
        for row in reader:
            data.append(row)

    attr_values = entropy_T2(data, 1)
    print(attr_values)
