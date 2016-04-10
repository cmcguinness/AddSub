import csv
import os
import metadata

stateNew = 0
stateDropped = 0
stateTotal = 0
stateBlackDropped = 0
stateBlackTotal = 0
stateDemDropped = 0
stateDemTotal = 0


def compare_files(name1,name2,county):
    global stateNew
    global stateDropped
    global stateTotal
    global stateBlackDropped
    global stateDemDropped

    file1 = open(name1, "r")
    file2 = open(name2, "r")

    reader1 = csv.reader(file1, delimiter = '\t')
    reader2 = csv.reader(file2, delimiter = '\t')

    rows1 = []
    rows2 = []

    for r in reader1:
        rows1.append(r)

    for r in reader2:
        rows2.append(r)

    def key_func(x):
        return int(x[1])


    rows1.sort(key=key_func)
    rows2.sort(key=key_func)

    iter1 = iter(rows1)
    iter2 = iter(rows2)

    done1 = False
    done2 = False

    # Assume at least one line in each....
    row1 = next(iter1)
    row2 = next(iter2)

    totalVoters = 0
    totalDropped = 0
    totalBlackDropped = 0
    totalBlack = 0
    totalDemDropped = 0
    totalDem = 0
    totalNew = 0
    last1 = -1
    last2 = -1

    def updateDemo(row):
        nonlocal totalBlack
        nonlocal totalDem
        nonlocal totalVoters
        global stateBlackTotal
        global stateDemTotal
        global stateTotal

        totalVoters += 1
        stateTotal += 1

        if row[20] == '3':
            totalBlack += 1
            stateBlackTotal += 1

        if row[23] == 'DEM':
            totalDem += 1
            stateDemTotal += 1


    updateDemo(row2)

    while not (done1 or done2):

        if int(row1[1]) < int(last1):
            print("Constraint violated on file 1:")
            print("\t".join(row1))
            quit(0)

        if int(row2[1]) < int(last2):
            print("Constraint violated on file 2:")
            print("\t".join(row2))
            quit(0)

        last1 = row1[1]
        last2 = row2[1]

        # Same person?
        if row1[1] == row2[1]:
            try:
                row1 = next(iter1)
            except StopIteration:
                done1 = True

            try:
                row2 = next(iter2)
                updateDemo(row2)
            except StopIteration:
                done2 = True

            continue

        if row1[1] < row2[1]:
            # print("\t".join(row1))

            totalDropped += 1
            stateDropped += 1
            if int(row1[20]) == 3:
                stateBlackDropped += 1
                totalBlackDropped += 1

            if row1[23] == 'DEM':
                totalDemDropped += 1
                stateDemDropped += 1


            try:
                row1 = next(iter1)
            except StopIteration:
                done1 = True

        else:
            totalVoters += 1
            stateTotal += 1
            totalNew += 1
            stateNew += 1
            try:
                row2 = next(iter2)
                updateDemo(row2)
            except StopIteration:
                done2 = True


    print("{},{},{},{},{},{},{},{}".format(county, totalVoters, totalNew, totalDropped, totalDem, totalDemDropped, totalBlack, totalBlackDropped))


print("County,Total,New,Dropped,Democracts,Democrats Dropped,Blacks,Blacks Dropped")

from_files = [f for f in os.listdir('/Users/charles/Projects/VoterFile/201602') if f.endswith(".txt")]
to_files = [f for f in os.listdir('/Users/charles/Projects/VoterFile/201603') if f.endswith(".txt")]

for i in range(len(from_files)):
    compare_files(os.path.join('/Users/charles/Projects/VoterFile/201602', from_files[i]),
                  os.path.join('/Users/charles/Projects/VoterFile/201603', to_files[i]),
                  metadata.county_name(from_files[i][0:3]))

print("{},{},{},{},{},{},{},{}".format('Florida', stateTotal, stateNew, stateDropped, stateDemTotal, stateDemDropped, stateBlackTotal, stateBlackDropped))
