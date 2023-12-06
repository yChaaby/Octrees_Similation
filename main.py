import matplotlib.pyplot as plt
from Univert import Univert, Etoile


solar_system = Univert(350)
body = Etoile(solar_system, 10,100,couleur="Pink",position=(2,1,-1) ,vitesse=(2,2,2))
body = Etoile(solar_system, 50,50,couleur="Red" ,vitesse=(1,0, 0))
body = Etoile(solar_system, 50,50,couleur="orange",position=(4,1,-1) ,vitesse=(1,0, 0))
body = Etoile(solar_system, 50,50,couleur="Blue",position=(4,3,1) ,vitesse=(1,0, 0))
body = Etoile(solar_system, 50,50,couleur="Green",position=(6,-4,-1) ,vitesse=(1,0, 0))

while True:
    solar_system.interaction_calculateur()
    solar_system.update_all()
    solar_system.draw_all()
    ##print(body.vitesse)
    
