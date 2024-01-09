from vectors import Vector

class Octree:
    def __init__(self, center, size):
        self.center = Vector(*center)
        self.size = size
        self.stars = []
        self.children = [None] * 8

    def insert_star(self, star):
        # Check in which octant the star belongs and insert it into the corresponding child
        if len(self.stars) == 0 and all(child is None for child in self.children):
            # cas cube vide
            self.stars.append(star)
        else:
            # trouve dans quel cube se situe l'etoile
            index = self.get_octant_index(star.position)

            # Create child if it doesn't exist
            if self.children[index] is None:
                self.subdivide(index)

            # Recursively insert the star into the appropriate child
            self.children[index].insert_star(star)

    def get_octant_index(self, position):
        # cette fonction determine dans quel cube des 8 sera l'etoiles en fonction de leur coordonnee 
        x, y, z = position
        index = 0
        if x >= self.center[0]:
            index |= 1
        if y >= self.center[1]:
            index |= 2
        if z >= self.center[2]:
            index |= 4
        return index

    def subdivide(self, index):
        # Calculate the size of the new child octant
        new_size = self.size / 2
        # Calculate the new center of the child octant
        new_center = self.center + Vector(
            new_size * (1 if index & 1 else -1),
            new_size * (1 if index & 2 else -1),
            new_size * (1 if index & 4 else -1)
        )
        # Creation de "child"
        self.children[index] = Octree(new_center, new_size)

    def update_all(self):
        pass

    def update_recursive(self):
        for star in self.stars:
            star.move()
            star.draw()

        for child in self.children:
            if child is not None:
                child.update_recursive()
    def __repr__(self, level=0):
        #Indentation en fonction du niveau
        indentation = "  " * level
        #représentation pour cet Octree
        representation = f"{indentation}Octree(center={self.center}, size={self.size}, num_stars={len(self.stars)})"

        # Appel récursif pour les enfants
        for child in self.children:
            if child is not None:
                representation += f"\n{child.__repr__(level + 1)}"
        return representation
    def get_neighbors(self, star):
        neighbors = [] #initialisation liste vide
        index = self.get_octant_index(star.position)
        # Ajout des etoiles du cube actuel
        neighbors.extend(self.stars)

        # Récursivement ajout des etoiles des cubes voisins
        for i in range(8):
            if self.children[i] is not None and i != index:
                neighbors.extend(self.children[i].get_neighbors(star))

        return neighbors