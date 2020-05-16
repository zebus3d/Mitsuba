import bpy
from .on_changed import *


def create_properties():

    # settigns comboboxes:
    texturelimit_options = (
        ("OFF", "No Limit", "", 0),
        ("128", "128", "", 1),
        ("512", "512", "", 2),
        ("1024", "1024", "", 3),
        ("2048", "2048", "", 4),
        ("4096", "4096", "", 5),
        ("8192", "8192", "", 6)
    )
    denoiser_options = (
        ("off", "Choose", "", 0),
        ('no_use', 'Not going to use Denoiser', "", 1),
        ('yes_use', 'Yes going to use Denoiser', "", 2)
    )
    caustics_options = (
        ("off", "Choose", "", 0),
        ('no_use', 'Not going to use Caustics', "", 1),
        ('yes_use', 'Yes going to use Caustics', "", 2)
    )

    single_animation_options = (
        ("off", "Choose", "", 0),
        ('single', 'Single Frame', "", 1),
        ('animation', 'Animation', "", 2)
    )

    # setup comboboxes:
    if texturelimit_options:
        bpy.types.Scene.TextureLimit = bpy.props.EnumProperty(
            items=texturelimit_options,
            name="Texture Limit",
            description="Limit texture size used",
            update=combo_texture_limit_changed
        )

    if denoiser_options:
        bpy.types.Scene.Denoisers = bpy.props.EnumProperty(
            items=denoiser_options,
            name="Denoisers",
            description="If you use Denoirser or not, this option configure the output passes and animated seed integrator",
            update=use_denoiser_changed
        )

    if caustics_options:
        bpy.types.Scene.Caustics = bpy.props.EnumProperty(
            items=caustics_options,
            name="Caustics",
            description="Enable/Disable Caustics",
            update=use_caustics_changed
        )

    if single_animation_options:
        bpy.types.Scene.SingleAnimation = bpy.props.EnumProperty(
            items=single_animation_options,
            name="FinalRender",
            description="Your Final Render is Single frame or Animation?",
            update=single_animation_changed
        )

    bpy.types.Scene.MinAOBounces = bpy.props.IntProperty(
        name='Minimun AO Bounces',
        default=4,
        min=0,
        soft_min=0,
        description='Minimun AO Bounces in simplify',
        update=min_ao_counces_changed
    )