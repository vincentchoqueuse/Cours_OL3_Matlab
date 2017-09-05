from numpy import *
from scipy.signal import *
from scipy.io.wavfile import *
from matplotlib.pyplot import *

Fe=44100
t=arange(0,10,1/Fe)
x=chirp(t,0,10,Fe/2)
write('audio/chirp.wav',Fe,x)

plot(t,x)
xlabel("temps(s)")

figure()
f, t, Sxx=spectrogram(x,Fe)
pcolormesh(t, f, Sxx)
xlabel("temp(s)")
ylabel("frequence (Hz)")
show()