import pickle
import matplotlib.pyplot as plt 
import numpy as np



def importAndFlatten(absfilename):
	vol = pickle.load(open(absfilename,'rb'))
	return np.rot90(np.nanmean(vol,axis = 2),-1)

path = '/mnt/moehlc/idaf/IDAF_Projects/140327_raman_bloodvessel_mri/data/averagedPickles/'
fname1 = 'volNN_distance_meanfilter_angioWT.pickle'
fname2 = 'volNN_distance_gaussfilter_angioWT.pickle'


im1 = importAndFlatten(path + fname1)
im2 = importAndFlatten(path + fname2)

plt.close()

fig, (ax1,ax2) = plt.subplots(ncols = 2)


ims1 = ax1.imshow(im1)
#fig.colorbar(ims1)
ax1.set_title('sample number: angioWT meanfilter')

ims2 = ax2.imshow(im2)
#fig.colorbar(ims2)
ax2.set_title('sample number: angioWT gaussfilter')




fig2 = plt.figure()
fig2.colorbar(ims1)



plt.show()

print np.unique((im1-im2).flatten())