import matplotlib.pyplot as plt
from Univert import *
import signal
import sys

solar_system = Univert(400)

Etoile(solar_system, 1,couleur="red",position=(10,10,10),)
Etoile(solar_system, 2,couleur="green",position=(13,13,13),)
for i in range(30): Etoile(solar_system, 1+i,couleur="red")

print("before")

def on_close(event):
    plt.close()
    global running
    running = False

plt.gcf().canvas.mpl_connect('close_event', on_close)
plt.show(block=False)

global running
running = True

while running:
   first = solar_system.octree.__repr__()
   print(solar_system.octree)
   solar_system.draw_all()
   solar_system.update_all()





#while True:
    
    
    
    #if solar_system.octree.__repr__() != first:
       # print('after')
       # print(solar_system.octree)
    #plt.pause(0.001)
    #print(body.vitesse)
