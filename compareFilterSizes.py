import pickle
import numpy
import matplotlib.pyplot as plt 

def importAndFlatten(absfilename):
	vol = pickle.load(open(absfilename,'rb'))
	return np.rot90(np.nanmean(vol,axis = 2),-1)

path = '/mnt/moehlc/idaf/IDAF_Projects/140327_raman_bloodvessel_mri/data/averagedPickles/'




vol_dist_10_ad = importAndFlatten(path + 'volAverage_distance_Size_10_angioAD.pickle')
vol_dist_20_ad = importAndFlatten(path + 'volAverage_distance_Size_20_angioAD.pickle')

vol_dist_10_wt = importAndFlatten(path + 'volAverage_distance_Size_10_angioWT.pickle')
vol_dist_20_wt = importAndFlatten(path + 'volAverage_distance_Size_20_angioWT.pickle')

plt.close()
fig = plt.figure()

ax1 = fig.add_subplot(2,2,1)
plt.imshow(vol_dist_10_ad)
ax1 = fig.add_subplot(2,2,2)
plt.imshow(vol_dist_20_ad)
