import bpy
from bpy.types import (Panel)

class MITSUBA_PT_ui(Panel):
    bl_label = "Mitsuba settings"
    bl_idname = "MITSUBA_PT_ui"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"

    @classmethod
    def poll(cls, context):
        engine = context.scene.render.engine
        if engine != 'MITSUBA':
            return False
        else:
            return True

    def draw(self, context):
        layout = self.layout

        layout.use_property_split = True
        layout.use_property_decorate = False

        scene = context.scene

        flow = layout.grid_flow(align=True)
        col = flow.column()

        # col = layout.box() # las cajas negras

        col.separator()
