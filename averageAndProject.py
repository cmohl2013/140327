import sys
sys.path.append("/mnt/moehlc/home/idaf_library")
import libidaf.idafIO as io
import numpy as np
from scipy.stats import nanmean
import pickle
import os




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



path = '/mnt/moehlc/idaf/IDAF_Projects/140327_raman_bloodvessel_mri/data/filteredPickles/angio_wt/'
pattern1mean = 'filtered_Size_40distanceSkel' # meanfiltered distance images
pattern1gauss = 'filtered_Size_20distanceSkel' # gaussfiltered distance images
pattern2mean = 'filtered_Size_40flowSkel' # meanfiltered flow images
pattern2gauss = 'filtered_Size_20flowSkel' # gaussfiltered flow images

savepath = '/mnt/moehlc/idaf/IDAF_Projects/140327_raman_bloodvessel_mri/data/averagedPickles/'
savename1mean = 'distance_meanfilter_angioWT'
savename1gauss = 'distance_gaussfilter_angioWT'
savename2mean = 'flow_meanfilter_angioWT'
savename2gauss = 'flow_gaussfilter_angioWT'

shape = (320,320,272) 

# mean filter distance
loadAverageSave(path,pattern1mean,shape,savepath,savename1mean)
# gauss filter distance
loadAverageSave(path,pattern1gauss,shape,savepath,savename1gauss)
# mean filter flow
loadAverageSave(path,pattern2mean,shape,savepath,savename2mean)
# gauss filter flow
loadAverageSave(path,pattern2gauss,shape,savepath,savename2gauss)

