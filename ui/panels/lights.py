import bpy
from bpy.types import Panel

# secondary panels

class MITSUBA_PT_ui_lights(Panel):
    bl_label = "Lights"
    bl_idname = "MITSUBA_PT_ui_lights"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"

    @classmethod
    def poll(cls, context):
        engine = context.engine
        return context.light and (engine in cls.COMPAT_ENGINES)

    def draw(self, context):
        layout = self.layout
        light = context.light

        layout.use_property_split = True
        layout.use_property_decorate = False

        scene = context.scene

        flow = layout.grid_flow(align=True)
        col = flow.column()

        col.prop(light, "color")
        col.prop(light, "energy")
