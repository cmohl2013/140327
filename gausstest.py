import numpy as np
import matplotlib.pyplot as plt

sigma = 20
dist = np.array(range(sigma*3)).astype('float')

mu = 0

y = 1./np.sqrt(2*np.pi*np.square(sigma))*np.exp(-np.square(dist-mu)/(2*np.square(sigma)))

plt.close()
plt.plot(dist,y)
plt.show()