import csv
import sys

import naive_bayes as nb
import decision_tree as dt


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

        # Create attributes with all the columns
        attributes = [x for x in range(len(data[0])-1)]
        # Initial call
        dt.tree = dt.DTL(data, attributes, False)

        for test in tests:
            output = "yes" if dt.classify(dt.tree, test) else "no"
            print(output)

    elif mode == "NB":

        # Carry this out if the third arg is calling for Naive Bayes
        nb.readData()
        nb.readTestData()
        nb.list_mean_no, nb.list_var_no = nb.cal_mean_var(nb.list_no)
        nb.list_mean_yes, nb.list_var_yes = nb.cal_mean_var(nb.list_yes)

        # Calculate the numerator bit for the classifiers, i.e., yes and no
        # Compare the probability of the classifiers and based on that, predict the outcome.
        for row in nb.testing_set:
            prob_yes = 1
            prob_no = 1
            for index, data in enumerate(row):
                prob_yes *= nb.pdf(float(data), index, nb.list_var_yes, nb.list_mean_yes)
                prob_no *= nb.pdf(float(data), index, nb.list_var_no, nb.list_mean_no)

            prob_yes *= len(nb.list_yes) / len(nb.training_set)
            prob_no *= len(nb.list_no) / len(nb.training_set)

            output = 'yes' if prob_yes >= prob_no else 'no'
            print(output)
