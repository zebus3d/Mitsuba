import bpy
from bpy.types import Operator
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.dom import minidom
import os


def prview_my_xml(my_xml):
    xmlstr_prettify = minidom.parseString( tostring(my_xml, encoding='utf-8', method='html') ).toprettyxml(indent="    ").replace("<?xml version=\"1.0\" ?>", "\nXML Preview:")
    print( xmlstr_prettify )


class PARSE_OT_scene(Operator):
    bl_label = "Export"
    bl_idname = "parse.scene"
    bl_description = "Export"
    
    def execute(self, context):    
        
        active_camera = bpy.data.scenes[context.scene.name].camera
        scn_props = context.scene.mitsuba
        integratorType = scn_props.integratorType
        maxDepth = str(scn_props.maxDepth)
        filepath = context.preferences.addons['Mitsuba'].preferences.filepath
        sensorType = scn_props.sensorType

        # scene to xml
        scene = Element('scene')
        scene.set('version', '2.0.0')

        integrator = SubElement(scene, 'integrator')

        integrator.set('type', integratorType)        
        if integratorType == 'path':
            integer = SubElement(integrator, 'integer')
            integer.set('name', 'max_depth')
            integer.set('value', maxDepth)

        sensor = SubElement(scene, 'sensor')
        sensor.set('type', sensorType)

        transform = SubElement(sensor, 'transform')
        transform.set('name', 'to_world')
        lookat = SubElement(transform, 'lookat')
        lookat.set('origin', '')
        lookat.set('target', '')
        lookat.set('up', '')

        
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
