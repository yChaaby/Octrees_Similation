import math

class Cube:
    def __init__(self, x, y, z, width, height, depth):
        self.x = x
        self.y = y
        self.z = z
        self.width = width
        self.height = height
        self.depth = depth

    def contains_point(self, point):
        return (
            self.x - self.width / 2 <= point[0] <= self.x + self.width / 2
            and self.y - self.height / 2 <= point[1] <= self.y + self.height / 2
            and self.z - self.depth / 2 <= point[2] <= self.z + self.depth / 2
        )

class Vector:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f"Vector({self.x}, {self.y}, {self.z})"
    def __str__(self):
        return f"{self.x}i + {self.y}j + {self.z}k"
    def __add__(self, other):
        return Vector(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z,
        )
    def __sub__(self, other):
        return Vector(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z,
        )    
    def __getitem__(self, item):
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        elif item == 2:
            return self.z
        else:
            raise IndexError("La dimention est juste en 3D, les valeurs autorisée sont 0,1,2 ")
    def __mul__(self, other):
        if isinstance(other, Vector):  # Produit de deux vecteur ( scalaire )
            return (
                self.x * other.x
                + self.y * other.y
                + self.z * other.z
            )
        elif isinstance(other, (int, float)):  # cas de produit µV
            return Vector(
                self.x * other,
                self.y * other,
                self.z * other,
            )
        else:
            raise TypeError("l'operation ne peut pas etre faite, que dans le cas du vecteur*(vecteur ou int/float)")
    def __truediv__(self, other): #divsion par un scalaire
        if isinstance(other, (int, float)):
            return self*(1/other)
        else:
            raise TypeError("la division ne peut etre faite que si Vector/float")
    def get_norme(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2) # calcul de la norme
    def normaliser(self):
        norme = self.get_norme()
        return self/norme
        
    


# un petit programme de teste 
test = Vector(1, 1, 1)
test2 = Vector(3, 5, 9)
print(test.normaliser().get_norme())