from scipy.io import *
from matplotlib.pyplot import *
from skimage import color
from skimage import filters

M1=imread('img/lenna.png')
M2=color.rgb2gray(M1)
val = filters.threshold_otsu(M2)
M3 = M2 > val
M4=filters.gaussian_filter(M2, sigma=5)

f, ax= subplots(2, 2)
ax[0,0].imshow(M1)
ax[0,1].imshow(M2,cmap=cm.gray)
ax[1,0].imshow(M3,cmap=cm.gray)
ax[1,1].imshow(M4,cmap=cm.gray)
show()