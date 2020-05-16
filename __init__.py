'''
    Copyright (c) 2020

    Jorge Hernández - Meléndez Saiz
    zebus3dream@gmail.com

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>.
'''


bl_info = {
    "name": "Mitsuba",
    "description": "",
    "author": "zebus3d",
    "version": (0, 0, 1),
    "blender": (2, 83, 0),
    "location": "",
    "wiki_url": "",
    "category": "Render"
}

if "bpy" in locals():
    import importlib
    if "MitsubaRenderEngine" in locals():
        importlib.reload(MitsubaRenderEngine),
    if "MitsubaDrawData" in locals():
        importlib.reload(MitsubaDrawData)
    if "MITSUBA_PT_ui" in locals():
        importlib.reload(MITSUBA_PT_ui)
else:
    import bpy
    from .classes.engine import MitsubaRenderEngine
    from .classes.draw import MitsubaDrawData
    from .ui import MITSUBA_PT_ui
    from .properties import create_properties


# RenderEngines also need to tell UI Panels that they are compatible with.
# We recommend to enable all panels marked as BLENDER_EEVEE, and then
# exclude any panels that are replaced by custom panels registered by the
# render engine, or that are not supported.
def get_panels():
    exclude_panels = [
        'VIEWLAYER_PT_filter',
        'VIEWLAYER_PT_layer_passes',
    ]
    target_panels = [
        'RENDER_PT_dimensions',
        'RENDER_PT_output',
        'RENDER_PT_color_management',
        'RENDER_PT_color_management_curves',
        ]

    # paneles compatibles:
    panels = []
    for panel in bpy.types.Panel.__subclasses__():
        if hasattr(panel, 'COMPAT_ENGINES'):
            panel_name = panel.__name__
            # print(panel_name)
            if panel_name in target_panels and panel_name not in exclude_panels:
                panels.append(panel)

    return panels

all_classes = [
    MitsubaRenderEngine,
    MITSUBA_PT_ui
    # MitsubaDrawData, # es una clase normal python no tiene tipo de blender por eso no la registro 
]


def register():
    from bpy.utils import register_class

    if len(all_classes) > 1:
        for cls in all_classes:
            register_class(cls)
    else:
        register_class(all_classes[0])

    # Register the RenderEngine
    # bpy.utils.register_class(MitsubaRenderEngine)

    create_properties()

    for panel in get_panels():
        panel.COMPAT_ENGINES.add('MITSUBA')



def unregister():

    from bpy.utils import unregister_class

    if len(all_classes) > 1:
        for cls in reversed(all_classes):
            unregister_class(cls)
    else:
        unregister_class(all_classes[0])

    # bpy.utils.unregister_class(MitsubaRenderEngine)

    del bpy.types.Scene.TextureLimit
    del bpy.types.Scene.Denoisers
    del bpy.types.Scene.Caustics
    del bpy.types.Scene.SingleAnimation
    del bpy.types.Scene.MinAOBounces

    for panel in get_panels():
        if 'MITSUBA' in panel.COMPAT_ENGINES:
            panel.COMPAT_ENGINES.remove('MITSUBA')


if __name__ == "__main__":
    register()