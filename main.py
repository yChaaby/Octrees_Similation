import matplotlib.pyplot as plt
from Univert import *


solar_system = Univert(400)






Etoile(solar_system, 10,couleur="red",position=(10,10,10),vitesse=(0,0,0))
Etoile(solar_system, 10,couleur="red",position=(-10,-10,-10),vitesse=(0,0,0))
Etoile(solar_system, 10,couleur="red",position=(-20,-20,-20),vitesse=(0,0,0))



for i in range(50): Etoile(solar_system, 1+i,couleur="Green")



print("before")
first = solar_system.octree.__repr__()
print(first)



while True:
    #print("---")
    
    solar_system.draw_all()
    solar_system.update_all()
    '''if solar_system.octree.__repr__() != first:
       print('after')
       print(solar_system.octree)'''
       
    #plt.pause(0.001)
    #print(body.vitesse)
