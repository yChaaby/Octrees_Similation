import math
from random import *

class Vector:
    # Un point de cet espace 3D : 
    # Placer le soleil au centre du système solaire, on utilise (0,0,0) :
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f"Vector({self.x}, {self.y}, {self.z})"
    
    def __str__(self):
        return f"{self.x}i + {self.y}j + {self.z}k"
 
    # L'ajout de deux vecteurs : 
    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(
                self.x + other.x,
                self.y + other.y,
                self.z + other.z
            )
        elif isinstance(other, (int, float)):
            # Si 'other' est un nombre, ajoutez-le à chaque composante du vecteur
            return Vector(
                self.x + other,
                self.y + other,
                self.z + other
            )
    
    """ 
        def modifier(self) :
            return Vector(-self.x/2,-self.y/2,-self.z/2)
    """
    
    # La soustraction de deux vecteurs : 
    def __sub__(self, other):
        return Vector(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z,
        )    
    
    # Grâce à __getitem__, nous avons rendu la classe Vector indexable 0,1,2 : 
    def __getitem__(self, item):
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        elif item == 2:
            return self.z
        else:
            raise IndexError("La dimention est juste en 3D, les valeurs autorisée sont 0,1,2 ")
        
    # Le produit de deux vecteurs :
    def __mul__(self, other):
        # Lorsque 'other' est un vecteur : (x1,y1,z1)*(x2,y2,z2) = (x1*x2) + (y1*y2) + (z1*z2) 
        if isinstance(other, Vector):  # Produit de deux vecteur ( scalaire )
            return (
                self.x * other.x
                + self.y * other.y
                + self.z * other.z
            )
        # Lorsque 'other' est un entier OU un float : (x,y,z)*k = (x*k,y*k,z*k)
        elif isinstance(other, (int, float)):  # cas de produit µV
            return Vector(
                self.x * other,
                self.y * other,
                self.z * other,
            )
        else:
            raise TypeError("l'opération ne peut pas être faite, que dans le cas du vecteur*(vecteur ou int/float)")
    
    # Nous ne pouvons pas diviser un vecteur par un autre, mais avec un scalaire !
    def __truediv__(self, other): # Divsion par un scalaire
        # Si le deuxième argument est de type 'scalaire' : 
        if isinstance(other, (int, float)):
            return self*(1/other)
        else:
            raise TypeError("La division ne peut être faite que si Vector/float")
    
    # norme = grandeur : ||A|| : 
    def get_norme(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2) # calcul de la norme
    
    # La normalisation donne un vecteur de même direction, mais avec une norme modifiée. C'est-à-dire, la norme valera 1 !
    def normaliser(self):
        norme = self.get_norme()
        return self/norme
        
    


# un petit programme de teste 
test = Vector(1, 2, 3)
print(test.get_norme())
print(test.normaliser())
print(uniform(-100,100))