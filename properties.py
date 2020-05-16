import bpy
from .on_changed import *


def create_properties():

    # settigns comboboxes:
    integrator_types = (
        ("OFF", "Direct", "", 0),
        ("128", "Path", "", 1),
    )

    # setup comboboxes:
    if integrator_types:
        bpy.types.Scene.IntegratorType = bpy.props.EnumProperty(
            items=integrator_types,
            name="Integrator Type",
            description="",
            # update=combo_texture_limit_changed
        )
