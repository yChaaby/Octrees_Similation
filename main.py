import matplotlib.pyplot as plt
from Univert import *


solar_system = Univert(500)


body = Etoile(solar_system, 50,couleur="black",)
body = Etoile(solar_system, 50,couleur="yellow",)
body = Etoile(solar_system, 100,couleur='Pink',)
body = Etoile(solar_system, 50,couleur="Red",)
body = Etoile(solar_system, 50,couleur="Orange", )
body = Etoile(solar_system, 50,couleur="purple",)
body = Etoile(solar_system, 50,couleur="#2E86C1",)
body = Etoile(solar_system, 80,couleur="#EC407A",)



while True:
    solar_system.interaction_calculateur()
    solar_system.update_all()
    solar_system.draw_all()
    #print(body.vitesse)
