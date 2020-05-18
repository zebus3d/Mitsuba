from bpy.types import Operator
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.dom import minidom

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

        print(filepath)

        return {'FINISHED'}
