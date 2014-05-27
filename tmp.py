import sys
import numpy as np
sys.path.append("/mnt/moehlc/home/idaf_library")
#import mahotas

import libidaf.idafIO as io
import matplotlib.pyplot as plt
import re






path = '/home/moehlc/raman_bloodvessel_dat/filteredVoldDat1/angio_wt/'
path = '/home/moehlc/raman_bloodvessel_dat/filteredVoldDatGauss1/angio_wt/'

path2 = '/home/moehlc/raman_bloodvessel_dat/rawVoldat2/angio_wt/'

pattern = 'filtered_Size_20'
pattern2 = '_trafo'

shape = (320,320,272)

fnames = io.getFilelistFromDir(path,pattern) #list of tiff stacks to be filtered
fnames2 = io.getFilelistFromDir(path2,pattern2)

num = 8

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
#vol_gauss = np.array(np.memmap(path3 + fname,dtype = 'float64', mode = 'r', shape = shape))
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