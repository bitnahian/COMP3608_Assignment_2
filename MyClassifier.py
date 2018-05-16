import csv
import sys

import naive_bayes as nb
import decision_tree as dt


    # Reads the csv containing the training set
def readData(filename):
    sset = []
    with open(filename, newline='') as data:
        reader = csv.reader(data, delimiter=',')

        for row in reader:
            sset.append(row)

    return sset

def run_nb(training_set, testing_set):
    list_yes = []
    list_no = []
    
    for row in training_set:
        if row[len(row) - 1] == 'yes':
            list_yes.append(row)

        elif row[len(row) - 1] == 'no':
            list_no.append(row)

    list_mean_no, list_var_no = nb.cal_mean_var(list_no)
    list_mean_yes, list_var_yes = nb.cal_mean_var(list_yes)

    # Calculate the numerator bit for the classifiers, i.e., yes and no
    # Compare the probability of the classifiers and based on that, predict the outcome.
    outputs = []
    for row in testing_set:
        prob_yes = 1
        prob_no = 1
        for index, data in enumerate(row):
            if data == 'yes' or data == 'no':
                continue
            prob_yes *= nb.pdf(float(data), index, list_var_yes, list_mean_yes)
            prob_no *= nb.pdf(float(data), index, list_var_no, list_mean_no)

        prob_yes *= len(list_yes) / len(training_set)
        prob_no *= len(list_no) / len(training_set)

        output = 'yes' if prob_yes >= prob_no else 'no'
        outputs.append(output)
    return outputs

def run_dt(data, tests):
        
    # Create attributes with all the columns
    attributes = [x for x in range(len(data[0])-1)]
    # Initial call
    dt.tree = dt.DTL(data, attributes, False)
    # dt.printTree(dt.tree, 0)
    outputs = []
    for test in tests:
        outputs.append("yes" if dt.classify(dt.tree, test) else "no")

    return outputs

if __name__ in "__main__":
    # Read the data in first
    csvfile = sys.argv[1]
    testfile = sys.argv[2]
    mode = sys.argv[3]
    # List of the training data, testting data, mean of all the attrs, variance of the attrs and list of yes and no
    training_set = []
    testing_set = []

    # Carry this out if the third arg is calling for Naive Bayes
    training_set = readData(csvfile)
    testing_set = readData(testfile)

    if mode == "DT":
        outputs = run_dt(training_set, testing_set)
    elif mode == "NB":
        outputs = run_nb(training_set, testing_set)

    for output in outputs:
        print(output)
