#parallel calculation of statistics

import numpy as np
import sys
sys.path.append("/home/moehlc/idaf_library")
import libidaf.idafIO as io
import multiprocessing as mp
import os

def initMemMap(savepath,name,shape):
	try:
		os.makedirs(savepath)
	except:
		print(savepath+' already exists')

	savename = name + '.mmap'
	print('initialize new memmap ' + savename)
	
	mmap = np.memmap(savepath + savename,dtype = 'float64', mode = 'w+',\
 	shape = shape)
	return mmap


def loadMemMapSlice(path,name,shape,sliceNr):
	return np.array(np.memmap(path + name,dtype = 'float64', mode = 'r',\
 	shape = shape)[:,:,sliceNr])



def loadMemMapSlices(path,names,shape,sliceNr):
	print('importing slices nr. ' + str(sliceNr))
	nFiles = len(names) #nr of filenames
	vol = np.zeros((shape[0],shape[1],nFiles))
	
	for i in range(nFiles):
		vol[:,:,i] = loadMemMapSlice(path,names[i],shape,sliceNr)
	return vol	

def calcNnSliceAndExport(inslices,sliceNr,outmap):
	#return number of values over z that are not nan
	outmap[:,:,sliceNr] = (~np.isnan(inslices)).sum(axis = 2)
	outmap.flush()

def calcMeanSliceAndExport(inslices,sliceNr,outmap):
	#return number of values over z that are not nan
	outmap[:,:,sliceNr] = np.nanmean(inslices,axis = 2)
	outmap.flush()	

def calcStdSliceAndExport(inslices,sliceNr,outmap):
	#return number of values over z that are not nan
	outmap[:,:,sliceNr] = np.nanstd(inslices,axis = 2)
	outmap.flush()		

def calcPercentileSliceAndExport(inslices,sliceNr,outmap,percentile):
	for i in range(inslices.shape[0]):
		for j in range(inslices.shape[1]):
			x = inslices[i,j,:].flatten()
			x = x[~np.isnan(x)] # remove nan
			if len(x) > 1:
				outmap[i,j,sliceNr] = np.percentile(x,percentile)
			else:
				outmap[i,j,sliceNr] = np.nan
	outmap.flush()


def calcStatisticsForSlice(sliceNr,path,fnames,shape,m):
	#load slices
	sl = loadMemMapSlices(path,fnames,shape,sliceNr)
	print('calculate mean nn and std of slice Nr. ' + str(sliceNr))
	calcNnSliceAndExport(sl,sliceNr,m['vol_nn'])
	calcMeanSliceAndExport(sl,sliceNr,m['vol_mean'])
	calcStdSliceAndExport(sl,sliceNr,m['vol_std'])
	print('calculate median of slice Nr. ' + str(sliceNr))
	calcPercentileSliceAndExport(sl,sliceNr,m['vol_median'],50)
	print('calculate percentiles of slice Nr. ' + str(sliceNr))
	calcPercentileSliceAndExport(sl,sliceNr,m['vol_percentile05'],5)
	calcPercentileSliceAndExport(sl,sliceNr,m['vol_percentile25'],25)
	calcPercentileSliceAndExport(sl,sliceNr,m['vol_percentile75'],75)
	calcPercentileSliceAndExport(sl,sliceNr,m['vol_percentile95'],95)

def calcStatisticsForPopulation(path,pattern,savepath,shape,namePrefix):
	fnames = io.getFilelistFromDir(path,pattern) #list of pickles to process

	memmaps = {}
	#initialization of memmaps
	memmaps['vol_nn'] = initMemMap(savepath,namePrefix + 'nn',shape)
	memmaps['vol_mean'] = initMemMap(savepath,namePrefix + 'mean',shape)
	memmaps['vol_std'] = initMemMap(savepath,namePrefix + 'std',shape)
	memmaps['vol_median'] = initMemMap(savepath,namePrefix + 'median',shape)
	memmaps['vol_percentile05'] = initMemMap(savepath,namePrefix + 'percentile05',shape)
	memmaps['vol_percentile25'] = initMemMap(savepath,namePrefix + 'percentile25',shape)
	memmaps['vol_percentile75'] = initMemMap(savepath,namePrefix + 'percentile75',shape)
	memmaps['vol_percentile95'] = initMemMap(savepath,namePrefix + 'percentile95',shape)

	#process slice by slice
	for sliceNr in range(shape[2]):
		#calcStatisticsForSlice(sliceNr,path,fnames,shape,memmaps)
		mp.Process(target = calcStatisticsForSlice, args =(sliceNr,path,fnames,shape,memmaps)).start()


if __name__ == '__main__':

	path_ad = '/facilities/idaf/IDAF_Projects/140327_raman_bloodvessel_mri/data/filteredMemMaps/angio_ad/'
	path_wt = '/facilities/idaf/IDAF_Projects/140327_raman_bloodvessel_mri/data/filteredMemMaps/angio_wt/'

	savepath_ad = '/facilities/idaf/IDAF_Projects/140327_raman_bloodvessel_mri/data/statisticsMemMaps/angio_ad/'
	savepath_wt = '/facilities/idaf/IDAF_Projects/140327_raman_bloodvessel_mri/data/statisticsMemMaps/angio_wt/'

	patternDist = 'filtered_Size_20distanceSkel' # gaussfiltered distance images
	patternFlow = 'filtered_Size_20flowSkel'

	shape = (320,320,272) 
	
	#calcStatisticsForPopulation(path_ad,patternDist,savepath_ad,shape,'dist_')
	calcStatisticsForPopulation(path_wt,patternDist,savepath_wt,shape,'dist_')

	#calcStatisticsForPopulation(path_ad,patternFlow,savepath_ad,shape,'flow_')
	#calcStatisticsForPopulation(path_wt,patternFlow,savepath_wt,shape,'flow_')


	


