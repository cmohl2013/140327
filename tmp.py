import sys
import numpy as np
sys.path.append("/mnt/moehlc/home/idaf_library")
#import mahotas

import libidaf.idafIO as io
import matplotlib.pyplot as plt
import re

path = '/mnt/moehlc/idaf/IDAF_Projects/140327_raman_bloodvessel_mri/data/filteredVoldDat1/angio_wt/'
path2 = 'tmpVolDat/'
pattern = 'filtered_Size_40'
pattern2 = '_trafo'

shape = (320,320,272)

fnames = io.getFilelistFromDir(path,pattern) #list of tiff stacks to be filtered
fnames2 = io.getFilelistFromDir(path2,pattern2)

num = 1

fname = fnames[num]

def matchlist(string,list):
	for f in list:
		if string.find(f) != -1:
			return f
	return -1	

fname2 = matchlist(fname,fnames2)



print(fname)
print(fname2)

vol_f = np.array(np.memmap(path + fname,dtype = 'float64', mode = 'r', shape = shape))
vol = np.array(np.memmap(path2 + fname2,dtype = 'float64', mode = 'r', shape = shape))

im_f = np.nanmean(vol_f,axis = 2)
im = np.nanmean(vol,axis = 2)


plt.close()


fig = plt.figure()
fig.add_subplot(1,2,1)
plt.imshow(im)
fig.add_subplot(1,2,2)
plt.imshow(im_f)
plt.show()