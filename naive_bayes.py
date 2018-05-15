import sys
import math
import csv




def readData():
    with open(sys.argv[1], newline='') as training_set:
        reader = csv.reader(training_set, delimiter=',')
        for row in reader:



