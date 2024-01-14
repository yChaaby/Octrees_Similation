import matplotlib.pyplot as plt
from Univert import *


solar_system = Univert(400)






et1=Etoile(solar_system, 10,couleur="red",position=(200,10,10),vitesse=(0,0,0))
et2=Etoile(solar_system, 10,couleur="red",position=(200,-10,-10),vitesse=(0,0,0))
#et1=Etoile(solar_system, 10,couleur="red",position=(200,150,150),vitesse=(0,0,0))
et1=Etoile(solar_system, 10,couleur="red",position=(200,80,60),vitesse=(0,0,0))
first = solar_system.octree.__repr__()
print("before")
print(first)

for ot in solar_system.octree.iterator():
    for etoile in ot.stars:
        if etoile!=et2:
            print(first)
            ot.remove_star()
            #print(ot.stars)
            pass
           


for ot in solar_system.octree.iterator():
    for etoile in ot.stars:
        print(etoile.position)

#for i in range(50): Etoile(solar_system, 1+i,couleur="Green")



print("after")
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
    
