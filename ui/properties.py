import bpy
from .when_updating_property import *


def create_properties():

    # settigns comboboxes:
    integrator_types = (
        ("path_tracer", "Path Tracer", "", 0),
        ("direct_illumination", "Direct Illumination", "", 1),
        ("photon_mapper", "Photon Mapper", "", 2),
        ("simple_volumetric", "Simple Volumetric Path Tracer", "", 3),
        ("extended_volumetric", "Extended Volumetric Path Tracer", "", 4),
        ("energy_redistribution", "Energy Redistribution PT", "", 5),
        ("primary_sample_space_mtl", "Primary Sample Space MTL", "", 6),
        ("stochastic_progresive", "Stochastic Progresive Phoyon Mapping", "", 7),
        ("ambient_occlusion", "Ambient Occlusion", "", 8),
    )

    # setup comboboxes:
    if integrator_types:
        bpy.types.Scene.IntegratorType = bpy.props.EnumProperty(
            items=integrator_types,
            name="Type",
            description="",
            # update=combo_texture_limit_changed
        )
