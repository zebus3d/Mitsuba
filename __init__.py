
bl_info = {
    "name": "Mitsuba",
    "description": "Extra Official addon for Mitsuba2",
    "author": "zebus3d",
    "version": (0, 0, 1),
    "blender": (2, 83, 0),
    "location": "",
    "wiki_url": "https://github.com/zebus3d/Mitsuba",
    "category": "Render"
}


'''
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


if "bpy" in locals():
    import importlib
    if "MitsubaAddonPreferences" in locals():
        importlib.reload(MitsubaAddonPreferences)
    if "MitsubaRenderEngine" in locals():
        importlib.reload(MitsubaRenderEngine),
    if "MitsubaDrawData" in locals():
        importlib.reload(MitsubaDrawData)
    if "MitsubaProperties" in locals():
        importlib.reload(MitsubaProperties)
    if "MITSUBA_PT_ui" in locals():
        importlib.reload(MITSUBA_PT_ui)
    if "MITSUBA_PT_ui_integrators" in locals():
        importlib.reload(MITSUBA_PT_ui_integrators)
    if "MITSUBA_PT_ui_intMITSUBA_PT_ui_samplesegrators" in locals():
        importlib.reload(MITSUBA_PT_ui_samples)
    if "PARSE_OT_scene" in locals():
        importlib.reload(PARSE_OT_scene)
    if "MITSUBA_PT_ui_sensor" in locals():
        importlib.reload(MITSUBA_PT_ui_sensor)
    if "MITSUBA_PT_ui_lights" in locals():
        importlib.reload(MITSUBA_PT_ui_lights)
else:
    import bpy
    from .ui.addon_preferences import MitsubaAddonPreferences
    from .core.engine import MitsubaRenderEngine
    from .core.draw import MitsubaDrawData
    from .ui.properties import MitsubaProperties
    from .ui.panels.main import MITSUBA_PT_ui
    from .ui.panels.integrators import MITSUBA_PT_ui_integrators
    from .ui.panels.samples import MITSUBA_PT_ui_samples
    from .ui.panels.sensor import MITSUBA_PT_ui_sensor
    from .core.parse_to_xml import PARSE_OT_scene
    from .ui.panels.lights import MITSUBA_PT_ui_lights


from bpy.props import PointerProperty


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
        'DATA_PT_lens',
        # 'CYCLES_LIGHT_PT_light',
        ]

    # paneles compatibles:
    panels = []
    for panel in bpy.types.Panel.__subclasses__():
        if hasattr(panel, 'COMPAT_ENGINES'):
            panel_name = panel.__name__
            # print(panel_name) # for view avalidable panels uncoment this line
            if panel_name in target_panels and panel_name not in exclude_panels:
                panels.append(panel)

    return panels


all_classes = [
        MitsubaAddonPreferences,
        MitsubaRenderEngine,
        MitsubaProperties,
        MITSUBA_PT_ui,
        MITSUBA_PT_ui_integrators,
        MITSUBA_PT_ui_samples,
        PARSE_OT_scene,
        MITSUBA_PT_ui_sensor,
        MITSUBA_PT_ui_lights
    ]


def register():
    from bpy.utils import register_class

    for cls in all_classes:
        register_class(cls)

    bpy.types.Scene.mitsuba = PointerProperty(type=MitsubaProperties)

    for panel in get_panels():
        panel.COMPAT_ENGINES.add('MITSUBA')


def unregister():
    from bpy.utils import unregister_class

    for cls in reversed(all_classes):
        unregister_class(cls)

    del bpy.types.Scene.mitsuba

    for panel in get_panels():
        if 'MITSUBA' in panel.COMPAT_ENGINES:
            panel.COMPAT_ENGINES.remove('MITSUBA')

