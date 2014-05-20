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

def streaming3Dfilter(data,outdata,fsize):
	amax=np.array(data.shape)-1 #max index
	amin=amax-amax #min index

	xyz = np.array(data.nonzero())#coordinates
	x = xyz[0,:]
	y = xyz[1,:]
	z = xyz[2,:]
	datxyz = np.array(data[x,y,z])

	for i in range(amax[0]+1): #x dim
		for j in range(amax[1]+1): # y dim
			for k in range(amax[2]+1): # z dim
				
				dist = np.sqrt(np.square(i-x) + np.square(j-y) + np.square(k-z)) 
				ind = dist<= fsize 
				datsel = datxyz[ind]
				if datsel.size == 0:
					outdata[i,j,k] = np.nan
				else:
					outdata[i,j,k] = np.mean(x)
		print('writing slice ' + str(i) + 'to '+ outdata.filename)	
		outdata.flush() #write to disk



def importStack(path,fname):
	absname = path +fname
	zsize = vigra.impex.numberImages(absname)
	im =vigra.readImage(absname, index = 0, dtype='FLOAT')
	#vol = np.zeros([im.height,im.width,zsize])
	vol = np.memmap('tmpVolDat/' + fname[0:-4],dtype='float64',mode = 'w+', shape = (im.height,im.width,zsize))
	#raise('hallo')
	for i in range(zsize):
		print("importing slice " + str(i) + ' of file '+fname)
		im=np.squeeze(vigra.readImage(absname, index = i, dtype='FLOAT'))
		vol[:,:,i] = im
	vol.flush()
	return vol

def filterAndSave(fname,path,savepath,filterSize):
	vol = importStack(path,fname)
	
	try:
		os.makdirs(savepath)
	except:
		print(savepath+' already exists')
	res = np.memmap(savepath + 'filtered_Size_'+ str(filterSize) + fname,dtype = 'float64', mode = 'w+', shape = vol.shape)	
	streaming3Dfilter(vol, res,filterSize)
	

def filterAndSave_batch(pattern,path,savepath,filterSize):
	fnames = io.getFilelistFromDir(path,pattern) #list of tiff stacks to be filtered
	for i in range(len(fnames)):
	#for i in range(1):
		print('start filter process for '+fnames[i])
		mp.Process(target = filterAndSave, args = (fnames[i],path,savepath,filterSize)).start() #parallel processing

def filterAndSave_batch_serial(pattern,path,savepath,filterSize):
	fnames = io.getFilelistFromDir(path,pattern) #list of tiff stacks to be filtered
	for i in range(len(fnames)):
	#for i in range(1):
		print('start filter process for '+fnames[i])
		filterAndSave(fnames[i],path,savepath,filterSize) #parallel processing



if __name__ == '__main__':

	path = '/mnt/moehlc/idaf/IDAF_Projects/140327_raman_bloodvessel_mri/data/segmented/angio_wt/'
	savepath = '/mnt/moehlc/idaf/IDAF_Projects/140327_raman_bloodvessel_mri/data/filteredVoldDat1/angio_wt/'

	filterSize = 40


	filterAndSave_batch('flowSkel',path,savepath,filterSize)
	filterAndSave_batch('distanceSkel',path,savepath,filterSize)
	#filterAndSave_batch_serial('flowSkel',path,savepath,filterSize)
	#filterAndSave_batch('distanceSkel',path,savepath,filterSize)







