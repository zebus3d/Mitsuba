import bpy



def integrator_changed(self, context):
    # Hay que compilar los cython de mitsuba con la misma version de python de blender:
    # cmake -DPYTHON_EXECUTABLE=/Applications/last_blender/Blender_2.90.app/Contents/Resources/2.90/python/bin/python3.7m  -GNinja ..
    # from ..binding_python.mitsuba import mitsuba
    pass