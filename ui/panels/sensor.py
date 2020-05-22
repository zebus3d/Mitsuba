import bpy
from bpy.types import Panel

# secondary panels

class MITSUBA_PT_ui_sensor(Panel):
    bl_label = "Sensor"
    bl_idname = "MITSUBA_PT_ui_sensor"
    bl_parent_id = "MITSUBA_PT_ui"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"

    def draw(self, context):
        layout = self.layout

        layout.use_property_split = True
        layout.use_property_decorate = False

        scene = context.scene
        scn_props = scene.mitsuba
        active_camera = scene.camera


        flow = layout.grid_flow(align=True)
        col = flow.column()

        col.prop(scene.mitsuba, 'sensorType')
        if scn_props.sensorType == 'thinlens':
            col.prop(scene.mitsuba, 'aperture_radius')
            col.prop(scene.mitsuba, 'focus_distance')

        col.prop(scene.mitsuba, 'focal_or_fov')
        if scn_props.focal_or_fov == 'focal_length':
            if active_camera:
                col.prop(active_camera.data, 'lens')
            else:
                col.alignment = 'RIGHT'
                col.label(icon='ERROR', text='The main camera at the scene has not been found.')
        else:
            col.prop(scene.mitsuba, 'fov')
            col.prop(scene.mitsuba, 'fov_axis')

        col.prop(scene.mitsuba, 'near_clip')
        col.prop(scene.mitsuba, 'far_clip')
