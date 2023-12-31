import matplotlib.pyplot as plt
from Univert import Univert, Etoile

solar_system = Univert(400, capacity=4)  # Ajouter la capacité du Quadtree

etoile1 = Etoile(solar_system, 50, 50, "green", vitesse=(1, 1, 1))
etoile2 = Etoile(solar_system, 50, 50, "blue", vitesse=(2, -1, 1))
etoile3 = Etoile(solar_system, 50, 50, "gray", vitesse=(1, -1, -1))
etoile4 = Etoile(solar_system, 50, 50, "green", vitesse=(5, 1, 2))

while True:
    solar_system.update_all()
    solar_system.draw_all()
