import open3d as o3d
import numpy as np
import copy

class ARAPGUI:
    def __init__(self,mesh,static_ids,static_pos):
        self.mesh_og = copy.deepcopy(mesh)
        self.mesh = mesh
        self.static_ids = static_ids
        self.static_pos = static_pos
        self.vis = o3d.visualization.VisualizerWithVertexSelection()
        self.vis.create_window()
        self.vis.add_geometry(self.mesh)
        # self.vis.register_selection_moving_callback(self.selection_moving_callback)
        self.vis.register_selection_moved_callback(self.selection_moved_callback)
        self.vis.run()  
        self.vis.destroy_window()

    def selection_moving_callback(self):
        selection = self.vis.get_picked_points()
        for point in selection:
            if point.index not in self.static_ids:
                self.mesh.vertices[point.index] = point.coord
        self.vis.update_geometry(None)
    
    def selection_moved_callback(self):
        selection = self.vis.get_picked_points()
        handle_ids = []
        handle_pos = []
        print("num of points selected ::: ",len(selection))
        for point in selection:
            # if point.index not in self.static_ids:
            handle_ids.append(point.index)
            handle_pos.append(point.coord)
        constraint_ids = o3d.utility.IntVector(self.static_ids + handle_ids)
        constraint_pos = o3d.utility.Vector3dVector(self.static_pos + handle_pos)
        mesh_prime = self.mesh_og.deform_as_rigid_as_possible(constraint_ids,constraint_pos,max_iter=50)
        for idx in range(len(self.mesh.vertices)):
                self.mesh.vertices[idx] = mesh_prime.vertices[idx]
        # o3d.visualization.draw_geometries([mesh_prime])
        self.mesh_og = copy.deepcopy(mesh_prime)
        self.vis.update_geometry(None)
        o3d.io.write_triangle_mesh("edited.obj", self.mesh)


# Change this id to select a new mesh
# in the below folders
mesh_id = "13"

# You don't need to change these unless
# the data is in different folders
data_path = "./vases4/"
segmentation_folder_path = data_path + "gt/"
off_folder_path =  data_path + "shapes/"

# Most certainly you don't need to change these 
# lines ever
segmentation_file_path = segmentation_folder_path + mesh_id + ".seg"
off_file_path = off_folder_path + mesh_id + ".off"

# Load the .off file
mesh = o3d.io.read_triangle_mesh(off_file_path)

# Read the file
with open(segmentation_file_path, 'r') as file:
    lines = file.readlines()

# Store segmentation data in a NumPy array
data = np.array([int(line.strip()) for line in lines])
print("Available segment ids in this object file :", np.unique(data))

# This is for coloring and viz
segementation_dict = {}
for segment in np.unique(data):
    segementation_dict[segment] = [0,0,0]
# segementation_dict = {1:[0,0,0],2:[0,0,0],3:[0,0,0],4:[0,0,0],5:[0,0,0]}

seg_id = int(input("Please select a valid segmentation id :  "))

segementation_dict[seg_id] = [0,0,1]
# print(segementation_dict)

# Create a color map for the mesh
colors = np.zeros((len(mesh.vertices), 3))  # Initialize with zeros
for triangle_id in range(len(mesh.triangles)):
    # Set the color for vertices of the specified triangle ID
    vertex_indices = mesh.triangles[triangle_id].tolist()
    colors[vertex_indices] = segementation_dict[data[triangle_id]]

# Assign the colors to the mesh
mesh.vertex_colors = o3d.utility.Vector3dVector(colors)

## Deformation
static_ids = set()
for key, value in segementation_dict.items():
    if not sum(value):
        handle_face_ids = np.where(data == key)[0].tolist()
        handle_vertex_ids = set()
        for triangle_id in handle_face_ids:
            vertex_indices = mesh.triangles[triangle_id].tolist()
            handle_vertex_ids.update(vertex_indices)
        static_ids = static_ids | handle_vertex_ids

static_ids = list(static_ids)
static_pos = []
vertices = np.asarray(mesh.vertices)
for id in static_ids:
    static_pos.append(vertices[id])


loaded_gui = ARAPGUI(mesh,static_ids,static_pos)

