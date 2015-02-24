""" Based on Jim McCann's export script:
	https://github.com/ixchow/ldfw/blob/master/tools/blend-to-js.py
"""
import bpy
import sys

objectName = None
for i in range(0, len(sys.argv)):
	if sys.argv[i] == '--':
		if len(sys.argv) == i + 2:
			objectName = sys.argv[i+1]

# Ensure proper argument usage
if objectName == None:
	print("Please pass '-- <objectToPrint>' after the script name", file=sys.stderr)
	bpy.ops.wm.quit_blender()

def printPoint(pt):
	x = str(pt[0]);
	y = str(pt[1]);
	z = str(pt[2]);

	print("  Point: (" + x + ", " + y + ", " + z + ")");
				
#Write a mesh with just position:
def printMesh(obj):
	print("Printing mesh " + str(objectName));

	bpy.ops.object.mode_set(mode='OBJECT')
	obj.data = obj.data.copy() #"make single user" (?)
	bpy.context.scene.layers = obj.layers
	#First, triangulate the mesh:
	bpy.ops.object.select_all(action='DESELECT')
	obj.select = True
	bpy.context.scene.objects.active = obj
	bpy.ops.object.mode_set(mode='EDIT')
	bpy.ops.mesh.select_all(action='SELECT')
	#use_beauty went away in 2.70, now use:
	bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY', ngon_method='BEAUTY')
	bpy.ops.object.mode_set(mode='OBJECT')

	if True:
		bpy.ops.mesh.vertex_color_add()
		bpy.context.scene.render.bake_type = 'FULL'
		bpy.context.scene.render.use_bake_to_vertex_color = True
		bpy.ops.object.bake_image()

	print("\nPrinting polys for object mesh \"" + objectName + "\":\n")

	if True:
		for poly in obj.data.polygons:
			print("Tri: ");

			assert(len(poly.vertices) == 3)
			for vi in poly.vertices:
				xf = obj.data.vertices[vi].co
				printPoint(xf)
			print("");

foundMesh = False

for obj in bpy.data.objects:
	if (obj.name == objectName):
		if obj.type == 'MESH':
			foundMesh = True
			printMesh(obj)

if not foundMesh:
	print("\nNo mesh found by the name " + str(objectName))