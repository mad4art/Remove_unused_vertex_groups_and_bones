bl_info = {
 "name": "Remove unused Vertex Groups and Bones",
 "author": "Leo",
 "version": (1, 0),
 "blender": (4, 0, 0),
 "location": "View3D > Tool Shelf > Object > Remove unused Vertex Groups and Bones",
 "description": "Deletes Vertex Groups and Bones with no assigned weight of active object",
 "warning": "",
 "wiki_url": "",
 "category": "3D View",
}

import bpy
from bpy.props import BoolProperty
from bpy.types import Operator

class OBJECT_OT_vertex_group_remove_unused(Operator):
 """Tooltip"""
 bl_idname = "object.vertex_group_remove_unused"
 bl_label = "Remove unused Vertex Groups and Bones"
 bl_options = {'REGISTER', 'UNDO'}

 @classmethod
 def poll(cls, context):
     return (context.object is not None and
             context.object.type == 'MESH')

 def execute(self, context):
     ob = context.active_object
     ob.update_from_editmode()
     
     vgroup_used = {i: False for i, k in enumerate(ob.vertex_groups)}
     
     for v in ob.data.vertices:
         for g in v.groups:
             if g.weight > 0.0:
               vgroup_used[g.group] = True
     
     for i, used in sorted(vgroup_used.items(), reverse=True):
         if not used:
             ob.vertex_groups.remove(ob.vertex_groups[i])

     if ob.type == 'ARMATURE':
         bone_used = {i: False for i, k in enumerate(ob.pose.bones)}
         
         for v in ob.data.vertices:
             for g in v.bone_groups:
                if g.weight > 0.0:
                  bone_used[g.group] = True
         
         for i, used in sorted(bone_used.items(), reverse=True):
             if not used:
                ob.pose.bones.remove(ob.pose.bones[i])
             
     return {'FINISHED'}

def register():
 bpy.utils.register_class(OBJECT_OT_vertex_group_remove_unused)
 bpy.types.OBJECT_PT_transform.append(draw_func)

def unregister():
 bpy.utils.unregister_class(OBJECT_OT_vertex_group_remove_unused)
 bpy.types.OBJECT_PT_transform.remove(draw_func)

def draw_func(self, context):
 self.layout.operator(
     OBJECT_OT_vertex_group_remove_unused.bl_idname,
     text="Remove unused Vertex Groups and Bones",
     icon='X'
 )

if __name__ == "__main__":
 register()