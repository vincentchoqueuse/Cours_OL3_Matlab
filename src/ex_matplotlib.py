from numpy import *
from matplotlib.pyplot import *

f0=2
#creation de la base temps
t=arange(1000)/1000

#creation de la sinusoide
x=cos(2*pi*f0*t)

#affichage
plot(t,x)
xlabel('temps(s)')
ylabel('sinusoide')
show()