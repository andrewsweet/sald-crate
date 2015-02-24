# sald-crate

export-model.py: a blender python script that prints to the console a list of vertices and triangles in the mesh, when run as follows:

blender --background crate.blend --python export-model.py -- Crate

where Crate is the name of whatever object mesh in the crate.blend file you'd like to print, or more generically:

blender --background <.blend file> --python export-model.py -- <object mesh name>
