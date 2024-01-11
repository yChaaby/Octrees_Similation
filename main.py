import matplotlib.pyplot as plt
from Univert import *


solar_system = Univert(400)






Etoile(solar_system, 1,couleur="red",position=(10,10,10),)
Etoile(solar_system, 2,couleur="green",position=(13,13,13),)
for i in range(30): Etoile(solar_system, 1+i,couleur="red")



print("before")
first = solar_system.octree.__repr__()
print(solar_system.octree)



while True:
    #print("---")
    
    solar_system.draw_all()
    solar_system.update_all()
    #if solar_system.octree.__repr__() != first:
       # print('after')
       # print(solar_system.octree)
    #plt.pause(0.001)
    #print(body.vitesse)
