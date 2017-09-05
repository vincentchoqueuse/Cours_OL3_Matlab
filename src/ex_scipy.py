from numpy import *
from scipy.stats import *
from matplotlib.pyplot import *

N=10000
noise=norm.rvs(scale=0.05,size=N)

x=arange(-0.2,0.2,0.01)
pdf=norm.pdf(x,scale=0.05)

hist(noise,20, normed=True)
plot(x,pdf)
xlabel('x')
ylabel('pdf(x)')
show()