import bpy
from .when_updating_property import integrator_changed
from bpy.types import PropertyGroup
from bpy.props import EnumProperty, IntProperty, FloatProperty, StringProperty

class MitsubaProperties(PropertyGroup):
    # integrators
    integrator_types = (
        ("direct", "Direct Illumination", "", 0),
        ("path", "Path Tracer", "", 1),
        ("aov", "(AOV) Arbitrary Output Variables", "", 2),
        ("moment", "Moment", "", 3),
        ("stokes", "Stokes Vector", "", 4),
        # ("photon_mapper", "Photon Mapper", "", 2),
        # ("simple_volumetric", "Simple Volumetric Path Tracer", "", 3),
        # ("extended_volumetric", "Extended Volumetric Path Tracer", "", 4),
        # ("energy_redistribution", "Energy Redistribution PT", "", 5),
        # ("primary_sample_space_mtl", "Primary Sample Space MTL", "", 6),
        # ("stochastic_progresive", "Stochastic Progresive Phoyon Mapping", "", 7),
        # ("ambient_occlusion", "Ambient Occlusion", "", 8),
    )
    integratorType: EnumProperty(
        items=integrator_types,
        name="Type",
        default="path",
        description="",
        update=integrator_changed
    )
    # tanto aperture_radius como focus_distance son solo del sensor thinlens:
    aperture_radius: FloatProperty(
        name='Aperture Radius',
        default=0.001,
        precision=3,
        step = 1,
        description='Denotes the radius of the camera’s aperture in scene units',
    )
    focus_distance: FloatProperty(
        name='Focus Distance',
        default=1,
        precision=2,
        step = 1,
        description='Denotes the world-space distance from the camera’s aperture to the focal plane',
    )

    focal_length_or_fov = (
        ("focal_length", "Focal Length", "", 0),
        ("fov", "Fov", "", 1),
    )
    focal_or_fov: EnumProperty(
        items=focal_length_or_fov,
        name="Focal",
        default="fov",
        description="Use Focal length or Fov",
    )
    # mejor usare el propio valor de la camara 50mm
    # focal_length: FloatProperty(
    #     name='Focal Length',
    #     default=50,  #50mm
    #     precision=3,
    #     subtype="DISTANCE",
    #     unit="LENGTH",
    #     description='Denotes the camera’s focal length specified using 35mm film equivalent units',
    # )
    fov: FloatProperty(
        name='Fov',
        default=40.00,
        min=0.01,
        max=179.00,
        precision=2,
        step = 1,
        description='Denotes the camera’s field of view in degrees',
    )
    fov_axis: StringProperty(
        name='Fov Axis',
        default='x',
        description='specifies the image axis',
    )

    near_clip: FloatProperty(
        name='Near Clip',
        default=0.01,
        description='Distance to the near clip plane',
    )
    far_clip: FloatProperty(
        name='Far Clip',
        default=10000,
        description='Distance to the far clip planes',
    )
    maxDepth: IntProperty(
        name='Max Depth',
        default=23,
        min=0,
        soft_min=0,
        description='',
        # update=min_ao_counces_changed
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
    # sample_count
    sampleCount: IntProperty(
        name='Pixel Samples',
        default=8,
        min=1,
        soft_min=1,
        description='Number of samples to use for estimating the illumination at each pixel',
        # update=min_ao_counces_changed
    )
    # sensor type:
    sensor_types = (
        ("perspective", "Perspective", "", 0),
        ("thinlens", "Thinlens", "", 1),
        # ("stratified", "Stratified", "", 1),
        # ("low_discrepancy", "Low discrepancy", "", 2),
        # ("halton_qmc_sampler", "Halton QMC sampler", "", 3),
        # ("hammersley_qmc_sampler", "Hammersley_QMC_sampler", "", 4),
        # ("sobol_qmc_sampler", "Sobol QMC sampler", "", 5),
    )
    sensorType: EnumProperty(
        items=sensor_types,
        name="Type",
        default="perspective",
        # default="thinlens",
        description="Perspective simple or Perspective with whin thinlens (use thinlens for DOF)",
        # update=combo_texture_limit_changed
    )
    lightIntensity: IntProperty(
        name='Intensity',
        default=1,
        min=0,
        soft_min=0,
        description='Light Intensity',
    )
