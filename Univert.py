import matplotlib.pyplot as plt
from vectors import Vector
import math


class Univert :
    def __init__(self, size):
        self.size = size # taille de la fenetre 
        self.etoiles = []
        self.fig, self.ax = plt.subplots(
            1,
            1,
            subplot_kw={"projection": "3d"}, # la projection est en 3D
            figsize=(self.size / 50, self.size / 50),
        )
        self.fig.tight_layout()
        self.ax.view_init(0, 0)
    def add_etoile(self, etoile):
        self.etoiles.append(etoile)
    def update_all(self):
        for etoile in self.etoiles:
            etoile.move()
            etoile.draw()
    def draw_all(self):
        self.ax.set_xlim((-self.size / 2, self.size / 2))
        self.ax.set_ylim((-self.size / 2, self.size / 2))
        self.ax.set_zlim((-self.size / 2, self.size / 2))
        plt.pause(0.001)
        self.ax.clear()
        
class SolarSystemBody:
    min_display_size = 10
    display_log_base = 1.3
    def __init__(self,solar_system,masse,position=(0, 0, 0),vitesse=(0, 0, 0),):
        self.solar_system = solar_system
        self.masse = masse
        self.position = position
        self.vitesse = Vector(*vitesse)
        self.display_size = max(
            math.log(self.masse, self.display_log_base),
            self.min_display_size,
        )
        self.colour = "Green"
        self.solar_system.add_etoile(self)
    def move(self):
        self.position = (
            self.position[0] + self.vitesse[0],
            self.position[1] + self.vitesse[1],
            self.position[2] + self.vitesse[2],
        )
    def draw(self):
        self.solar_system.ax.plot(
            *self.position,
            marker="o",
            markersize=self.display_size,
            color=self.colour
        )
        