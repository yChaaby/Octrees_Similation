import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
#nothing special
class Octree:
    def __init__(self, center, size, num_stars):
        self.center = center
        self.size = size
        self.num_stars = num_stars
        self.children = []

def draw_octree_from_repr(ax, octree_repr):
    # Draw the octree and its children
    draw_octree(ax, octree_repr)

def draw_octree(ax, octree_repr):
    if octree_repr is not None:
        # Draw the boundaries of the current cube
        draw_boundary(ax, octree_repr.center, octree_repr.size)

        # Recursion for the children
        for child_repr in octree_repr.children:
            draw_octree(ax, child_repr)

def draw_boundary(ax, center, size):
    # Extract cube vertices from octree information
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

    # Define cube faces using vertices
    faces = [
        [vertices[0], vertices[1], vertices[2], vertices[3]],
        [vertices[4], vertices[5], vertices[6], vertices[7]],
        [vertices[0], vertices[1], vertices[5], vertices[4]],
        [vertices[2], vertices[3], vertices[7], vertices[6]],
        [vertices[1], vertices[2], vertices[6], vertices[5]],
        [vertices[0], vertices[3], vertices[7], vertices[4]]
    ]

    # Draw the cube boundary
    cube_boundary = Poly3DCollection(faces, edgecolor='blue', alpha=0.1)
    ax.add_collection3d(cube_boundary)

    # Adjust axis limits
    ax.set_xlim((center[0] - size, center[0] + size))
    ax.set_ylim((center[1] - size, center[1] + size))
    ax.set_zlim((center[2] - size, center[2] + size))

# Example usage
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Example octree representation
octree_repr = Octree(center=(0, 0, 0), size=200.0, num_stars=0)
octree_repr.children = [
    Octree(center=(-100, -100, -100), size=100.0, num_stars=1),
    Octree(center=(100, -100, -100), size=100.0, num_stars=1),
    Octree(center=(100, 100, -100), size=100.0, num_stars=0),
    # ... add more children as needed
]

draw_octree_from_repr(ax, octree_repr)
plt.show()
