from vectors import Vector


class Octree:

    def __init__(self, center: Vector, size: float,depth=None):
        self.center = center
        self.size = size
        if depth is None:
            self.depth = 0
        else:
            self.depth=depth
        self.children = [None] * 8
        self.stars = []

    def insert_star(self, star):
        if self.is_leaf():
            if len(self.stars) < 1:
                self.stars.append(star)
            else:
                self.subdivide()
                self.insert_star(star)
        else:
            child = self.get_child(star)
            if child is not None:
                child.insert_star(star)

    def get_child(self, star) :
        for child in self.children:
            if child is not None and child.contains(star.position):
                return child
        return None

    def contains(self, star: Vector) -> bool:
        return (
            self.center[0] <= star[0] <= self.center[0] + self.size and
            self.center[1] <= star[1] <= self.center[1] + self.size and
            self.center[2] <= star[2] <= self.center[2] + self.size
        )

    def subdivide(self):
        for i in range(8):
            
            self.children[i] = Octree(
                center=(
                    self.center[0] + (i // 4) * self.size / 2,
                    self.center[1] + (i // 2) % 2 * self.size / 2,
                    self.center[2] + (i % 2) * self.size / 2,
                ),
                size=self.size / 2,
                depth=self.depth + 1,
            )
            
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

    def get_stars(self) -> list:
        if self.is_leaf():
            return self.stars
        else:
            stars = []
            for child in self.children:
                if child is not None:
                    stars += child.get_stars()
            return stars

    def is_leaf(self) -> bool:
        return all(child is None for child in self.children)
    def update_all(self):
        pass
    def update_recursive(self): #useless function 
        for star in self.stars:
            star.move()
            star.draw()

        for child in self.children:
            if child is not None:
                child.update_recursive()
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
    
    def __repr__(self):
        # Indentation for each level
        indentation = "  " * self.depth

        # Representation for this Octree
        representation = f"{indentation}Octree(center={self.center}, size={self.size}, depth={self.depth}, num_stars={len(self.stars)})\n"

        # Recursively print children
        for child in self.children:
            if child:
                representation += child.__repr__()
        return representation