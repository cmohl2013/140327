import sys
sys.path.append("/mnt/moehlc/home/idaf_library")
#import mahotas
import vigra
import libidaf.idafIO as io
import numpy as np
from scipy import ndimage
from scipy.stats import nanmean
#import matplotlib.pyplot as plt
import time
import pickle
import os
import multiprocessing as mp


radius = 4.4

t = np.zeros([10,10,10])
t[0,4,0] = 10
t[3,3,0] = 2
t[3,4,0] = 2
t[6,6,0] = 4


x,y,z = t.nonzero()


i = 0
j = 0
k = 0

dist = np.sqrt(np.square(i-x) + np.square(j-y) + np.square(k-z)) 


ind = dist<= radius 
xsel = x[ind]
ysel = y[ind]
zsel = z[ind]

data = t[xsel,ysel,zsel]






