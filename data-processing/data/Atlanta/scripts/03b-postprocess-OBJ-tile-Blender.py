import bpy
import os
import mathutils
import math
import sys
# import nvector as nv
# nv.test(coverage=True, doctests=True)

print()
print("==========================================")
print("This is Blender Python script that post-processes the OBJ file obtained through osm2world")
print("Author Sinisa Kolaric")
print()

argv = sys.argv
argv = argv[argv.index("--") + 1:]  # get all args after "--" 

print("Passed-in arguments: ")
print(argv)  # should be ['-84.360000', '33.740000', '-84.340000', '33.760000']

# See: https://microem.ru/files/2012/08/GPS.G1-X-00006.pdf
a = 6378137
f = 0.00335281066 #1/298.257223563
b = 6356752.31424518 # a*(1-f)
e  = math.sqrt((a*a - b*b)/(a*a))
e2 = math.sqrt((a*a - b*b)/(b*b))
def WGS84_to_ECEF(lon, lat, alt):
    N = a/math.sqrt( 1 - e*e*math.sin(lat)*math.sin(lat) )
    x = ( N + alt ) * math.cos(lat) * math.cos(lon)
    y = ( N + alt ) * math.cos(lat) * math.sin(lon)
    z = ( ((b*b)/(a*a)) * N + alt ) * math.sin(lat)
    return x, y, z

    
# full_path_to_import_file = "..\\derived-data\\buildings " + argv[0] + ", " + argv[1] + ", " + argv[2] + ", " + argv[3] + ".osm.obj";
full_path_to_import_file = "..\\tileset-3d\\tile-buildings(" + argv[0] + "," + argv[1] + "," + argv[2] + "," + argv[3] + ").osm.obj";
print("Full path to import file: ", full_path_to_import_file)

tile_west_deg  = float(argv[0])
tile_south_deg = float(argv[1])
tile_east_deg  = float(argv[2])
tile_north_deg = float(argv[3])
tile_west_rad  = tile_west_deg * math.pi / 180.0;
tile_south_rad = tile_south_deg * math.pi / 180.0;
tile_east_rad  = tile_east_deg * math.pi / 180.0;
tile_north_rad = tile_north_deg * math.pi / 180.0;

tile_center_LON_deg = (tile_west_deg + tile_east_deg) / 2.0;
tile_center_LAT_deg = (tile_south_deg + tile_north_deg) / 2.0;
tile_center_LON_rad = (tile_west_rad + tile_east_rad) / 2.0;
tile_center_LAT_rad = (tile_south_rad + tile_north_rad) / 2.0;

# Notes:
# x) osm2world exports OBJ with origin at the center of export bounding box: O = (W+E)/2, (S+N)/2
# x) however, b3dm files must have coordinates in ECEF
# x) thus, all vertices in the OBJ export must be translated by vector O
####################################################################################
####################################################################################
tile_center_ECEF    = WGS84_to_ECEF(tile_center_LON_rad, tile_center_LAT_rad, 0.0) # returns x, y, z
####################################################################################
####################################################################################

bpy.ops.import_scene.obj(filepath=full_path_to_import_file)

# make sure to get all imported objects
obj_objects = bpy.context.selected_objects[:]

print("Count of selected objects (bpy.context.selected_objects): ", len(bpy.context.selected_objects))

# ######################################################################
# # create the BLUE material (transparent)
# polygonMaterial = bpy.data.materials.new('polygonMaterial')
# polygonMaterial.diffuse_color = (0.3, 0.3, 1.0) # (0.99, 0.0, 0.0)
# polygonMaterial.diffuse_shader = 'LAMBERT'
# polygonMaterial.diffuse_intensity = 0.99
# # polygonMaterial.specular_color = (0.0, 0.0, 0.99)
# # polygonMaterial.specular_shader = 'COOKTORR'
# # polygonMaterial.specular_intensity = 0.5
# polygonMaterial.alpha = 0.50
# polygonMaterial.ambient = 0.5

######################################################################
# create the SLIGHTLY BLUE material (transparent)
polygonMaterial = bpy.data.materials.new('polygonMaterial')
polygonMaterial.diffuse_color = (0.9, 0.9, 1.0) # (0.99, 0.0, 0.0)
polygonMaterial.diffuse_shader = 'LAMBERT'
polygonMaterial.diffuse_intensity = 1.0
polygonMaterial.specular_color = (1.0, 1.0, 1.0)
polygonMaterial.specular_shader = 'COOKTORR'
polygonMaterial.specular_intensity = 0.5
polygonMaterial.alpha = 0.5
polygonMaterial.ambient = 1.0


# ######################################################################
# # create the WHITE material (transparent)
# polygonMaterial = bpy.data.materials.new('polygonMaterial')
# polygonMaterial.diffuse_color = (1.0, 1.0, 1.0) # (0.99, 0.0, 0.0)
# polygonMaterial.diffuse_shader = 'LAMBERT'
# polygonMaterial.diffuse_intensity = 0.99
# # polygonMaterial.specular_color = (0.0, 0.0, 0.99)
# # polygonMaterial.specular_shader = 'COOKTORR'
# # polygonMaterial.specular_intensity = 0.5
# polygonMaterial.alpha = 0.60
# polygonMaterial.ambient = 0.5


# # get the current path and make a new folder for the exported meshes
# per_obj_export_path = bpy.path.abspath('..//derived-data//per-building/')
# if not os.path.exists(per_obj_export_path):
    # os.makedirs(per_obj_export_path)

i=0

# iterate through all objects
for obj in obj_objects:

    # SK: loc, rot, scale = bpy.context.object.matrix_world.decompose()
    # print the name of the current obj
    # print("==== obj.name: ", obj.name, ", object type: ", obj.type, ", index: ", i)
    i = i+1
    # print ("    obj.dimensions: ", obj.dimensions)
    # print ("    obj.location.x: ", obj.location.x)
    # print ("    obj.location: ", obj.location)
    # print ("    obj.matrix_world: ", obj.matrix_world)
    # print ("    obj.matrix_world.to_translation: ", obj.matrix_world.to_translation)
    # print ("    obj.matrix_local.to_translation: ", obj.matrix_local.to_translation)
    # print ("    obj.rotation_euler: ", obj.rotation_euler)
    # print ("    object.matrix_world.to_euler('XYZ'): ", obj.matrix_world.to_euler('XYZ'))
    
    # set current object to the active one
    bpy.context.scene.objects.active = obj

    # get the generated material
    polygonMaterial = bpy.data.materials['polygonMaterial']

    # if a material exists overwrite it
    if len(obj.data.materials):
        # assign to 1st material slot
        obj.data.materials[0] = polygonMaterial
    # if there is no material append it
    else:
        obj.data.materials.append(polygonMaterial)

    # for face in obj.data.tessfaces: # Iterate over all faces
        # face.material_index = 0
    for poly in obj.data.polygons: # Iterate over all polygons
        #if poly.select:
        poly.material_index = 0
        

    # mesh = obj.data
    # print ("    len(obj.data.vertices): ", len(mesh.vertices))
    # lx = [] # list of objects x locations
    # ly = [] # list of objects y locations
    # lz = [] # list of objects z locations 
    # for v in mesh.vertices:
        # v.co.x = v.co.x + tile_center_ECEF[0]
        # v.co.y = v.co.y + tile_center_ECEF[1]
        # v.co.z = v.co.z + tile_center_ECEF[2]
        # lx.append(v.co.x)
        # ly.append(v.co.y)
        # lz.append(v.co.z)
    # bb_west = min(lx)
    # bb_south = min(lz)
    # bb_east = max(lx)
    # bb_north = max(lz)
    # bb_bottom = min(ly)
    # bb_top = max(ly)
    # print ("    BB(west, south, east, north, bottom, top): ", bb_west, bb_south, bb_east, bb_north, bb_bottom, bb_top)
        
    # # deselect all meshes
    # bpy.ops.object.select_all(action='DESELECT')

    # # select the object
    # obj.select = True
    # #bpy.context.scene.objects.active = obj

    # # export object with its name as OBJ file name
    # fPath = str((per_obj_export_path + obj.name + '.obj'))
    # print("Export path: ", fPath)
    # bpy.ops.export_scene.obj(filepath=fPath, use_selection=True)


bpy.ops.object.select_all(action='SELECT')
# make sure to get all imported objects
# obj_objects = bpy.context.selected_objects[:]    
       
print()       
print("Count of selected objects, len(obj_objects): ", len(obj_objects))
print()

full_path_to_export_file = "..\\tileset-3d\\tile-buildings(" + argv[0] + "," + argv[1] + "," + argv[2] + "," + argv[3] + ").osm.obj.postprocessed.obj";
print("Full path to export file: ", full_path_to_export_file)

if (len(obj_objects) > 0):
    print("len(obj_objects) is greater than zero, so export the post-processed scene (i.e., objects in it) to Wavefront OBJ")
    bpy.ops.export_scene.obj(filepath=full_path_to_export_file)
    print()
    print("A total of ", len(obj_objects), " objects have been exported to Wavefront OBJ")
else:
    print("len(obj_objects) equals zero, so create an empty (0-length) export file, to prevent the default export into it (a cube)")
    open(full_path_to_export_file, 'w').close()
    print()
    print("An empty export file to Wavefront OBJ has been created")

print("Export file: ", full_path_to_export_file)
statinfo = os.stat(full_path_to_export_file)
print("Export file size (bytes): ", "{:,}".format(statinfo.st_size))

print()
print("Tile processed:")
print("---------------")
print("  west  (deg, rad):", tile_west_deg, tile_west_rad)
print("  south (deg, rad):", tile_south_deg, tile_south_rad)
print("  east  (deg, rad):", tile_east_deg, tile_east_rad)
print("  north (deg, rad):", tile_north_deg, tile_north_rad)
print("---------------")
print("  extent LON (deg, rad):", tile_east_deg - tile_west_deg, tile_east_rad - tile_west_rad)
print("  extent LAT (deg, rad):", tile_north_deg - tile_south_deg, tile_north_rad - tile_south_rad)
print("---------------")
print("  center LON (deg, rad):", tile_center_LON_deg, tile_center_LON_rad)
print("  center LAT (deg, rad):", tile_center_LAT_deg, tile_center_LAT_rad)
print("  center ECEF (x, y, z):", WGS84_to_ECEF(tile_center_LON_rad, tile_center_LAT_rad, 0.0))
print("  tile_center_ECEF (x, y, z):", tile_center_ECEF)
