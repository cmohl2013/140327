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
#SAVE MEMAPS AS pickles




def exportPickle(vol,savepath, fname):
	
	if fname.find('.') != -1: #if file extension zB .tif present
		fnameTrunc = fname[0:fname.find('.')]
	else:
		fnameTrunc = fname		


	try:
		os.makedirs(savepath)
	except:
		print(savepath+' already exists')

	pickle.dump(vol,open(savepath + fnameTrunc +'.pickle','w'))


def expPickles(inpath,outpath,pattern,volshape):
	fnames = io.getFilelistFromDir(inpath,pattern) #list of tiff stacks to be filtered

	for i in range(len(fnames)):
		vol = np.array(np.memmap(inpath + fnames[i],dtype = 'float64', mode = 'r', shape = volshape))
		print('saving file ' + str(i) + ' of ' + str(len(fnames)))
		exportPickle(vol,outpath,fnames[i])
	print('completed')	



#input dirs, locally on animate-x3
path_filtered40 =      '/home/moehlc/raman_bloodvessel_dat/filteredVoldDat1/angio_wt/'
path_gaussfiltered20 = '/home/moehlc/raman_bloodvessel_dat/filteredVoldDatGauss1/angio_wt/'

savepath = '/mnt/moehlc/idaf/IDAF_Projects/140327_raman_bloodvessel_mri/data/filteredPickles/angio_wt/'

pattern = 'filtered_Size_40'
pattern2 = 'filtered_Size_20'

#dimensions of volume
shape = (320,320,272)

expPickles(path_filtered40,savepath,pattern,shape) #save meanfiltered data
expPickles(path_gaussfiltered20,savepath,pattern2,shape) #save meanfiltered data




