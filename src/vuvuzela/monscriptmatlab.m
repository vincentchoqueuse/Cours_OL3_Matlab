f0=1000;    %la fr�quence de ma sinusoide
Fe=44100;   %la fr�quence d'�chantillonage
Te=1/Fe;     %la periode d'�chantillonnage
t=[0:Te:2]

x=sin(2*pi*f0*t);
plot(t,x)
