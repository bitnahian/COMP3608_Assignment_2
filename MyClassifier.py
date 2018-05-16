import csv
import sys
import math

class Tree:

    def __init__(self, attribute, default):
        self.attribute = attribute
        self.default = default
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
# Always pass in relevant data, i.e. with split attributes
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
        p_no = (value['size']-value['yes'])/value['size'] 
        total_size = len(data)
        entropy += (-p_yes * (math.log2(p_yes) if p_yes > 0 else p_yes)-p_no*(math.log2(p_no) if p_no > 0 else p_no))* (value['size']/total_size) 
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
def choose_best_attribute(data, attributes):
    val = []
    for i in attributes:
        val.append((i, entropy_T2(data, i)))
    sub_attributes = None 
    min_val, index = float("inf"), 0
    # This index isn't representative of what should be the best attribute
    for value in val:
        if value[1][1] < min_val:
            min_val = value[1][1]
            index = value[0]
            sub_attributes = value[1][0]
    # Return the best attribute and values of the sub_attributes
    return index, sub_attributes

# Returns a set of data containing rows with sub_attribute passed
# best_attribute is the index
# sub_attribute is the v_i for that index
def select_with_v_i(data, best_attribute, sub_attribute):
    new_data = []
    for row in data:
        if row[best_attribute] == sub_attribute:
            # Make a new row without the column containing best_attr
            new_data.append(row)
    return new_data

def make_split_attributes(attributes, best_attribute):
    new_attributes = []
    for attribute in attributes:
        new_attributes.append(attribute)
    
    new_attributes.remove(best_attribute) 
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
    best_attribute, sub_attributes = choose_best_attribute(data, attributes)
    # Build a tree with root as best
    tree = Tree(best_attribute, mode)
    # For all sub_attributes in the best_attribute
    for sub_attr in sub_attributes:
        # Make new relevant data containing only those with sub_attribute
        # i.e. this is the part where we are technically doing the and condition
        new_data = select_with_v_i(data, best_attribute, sub_attr)
        # Create new list of attribute by splitting best_attribute from list of
        # attributes to pass in the recursive call
        split_attributes = make_split_attributes(attributes, best_attribute)
        # Create a sub tree, which should either yield a leaf or a sub_tree
        sub_tree = DTL(new_data, split_attributes, mode)
        # Check if sub_tree is a boolean
        if isinstance(sub_tree, (bool,)):
            tree.add_leaf(sub_attr, sub_tree)
        else:
            tree.add_node(sub_attr, sub_tree)
    return tree

def printTree(tree, level):
    levels = str(tree.attribute) + " "
    for i in range(level):
        levels += " | "
    for leaf, value in tree.leaves.items():
        print("{}{} : {}".format(levels,leaf,value))
    for node, value in tree.nodes.items():
        print("{}{} :".format(levels, node))
        printTree(value, level+1)

def classify(tree, test):
    index = tree.attribute
    branch = test[index]

    # Check in leaf
    if branch in tree.leaves:
        return tree.leaves[branch]
    elif branch in tree.nodes:
        return classify(tree.nodes[branch], test)
    else:
        return tree.default

if __name__ in "__main__":
    # Read the data in first
    csvfile = sys.argv[1]
    testfile = sys.argv[2]
    mode = sys.argv[3]

    tests = []
    data = []
    with open(csvfile, "r") as myfile:
        reader = csv.reader(myfile, delimiter = ',')
        for row in reader:
            data.append(row)
    with open(testfile, "r") as myfile:
        reader = csv.reader(myfile, delimiter = ',')
        for row in reader:
            tests.append(row)

    # Create attributes with all the columns
    attributes = [x for x in range(len(data[0])-1)]
    # Initial call
    tree = DTL(data, attributes, False)
    # printTree(tree, 0)
    if mode == "DT":
        for test in tests:
            output = "yes" if classify(tree, test) else "no"
            print(output) 
    else:
        for test in tests:
            print("yes")
