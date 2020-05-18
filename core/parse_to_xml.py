from bpy.types import Operator
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.dom import minidom
import os

class PARSE_OT_scene(Operator):
    bl_label = "Export"
    bl_idname = "parse.scene"
    bl_description = "Export"
    
    def execute(self, context):    
        
        scn_props = context.scene.mitsuba
        integratorType = scn_props.integratorType
        maxDepth = str(scn_props.maxDepth)
        filepath = context.preferences.addons['Mitsuba'].preferences.filepath

        # scene to xml
        scene = Element('scene')
        scene.set('version', '2.0.0')

        integrator = SubElement(scene, 'integrator')

        integrator.set('type', integratorType)        
        if integratorType == 'path':
            integer = SubElement(integrator, 'integer')
            integer.set('name', 'max_depth')
            integer.set('value', maxDepth)

        xmlstr_prettify = minidom.parseString( tostring(scene, encoding='utf-8', method='html') ).toprettyxml(indent="    ")
        
        print( xmlstr_prettify )

        if filepath and os.path.isfile( filepath ):           
            print(filepath)
            # mitusba_binary = os.path.basename( os.path.normpath(filepath) )
            # dir_path = filepath.replace(mitusba_binary, '')
            # print(dir_path, mitusba_binary)
            # print( os.path.isfile( filepath ) )
        else:
            self.report({'WARNING'}, 'It is mandatory to indicate in the preferences the correct location of the mitsuba executable. ')

        return {'FINISHED'}
