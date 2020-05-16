import bpy


def min_ao_counces_changed(self, context):
    if not bpy.context.scene.render.use_simplify:
        bpy.context.scene.render.use_simplify = True

    if bpy.context.scene.cycles.ao_bounces < bpy.context.scene.MinAOBounces:
        bpy.context.scene.cycles.ao_bounces = bpy.context.scene.MinAOBounces

    if bpy.context.scene.cycles.ao_bounces_render < bpy.context.scene.MinAOBounces:
        bpy.context.scene.cycles.ao_bounces_render = bpy.context.scene.MinAOBounces

    bpy.ops.simplify.ao()


def combo_texture_limit_changed(self, context):
    current = bpy.context.scene.TextureLimit

    if not bpy.context.scene.render.use_simplify:
        bpy.context.scene.render.use_simplify = True

    bpy.context.scene.cycles.texture_limit = current
    bpy.context.scene.cycles.texture_limit_render = current


def use_denoiser_changed(self, context):
    if bpy.context.scene.Denoisers == 'no_use' and bpy.context.scene.SingleAnimation != 'single':
        bpy.context.scene.cycles.use_animated_seed = True
        # bpy.context.scene.denoising_store_passes = False
        bpy.context.view_layer.cycles.denoising_store_passes = False
    elif bpy.context.scene.Denoisers == 'yes_use':
        bpy.context.scene.cycles.use_animated_seed = False
        # bpy.context.scene.denoising_store_passes = True
        bpy.context.view_layer.cycles.denoising_store_passes = True


def single_animation_changed(self, context):
    if bpy.context.scene.SingleAnimation == 'single' and bpy.context.scene.Denoisers != 'yes_use':
        bpy.context.scene.cycles.use_animated_seed = False
    elif bpy.context.scene.SingleAnimation == 'animation' and bpy.context.scene.Denoisers != 'yes_use':
        bpy.context.scene.cycles.use_animated_seed = True


def use_caustics_changed(self, context):
    if bpy.context.scene.Caustics == 'no_use':
        bpy.context.scene.cycles.caustics_reflective = False
        bpy.context.scene.cycles.caustics_refractive = False
    elif bpy.context.scene.Caustics == 'yes_use':
        bpy.context.scene.cycles.caustics_reflective = True
        bpy.context.scene.cycles.caustics_refractive = True