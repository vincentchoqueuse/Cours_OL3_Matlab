Fe =44100; % d�finition de Fe
t= [0:1/ Fe :1]; % d�finition de la base temps
x=sin (2* pi *1000* t) % creation d une sinusoide � 10 Hz
plot (t,x)

player = audioplayer(x, Fe);
play(player)