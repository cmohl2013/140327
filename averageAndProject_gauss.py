import sys
sys.path.append("/mnt/moehlc/home/idaf_library")
import libidaf.idafIO as io
import numpy as np
from scipy.stats import nanmean
import pickle
import os

import multiprocessing as mp


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


def loadAndAverage(path,pattern,shape):
	vol = np.zeros(shape) # 3d volume for summing up
	nn = np.zeros(shape) # 3 D matrix for number of samples
	fnames = io.getFilelistFromDir(path,pattern) #list of tiff stacks to be filtered
	n = len(fnames)

	#import each volume, sum pixels and keep track of sample number
	for i in range(n):
		volTmp = pickle.load(open(path + fnames[i],'rb'))
		nn [~np.isnan(volTmp)] += 1 # increase number of samples by 1 where volTmp is not nan
		volTmp[np.isnan(volTmp)] = 0 # set nans to zero
		vol += volTmp
		print(str(100*i/float(n)))
	vol_average = vol/nn
	
	return vol_average, nn	


def loadAverageSave(path,pattern,shape,savepath,savename):
	vol_average, nn = loadAndAverage(path, pattern, shape)
	exportPickle(vol_average,savepath,'volAverage_' + savename)
	exportPickle(nn,savepath,'volNN_' + savename)

def loadAverageSave_parallel(path,pattern,shape,savepath,savename):
	print('start process for '+savename)
	mp.Process(target = loadAverageSave, args = (path,pattern,shape,savepath,savename)).start() #parallel processing	


path_ad = '/mnt/moehlc/idaf/IDAF_Projects/140327_raman_bloodvessel_mri/data/filteredPickles/angio_ad/'
path_wt = '/mnt/moehlc/idaf/IDAF_Projects/140327_raman_bloodvessel_mri/data/filteredPickles/angio_wt/'




pattern1_20 = 'filtered_Size_20distanceSkel' # gaussfiltered distance images
pattern2_20 = 'filtered_Size_20flowSkel'
pattern1_10 = 'filtered_Size_10distanceSkel' # gaussfiltered distance images
pattern2_10 = 'filtered_Size_10dflowSkel'

savepath = '/mnt/moehlc/idaf/IDAF_Projects/140327_raman_bloodvessel_mri/data/averagedPickles/'

savename1_20_wt = 'distance_Size_20_angioWT'
savename2_20_wt = 'flow_Size_20_angioWT'
savename1_10_wt = 'distance_Size_10_angioWT'
savename2_10_wt = 'flow_Size_10_angioWT'

savename1_20_ad = 'distance_Size_20_angioAD'
savename2_20_ad = 'flow_Size_20_angioAD'
savename1_10_ad = 'distance_Size_10_angioAD'
savename2_10_ad = 'flow_Size_10_angioAD'



shape = (320,320,272) 

loadAverageSave_parallel(path_ad,pattern1_20,shape,savepath,savename1_20_ad)
loadAverageSave_parallel(path_ad,pattern2_20,shape,savepath,savename2_20_ad)
loadAverageSave_parallel(path_ad,pattern1_10,shape,savepath,savename1_10_ad)
loadAverageSave_parallel(path_ad,pattern2_10,shape,savepath,savename2_10_ad)


loadAverageSave_parallel(path_wt,pattern1_20,shape,savepath,savename1_20_wt)
loadAverageSave_parallel(path_wt,pattern2_20,shape,savepath,savename2_20_wt)
loadAverageSave_parallel(path_wt,pattern1_10,shape,savepath,savename1_10_wt)
loadAverageSave_parallel(path_wt,pattern2_10,shape,savepath,savename2_10_wt)


