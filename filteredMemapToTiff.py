import sys
import numpy as np
sys.path.append("/mnt/moehlc/home/idaf_library")
#import mahotas

import libidaf.idafIO as io
import matplotlib.pyplot as plt
import re
import vigra
import os
import pickle
#SAVE MEMAPS AS 32bit tiff stacks

#input dirs, locally on animate-x3
path_filtered40 =      '/home/moehlc/raman_bloodvessel_dat/filteredVoldDat1/angio_wt/'
path_gaussfiltered20 = '/home/moehlc/raman_bloodvessel_dat/filteredVoldDatGauss1/angio_wt/'

savepath = '/mnt/moehlc/idaf/IDAF_Projects/140327_raman_bloodvessel_mri/data/filteredPickles/'



def exportPickle(vol,savepath, fname):
	
	if fname.find('.') != -1: #if file extension zB .tif present
		fnameTrunc = fname[0:fname.find('.')]
	else:
		fnameTrunc = fname		


	try:
		os.makedirs(savepath)
	except:
		print(path+' already exists')

	pickle.dump(vol,open(savepath + fnameTrunc +'.pickle','w'))	

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

exportPickle(vol_f,savepath,fname)

#vol_f2 = np.array(np.memmap(path_gaussfiltered20 + fname2,dtype = 'float64', mode = 'r', shape = shape))

#vigra.impex.writeImage(vol_f,savepath+fname,dtype = 'FLOAT',mode = 'w')



