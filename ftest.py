
import numpy as np 
from scipy.stats import nanmean
import matplotlib.pyplot as plt







def streaming3Dfilter(data,outdata,fsize):
	amax=np.array(data.shape)-1 #max index
	amin=amax-amax #min index

	for i in range(amax[0]+1): #x dim
		for j in range(amax[1]+1): # y dim
			for k in range(amax[2]+1): # z dim
				upper = np.array([i,j,k])+fsize
				lower = np.array([i,j,k])-fsize 
				#calculate upper and lower indices
				upper = np.min(np.array([upper,amax]),axis =0)
				lower = np.max(np.array([lower,amin]),axis =0)

				x = data[lower[0]:upper[0]+1,lower[1]:upper[1]+1,lower[2]:upper[2]+1].flatten()
				#raise('hallo')
				outdata[i,j,k] = nanmean(x)
				
			outdata.flush()

			



sh = (2000,2000,2000)

im = np.memmap('tmpIn',dtype='float64',mode = 'w+', shape = sh)
out = np.memmap('tmpOut',dtype='float64',mode = 'w+', shape = sh)

#im[:,:,:] = np.random.rand(sh[0],sh[1],sh[2])
im.flush()

fsize = 5


streaming3Dfilter(im,out,fsize)
plt.close()
plt.imshow(np.squeeze(im))
#plt.show()