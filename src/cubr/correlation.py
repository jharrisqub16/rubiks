# Contains array which correlates the camera/face and the coordinates to the cube position.

# TODO NB currently it is designed to iterate through the positions and check the coordinates:
# This is done to require a smaller array, rather using pixel coords.

# TODO For the first robot iteration, 8,9 and 20 require larger areas as they are viewed through the motor posts
# Perhaps this can use the "spare" member, which would also be used for the orientation in the second robot

# TODO at some point, this will probably be used for adjusting/displaying the "Regions of interest" in a preview menu

import numpy as np

correlation = np.zeros((3,54), dtype=np.ndarray)

# RUF camera
correlation[0, 38] = (83 , 93)
correlation[0, 41] = (113 , 110)
correlation[0, 44] = (143 , 130)
correlation[0, 43] = (145 , 175)
correlation[0, 42] = (148 , 205)
correlation[0, 27] = (178, 130)
correlation[0, 30] = (178, 175)
correlation[0, 28] = (213, 115)
correlation[0, 18] = (92 , 68 )
correlation[0, 21] = (125 , 80)
correlation[0, 24] = (150 , 98)
correlation[0, 19] = (128 , 50 )
correlation[0, 25] = (195, 80)
correlation[0, 20] = (163 ,  37)
correlation[0, 23] = (195, 50)
correlation[0, 26] = (230, 65)


# BRD camera
correlation[1, 45] = (88 , 83)
correlation[1, 46] = (118 , 100)
correlation[1, 47] = (148 , 120)
correlation[1, 50] = (150 , 165)
correlation[1, 53] = (146 , 200)
correlation[1, 36] = (183, 120)
correlation[1, 39] = (183, 165)
correlation[1, 37] = (218, 105)
correlation[1, 2 ] = (97 , 58 )
correlation[1, 1 ] = (130 , 70)
correlation[1, 0 ] = (155 , 88)
correlation[1, 5 ] = (133 , 40 )
correlation[1, 3 ] = (200, 70)
correlation[1, 8 ] = (168 ,  27)
correlation[1, 7 ] = (200, 40)
correlation[1, 6 ] = (235, 55)


# UBL camera
correlation[2, 29] =  (83 , 83)
correlation[2, 32] =  (113 , 100)
correlation[2, 35] =  (143 , 120)
correlation[2, 34] =  (145 , 165)
correlation[2, 33] =  (148 , 195)
correlation[2, 51] =  (178, 120)
correlation[2, 52] =  (178, 165)
correlation[2, 48] =  (213, 105)
correlation[2, 15] =  (92 , 58 )
correlation[2, 16] =  (125 , 70)
correlation[2, 17] =  (150 , 88)
correlation[2, 12] =  (128 , 40 )
correlation[2, 14] =  (195, 70)
correlation[2, 9 ] =  (163 ,  27)
correlation[2, 10] =  (195, 40)
correlation[2, 11] =  (230, 55)
