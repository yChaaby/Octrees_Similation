import matplotlib.pyplot as plt
from Univert import *


solar_system = Univert(300)


body = Etoile(solar_system, 50,couleur="black",)
body = Etoile(solar_system, 50,couleur="yellow",)
body = Etoile(solar_system, 100,couleur='Pink',)
body = Etoile(solar_system, 50,couleur="Red",)
body = Etoile(solar_system, 50,couleur="#8C1313", )
body = Etoile(solar_system, 90,couleur="Orange", )
body = Etoile(solar_system, 10,couleur="purple",)
body = Etoile(solar_system, 20,couleur="#FFA200",)
body = Etoile(solar_system, 50,couleur="#2E86C1",)
body = Etoile(solar_system, 50,couleur="#2AB41A",)
body = Etoile(solar_system, 50,couleur="#00FFFB",)
body = Etoile(solar_system, 50,couleur="#2E86C1",)
body = Etoile(solar_system, 80,couleur="#A71E75",)

print("before")
first = solar_system.octree.__repr__()
print(solar_system.octree)


while True:
    #print("---")
    solar_system.interaction_calculateur()
    solar_system.draw_all()
    if solar_system.octree.__repr__() != first:
        print('after')
        print(solar_system.octree)
    #plt.pause(0.001)
    #print(body.vitesse)
