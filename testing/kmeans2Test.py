#from numpy import array
import numpy as np
from scipy.cluster.vq import vq, kmeans, whiten, kmeans2

import cv2

from collections import Counter
features  = np.array([  [30.,100.],
                        [30.,100. ],
                        [30.,100. ],
                        [30.,100. ],
                        [30.,100. ],
                        [30.,100. ],
                        [30.,100. ],
                        [30.,100. ],
                        [50.,40.],
                        [50.,40.],
                        [50.,40.],
                        [50.,40.],
                        [50.,40.],
                        [50.,40.],
                        [50.,40.],
                        [50.,40.],
                        [50.,100. ],
                        [50.,100. ],
                        [50.,100. ],
                        [50.,100. ],
                        [50.,100. ],
                        [50.,100. ],
                        [50.,100. ],
                        [50.,100.]])
#whitened = whiten(features)
#book = np.array((whitened[0],whitened[2]))
#codebook, dist = kmeans(whitened,book)
#print(codebook)
#print(dist)
numGroups = 3


idx = []

res, idx = kmeans2(features, numGroups, iter=100, minit='points')
#res, idx = kmeans2(features, numGroups, iter=100)

print(res)
print(idx)

counts = Counter(idx)
print(counts)
loopCount = 0
while (1):
    repeat = False
    for index in range(numGroups):
        if counts[index] != 8:
            repeat = True

    print(counts)
    print('loop')
    loopCount += 1
    if repeat:
        res, idx = kmeans2(features, numGroups, iter=100, minit='points')
        counts = Counter(idx)

    else:
        break

print(loopCount)


print(res)
print(idx)
## Define criteria = ( type, max_iter = 10 , epsilon = 1.0 )
#criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
#
## Set flags (Just to avoid line break in the code)
#flags = cv2.KMEANS_RANDOM_CENTERS
#
## Apply KMeans
##compactness,labels,centers = cv2.kmeans(features,2,None,criteria,10,flags)
#
#ret, labels, centers = cv2.kmeans(features, 2, criteria, 10, 0)
#
#print(compactness)
#print(labels)
#print(centers)


