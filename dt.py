import csv
import sys
import math

class Tree:

    def __init__(self, attribute):
        self.attribute = attribute
        self.leaves = {}
        self.nodes = {} 

    def set_attribute(self, attribute):
        self.attribute = attribute

    def add_leaf(self, attr_value, classification):
        self.leaves[attr_value] = classification

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
# Always pass in relevant data
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
    
    entropy = 0
    for key, value in attr_values.items():
        p_yes = value['yes']/value['size']
        entropy += -p_yes * math.log2(p_yes) 
    # Return the sub attributes and the entropy
    return [*attr_values], entropy

# Returns the majority of the examples
def majority(data):
    yes_count = 0
    for row in data:
        if 'yes' in row:
            yes_count += 1
    no_count = len(data) - yes_count
    if yes_count >= no_count:
        return True
    else:
        return False

# Returns best attribute with min T2 entropy
def choose_best_attribute(data):
    val = []
    for i in range(len(data[0])):
        val.append(entropy_T2(data, i))
    sub_attributes = None 
    min_val, index = float("-inf"), 0
    for i, value in enumerate(val):
        if value[1] < min_val:
            min_val = value[1]
            index = i
            sub_attributes = value
    # Return the best attribute and values of those attributes
    return i, sub_attributes

# Returns a set of data containing rows with sub_attribute passed
# best_attribute is the index
# sub_attribute is the v_i for that index
def select_with_v_i(data, best_attribute, sub_attribute):
    new_data = []
    for row in data:
        if row[best_attribute] == sub_attribute:
            new_data.append(row)

    return new_data

def make_split_attributes(attributes, best_attribute):
    new_attributes = []
    for attribute in attributes:
        if attribute != best_attribute: 
            new_attributes.append(attribute)

    return new_attributes

# Pass all the attributes
def DTL(data, attributes, default):
    # If examples is empty then return default
    if len(data) == 0:
        return default

    # If all examples have the same classification then return the classification
    yes_count = sum(1 if 'yes' in row else 0 for row in data)
    # This is where we return the leaf node
    if yes_count == len(data) or yes_count == 0:
        return True if 'yes' in data[0] else False
    
    mode = majority(data)
    # If attributes are empty and the data cannot be split further, return majority
    if len(attributes) == 0:
        return mode
    # Minimum T2 entropy implies highest information gain, so select this
    # feature
    best_attribute, sub_attributes = choose_best_attribute(data)
    # Build a tree with root as best
    tree = Tree(best_attribute)
    for sub_attr in sub_attributes: 
        new_data = select_with_v_i(data, best_attribute, sub_attr)
        split_attributes = make_split_attributes(attributes, best_attribute)
        sub_tree = DTL(new_data, split_attributes, mode)
        # Check if sub_tree is a boolean
        if isinstance(sub_tree, (bool,)):
            tree.add_leaf(sub_attr, sub_tree)
        else:
            tree.add_node(sub_attr, sub_tree)
    return tree

if __name__ in "__main__":
    # Read the data in first
    csvfile = sys.argv[1]
    data = []
    with open(csvfile, "r") as myfile:
        reader = csv.reader(myfile, delimiter = ',')
        for row in reader:
            data.append(row)

    # Always choose minimum T2
    
    
    print(attr_values)
