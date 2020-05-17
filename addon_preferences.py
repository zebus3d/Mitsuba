from bpy.types import AddonPreferences
from bpy.props import (StringProperty)

class MitsubaAddonPreferences(AddonPreferences):
    # this must match the addon name
    bl_idname = "mitsuba_addon_preferences"

    install_path: StringProperty(
        name="Path to Mitsuba Installation",
        description='Path to Mitsuba install directory',
        subtype='DIR_PATH',
        # default=find_mitsuba_path(),
        )
    
    def draw(self, context):
        layout = self.layout
        layout.label(text="This is a preferences view for our add-on")
        layout.prop(self, "install_path")
