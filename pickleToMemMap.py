import numpy as np
import sys
sys.path.append("/home/moehlc/idaf_library")
import libidaf.idafIO as io
import os
import multiprocessing as mp

def pickleToMemMap(path,fname,savepath):


	print('importing ' + fname + '...')
	vol = np.load(path + fname)
	print('importing ' + fname + ' DONE')
	try:
		os.makedirs(savepath)
	except:
		print(savepath+' already exists')

	savename = fname[:fname.find('.')] + '.mmap'	
	mmap = np.memmap(savepath + savename,dtype = 'float64', mode = 'w+',\
 	shape = vol.shape)
 	mmap[:] = vol[:]
 	mmap.flush()	


def picklesToMemMaps(path,pattern,savepath):
	fnames = io.getFilelistFromDir(path,pattern) #list of pickles to process

	for fname in fnames:
		#pickleToMemMap(path,fname,savepath)
		mp.Process(target = pickleToMemMap, args = (path,fname,savepath)).start() #parallel processing




if __name__ == '__main__':

	path_ad = '/facilities/idaf/IDAF_Projects/140327_raman_bloodvessel_mri/data/filteredPickles/angio_ad/'
	path_wt = '/facilities/idaf/IDAF_Projects/140327_raman_bloodvessel_mri/data/filteredPickles/angio_wt/'

	savepath_ad = '/facilities/idaf/IDAF_Projects/140327_raman_bloodvessel_mri/data/filteredMemMaps/angio_ad/'
	savepath_wt = '/facilities/idaf/IDAF_Projects/140327_raman_bloodvessel_mri/data/filteredMemMaps/angio_wt/'


	pattern = 'filtered_Size_20' # gaussfiltered distance images

	picklesToMemMaps(path_wt,pattern,savepath_wt)
	picklesToMemMaps(path_ad,pattern,savepath_ad)






