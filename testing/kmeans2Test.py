#from numpy import array
import numpy as np
from scipy.cluster.vq import vq, kmeans, whiten, kmeans2

import cv2

features  = np.array([[ 30.0,2.3],
                   [ 1.5,2.5],
                   [ 0.8,0.6],
                   [ 0.4,1.8],
                   [ 0.1,0.1],
                   [ 0.2,1.8],
                   [ 2.0,0.5],
                   [ 0.3,1.5],
                   [ 1.0,1.0]])
#whitened = whiten(features)
#book = np.array((whitened[0],whitened[2]))
#codebook, dist = kmeans(whitened,book)
#print(codebook)
#print(dist)

res, idx = kmeans2(features,2, 20)

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


