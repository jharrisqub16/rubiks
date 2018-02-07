import numpy as np

# Imagine that this wraps at 20, like the H values wrap at 180
#colourList = [2, 3, 4, 4, 5, 5, 5, 6, 6, 7, 12, 13, 14, 14, 15, 15, 15, 16, 16, 17]
colourList = [0, 0, 0, 1, 1, 2, 7, 8, 9, 9, 10, 10, 10, 11, 11, 12, 13, 13, 14, 15]


groups = 2
groupSize=10
bestStd =1000

def formSublist(index):
    if (index+groupSize) <= len(colourList):
        sublist = colourList[index: (index+groupSize)]

        return sublist
    else:
        sublist = [x-20 for x in colourList[index: ]] + colourList[ : (index+groupSize)%groupSize]

        return sublist


position = 0
bestPosition = 0

for x in range(0, groupSize):
    print "NEXT"
    # For each group positioning
    firstList = formSublist(x)
    secondList = formSublist(x+groupSize)

    print(firstList)
    print(secondList)
    #for groups in range(0, groups):

    stdDev = np.std(firstList) + np.std(secondList)
    if stdDev < bestStd:
        bestStd = stdDev
        bestPosition = position

    position += 1


print "BEST GROUPING IS"
print(formSublist(bestPosition))
print(formSublist(bestPosition + groupSize))
