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


def nanmeanFilter(x):
	return nanmean(x)


path = '/mnt/moehlc/idaf/IDAF_Projects/140327_raman_bloodvessel_mri/data/segmented/angio_wt/'
pattern = 'flowSkel'

filterSize = 40


fnames = io.getFilelistFromDir(path,pattern)

fname = fnames[0]

absname = path + fname

#import
zsize = vigra.impex.numberImages(absname)
im =vigra.readImage(absname, index = 0, dtype='FLOAT')
#vol = np.zeros([im.height,im.width,zsize])
vol = np.memmap('vol_dat',dtype = 'float64', mode = 'w+', shape = (im.height,im.width,zsize))
#for i in range(zsize):
for i in range(100,103):
	print("importing slice " + str(i))
	im=np.squeeze(vigra.readImage(absname, index = i, dtype='FLOAT'))
	vol[:,:,i] = im
	vol.flush()
vol[vol == 0] = np.nan


volsmall =vol[:,:,100:101]

t = time.time()
res = ndimage.generic_filter(volsmall, nanmeanFilter,size = filterSize)
print('elapsed time [min]: ' + str((time.time()-t)/60))

resp = np.nanmean(res,axis=2)

plt.close()
plt.imshow(resp)
plt.show()

