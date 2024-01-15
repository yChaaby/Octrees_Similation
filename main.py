import matplotlib.pyplot as plt
from Univert import *


solar_system = Univers(400)






'''Etoile(solar_system, 10,couleur="red",position=(10,15,10),vitesse=(0,0,0))
Etoile(solar_system, 10,couleur="green",position=(-12,-1,-10),vitesse=(0,0,0))
Etoile(solar_system, 10,couleur="yellow",position=(-20,-20,-20),vitesse=(0,0,0))'''



# Palette de couleurs
cmap = plt.get_cmap("viridis")

for i in range(5):
    # Obtenir la couleur de la palette en fonction de i
    couleur = cmap(i / 29.0)  # Normalisation pour obtenir une valeur entre 0 et 1

    # Créer une étoile avec une couleur différente à chaque itération
    Etoile(solar_system, 10 + i, couleur='green',vitesse=(0,0,0))



'''print("before")
first = solar_system.octree.__repr__()
print(first)'''


def on_close(event):
    plt.close()
    global running
    running = False

plt.gcf().canvas.mpl_connect('close_event', on_close)
plt.show(block=False)

global running
running = True

while running:

   solar_system.draw_all()
   solar_system.update_all()
   solar_system.draw_octree_from_repr()
   '''if solar_system.octree.__repr__() != first:
       print('after')
       print(solar_system.octree)'''
       
    #plt.pause(0.001)
    #print(body.vitesse)
