import sys
import math

# sys.argv[1] will be the csv name

test1 = [['yes']]
test2 = [['yes'],['no']]
test3 = [['yes'],['yes'],['no'], ['no']]
test4 = [['yes'],['yes'],['yes']]

def entropy(fold):
    size = len(fold)
    yes_count = sum(1 if 'yes' in row else 0 for row in fold)
    no_count = size - yes_count
    p_yes, p_no  = yes_count/size , no_count/size
    entropy = -p_yes * (math.log2(p_yes) if p_yes > 0 else p_yes) - p_no*(math.log2(p_no) if p_no > 0 else p_no)

    return entropy

print(entropy(test1))
print(entropy(test2))
print(entropy(test3))
print(entropy(test4))
