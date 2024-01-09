import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.markers import MarkerStyle
from QuadTree import Octree
from vectors import Vector
import math
import itertools
from random import *

class Univert:
    # Cette première méthode __init__ initialise un système solaire !
    def __init__(self, size):
        # La taille du cube qui contiendra le système solaire :
        self.size = size
        # Cet attribut est une liste vide. Mais, il contiendra toutes les étoiles du système solaire prochainement !
        self.etoiles = []
        # Create an Octree structure to store stars first one with (0,0,0)
        self.octree = Octree((0, 0, 0), size)
        self.fig, self.ax = plt.subplots(
            1,
            1,
            subplot_kw={"projection": "3d"},  # la projection est en 3D
            figsize=(self.size / 50, self.size / 50),
        )
        self.fig.tight_layout()
        self.ax.view_init(0, 0)

    # Cette méthode permet d'ajouter des étoiles en orbite au système solaire :
    def add_etoile(self, etoile):
        # Add the star to the Octree
        self.octree.insert_star(etoile)

    #Cette méthode déplace et dessine chaque étoile du système étoile, fait deux choses à fois 
    def update_all(self):
        self.octree.update_all() #la mise de la structure aussi 
        self.ax.set_xlim((-self.size / 2, self.size / 2))
        self.ax.set_ylim((-self.size / 2, self.size / 2))
        self.ax.set_zlim((-self.size / 2, self.size / 2))
        plt.pause(0.01)
        self.ax.clear()

    def draw_all(self):
        self.ax.set_xlim((-self.size / 2, self.size / 2))
        self.ax.set_ylim((-self.size / 2, self.size / 2))
        self.ax.set_zlim((-self.size / 2, self.size / 2))
        plt.pause(0.01)
        self.ax.clear()

    # Calculer les interactions entre toutes les étoiles du systèmes solaire :
    def interaction_calculateur(self):
        # Mettre à jour les positions des étoiles dans l'Octree
        self.octree.update_all()

        # Calculer les interactions gravitationnelles à l'intérieur de l'Octree
        self.octree.update_recursive()

        # Pour chaque étoile, appliquer les interactions gravitationnelles avec les voisins dans l'Octree
        for star in self.octree.stars:
            # Récupérer les voisins de l'étoile depuis l'Octree
            neighbors = self.octree.get_neighbors(star)

            # Appliquer les interactions gravitationnelles avec chaque voisin
            for neighbor in neighbors:
                star.accelerate_due_to_gravity(neighbor)
class Etoile:
    # La taille minimale d'une étoile !
    min_display_size = 10
    display_log_base = 1.3

    """
    - theWorld : Permet de relier une étoile à un système solaire. La'rgument doit être de type 'Univert' !
    - masse : Un nombre entier qui définit la masse du corps.
    - couleur : Une chaîne de caractères qui définit la couleur de l'étoile !
    - position : Est un point dans l'espace 3D définissant la position de l'étoile. La valeur par défaut est l'origine !
    - vitesse : Définit la vitesse du corps. Puisque la vitesse d’un corps en mouvement a une ampleur et une direction, 
                elle doit être un vecteur.
    """
    def __init__(self, theWorld, masse, couleur, position=None, vitesse=None):
        self.theWorld = theWorld
        self.masse = masse
        # cela générera des positions et des vitesses initiales aléatoires pour chaque étoile si ces derniers ne sont pas précisés.
        if position is None:
            position = (uniform(-100, 100), uniform(-100, 100), uniform(-100, 100))
        if vitesse is None:
            vitesse = (
                uniform(-1, 1) + uniform(-0.1, 0.1),
                uniform(-1, 1) + uniform(-0.1, 0.1),
                uniform(-1, 1) + uniform(-0.1, 0.1),
            )

        self.position = position
        # On convertit le tuple en Vector. l'étoile (*) pour récupérer la valeur stockée dans 'vitesse', à savoir le tuple.
        self.vitesse = Vector(*vitesse)

        # TAILLE_AFFICHAGE_ÉTOILE = MAX(TAILLE DU MARQUEUR CALCULÉE,LA TAILLE MINIMALE DU MARQUEUR --> 10)
        self.display_size = max(
            # Pour convertir la masse en taille du marqueur ! 
            5,
            self.min_display_size,
        )

        self.couleur = couleur
        # Après avoir créé l'étoile, on l'ajoute au système solaire !
        self.theWorld.add_etoile(self)

    # LES MÉTHODES POUR LA CLASSE ÉTOILE :
    # 1. DÉPLACEMENT : Cette méthode redéfinit l'attribut 'position' en fonction de l'attribut 'vitesse' !
    def move(self):
        self.position = (
            self.position[0] + self.vitesse[0],
            self.position[1] + self.vitesse[1],
            self.position[2] + self.vitesse[2],
        )

        if not self.is_inside_solar_system(self.position):
            self.adjust_position()

    def adjust_position(self):
        self.position = (-self.position[0],
                         -self.position[1],
                         -self.position[2])

    # Cette méthode nous renvoie TRUE si une étoile est à l'intérieur du système solaire, sinon FALSE 
    def is_inside_solar_system(self, position):
        x, y, z = position
        size = self.theWorld.size / 2
        return -size <= x <= size and -size <= y <= size and -size <= z <= size

    # 2. DESSINER UNE ÉTOILE DANS UN SYSTÈME SOLAIRE !
    def draw(self):
        # custom_marker_path = Path([(0, 0), (1, 1), (2, 0), (3, 2)])

        # Créer un style de marqueur personnalisé

        # custom_marker = MarkerStyle(marker=custom_marker_path, fillstyle='none')
        self.theWorld.ax.plot(
            *self.position,
            marker='.',
            # markersize=self.display_size + self.position[0] / 30,
            color=self.couleur
        )

    # Calculer l'accélération due à la gravité :
    """
    Cette méthode calcule :
    D'abord, La force due à la gravité entre deux étoiles (F = m1*m2 / r**2)
    Ensuite, L'accélération à laquelle chaque étoile est soumise
    Enfin, Modifier la vitesse d'une étoile permettra de modifier la position d'une étoile dans l'espace 3D
    """
    # Les paramètres 'self' et 'other' représentent les deux étoiles en interaction :
    def accelerate_due_to_gravity(self, other):
        # La distance entre deux étoiles en vecteurs en utilisant la méthode __sub__ définie précédemment !
        distance = Vector(*other.position) - Vector(*self.position)
        # La distance en nombre entier !
        distance_mag = distance.get_norme()
        if distance_mag==0:
            return
        # La force due à la gravité (F = m1*m2 / r**2) !
        force_mag = self.masse * other.masse / (distance_mag ** 2)
        speed_factor = (1.0 + self.vitesse.get_norme() + other.vitesse.get_norme()) / 2
        force = distance.normaliser() * (force_mag + speed_factor)
        reverse = 1
        for body in self, other:
            acceleration = force / body.masse
            body.vitesse += acceleration * reverse
            reverse = -1