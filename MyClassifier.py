import csv
import sys

import naive_bayes as nb
import decision_tree as dt


def run_nb(training_set, testing_set):
    list_mean_no, list_var_no = nb.cal_mean_var(list_no)
    list_mean_yes, list_var_yes = nb.cal_mean_var(list_yes)

    # Calculate the numerator bit for the classifiers, i.e., yes and no
    # Compare the probability of the classifiers and based on that, predict the outcome.
    outputs = []
    for row in testing_set:
        prob_yes = 1
        prob_no = 1
        for index, data in enumerate(row):
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
    
    outputs = []
    for test in tests:
        outputs.append("yes" if dt.classify(dt.tree, test) else "no")

    return outputs

if __name__ in "__main__":
    # Read the data in first
    csvfile = sys.argv[1]
    testfile = sys.argv[2]
    mode = sys.argv[3]

    if mode == "DT":
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
        outputs = run_dt(data, tests)
        
    elif mode == "NB":

        # List of the training data, testting data, mean of all the attrs, variance of the attrs and list of yes and no
        training_set = []
        testing_set = []

        # Carry this out if the third arg is calling for Naive Bayes
        training_set, list_yes, list_no = nb.readData(csvfile)
        testing_set = nb.readTestData(testfile)
        outputs = run_nb(training_set, testing_set)

    for output in outputs:
        print(output)
