import pickle
import matplotlib.pyplot as plt 
import numpy as np


path = '/mnt/moehlc/idaf/IDAF_Projects/140327_raman_bloodvessel_mri/data/averagedPickles/'

fname1 = 'volAverage_distance_meanfilter_angioWT.pickle'
fname2 = 'volAverage_distance_gaussfilter_angioWT.pickle'

vol_mean = pickle.load(open(path + fname1,'rb'))
vol_gauss = pickle.load(open(path + fname2,'rb'))
im = np.rot90(np.nanmean(vol_mean,axis = 2),1)
im2 = np.rot90(np.nanmean(vol_gauss,axis = 2),1)
plt.close()
fig = plt.figure()
fig.add_subplot(2,1,1)
plt.imshow(im)

fig.add_subplot(2,1,2)
plt.imshow(im2)

plt.show()