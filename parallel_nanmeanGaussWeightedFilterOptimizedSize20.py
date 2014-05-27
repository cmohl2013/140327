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


def gaussWeight(dat,sigma,mu):
	return 1./np.sqrt(2*np.pi*np.square(sigma))*np.exp(-np.square(dat-mu)/(2*np.square(sigma)))

def streaming3Dfilter(data,outdata,sigma):
	fsize = int(np.round(sigma*3)) # filter size
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
				weight = gaussWeight(dist[ind],sigma,0)
				datsel = datxyz[ind]
				if datsel.size == 0:
					outdata[i,j,k] = np.nan
				else:
					outdata[i,j,k] = np.average(datsel,weights = weight)
		print('writing slice ' + str(i) + 'to '+ outdata.filename)	
		print('progress: ' + str(i/float(amax[0])*100) + ' percent done')
		outdata.flush() #write to disk



def importStack(path,fname,tmpStackDir):
	absname = path +fname
	zsize = vigra.impex.numberImages(absname)
	im =vigra.readImage(absname, index = 0, dtype='FLOAT')
	#vol = np.zeros([im.height,im.width,zsize])
	
	try:
		os.makedirs(tmpStackDir)
	except:
		print(tmpStackDir+' already exists')

	vol = np.memmap(tmpStackDir + fname[0:-4],dtype='float64',mode = 'w+', shape = (im.height,im.width,zsize))
	#raise('hallo')
	for i in range(zsize):
		print("importing slice " + str(i) + ' of file '+fname)
		im=np.squeeze(vigra.readImage(absname, index = i, dtype='FLOAT'))
		vol[:,:,i] = im
	vol.flush()
	return vol

def filterAndSave(fname,path,savepath,filterSize,volpath):
	vol = importStack(path,fname,volpath)
	
	try:
		os.makedirs(savepath)
	except:
		print(savepath+' already exists')
	res = np.memmap(savepath + 'filtered_Size_'+ str(filterSize) + fname,dtype = 'float64', mode = 'w+', shape = vol.shape)	
	streaming3Dfilter(vol, res,filterSize)
	

def filterAndSave_batch(pattern,path,savepath,filterSize,volpath):
	fnames = io.getFilelistFromDir(path,pattern) #list of tiff stacks to be filtered
	for i in range(len(fnames)):
	#for i in range(1):
		print('start filter process for '+fnames[i])
		mp.Process(target = filterAndSave, args = (fnames[i],path,savepath,filterSize,volpath)).start() #parallel processing

def filterAndSave_batch_serial(pattern,path,savepath,filterSize,volpath):
	fnames = io.getFilelistFromDir(path,pattern) #list of tiff stacks to be filtered
	for i in range(len(fnames)):
	#for i in range(1):
		print('start filter process for '+fnames[i])
		filterAndSave(fnames[i],path,savepath,filterSize,volpath) #parallel processing



if __name__ == '__main__':

	path = '/home/moehlc/raman_bloodvessel_dat/segmented/angio_wt/'
	savepath = '/home/moehlc/raman_bloodvessel_dat/filteredVoldDatGauss1/angio_wt/'
	volpath = '/home/moehlc/raman_bloodvessel_dat/rawVoldat2/angio_wt/'

	filterSize = 20


	filterAndSave_batch('flowSkel',path,savepath,filterSize,volpath)
	filterAndSave_batch('distanceSkel',path,savepath,filterSize,volpath)
	#filterAndSave_batch_serial('flowSkel',path,savepath,filterSize)
	#filterAndSave_batch('distanceSkel',path,savepath,filterSize)






