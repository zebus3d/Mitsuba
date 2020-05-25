from bpy.types import AddonPreferences
from bpy.props import StringProperty

class MitsubaAddonPreferences(AddonPreferences):
    # this must match the addon name
    bl_idname = 'Mitsuba'

    mitsuba2_path: StringProperty(
        name='Mitsuba2 folder',
        # subtype='FILE_PATH',
        subtype='DIR_PATH'
    )


    def draw(self, context):
        layout = self.layout
        # layout.label(text="This is a preferences view for our add-on")
        layout.prop(self, "mitsuba2_path")
