import bpy
from bpy.types import (Panel)

class MITSUBA_PT_ui(Panel):
    bl_label = "Mitsuba Render settings"
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

        col = layout.box()
        col.label(text="Simplify")

        col.separator()

        # col.alignment = 'RIGHT'
        col = layout.box()
        col.label(text="Miscellaneous")

        col.prop(scene.cycles, 'use_adaptive_sampling')
        col.prop(scene, 'Caustics')
        col.prop(scene, 'Denoisers')
        col.prop(scene, 'SingleAnimation')