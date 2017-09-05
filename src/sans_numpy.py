from math import *

angles=[0,pi/6,pi/4,pi/3,pi/2]

mes_cosinus=[]

for k in range(len(angles)):
    valeur=cos(angles[k])
    mes_cosinus.append(valeur)

print(mes_cosinus)