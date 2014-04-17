import sys
sys.path.append("/mnt/moehlc/home/idaf_library")
#import mahotas
import vigra
import libidaf.idafIO as io
import numpy as np
from scipy import ndimage
from scipy.stats import nanmean
import matplotlib.pyplot as plt
import time
import pickle
import os
import multiprocessing as mp

def nanmeanFilter(x):
	return nanmean(x)

def importStack(absname):
	zsize = vigra.impex.numberImages(absname)
	im =vigra.readImage(absname, index = 0, dtype='FLOAT')
	vol = np.zeros([im.height,im.width,zsize])
	for i in range(zsize):
	#print("importing slice " + str(i))
		im=np.squeeze(vigra.readImage(absname, index = i, dtype='FLOAT'))
		vol[:,:,i] = im
	vol[vol == 0] = np.nan
	return vol

def filterAndSave(fname,path,savepath,filterSize):
	vol = importStack(path + fname)
	#volsmall =vol[100:150,100:150,100:101]
	volsmall = vol
	res = ndimage.generic_filter(volsmall, nanmeanFilter,size = filterSize)
	try:
		os.makdirs(savepath)
	except:
		print(savepath+' already exists')

	with open(savepath + fname[:-4] + '.pickle','w') as f:
		pickle.dump([res, filterSize],f)

def filterAndSave_batch(pattern,path,savepath,filterSize):
	fnames = io.getFilelistFromDir(path,pattern) #list of tiff stacks to be filtered
	for i in range(len(fnames)):
		mp.Process(target = filterAndSave, args = (fnames1[i],path,savepath,filterSize)).start() #parallel processing





path = '/mnt/moehlc/idaf/IDAF_Projects/140327_raman_bloodvessel_mri/data/segmented/angio_wt/'
savepath = '/mnt/moehlc/idaf/IDAF_Projects/140327_raman_bloodvessel_mri/data/pickle/angio_wt/'

filterSize = 40


filterAndSave_batch('flowSkel',path,savepath,filterSize)
filterAndSave_batch('distanceSkel',path,savepath,filterSize)







