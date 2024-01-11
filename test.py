import random as rnd
import numpy as np
import matplotlib.pyplot as plt
from collections import deque
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation
import matplotlib.patches as patches

class CONSTANTSCLASS():
    # USEFULL CONFIGURATIONS(JUST FOR EXAMPLE):
    
    # FOR QUAD TREE RECTANGULAR VIEW(2D):
    # DIMENSION=2
    # SIMULATION_ON=False
    # QUADTREE_THRESHOLD=4
    # MAX_NUMBER_OF_SMALL_OBJECTS=20
    # SIMULATION_OPTION="R" OR "S"
    # QUADTREE_MAXIMUM_DEPTH=4
    # NOTE: DIMENSION MUST BE 2 TILL YOU SEE THE SECTIONING. 
    # NOTE: IN 3D, STILL QUADTREE STRUCTURE IS BEING USED. 
    # BUT THE CUBIC VIEW IS NOT SET
    #/////////////////////////////////////////////////////////////
    
    
    # FOR SOLAR SYSTEM 2D: 
    # SIMULATION_OPTION="S"
    # QUADTREE_THRESHOLD=40
    # DIMENSION=2
    # SOLAR_MAX_POSITION=1.5e12 
    # TILL SATURN EASIER TO WATCH
    # NOTE: THE SOLAR SYSTEM 3D IS NOT READY. THERE IS NO INCLINATION ANGLE DEFINED
    # //////////////////////////////////////////////////////////////
    
    # FOR 2D RANDOM OBJECTS
    # SIMULATION_OPTION="R"
    # QUADTREE_THRESHOLD=60
    # MAX_NUMBER_OF_SMALL_OBJECTS=40
    # MAX_NUMBER_OF_STARS=1
    # DIMENSION=2
    #////////////////////////////////////////////////////////////////
    
    # FOR 3D RANDOM OBJECTS
    # SIMULATION_OPTION="R"
    # QUADTREE_THRESHOLD=60
    # MAX_NUMBER_OF_SMALL_OBJECTS=40
    # MAX_NUMBER_OF_STARS=1
    # DIMENSION=3
    #/////////////////////////////////////////////////////////////////
    
    # General Random Objects Settings:
    MAX_NUMBER_OF_SMALL_OBJECTS=50
    MAX_NUMBER_OF_STARS=1
    MAX_MASS=1.0e26
    STAR_MASS=MAX_MASS*2.0e10
    MIN_MASS=MAX_MASS/100
    MAX_POSITION=5.0e+13
    MIN_POSITION=-MAX_POSITION
    POSITION_SCALE=0.9
    
    # Initial Velocity Settings:
    INITIAL_VELOCITY_FACTOR=1
    STAR_INITIAL_VELOCITY_FACTOR=0.01
    
    # Gravitational Constant and Universal change of time for every animation interval:
    G=6.67e-11
    DT=86400.0
    
    # Simulation and View Settings
    SIMULATION_ON=True
    SIMULATION_OPTION="S" # Values: R => RANDOM, S => SOLAR SYSTEM
    MAX_GRAPHICAL_SIZE=20
    MIN_GRAPHICAL_SIZE=3
    ANIMATION_INTERVAL=150
    
    # QuadTree Settings
    QUADTREE_THRESHOLD=60
    QUADTREE_MAXIMUM_DEPTH=4

    #Available Dimensions: 2,3
    #QuadTree Sectioning View only can be seen with 2D Simulation
    #QuadTree Sectioning can still function with 3D
    DIMENSION=2
    
    # SOLAR SYSTEM Settings
    EARTH_MASS=5.9736e+24 #Kg
    EARTH_ORBIT=1.5e+11 #m
    SOLAR_DT=86400.0
    SOLAR_MAX_POSITION=1.5e12
    SOLAR_OBJECTS_ORBIT=np.array([1.0e-4, 0.4, 0.7, 1., 1.5, 2.77, 5.2, 10, 19, 30, 39.5])
    SOLAR_OBJECTS_MASS=np.array([333000.0, 0.0553, 0.815, 1., 0.107, 0.000157, 317.83, 95.162, 14.536, 17.147, 0.0022])
    SOLAR_OBJECTS_NAMES=[ 'Sun', 'Mercury', 'Venus', 'Earth', 'Mars', 'Ceres', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto']
    
    #Constant Function to calculate the magnitude of vectors
    def MAGNITUDE(self,np_arr):
        return np.sqrt(np_arr.dot(np_arr))
    
    #Constant function to calculate the incoming force from an object
    def GFORCE(self,del_r,mass):
        threshold=1
        if not np.all(np.abs(del_r)>threshold):
            return 0.
        else:
            f=CONSTANTS.G*mass*del_r/(CONSTANTS.MAGNITUDE(del_r)**3)
            return f

#Creating Constant Object for easy use:    
CONSTANTS=CONSTANTSCLASS()
    
class SkyObject():
    def __init__(self,r,mass,name="NONE"):
        self.r=r
        if name=="NONE":
            self.name=str(int(mass/CONSTANTS.MIN_MASS))
        else:
            self.name=name
        self.v=np.zeros(CONSTANTS.DIMENSION)
        self.a=np.zeros(CONSTANTS.DIMENSION)
        self.mass=mass
    
    #Leap frog formulation through update states
    def updateStats(self):
        self.v+=self.a*CONSTANTS.DT
        self.r+=self.v*CONSTANTS.DT  
    
    def __repr__(self):
        s0="Name: "+self.name
        s1=", r: "+str(self.r)
        s2=", v_mag: "+str(CONSTANTS.MAGNITUDE(self.v))
        s3=", a_mag: "+str(CONSTANTS.MAGNITUDE(self.a))
        return s0+s1+s2+s3

class Node():
    def __init__(self,r,size,depth):
        self.r=r
        self.size=size
        self.objects=[]
        self.children=[]
        self.RM=np.zeros(CONSTANTS.DIMENSION)
        self.totalMass=0.
        self.__depth=depth
    
    #for every dimension there must be two position with half size.
    #recursive function so that it could be usable with both 3D and 2D
    def splitHelper(self,dimension,pos,size):
        if dimension<CONSTANTS.DIMENSION:
            hSize=self.size[dimension]/2
            size[dimension]=hSize
            
            pos[dimension]=self.r[dimension]
            self.splitHelper(dimension+1,pos,size)
            
            pos[dimension]=self.r[dimension]+hSize
            self.splitHelper(dimension+1,pos,size)
        else:
            self.children.append(Node(np.array(pos),np.array(size),self.__depth+1))

    def split(self):
        if len(self.children)==0:
            dimension=0
            pos=np.zeros(CONSTANTS.DIMENSION)
            size=np.zeros(CONSTANTS.DIMENSION)
            self.splitHelper(dimension, pos, size)
            newobj=[]
            for obj in self.objects:
                newobj.append(obj)
            del self.objects[:]
            for obj in newobj:
                self.insert(obj)
                
    #gives the area of the new node for certain dimension  
    #for overal area evaluation this must be looped over all dimensions.    
    def getAreaHelper(self,r_dim,dimension):
        if r_dim>=self.r[dimension] and r_dim<self.r[dimension]+self.size[dimension]:
            hSize=self.size[dimension]/2
            if r_dim<self.r[dimension]+hSize:
                return 0
            else:
                return 1
        else:
            return -1
    #gives the area in which the node or object must be inserted 
    def getArea(self,r):
        if len(self.children)>0:
            ar=0
            for d in range(CONSTANTS.DIMENSION):
                area_part=self.getAreaHelper(r[d],d)
                if area_part!=0 and area_part!=1:
                    return -1
                else:
                    ar=ar*2+area_part
            return ar         
        return -1
    
    def getCOM(self):
        rmdata=self.calRM()
        return rmdata[1]/rmdata[0]
    
    #Calculates the sum of r*mass 
    def calRM(self):
        self.RM=np.zeros(CONSTANTS.DIMENSION)
        self.totalMass=0
        if len(self.children)>0:
            for child in self.children:
                chdata=child.calRM()
                if chdata[0]>0:
                    self.totalMass+=chdata[0]
                    self.RM+=chdata[1]
        elif len(self.objects)>0:
            if len(self.objects)>1:
                for obj in self.objects:
                    obj.updateStats()
                    self.totalMass+=obj.mass
                    self.RM+=obj.r*obj.mass
            else:
                self.totalMass=self.objects[0].mass
                self.RM=self.objects[0].r
        return [self.totalMass,self.RM]
    
    #Inserts the new object to the node. if this node has less than
    # 4 objects and no children then this object would be added to 
    # objects list. Otherwise, the object would be passed to the respective
    # child node to be inserted.
    def insert(self,skyobject):
        if self.inBoundary(skyobject.r):
            if len(self.children)==0 and len(self.objects)==CONSTANTS.QUADTREE_THRESHOLD:
                if self.__depth<CONSTANTS.QUADTREE_MAXIMUM_DEPTH:
                    self.split()
                else:
                    print("The Maximum Depth Has Been Filled. This Object Cannot Be Inserted: "+str(skyobject))
                    return 
            area=self.getArea(skyobject.r)
            if area>=0:  
                self.children[area].insert(skyobject)
            else:
                self.objects.append(skyobject)
        else:
            print("Object Out of Area and Not Inserted: "+str(skyobject))
            print("Node Depth: "+str(self.__depth))
    
    #check if the input coordinates are within the node area.
    def inBoundary(self,r):
        if np.all(r>=self.r) and np.all(r<self.r+self.size):
            return True
        else:
            return False
    def __repr__(self):
        return "Offset: "+str(self.r)+", Size: "+str(self.size)+", Depth: "+str(self.__depth)

class QuadTree():
    def __init__(self,objects):
        self.totalMass=0
        self.createRoot(objects)
        print("Total Mass: "+str(self.totalMass))
        print("COM r: "+str(self.COM))
        self.initializeVelocity(objects)
        self.createTree(objects)
        self._stack=deque()
        self.root.calRM()
    
    #uses the calculated Center of Mass to evaluate an initial velocity for the objects
    # over the center of mass. 
    def initializeVelocity(self,objects):
        for obj in objects:
            del_r=obj.r-self.COM
            ang_0=np.arctan(del_r[1]/del_r[0])
            if del_r[0]<0:
                ang_0+=np.pi
            v_size=np.sqrt(CONSTANTS.G*(self.totalMass-obj.mass)/CONSTANTS.MAGNITUDE(del_r))
            v_x=-v_size*np.sin(ang_0)
            v_y=v_size*np.cos(ang_0)
            
            v_0=[v_x,v_y]
            if CONSTANTS.DIMENSION==3:
                v_0.append(0)
            obj.v+=np.array(v_0)*CONSTANTS.INITIAL_VELOCITY_FACTOR
            if obj.mass==CONSTANTS.STAR_MASS or (CONSTANTS.SIMULATION_OPTION=="S" and obj.mass==CONSTANTS.SOLAR_OBJECTS_MASS[0]*CONSTANTS.EARTH_MASS):
                obj.v*=CONSTANTS.STAR_INITIAL_VELOCITY_FACTOR
                
    #Creates the root node for the Quad Tree
    def createRoot(self,objects):
        rm=np.zeros(CONSTANTS.DIMENSION)
        for obj in objects:
            self.totalMass+=obj.mass
            rm+=obj.mass*obj.r
        self.COM = rm/self.totalMass
        fsize=(CONSTANTS.MAX_POSITION-CONSTANTS.MIN_POSITION)
        self.root=Node(np.array([CONSTANTS.MIN_POSITION for i in range(CONSTANTS.DIMENSION)]),np.array([fsize for i in range(CONSTANTS.DIMENSION)]),0)
    
    #updates the acceleration within every object inside quad tree.
    #the simulation happens with two steps:
    # 1. update the acceleration for every object first
    # 2. update their respective velocity and position
    def gravityUpdate(self,node,parent_force):
        if node.totalMass==0:
            return 
        if len(node.objects)>0:
            for idx,obj in enumerate(node.objects):
                obj.a=np.zeros(CONSTANTS.DIMENSION)
                for jdx,other in enumerate(node.objects):
                    if idx!=jdx:
                        obj.a+=CONSTANTS.GFORCE(other.r-obj.r,other.mass)
                #print("Parent a: "+str(parent_force))
                #print("Object a Till now: "+str(obj.a))
                obj.a+=parent_force
        elif len(node.children)>0:
            for idx,focus in enumerate(node.children):
                if focus.totalMass!=0:
                    f=np.zeros(CONSTANTS.DIMENSION)
                    focusCOM=focus.RM/focus.totalMass
                    for jdx,other in enumerate(node.children):
                        if idx!=jdx and other.totalMass!=0:
                            otherCOM=other.RM/other.totalMass
                            f+=CONSTANTS.GFORCE(otherCOM-focusCOM,other.totalMass)
                    self.gravityUpdate(focus,f+parent_force)
    
    #update tree is the function to be called from outside of class 
    # to update the tree in every frame.
    def updateTree(self):
        self.gravityUpdate(self.root, np.zeros(CONSTANTS.DIMENSION))
        self.COM=self.root.getCOM()
        print("New COM: "+str(self.COM))
        print("/////////////End Frame///////////////")
        
    def createTree(self,objects):
        for obj in objects:
            self.root.insert(obj)
    
    #as there is no list structure to save the data, there must be 
    #recursive stacking functions to stack the nodes or objects for 
    #output.  
    def stackNodes(self,node):
        self._stack.append(node)
        if len(node.children)>0:
            for child in node.children:
                self.stackNodes(child)
                
    def stackSkyObjects(self,node):
        if len(node.children)>0:
            for child in node.children:
                self.stackSkyObjects(child)
        elif len(node.objects)>0:
            for obj in node.objects:
                self._stack.append(obj)
        

class QuadTreeDraw():
    def __init__(self,quad_tree):  
        self.quad_tree=quad_tree
        if CONSTANTS.DIMENSION==3:
            self.fig = plt.figure(figsize=(10,10))
        else: 
            self.fig=plt.figure()
        plt.axes()
        plt.title("QuadTree")
        #not CONSTANTS.SIMULATION_ON and
        if CONSTANTS.DIMENSION==2:
            ax2=self.fig.add_subplot(111)
            self.quad_tree.stackNodes(self.quad_tree.root)
            for node in self.quad_tree._stack:
                #print(node)
                if len(node.children)>0 or len(node.objects)>0:
                    plt.gca().add_patch(patches.Rectangle((node.r[0], node.r[1]),node.size[0],node.size[1],fill=False,zorder=0)) 
            ax2.axis('scaled')
        self.quad_tree._stack.clear()
        self.quad_tree.stackSkyObjects(self.quad_tree.root)
        self.r=[]
        for i in range(CONSTANTS.DIMENSION):
            self.r.append([])
        self.names=[]
        self.mass=[]
        
        for obj in self.quad_tree._stack:
            for i,pos in enumerate(obj.r):
                self.r[i].append(pos)
            self.mass.append(obj.mass)
            self.names.append(obj.name)
        
        if CONSTANTS.DIMENSION==3:
            self.ax=self.fig.add_subplot(111, projection='3d')
        else:
            self.ax=self.fig.add_subplot(111)
        
        # setting colors for objects with respect to their mass.
        self.norm = plt.Normalize(1,4)
        self.cmap=plt.cm.Spectral
        self.colors=[1*item/CONSTANTS.MAX_MASS for item in self.mass]
        self.maxmass=max(self.mass)
        
        # set the hover effect:
        self.annot = self.ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",bbox=dict(boxstyle="round", fc="w"),arrowprops=dict(arrowstyle="->"))
        self.annot.set_visible(False)
        self.fig.canvas.mpl_connect("motion_notify_event", self.hover)
        
        # depending on the Dimension choice, scattering happens.
        if CONSTANTS.DIMENSION==3:
            self.sc = self.ax.scatter(self.r[0],self.r[1],self.r[2],c=self.colors, s=CONSTANTS.MIN_GRAPHICAL_SIZE+CONSTANTS.MAX_GRAPHICAL_SIZE*np.array(self.mass)/self.maxmass, cmap=self.cmap, norm=self.norm,zorder=7)
        else:
            self.sc = self.ax.scatter(self.r[0],self.r[1],c=self.colors, s=CONSTANTS.MIN_GRAPHICAL_SIZE+CONSTANTS.MAX_GRAPHICAL_SIZE*np.array(self.mass)/self.maxmass, cmap=self.cmap, norm=self.norm,zorder=7)
        if CONSTANTS.SIMULATION_ON:
            anim = matplotlib.animation.FuncAnimation(self.fig, self.animate, 19, interval=CONSTANTS.ANIMATION_INTERVAL, blit=False)
            
        plt.show()

    #needed hovering functions:
    def updateAnnotation(self,ind):
        pos = self.sc.get_offsets()[ind["ind"][0]]
        self.annot.xy = pos
        text = "{}".format(" ".join([str(self.names[n]) for n in ind["ind"]]))
        self.annot.set_text(text)
        self.annot.get_bbox_patch().set_facecolor(self.cmap(self.norm(self.mass[ind["ind"][0]])))
        self.annot.get_bbox_patch().set_alpha(0.4) 
    
    def hover(self,event):
        vis = self.annot.get_visible()
        if event.inaxes == self.ax:
            cont, ind = self.sc.contains(event)
            if cont:
                self.updateAnnotation(ind)
                self.annot.set_visible(True)
                self.fig.canvas.draw_idle()
            else:
                if vis:
                    self.annot.set_visible(False)
                    self.fig.canvas.draw_idle()
    
    #animate function: calls upon the tree update function and gets the 
    # new coordinates of every object with stacks.
    def animate(self,i):
        self.quad_tree.updateTree()
        self.quad_tree._stack.clear()
        self.quad_tree.stackSkyObjects(self.quad_tree.root)
        newOffsets=[]
        if CONSTANTS.DIMENSION==3:
            for i in range(CONSTANTS.DIMENSION):
                newOffsets.append([])
            for obj in self.quad_tree._stack:
                for i,pos in enumerate(obj.r):
                    newOffsets[i].append(pos)
                print(obj)
        else:
            for obj in self.quad_tree._stack:
                newOffsets.append(obj.r)
        if CONSTANTS.DIMENSION==3:
            self.sc._offsets3d=(newOffsets[0],newOffsets[1],newOffsets[2])
        else:
            self.sc.set_offsets(newOffsets)
        return self.sc

#creates all of the objects needed for simulation. 
# only options valid: R , S
def getObjects():
    objects=[]   
            
    if CONSTANTS.SIMULATION_OPTION=="R":
        for counter in range(CONSTANTS.MAX_NUMBER_OF_STARS):
            pos=np.array([rnd.randint(CONSTANTS.MIN_POSITION,CONSTANTS.MAX_POSITION)*CONSTANTS.POSITION_SCALE**4+0. for i in range(CONSTANTS.DIMENSION)])
            m=CONSTANTS.STAR_MASS+0.
            objects.append(SkyObject(pos,m))
        
        for number in range(CONSTANTS.MAX_NUMBER_OF_SMALL_OBJECTS):
            pos=np.array([rnd.randint(CONSTANTS.MIN_POSITION,CONSTANTS.MAX_POSITION)*CONSTANTS.POSITION_SCALE+0. for i in range(CONSTANTS.DIMENSION)])
            m= rnd.randint(CONSTANTS.MIN_MASS,CONSTANTS.MAX_MASS)+0.
            objects.append(SkyObject(pos,m))  
            
    elif CONSTANTS.SIMULATION_OPTION=="S":
        CONSTANTS.MIN_MASS=min(CONSTANTS.SOLAR_OBJECTS_MASS)*CONSTANTS.EARTH_MASS
        CONSTANTS.MAX_POSITION=CONSTANTS.SOLAR_MAX_POSITION
        CONSTANTS.MIN_POSITION=-CONSTANTS.MAX_POSITION
        CONSTANTS.DT=CONSTANTS.SOLAR_DT
        CONSTANTS.ANIMATION_INTERVAL=50
        for idx in range(len(CONSTANTS.SOLAR_OBJECTS_MASS)):
            ang_0=1.0+rnd.random()*2*np.pi
            r=CONSTANTS.EARTH_ORBIT*CONSTANTS.SOLAR_OBJECTS_ORBIT[idx]
            pos_0=[r*np.cos(ang_0),r*np.sin(ang_0)]
            #pos_0=[r,0.]
            if CONSTANTS.DIMENSION==3:
                pos_0.append(0.)
            pos=np.array(pos_0)
            m= CONSTANTS.EARTH_MASS*CONSTANTS.SOLAR_OBJECTS_MASS[idx]
            objects.append(SkyObject(pos,m,CONSTANTS.SOLAR_OBJECTS_NAMES[idx]))
        
    return objects

def main():
    skyobjects=getObjects()
    quad_tree=QuadTree(skyobjects)
    QuadTreeDraw(quad_tree)

if __name__ == '__main__':
    main()