import bpy, os
from bpy.types import Operator
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.dom import minidom
from mathutils import Vector
import tempfile
from subprocess import Popen, PIPE


def prview_my_xml(my_xml):
    xmlstr_prettify = minidom.parseString( tostring(my_xml, encoding='utf-8', method='html') ).toprettyxml(indent="    ")
    xmlstr_prettify = xmlstr_prettify.replace('origin=', '\n                    origin=')
    xmlstr_prettify = xmlstr_prettify.replace('target=', '\n                    target=')
    xmlstr_prettify = xmlstr_prettify.replace('up=', '\n                    up=')
    print( xmlstr_prettify )
    return xmlstr_prettify


def vector3_to_string(v):
    vector3_stringified = str(v[0]) + ', ' + str(v[1]) + ', ' + str(v[2])
    return vector3_stringified


class PARSE_OT_scene(Operator):
    bl_label = "Export"
    bl_idname = "parse.scene"
    bl_description = "Export"

    def execute(self, context):

        scene = bpy.data.scenes[context.scene.name]
        active_camera = scene.camera

        if not active_camera:
            self.report({'ERROR'}, 'The main camera at the scene has not been found.')
            return {'CANCELLED'}

        cam_origin = vector3_to_string( active_camera.location )
        cam_target = vector3_to_string( active_camera.matrix_world @ Vector((0, 0, -1, 1)) )
        cam_up = vector3_to_string( active_camera.matrix_world @ Vector((0, 1, 0, 0)) )
        # La @ es para multiplicar matrices con vectores.

        scn_props = context.scene.mitsuba
        integratorType = scn_props.integratorType
        maxDepth = str( scn_props.maxDepth )
        filepath = context.preferences.addons['Mitsuba'].preferences.filepath

        sensorType = scn_props.sensorType

        # aperture_radius = str( '%5.3f'% scn_props.aperture_radius )
        aperture_radius = str( scn_props.aperture_radius )
        focus_distance = str( scn_props.focus_distance )

        focal_or_fov = scn_props.focal_or_fov
        # focal_length = str( scn_props.focal_length ) # mejor usare el de la propia camara:
        focal_length = str( active_camera.data.lens ) + 'mm'
        fov = str( "%.2f" % scn_props.fov )

        samplerType = scn_props.samplerType
        sampleCount = str( scn_props.sampleCount )

        r_width = str( scene.render.resolution_x )
        r_height = str( scene.render.resolution_y )

        lightIntensity = str( scn_props.lightIntensity )

        # self.report({'INFO'}, 'Exporting scene')
        print("# Exporting scene...")

        # scene to xml
        scene = Element('scene')
        scene.set('version', '2.0.0')

        # integrator
        integrator = SubElement(scene, 'integrator')

        # Instantiate a path tracer with a max.
        # path length of maxDepth
        integrator.set('type', integratorType)
        if integratorType == 'path':
            integer = SubElement(integrator, 'integer')
            integer.set('name', 'max_depth')
            integer.set('value', maxDepth)

        # Sensor
        sensor = SubElement(scene, 'sensor')
        sensor.set('type', sensorType)
        # sensor exceptions for thinlens:
        if sensorType == 'thinlens':
            ar_float = SubElement(sensor, 'float')
            ar_float.set('name', 'aperture_radius')
            ar_float.set('value', aperture_radius)
            #
            fd_float = SubElement(sensor, 'float')
            fd_float.set('name', 'focus_distance')
            fd_float.set('value', focus_distance)
        # common options for the both sensors:
        transform = SubElement(sensor, 'transform')
        transform.set('name', 'to_world')
        # lookat transformations – this is primarily useful for setting up cameras.
        # The origin coordinates specify the camera origin, target is the point
        # that the camera will look at, and the (optional) up parameter determines
        # the upward direction in the final rendered image.
        lookat = SubElement(transform, 'lookat')
        lookat.set('origin', cam_origin)
        lookat.set('target', cam_target)
        lookat.set('up', cam_up)
        #
        if focal_or_fov == 'focal_length':
            fl_str = SubElement(sensor, 'string')
            fl_str.set('name', 'focal_length')
            fl_str.set('value', focal_length)
        else:
            fov_float = SubElement(sensor, 'float')
            fov_float.set('name', 'fov')
            fov_float.set('value', fov)

        # sampler
        # Render with x samples per pixel using a samplerType sampling strategy
        sampler = SubElement(sensor, 'sampler')
        sampler.set('type', samplerType)
        integer = SubElement(sampler, 'integer')
        integer.set('name', 'sample_count')
        integer.set('value', sampleCount)

        # Generate an EXR image
        film = SubElement(sensor, 'film')
        film.set('type', 'hdrfilm')
        integer = SubElement(film, 'integer')
        integer.set('name', 'width')
        integer.set('value', r_width)
        integer = SubElement(film, 'integer')
        integer.set('name', 'height')
        integer.set('value', r_height)

        # lights
        for obj in bpy.data.objects:
            if not obj.hide_render and obj.type == 'LIGHT' and obj.data.id_data.type == 'POINT':
                light = obj.data.id_data
                emmitter = SubElement(scene, 'emitter')
                emmitter.set('type', 'point')
                spectrum = SubElement(emmitter, 'spectrum')
                spectrum.set('name', 'intensity')
                spectrum.set('value', str( lightIntensity ))
                point = SubElement(emmitter, 'point')
                point.set('name', 'position')
                point.set('x', str( obj.location.x ))
                point.set('y', str( obj.location.y ))
                point.set('z', str( obj.location.z ))

        # shapes obj
        tmp_dir = tempfile.gettempdir()+'/mitsuba'

        if not os.path.isdir(tmp_dir):
            os.makedirs(tmp_dir)

        if bpy.context.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')

        bpy.ops.object.select_all(action='DESELECT')

        for obj in bpy.data.objects:
            if not obj.hide_render and obj.type == 'MESH':
                context.view_layer.objects.active = obj
                obj.select_set(True)

                obj_target_name = obj.name + '.obj'

                target_file = os.path.join(tmp_dir, obj_target_name)
                print("# Exporting " + target_file + '...')
                bpy.ops.export_scene.obj(filepath=target_file, axis_forward='Y', axis_up='Z', use_selection=True, use_animation=False, use_mesh_modifiers=True, use_smooth_groups=True, use_normals=True, use_uvs=True, use_materials=False, keep_vertex_order=True, global_scale=1)

                obj.select_set(False)

                if os.path.isfile(target_file):
                    shape = SubElement(scene, 'shape')
                    shape.set('type', 'obj')
                    sstring = SubElement(shape, 'string')
                    sstring.set('name', 'filename')
                    sstring.set('value', target_file)

        # preview an data
        data_xml = prview_my_xml(scene)

        # write output xml file in the disk
        final_xml_file_path = tmp_dir+'/test_example.xml'
        print("# Writing " + final_xml_file_path + '...')
        final_xml_file = open(final_xml_file_path,'w')
        final_xml_file.write(data_xml)
        final_xml_file.close()

        # renderize scene xml
        if filepath and os.path.isfile( filepath ):
            if os.path.isfile(final_xml_file_path):
                print("# Rendering...")
                # self.report({'INFO'}, 'Starting rendering...')
                process = Popen([filepath, final_xml_file_path], stdout=PIPE, stderr=PIPE)
                stdout, stderr = process.communicate()
                # print("Finish!.")
                self.report({'INFO'}, 'Render completed!')
        else:
            self.report({'WARNING'}, 'It is mandatory to indicate in the addon preferences the correct location of the mitsuba executable. ')

        bpy.ops.image.reload()
        return {'FINISHED'}
