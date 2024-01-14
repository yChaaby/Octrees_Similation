from vectors import Vector

class Octree:
    def __init__(self, center, size, head=None):
        self.center = Vector(*center)
        self.size = size
        self.head = head
        self.stars = []
        self.children = [None] * 8
        self.total_mass = 0

    def insert_star(self, star):
        # deja divisé ou pas
        if all(child is None for child in self.children):
            if len(self.stars) == 0:
                # cas cube vide
                self.stars.append(star)
                self.total_mass += star.masse
            else:
                if get_first_non_none_element(self.stars)==star:
                    return
                index = self.get_octant_index(star.position)
                if self.children[index] is None:
                    self.subdivide(index)
                self.children[index].insert_star(star)
                self.insert_star(self.stars[0])
                self.stars=[]       
        else:
            # trouve dans quel cube se situe l'etoile
            index = self.get_octant_index(star.position)
            
            # si le fils n'existe pas on le cree 
            if self.children[index] is None:
                self.subdivide(index)

            #insertion d'une facon recursive 
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
        new_size = (self.size / 2)
        # Calculate the new center of the child octant
        new_center = self.center + Vector(
            new_size * (1 if index & 1 else -1),
            new_size * (1 if index & 2 else -1),
            new_size * (1 if index & 4 else -1)
        )
        # Creation de "child"
        self.children[index] = Octree(new_center, new_size, self)

    def update_all(self):
       
       pass
    def remove_star(self):

        if self.head is None:# cas de pere de centre 0,0,0
            self.stars=[]
            return

    # Supprimer cette étoile de l'octree actuel
        self.stars = []

    # Vérifier le nombre de fils du parent
        index=self.head.children.index(self)
        self.head.children[index]=None
          # S'il reste un seul fils, supprimer le fils, la division et réinsérer le fils
           
        self.equi()
               

        # Appeler la méthode remove_star sur le parent récursivement
            #self.head.remove_star()
            
    def iterator(self):
        yield self
        for child in self.children:
            if child is not None:
                yield from child.iterator()
        
        

    def update_recursive(self): #useless function 
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
    def calculate_force(self, star):
        # Calculez la force d'attraction gravitationnelle entre l'étoile et cet octree
        direction = self.center - Vector(*star.position)
        distance = direction.get_norme()
        if distance == 0:
            return Vector(0, 0, 0)

        #algo de Barnes-Hut pour calculer la force
        theta = self.size / distance
        if theta < 1:
            #approximation de Barnes-Hut
            force =  direction * self.total_mass / (distance ** 3)
            
        else:
            force = self.calculate_direct_methode_force(star)
            

        return force
    def equi(self):
        first_octtree=self.head
        while first_octtree.head != None:
            first_octtree = first_octtree.head
        pere = self.head
        #print(pere.children)
        
        if pere.children.count(None) == 7:
            #print("in",pere)
            
            #index = pere.children.index(pere)
            #pere.head.children[index]=None
            etoileTemp=None
            for child in pere.children:
                if child ==None:
                    continue
                if len(child.stars)!=0:
                    for etoile in child.stars:
                        etoileTemp=etoile
                        print(etoile)
            if etoileTemp != None:
                first_octtree.insert_star(etoileTemp)
            if pere.head!=None:
                pere.head.equi()
            else:
                return
        elif pere.children.count(None) == 8:
            index = pere.head.children.index(pere)
            pere.head.children[index]=None
            pere.head.equi()
        
        else : return
        
    def calculate_direct_methode_force(self, star):
        # Calcule la force d'attraction gravitationnelle directe entre l'étoile et cet octree
        direction = self.center - Vector(*star.position)
        distance = direction.get_norme()
        if distance == 0:
            return Vector(0, 0, 0)  # Éviter une division par zéro
        force = ( direction * float(self.total_mass) ) / (distance ** 3)
        return force
    def finalize(self):
        print(self,"detruit")
        self=None
    def star_inside(self):
        x,y,z = get_first_non_none_element(self.stars).position
        center = self.center
        size = self.size
        return center-size <= x <= size+center and center-size <= y <= size+center and center-size <= z <= size+center
    
def get_first_non_none_element(my_list):
    for element in my_list:
        if element is not None:
            return element
    return None