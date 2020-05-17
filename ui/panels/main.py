import bpy
from bpy.types import Panel

# Main panel

class MITSUBA_PT_ui(Panel):
    bl_label = "Mitsuba Engine Settings"
    bl_idname = "MITSUBA_PT_ui"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"

    @classmethod
    def poll(cls, context):
        engine = context.scene.render.engine
        return engine == 'MITSUBA'

    def draw(self, context):
        pass
