import os
import sys


print(os.path.dirname(os.path.abspath(__file__)))

cwd = os.path.dirname(os.path.abspath(__file__))

print(cwd)

filename = os.path.join(cwd, 'images', 'rubiksCube.jpg')


print(filename)
