
import matplotlib.pyplot as plt
from vectors import Vector, Rectangle
import math

class Quadtree:
    def __init__(self, boundary, capacity):
        self.boundary = boundary  # La limite de la zone du quadtree
        self.capacity = capacity  # Capacité maximale de chaque noeud du quadtree
        self.points = []  # Les étoiles stockées dans la zone du quadtree
        self.subdivided = False  # Indique si le quadtree est subdivisé
        # Définition des quatre quadrants du quadtree
        self.northwest = None
        self.northeast = None
        self.southwest = None
        self.southeast = None

    def insert(self, etoile):
        # Insère une étoile dans le quadtree
        if not self.boundary.contains_point(etoile.position):
            return False  # L'étoile n'est pas dans cette zone du quadtree

        if len(self.points) < self.capacity:
            self.points.append(etoile)
            return True  # L'insertion a réussi

        if not self.subdivided:
            self.subdivide()

        # Essayez d'insérer l'étoile dans les quadrants fils
        return (
            self.northwest.insert(etoile)
            or self.northeast.insert(etoile)
            or self.southwest.insert(etoile)
            or self.southeast.insert(etoile)
        )

    def subdivide(self):
        # Subdivise le quadtree en quatre quadrants
        x = self.boundary.x
        y = self.boundary.y
        w = self.boundary.width / 2
        h = self.boundary.height / 2

        nw_boundary = Rectangle(x - w / 2, y + h / 2, w, h)
        self.northwest = Quadtree(nw_boundary, self.capacity)

        ne_boundary = Rectangle(x + w / 2, y + h / 2, w, h)
        self.northeast = Quadtree(ne_boundary, self.capacity)

        sw_boundary = Rectangle(x - w / 2, y - h / 2, w, h)
        self.southwest = Quadtree(sw_boundary, self.capacity)

        se_boundary = Rectangle(x + w / 2, y - h / 2, w, h)
        self.southeast = Quadtree(se_boundary, self.capacity)

        self.subdivided = True

    def draw_boundary(self):
        # Dessine la limite de la zone du quadtree
        plt.plot(
            [self.boundary.x - self.boundary.width / 2, self.boundary.x - self.boundary.width / 2],
            [self.boundary.y - self.boundary.height / 2, self.boundary.y + self.boundary.height / 2],
            color='gray',
            linestyle='--'
        )
        plt.plot(
            [self.boundary.x + self.boundary.width / 2, self.boundary.x + self.boundary.width / 2],
            [self.boundary.y - self.boundary.height / 2, self.boundary.y + self.boundary.height / 2],
            color='gray',
            linestyle='--'
        )
        plt.plot(
            [self.boundary.x - self.boundary.width / 2, self.boundary.x + self.boundary.width / 2],
            [self.boundary.y - self.boundary.height / 2, self.boundary.y - self.boundary.height / 2],
            color='gray',
            linestyle='--'
        )
        plt.plot(
            [self.boundary.x - self.boundary.width / 2, self.boundary.x + self.boundary.width / 2],
            [self.boundary.y + self.boundary.height / 2, self.boundary.y + self.boundary.height / 2],
            color='gray',
            linestyle='--'
        )

        # Dessine la limite des quadrants fils s'ils existent
        if self.subdivided:
            self.northwest.draw_boundary()
            self.northeast.draw_boundary()
            self.southwest.draw_boundary()
            self.southeast.draw_boundary()



class Univert :
    def __init__(self, size, capacity):
        self.size = size
        self.capacity = capacity
        self.quadtree = Quadtree(Rectangle(0, 0, size, size), self.capacity)
        self.fig, self.ax = plt.subplots(
            1,
            1,
            subplot_kw={"projection": "3d"},
            figsize=(self.size / 50, self.size / 50),
        )
        self.fig.tight_layout()
        self.ax.view_init(0, 0)
        
    
    def update_all(self):
        # Réinitialiser le quadtree à chaque mise à jour
        for etoile in self.quadtree.points:
            etoile.move()
            etoile.draw()

        self.quadtree = Quadtree(Rectangle(0, 0, self.size, self.size), self.capacity)
        for etoile in self.quadtree.points:
            self.quadtree.insert(etoile)

    def draw_all(self):
        self.ax.set_xlim((-self.size / 2, self.size / 2))
        self.ax.set_ylim((-self.size / 2, self.size / 2))
        self.ax.set_zlim((-self.size / 2, self.size / 2))
        self.quadtree.draw_boundary()
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

    def __init__(self, theWorld, masse, volume, couleur, position=(0, 0, 0), vitesse=(0, 0, 0),):
        self.theWorld = theWorld
        self.masse = masse
        self.position = position
        self.vitesse = Vector(*vitesse)
        self.display_size = max(
            math.log(self.masse, self.display_log_base),
            self.min_display_size,
        )
        self.couleur = couleur
        self.theWorld.quadtree.insert(self)

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
