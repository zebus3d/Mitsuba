import bpy
from bpy.types import Operator
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.dom import minidom
import os
from mathutils import Vector

def prview_my_xml(my_xml):
    xmlstr_prettify = minidom.parseString( tostring(my_xml, encoding='utf-8', method='html') ).toprettyxml(indent="    ").replace("<?xml version=\"1.0\" ?>", "\nXML Preview:")
    print( xmlstr_prettify )


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
        # La @ es para multiplicar matrices con vectores
        cam_target = vector3_to_string( active_camera.matrix_world @ Vector((0, 0, -1, 1)) )
        cam_up = vector3_to_string( active_camera.matrix_world @ Vector((0, 1, 0, 0)) )

        scn_props = context.scene.mitsuba
        integratorType = scn_props.integratorType
        maxDepth = str(scn_props.maxDepth)
        filepath = context.preferences.addons['Mitsuba'].preferences.filepath
        sensorType = scn_props.sensorType
        samplerType = scn_props.samplerType
        sampleCount = str(scn_props.sampleCount)

        r_width = str( scene.render.resolution_x )
        r_height = str( scene.render.resolution_y )

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

        # sensor
        # Instantiate Camera
        sensor = SubElement(scene, 'sensor')
        sensor.set('type', sensorType)
        # <float name="fov" value="45"/>

        # sampler
        # Render with x samples per pixel using a samplerType sampling strategy
        sampler = SubElement(sensor, 'sampler')
        sampler.set('type', samplerType)
        integer = SubElement(sampler, 'integer')
        integer.set('name', 'sample_count')
        integer.set('value', sampleCount)

        # transform
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

        # Generate an EXR image
        film = SubElement(sensor, 'film')
        film.set('type', 'hdrfilm')
        integer = SubElement(film, 'integer')
        integer.set('name', 'width')
        integer.set('value', r_width)
        integer = SubElement(film, 'integer')
        integer.set('name', 'height')
        integer.set('value', r_height)

        prview_my_xml(scene)

        if filepath and os.path.isfile( filepath ):
            print(filepath)
            # mitusba_binary = os.path.basename( os.path.normpath(filepath) )
            # dir_path = filepath.replace(mitusba_binary, '')
            # print(dir_path, mitusba_binary)
            # print( os.path.isfile( filepath ) )
        else:
            self.report({'WARNING'}, 'It is mandatory to indicate in the addon preferences the correct location of the mitsuba executable. ')

        return {'FINISHED'}
