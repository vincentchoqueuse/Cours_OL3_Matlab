from numpy import *
from scipy.io.wavfile import *
from matplotlib.pyplot import *

filein='./audio/sample.wav'
fileout='./audio/sample_out.wav'
Fe,signal=read(filein)

#substract left / right channels
x_mono=signal[:,0]-signal[:,1]
write(fileout,Fe,x_mono)

f, ax = subplots(3)
ax[0].plot(signal[:,0])
ax[1].plot(signal[:,1])
ax[2].plot(x_mono)
xlabel("samples")
show()