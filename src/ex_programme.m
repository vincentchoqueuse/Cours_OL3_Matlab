% creation de la base temps
Fe=1000;
t=0:1/Fe:1;

% generation de la sinusoide
f0=5;
x=sin(2*pi*f0*t);

% affichage
plot(t,x)
xlabel('base temps(s)')
