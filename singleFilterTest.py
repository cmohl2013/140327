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

@profile
def streaming3Dfilter(data,outdata,fsize):
	amax=np.array(data.shape)-1 #max index
	amin=amax-amax #min index

	dataR = np.array(data.copy())
	for i in range(amax[0]+1): #x dim
		for j in range(amax[1]+1): # y dim
			for k in range(amax[2]+1): # z dim
				upper = np.array([i,j,k])+fsize
				lower = np.array([i,j,k])-fsize 
				#calculate upper and lower indices
				upper = np.min(np.array([upper,amax]),axis =0)
				lower = np.max(np.array([lower,amin]),axis =0)

				x = np.array(dataR[lower[0]:upper[0]+1,lower[1]:upper[1]+1,lower[2]:upper[2]+1].flatten())
				x = x[~np.isnan(x)]
				#raise('hallo')
				if x.size == 0:
					outdata[i,j,k] = np.nan
				else:
					outdata[i,j,k] = nanmean(x)
		print('writing slice ' + str(i) + 'to '+ outdata.filename)	
		outdata.flush() #write to disk


def importStack(path,fname):
	absname = path +fname
	zsize = vigra.impex.numberImages(absname)
	im =vigra.readImage(absname, index = 0, dtype='FLOAT')
	#vol = np.zeros([im.height,im.width,zsize])
	vol = np.memmap('tmp/' + fname[0:-4],dtype='float64',mode = 'w+', shape = (im.height,im.width,zsize))
	#raise('hallo')
	for i in range(zsize):
		print("importing slice " + str(i) + ' of file '+fname)
		im=np.squeeze(vigra.readImage(absname, index = i, dtype='FLOAT'))
		vol[:,:,i] = im
	vol[vol == 0] = np.nan
	vol.flush()
	return vol

def filterAndSave(fname,path,savepath,filterSize):
	vol = importStack(path,fname)
	#volsmall =vol[100:150,100:150,100:101]
	#volsmall = vol
	
	
	try:
		os.makdirs(savepath)
	except:
		print(savepath+' already exists')
	res = np.memmap(savepath + 'filtered_Size_'+ str(filterSize) + fname,dtype = 'float64', mode = 'w+', shape = vol.shape)	
	#res = ndimage.generic_filter(vol, nanmeanFilter,size = filterSize)
	streaming3Dfilter(vol, res,filterSize)	


path = '/mnt/moehlc/idaf/IDAF_Projects/140327_raman_bloodvessel_mri/data/segmented/angio_wt/'
savepath = 'tmp_out/'

filterSize = 70	


pattern = 'flowSkel'
fnames = io.getFilelistFromDir(path,pattern) #list of tiff stacks to be filtered
fname = fnames[0]

#vol = importStack(path,fname)

filterAndSave(fname,path,savepath,filterSize)



