import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.markers import MarkerStyle
from vectors import Vector
import math
import itertools
from random import *

class Univert :
    # Cette première méthode __init__ initialise un système solaire !
    def __init__(self, size):
        # La taille du cube qui contiendra le système solaire :
        self.size = size
        # Cet attribut est une liste vide. Mais, il contiendra toutes les étoiles du système solaire prochainement !
        self.etoiles = []
        self.fig, self.ax = plt.subplots(
            1,
            1,
            subplot_kw={"projection": "3d"}, # la projection est en 3D
            figsize=(self.size / 50, self.size / 50),
        )
        self.fig.tight_layout()
        self.ax.view_init(0,0)

    # Cette méthode permet d'ajouter des étoiles en orbite au système solaire :
    def add_etoile(self, etoile):
        self.etoiles.append(etoile)

    # Cette méthode déplace et dessine chaque étoile du système étoile. C'est une méthode qui fait deux choses à fois ! 
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

    # Calculer les interactions entre toutes les étoiles du systèmes solaire :
    def interaction_calculateur(self):
        etoiles_copy = self.etoiles.copy()
        for idx, first in enumerate(etoiles_copy):
            for second in etoiles_copy[idx + 1:]:
                first.accelerate_due_to_gravity(second)
        
class Etoile:
    # La taille minimale d'une étoile !
    min_display_size = 10
    display_log_base = 1.3
    """
        - theWorld : Permet de relier une étoile à un système solaire. La'rgument doit être de type 'Univert' !
        - masse : Un nombre entier qui définit la masse du corps.
        - couleur : Une chaîne de caractères qui définit la couleur de l'étoile !
        - position : Est un point dans l'espace 3D définissant la position de l'étoile. La valeur par défaut est l'origine !
        - vitesse : Définit la vitesse du corps. Puisque  la vitesse d’un corps en mouvement a une ampleur et une direction, 
                    elle doit être un vecteur.
    """
    def __init__(self, theWorld, masse,couleur, position=None, vitesse=None,) :
        self.theWorld = theWorld
        self.masse = masse
         #cela générera  des positions et des vitesses initiales aléatoires pour chaque étoile si ces derniers ne sont pas préciser.
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
            math.log(self.masse, self.display_log_base),
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

        if not self.is_inside_solar_system(self.position) :
            self.adjust_position()
    
    def adjust_position(self) :
        self.position = (-self.position[0],
                        -self.position[1],
                        -self.position[2])
                        
    
    # Cette méthode nous renvoie TRUE si une étoile est à l'intérieur du système solaire, sinon FALSE 
    def is_inside_solar_system(self,position) :
        x,y,z=position
        size=self.theWorld.size/2
        return -size <= x <= size and -size <= y <= size and -size <= z <= size

    # 2. DESSINER UNE ÉTOILE DANS UN SYSTÈME SOLAIRE !
    def draw(self):
        #custom_marker_path = Path([(0, 0), (1, 1), (2, 0), (3, 2)])

        # Créer un style de marqueur personnalisé
        
        #custom_marker = MarkerStyle(marker=custom_marker_path, fillstyle='none')
        self.theWorld.ax.plot(
            *self.position,
            marker='o',
            markersize=self.display_size + self.position[0] / 30,
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
        # La force due à la gravité (F = m1*m2 / r**2) !
        force_mag = self.masse * other.masse / (distance_mag ** 2)
        speed_factor = (1.0 + self.vitesse.get_norme() + other.vitesse.get_norme())/2
        force = (speed_factor+distance.normaliser()) * (force_mag)
        reverse = 1
        for body in self, other:
            acceleration = force / body.masse
            body.vitesse += acceleration * reverse
            reverse = -1

# La création de deux nouvelles classes SOLEIL & PLANÈTE de type Etoile : 
"""
- la masse a une valeur par défaut, à savoir 10_000. De même pour la position et la vitesse.
- Cette classe 'Soleil' hérite de sa classe parente tous les attributs ainsi que toutes les méthodes.

"""
class Soleil(Etoile) :
    def __init__(self, theWorld, masse=10_000, position=(0, 0, 0), vitesse=(0, 0, 0),):
        # super(Soleil, self) : Crée un objet de type 'super' qui représente la classe parente de la classe 'Soleil'.
        # Puis, appelle la méthode __init__ de la classe parente 'Etoile' avec les paramètres spécifiés.
        super(Soleil,self).__init__(theWorld, masse, position, vitesse)
        # La couleur du soleil, c'est inchangeable !
        self.couleur="Yellow"

class Planete(Etoile) :
    # couleurs est un attribut de classe. (RED,GREEN,BLUE)
    couleurs=itertools.cycle([(1,0,0),(0,1,0),(0,0,1)])

    def __init__(self, theWorld, masse=10,position=(0, 0, 0),vitesse=(0, 0, 0),):
        super(Planete,self).__init__(theWorld,masse,position, vitesse)
        """
            Initiliase l'attribut 'couleur' de l'objet 'Planete' avec la prochaine couleur du générateur cyclique 'couleurs'.
            Cela garantit que chaque planète a une couleur différente.
        """
        self.couleur=next(Planete.couleurs)