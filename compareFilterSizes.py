import pickle
import numpy as np
import matplotlib.pyplot as plt 

def importAndFlatten(path,absfilename):
	print('loading ' + absfilename +'...')
	volfilename = 'volAverage_' + absfilename
	nfilename = 'volNN_' + absfilename
	vol = pickle.load(open(path + volfilename,'rb'))
	nn = pickle.load(open(path + nfilename,'rb'))

	maxSamples = nn.flatten().max()
	vol[nn<maxSamples] = np.nan
	print('loading ' + absfilename +' done')
	return np.rot90(np.nanmean(vol,axis = 2),-1)



def plotGrid(vol_dist_10_ad,vol_dist_20_ad,vol_dist_10_wt,vol_dist_20_wt,low,high):
	fig = plt.figure()

	ax1 = fig.add_subplot(2,2,1)
	plt.imshow(vol_dist_10_ad)
	plt.clim(low,high)
	ax2 = fig.add_subplot(2,2,2)
	ims1 = plt.imshow(vol_dist_20_ad)
	plt.clim(low,high)
	fig.colorbar(ims1)

	ax3 = fig.add_subplot(2,2,3)
	plt.imshow(vol_dist_10_wt)
	plt.clim(low,high)
	ax4 = fig.add_subplot(2,2,4)
	ims2 = plt.imshow(vol_dist_20_wt)
	plt.clim(low,high)
	fig.colorbar(ims2)

	return fig


path = '/mnt/moehlc/idaf/IDAF_Projects/140327_raman_bloodvessel_mri/data/averagedPickles/'

vol_dist_10_ad = importAndFlatten(path,'distance_Size_10_angioAD.pickle')
vol_dist_20_ad = importAndFlatten(path,'distance_Size_20_angioAD.pickle')
vol_dist_10_wt = importAndFlatten(path,'distance_Size_10_angioWT.pickle')
vol_dist_20_wt = importAndFlatten(path,'distance_Size_20_angioWT.pickle')


vol_flow_10_ad = importAndFlatten(path,'flow_Size_10_angioAD.pickle')
vol_flow_20_ad = importAndFlatten(path,'flow_Size_20_angioAD.pickle')
vol_flow_10_wt = importAndFlatten(path,'flow_Size_10_angioWT.pickle')
vol_flow_20_wt = importAndFlatten(path,'flow_Size_20_angioWT.pickle')





plt.close()
fig1 = plotGrid(vol_dist_10_ad,vol_dist_20_ad,vol_dist_10_wt,vol_dist_20_wt,1,1.9)
fig2 = plotGrid(vol_flow_10_ad,vol_flow_20_ad,vol_flow_10_wt,vol_flow_20_wt,39,100)

plt.show()
