import pickle
import matplotlib.pyplot as plt 
import numpy as np
import vigra

def importStack(path,fname):
	absname = path +fname
	zsize = vigra.impex.numberImages(absname)
	im =vigra.readImage(absname, index = 0, dtype='FLOAT')
	#vol = np.zeros([im.height,im.width,zsize])
	
	

	vol = np.zeros((im.height,im.width,zsize))
	#vol = np.memmap(tmpStackDir + fname[0:-4],dtype='float64',mode = 'w+', shape = (im.height,im.width,zsize))
	#raise('hallo')
	for i in range(zsize):
		print("importing slice " + str(i) + ' of file '+fname)
		im=np.squeeze(vigra.readImage(absname, index = i, dtype='FLOAT'))
		vol[:,:,i] = im
	
	return vol






path = '/mnt/moehlc/idaf/IDAF_Projects/140327_raman_bloodvessel_mri/data/averagedPickles/'
volpath = '/mnt/moehlc/idaf/IDAF_Projects/140327_raman_bloodvessel_mri/data/registered_data/angio_wt/'

fname1 = 'volAverage_distance_meanfilter_angioWT.pickle'
fname2 = 'volAverage_distance_gaussfilter_angioWT.pickle'
fname3 = 'volAverage_flow_meanfilter_angioWT.pickle'
fname4 = 'volAverage_flow_gaussfilter_angioWT.pickle'
fname_raw = '09_01_13_A11143_Gp3_1_09_01_13_A11143_Gp3_1_xtip1__E28_Process 3_trafo.tif'


vol_raw = importStack(volpath,fname_raw)
vol_mean = pickle.load(open(path + fname1,'rb'))
vol_gauss = pickle.load(open(path + fname2,'rb'))

volFlow_mean = pickle.load(open(path + fname3,'rb'))
volFlow_gauss = pickle.load(open(path + fname4,'rb'))

im_raw = np.rot90(np.nanmean(vol_raw,axis = 2),-1)
im = np.rot90(np.nanmean(vol_mean,axis = 2),-1)
im2 = np.rot90(np.nanmean(vol_gauss,axis = 2),-1)

im3 = np.rot90(np.nanmean(volFlow_mean,axis = 2),-1)
im4 = np.rot90(np.nanmean(volFlow_gauss,axis = 2),-1)

plt.close()

fig = plt.figure()

fig.add_subplot(2,3,1)
ax1 = plt.imshow(im)
#fig.colorbar(ax1)

fig.add_subplot(2,3,2)
ax2 = plt.imshow(im2)
#fig.colorbar(ax2)

fig.add_subplot(2,3,3)
plt.imshow(im_raw, cmap = 'gray')

fig.add_subplot(2,3,4)
ax4 = plt.imshow(im3)

fig.add_subplot(2,3,5)
ax5 = plt.imshow(im4)




plt.show()