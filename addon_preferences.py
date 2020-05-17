from bpy.types import AddonPreferences
from bpy.props import StringProperty

class MitsubaAddonPreferences(AddonPreferences):
    # this must match the addon name
    bl_idname = 'Mitsuba'

    filepath: StringProperty(
        name="Path to Mitsuba Installation",
        subtype="FILE_PATH",
        # default=find_mitsuba_path(),
    )


    def draw(self, context):
        layout = self.layout
        layout.label(text="This is a preferences view for our add-on")
        layout.prop(self, "filepath")
