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
import multiprocessing as mp
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
		#mp.Process(target = exportPickle, args = (vol,outpath,fnames[i])).start()
		exportPickle(vol,outpath,fnames[i])
	print('completed')	



#input dirs, locally on animate-x3

path_wt = '/home/moehlc/raman_bloodvessel_dat/filteredVoldDatGauss1/angio_wt/'
path_ad = '/home/moehlc/raman_bloodvessel_dat/filteredVoldDat1/angio_ad/'

savepath_wt= '/mnt/moehlc/idaf/IDAF_Projects/140327_raman_bloodvessel_mri/data/filteredPickles/angio_wt/'
savepath_ad= '/mnt/moehlc/idaf/IDAF_Projects/140327_raman_bloodvessel_mri/data/filteredPickles/angio_ad/'

pattern1 = 'filtered_Size_10'
pattern2 = 'filtered_Size_20'

#dimensions of volume
shape = (320,320,272)

expPickles(path_ad,savepath_ad,pattern1,shape) #save meanfiltered data
expPickles(path_wt,savepath_wt,pattern2,shape) #save meanfiltered data
expPickles(path_ad,savepath_ad,pattern2,shape) #save meanfiltered data
expPickles(path_wt,savepath_wt,pattern1,shape) #save meanfiltered data



