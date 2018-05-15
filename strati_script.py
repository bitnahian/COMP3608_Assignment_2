import csv

yes = []
no = []

fold = 10

with open('pima.csv', newline = '') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        if 'yes' in row:
            yes.append(row)
        else:
            no.append(row)

stratified = [ [] for x in range(fold)] # Create the stratification list

index = 0

while len(yes) > 0 or len(no) > 0: 
    if len(yes) > 0:
        stratified[index%fold].append(yes[0])
        del yes[0]
        index += 1
        continue
    if len(no) > 0:
        stratified[index%fold].append(no[0])
        del no[0]
        index += 1
        continue

with open('pima-folds.csv', 'w', newline = '') as writefile:
    csvwriter = csv.writer(writefile, delimiter = ",")
    for index, folds in enumerate(stratified):
        writefile.write("fold{}\n".format(index+1)) 
        for row in folds:
            csvwriter.writerow(row)
        if index < fold - 1:
            writefile.write("\n")
