import bpy
from .when_updating_property import *
from bpy.types import PropertyGroup
from bpy.props import EnumProperty, IntProperty

class MitsubaProperties(PropertyGroup):
    # integrators
    integrator_types = (
        ("direct_illumination", "Direct Illumination", "", 0),
        ("path_tracer", "Path Tracer", "", 1),
        ("photon_mapper", "Photon Mapper", "", 2),
        ("simple_volumetric", "Simple Volumetric Path Tracer", "", 3),
        ("extended_volumetric", "Extended Volumetric Path Tracer", "", 4),
        ("energy_redistribution", "Energy Redistribution PT", "", 5),
        ("primary_sample_space_mtl", "Primary Sample Space MTL", "", 6),
        ("stochastic_progresive", "Stochastic Progresive Phoyon Mapping", "", 7),
        ("ambient_occlusion", "Ambient Occlusion", "", 8),
    )
    integratorType: EnumProperty(
        items=integrator_types,
        name="Type",
        default="path_tracer",
        description="",
        # update=combo_texture_limit_changed
    )
    
    # sampler:
    sampler_types = (
        ("independent", "Independent", "", 0),
        ("in_the_future", "In the future there will be more", "", 1),
        # ("stratified", "Stratified", "", 1),
        # ("low_discrepancy", "Low discrepancy", "", 2),
        # ("halton_qmc_sampler", "Halton QMC sampler", "", 3),
        # ("hammersley_qmc_sampler", "Hammersley_QMC_sampler", "", 4),
        # ("sobol_qmc_sampler", "Sobol QMC sampler", "", 5),
    )
    samplerType: EnumProperty(
        items=sampler_types,
        name="Type",
        default="independent",
        description="",
        # update=combo_texture_limit_changed
    )
    sampleCount: IntProperty(
        name='Pixel Samples',
        default=16,
        min=1,
        soft_min=1,
        description='Number of samples to use for estimating the illumination at each pixel',
        # update=min_ao_counces_changed
    )
