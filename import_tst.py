import sys
sys.path.append("/mnt/moehlc/home/idaf_library")
#import mahotas
import vigra
import libidaf.idafIO as io
import numpy as np
from scipy import ndimage
from scipy.stats import nanmean

def nanmeanFilter(x):
	return nanmean(x)


path = '/mnt/moehlc/idaf/IDAF_Projects/140327_raman_bloodvessel_mri/data/segmented/angio_wt/'
pattern = 'flowSkel'

filterSize = 30


fnames = io.getFilelistFromDir(path,pattern)

fname = fnames[0]

absname = path + fname

#import
zsize = vigra.impex.numberImages(absname)
im =vigra.readImage(absname, index = 0, dtype='FLOAT')
vol = np.zeros([im.height,im.width,zsize])
for i in range(zsize):
	im=np.squeeze(vigra.readImage(absname, index = i, dtype='FLOAT'))
	vol[:,:,i] = im
vol[vol == 0] = np.nan


res = ndimage.generic_filter(vol, nanmeanFilter,size = filterSize)

