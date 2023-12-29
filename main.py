import matplotlib.pyplot as plt
from Univert import *


solar_system = Univert(500)

body = Etoile(solar_system, 100,couleur='Pink',position=(2,1,-1),vitesse=(5,7,8),)
body = Etoile(solar_system, 50,couleur="Red",position=(2,3,-2),vitesse=(5,7,8),)
body = Etoile(solar_system, 50,couleur="Orange",position=(4,1,0) ,vitesse=(5,7,8),)
body = Etoile(solar_system, 50,couleur="Blue",position=(4,3,1) ,vitesse=(5,7,8),)
body = Etoile(solar_system, 50,couleur="Green",position=(6,-4,-1) ,vitesse=(5,7,8),)

while True:
    solar_system.interaction_calculateur()
    solar_system.update_all()
    solar_system.draw_all()
    print(body.vitesse)
