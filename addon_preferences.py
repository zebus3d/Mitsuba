from bpy.types import AddonPreferences
from bpy.props import (StringProperty)

class MitsubaAddonPreferences(AddonPreferences):
    # this must match the addon name
    bl_idname = __name__

    install_path : StringProperty(
        name="Path to Mitsuba Installation",
        description='Path to Mitsuba install directory',
        subtype='DIR_PATH',
        # default=find_mitsuba_path(),
        )
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "install_path")
