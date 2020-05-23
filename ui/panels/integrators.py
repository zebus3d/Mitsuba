import bpy
from bpy.types import Panel

# secondary panels

class MITSUBA_PT_ui_integrators(Panel):
    bl_label = "Integrator"
    bl_idname = "MITSUBA_PT_ui_integrators"
    bl_parent_id = "MITSUBA_PT_ui_main"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"

    def draw(self, context):
        layout = self.layout

        layout.use_property_split = True
        layout.use_property_decorate = False

        scene = context.scene

        flow = layout.grid_flow(align=True)
        col = flow.column()

        col.prop(scene.mitsuba, 'integratorType')
        if context.scene.mitsuba.integratorType == 'path':
            col.prop(scene.mitsuba, 'maxDepth')
