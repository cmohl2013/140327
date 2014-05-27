import sys
import numpy as np
sys.path.append("/mnt/moehlc/home/idaf_library")
#import mahotas

import libidaf.idafIO as io
import matplotlib.pyplot as plt
import re



#SAVE MEMAPS AS 32bit tiff stacks

#input dirs, locally on animate-x3
path_filtered40 =      '/home/moehlc/raman_bloodvessel_dat/filteredVoldDat1/angio_wt/'
path_gaussfiltered20 = '/home/moehlc/raman_bloodvessel_dat/filteredVoldDatGauss1/angio_wt/'

#filename patterns
pattern = 'filtered_Size_40'
pattern2 = 'filtered_Size_20'

#dimensions of volume
shape = (320,320,272)

fnames = io.getFilelistFromDir(path_filtered40,pattern) #list of tiff stacks to be filtered
fnames2 = io.getFilelistFromDir(path_gaussfiltered20,pattern2)

num = 1

fname = fnames[num]
fname2 =fnames2[num]

print(fname)
print(fname2)

vol_f = np.array(np.memmap(path_filtered40 + fname,dtype = 'float64', mode = 'r', shape = shape))
#vol_gauss = np.array(np.memmap(path3 + fname,dtype = 'float64', mode = 'r', shape = shape))
vol_f2 = np.array(np.memmap(path_gaussfiltered20 + fname2,dtype = 'float64', mode = 'r', shape = shape))

im_f = np.nanmean(vol_f,axis = 2)
im_f2 = np.nanmean(vol_f2,axis = 2)


plt.close()


fig = plt.figure()
fig.add_subplot(1,2,1)
plt.imshow(im_f)
fig.add_subplot(1,2,2)
plt.imshow(im_f2)
plt.show()