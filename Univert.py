import matplotlib.pyplot as plt
from vectors import Vector
import math


class Univert :
    def __init__(self, size):
        self.size = size # taille de la fenetre 
        self.etoiles = [] # la structure pour l'instant c'est une liste (tableau +-)
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
    def interaction_calculateur(self):
        etoiles_copy = self.etoiles.copy()
        for idx, first in enumerate(etoiles_copy):
            for second in etoiles_copy[idx + 1:]:
                first.accelerate_due_to_gravity(second)
        
class Etoile:
    min_display_size = 10
    display_log_base = 1.3
    def __init__(self, theWorld, masse,volume, couleur, position=(0, 0, 0), vitesse=(0, 0, 0),):
        self.theWorld = theWorld
        self.masse = masse
        self.position = position
        self.vitesse = Vector(*vitesse)
        self.display_size = max(
            math.log(self.masse, self.display_log_base),
            self.min_display_size,
        )
        self.couleur = couleur
        self.theWorld.add_etoile(self)
    def move(self):
        self.position = (
            self.position[0] + self.vitesse[0],
            self.position[1] + self.vitesse[1],
            self.position[2] + self.vitesse[2],
        )
    def draw(self):
        self.theWorld.ax.plot(
            *self.position,
            marker="o",
            markersize=self.display_size + self.position[0] / 20,
            color=self.couleur
        )
    def accelerate_due_to_gravity(self, other):
        distance = Vector(*other.position) - Vector(*self.position)
        distance_mag = distance.get_norme()
        force_mag = self.masse * other.masse / (distance_mag ** 2)
        force = distance.normaliser() * force_mag
        reverse = 1
        for body in self, other:
            acceleration = force / body.masse
            body.vitesse += acceleration * reverse
            reverse = -1

        