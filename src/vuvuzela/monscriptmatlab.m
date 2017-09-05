f0=1000;    %la fréquence de ma sinusoide
Fe=44100;   %la fréquence d'échantillonage
Te=1/Fe;     %la periode d'échantillonnage
t=[0:Te:2]

x=sin(2*pi*f0*t);
plot(t,x)
