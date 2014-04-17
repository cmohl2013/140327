import numpy as np
from scipy import ndimage
from scipy.stats import nanmean
n = 5
im = np.ones((n,n,n))*np.arange(n)
im[:4,:4,:4]=np.nan
def test(x):
	return nanmean(x)


size = 2

res = ndimage.generic_filter(im, test,size = size)

print(im)
print(res)

