import numpy as np

import copy
# Imagine that this wraps at 20, like the H values wrap at 180
#colourList = [2, 3, 4, 4, 5, 5, 5, 6, 6, 7, 12, 13, 14, 14, 15, 15, 15, 16, 16, 17]
colourList = [[0,0] , [0,0], [0,0], [1,0], [1,0], [2,0], [7,0], [8,0], [9,0], [9,0], [10,0], [10,0], [10,0], [11,0], [11,0], [12,0], [13,0], [13,0], [14,0], [15,0]]


groups = 2
groupSize=10
bestStd =1000

def formSublist(index, applyWrap):

    # This is a pile of nonsense
    tempList = copy.deepcopy(colourList)

    if (index+groupSize) <= len(tempList):
        sublist = tempList[index: (index+groupSize)]

    else:
        #sublist = [x-20 for x in tempList[index: ]] + tempList[ : (index+groupSize)%groupSize]
        if applyWrap:
            start = tempList[ : (index+groupSize)%groupSize]
            wrapped = tempList[index: ]
            print("wrapped:{0}".format(wrapped))
            print(start)

            for element in wrapped:
                element[0] -= 20

            sublist = wrapped + start

        else:
            sublist = tempList[index: ] + tempList[ : (index+groupSize)%groupSize]

    return sublist


position = 0
bestPosition = 0


for x in range(0, groupSize):
    print "NEXT"
    # For each group positioning
    firstList = formSublist(x, True)
    secondList = formSublist(x+groupSize, True)

   # print(firstList)
   # print(secondList)
    #for groups in range(0, groups):

    stdDev = np.std([item[0] for item in firstList])+ np.std([item[0] for item in secondList])
    print(stdDev)
    if stdDev < bestStd:
        bestStd = stdDev
        bestPosition = position

    position += 1

print "BEST GROUPING IS"
print(bestPosition)

print(formSublist(bestPosition, False))
print(formSublist(bestPosition + groupSize, False))


