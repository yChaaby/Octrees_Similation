import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.markers import MarkerStyle
from Octtree import Octree
from vectors import Vector
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from random import *



class Univers:
    # Cette première méthode __init__ initialise un système solaire !
    def __init__(self, size):
        # La taille du cube qui contiendra le système solaire :
        self.size = size
        # Cet attribut est une liste vide. Mais, il ne contiendra plus toutes les étoiles du système solaire prochainement !
        self.etoiles = []
        # notre structure ou on va stocker nos etoiles ( initialiser avec le centre )
        self.octree = Octree((0, 0, 0), size/2)
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
        self.etoiles.append(etoile)

    #Cette méthode déplace et dessine chaque étoile du système étoile, fait deux choses à fois 
    def update_all(self):
        for etoile in self.etoiles:
            etoile.update_gravity(self.octree)
            etoile.move()
            etoile.draw()
        #la doit etre le octtre_eupdate() ...
        self.octree = Octree((0, 0, 0), self.size/2)
        for etoile in self.etoiles:
            self.octree.insert_star(etoile)
        
        

    def draw_all(self):
        self.ax.set_xlim((-self.size / 2, self.size / 2))
        self.ax.set_ylim((-self.size / 2, self.size / 2))
        self.ax.set_zlim((-self.size / 2, self.size / 2))
        self.ax.axis('off')
        plt.pause(0.001)
        self.ax.clear()

    # Calculer les interactions entre toutes les étoiles du systèmes solaire :
    
    def draw_octree_from_repr(self):
        # dessiner l'octree et ces enfants 
        self.draw_octree(self.octree)

    def draw_octree(self, octree_repr):
        if octree_repr is not None:
            # Dessine les limites du cube actuel
            self.draw_boundary(octree_repr.center, octree_repr.size)

            # La récursivité pour les enfants
            for child_repr in octree_repr.children:
                self.draw_octree(child_repr)

    def draw_boundary(self, center, size):
        # Extraire les sommets d'un cube à partir des informations de l'octree
        vertices = [
            (center[0] + size, center[1] + size, center[2] + size),
            (center[0] + size, center[1] - size, center[2] + size),
            (center[0] - size, center[1] - size, center[2] + size),
            (center[0] - size, center[1] + size, center[2] + size),
            (center[0] + size, center[1] + size, center[2] - size),
            (center[0] + size, center[1] - size, center[2] - size),
            (center[0] - size, center[1] - size, center[2] - size),
            (center[0] - size, center[1] + size, center[2] - size)
        ]

        # Définir les faces d'un cube à l'aide des sommets
        faces = [
            [vertices[0], vertices[1], vertices[2], vertices[3]],
            [vertices[4], vertices[5], vertices[6], vertices[7]],
            [vertices[0], vertices[1], vertices[5], vertices[4]],
            [vertices[2], vertices[3], vertices[7], vertices[6]],
            [vertices[1], vertices[2], vertices[6], vertices[5]],
            [vertices[0], vertices[3], vertices[7], vertices[4]]
        ]

        # Tracer les limites du cube
        face_color = '#4D5656'
        edge_color = '#2E4053'
        cube_boundary = Poly3DCollection(faces, edgecolor=edge_color,facecolor=face_color, linewidths=1,alpha=0.15,antialiased=True)
        self.ax.add_collection3d(cube_boundary)

        # Ajuster les limites de l'axe
        self.ax.set_xlim((center[0] - size, center[0] + size))
        self.ax.set_ylim((center[1] - size, center[1] + size))
        self.ax.set_zlim((center[2] - size, center[2] + size))     
    def update_octtree(self):
        for child in self.octree.iterator():
            if len(child.stars)==1: #feuille
                if not child.star_inside():
                    tempStar = get_first_non_none_element(child.stars)
                    child.remove_star()
                    self.octree.insert_star(tempStar)

class Etoile:
    # La taille minimale d'une étoile !
    min_display_size = 10
    display_log_base = 1.3

    """
    - theWorld : Permet de relier une étoile à un système solaire. La'rgument doit être de type 'Univers' !
    - masse : Un nombre entier qui définit la masse du corps.
    - couleur : Une chaîne de caractères qui définit la couleur de l'étoile !
    - position : Est un point dans l'espace 3D définissant la position de l'étoile. La valeur par défaut est l'origine !
    - vitesse : Définit la vitesse du corps. Puisque la vitesse d’un corps en mouvement a une ampleur et une direction, 
                elle doit être un vecteur.
    """
    def __init__(self, theWorld, masse, couleur, position=None, vitesse=None):
        self.theWorld = theWorld
        self.masse = masse
        INTERVALE_DEPOS=200
        # cela générera des positions et des vitesses initiales aléatoires pour chaque étoile si ces derniers ne sont pas précisés.
        if position is None:
            position = Vector(uniform(-INTERVALE_DEPOS, INTERVALE_DEPOS), uniform(-INTERVALE_DEPOS, INTERVALE_DEPOS), uniform(-INTERVALE_DEPOS, INTERVALE_DEPOS))
        if vitesse is None:
            vitesse = Vector(
                uniform(-1, 1) + uniform(-0.1, 0.1),
                uniform(-1, 1) + uniform(-0.1, 0.1),
                uniform(-1, 1) + uniform(-0.1, 0.1),
            )
            

        self.position = Vector(*position)
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
        self.position = self.position + self.vitesse

        if not self.is_inside_solar_system(self.position):
            self.adjust_position()

    def adjust_position(self):
        self.position = Vector(-self.position[0],
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
    def update_gravity(self, octree):
        # Calculer la force gravitationnelle en utilisant l'algorithme de Barnes-Hut
        force = octree.calculate_force(self)
        
        self.vitesse += force
        # mise a jour de la position en fonction de la vitesse
        self.position += self.vitesse

    # Calculer l'accélération due à la gravité :
    """
    Cette méthode calcule :
    D'abord, La force due à la gravité entre deux étoiles (F = m1*m2 / r**2)
    Ensuite, L'accélération à laquelle chaque étoile est soumise
    Enfin, Modifier la vitesse d'une étoile permettra de modifier la position d'une étoile dans l'espace 3D
    """
    # Les paramètres 'self' et 'other' représentent les deux étoiles en interaction :
    
def get_first_non_none_element(my_list):
    for element in my_list:
        if element is not None:
            return element
    return None