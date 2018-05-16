import sys
import csv
import math
import statistics


# Reads the csv containing the training set
def readData():
    with open(sys.argv[1], newline='') as training_data:
        reader = csv.reader(training_data, delimiter=',')

        for row in reader:
            training_set.append(row)

            if row[len(row) - 1] == 'yes':
                list_yes.append(row)

            elif row[len(row) - 1] == 'no':
                list_no.append(row)


# Reads the csv containing the testing set
def readTestData():
    with open(sys.argv[2], newline='') as testing_data:
        reader = csv.reader(testing_data, delimiter=',')

        for row in reader:
            testing_set.append(row)


# For every attribute in the yes and no list, calculate the mean and variance using statistics lib
def cal_mean_var(dataset):
    list_mean = {}
    list_var = {}

    for i in range(len(dataset[0]) - 1):
        column = list(map(lambda row: float(row[i]), dataset))
        list_mean[i] = statistics.mean(column)
        list_var[i] = statistics.variance(column, list_mean[i])

    return list_mean, list_var


# Calculate the pdf for the no classifier given the specific value, the type of attribute, mean and variance
# Return the value for further calculation
def pdf(x, index, list_var, list_mean):
    power = math.pow((x - list_mean[index]), 2) / (2 * list_var[index])
    exponent_val = math.pow(math.e, -power)

    final_val = (1 / (math.sqrt(2 * list_var[index] * math.pi))) * exponent_val

    return final_val


# List of the training data, testting data, mean of all the attrs, variance of the attrs and list of yes and no
training_set = []
testing_set = []
list_yes = []
list_no = []
list_mean_no = {}
list_mean_yes = {}
list_var_no = {}
list_var_yes = {}
