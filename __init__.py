import argparse
import threading
import math
from math import radians
from . import dispatcher,osc_server
from mathutils import Quaternion,Vector
import bpy
from .humanoid_controller import ICYP_PT_VMC_Client_controller,Add_reqwire_humanbone_custom_propaty,Add_defined_humanbone_custom_propaty


bl_info = {
    "name":"VMC Client",
    "author": "iCyP",
    "version": (0, 0),
    "blender": (2, 80, 0),
    "location": "",
    "description": "",
    "warning": "",
    "support": "TESTING",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Tools"
}

class ICYP_VMC_Client_PT_controller(bpy.types.Panel):
    bl_idname = "ICYP_PT_vmc_ui_controller"
    bl_label = "VMC Client"
    #どこに置くかの定義
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "VMC Client"
    @classmethod
    def poll(self, context):
        try:
            if context.active_object.type == "ARMATURE":
                return True
        except:
            pass
        return False

    def draw(self, context):
        self.layout.operator(ICYP_OP_VMC_Client.bl_idname)
        return

class ICYP_OP_VMC_Client(bpy.types.Operator):
    bl_idname = "icyp.vmc_client"
    bl_label = "TEST Client"
    bl_description = "start vmc client"
    bl_options = {'REGISTER', 'UNDO'}

    _axis_tranlation_quatanion =  Quaternion(Vector([0,1,0]),radians(180)) @ Quaternion(Vector([1,0,0]),radians(-90))
    server = None
    dispatcher = None
    def print_VMC_Data_transform(self,addr, bone_name, loc_x, loc_y, loc_z, qua_x, qua_y, qua_z, qua_w):
        #print(addr, bone_name, loc_x, loc_y, loc_z, qua_x, qua_y, qua_z, qua_w)
        if (type(bone_name) is not str) \
            or (type(loc_x) is not float) or (type(loc_y) is not float) or (type(loc_z) is not float)\
            or (type(qua_x) is not float) or (type(qua_y) is not float) or (type(qua_z) is not float) or (type(qua_w) is not float):
            raise ValueError("unexpected input in vmc capture")
        loc = (loc_x, loc_z ,-loc_y)
        quat = Quaternion([qua_w,qua_x, qua_y, qua_z]) @ self._axis_tranlation_quatanion
        if self.armature_obj.data[bone_name] in self.armature_obj.data.bones:
            self.armature_obj.pose.bones[self.armature_obj.data[bone_name]].location = loc
            self.armature_obj.pose.bones[self.armature_obj.data[bone_name]].rotation_quaternion = quat
        return #(bone_name, loc, quat)

    def print_VMC_Data_blend_shape(self,addr,shape_key,shape_value):
        if (type(shape_key) is not str) or (type(shape_value) is not float):
            raise ValueError("unexpected input in vmc capture")
        #print(addr,shape_key,shape_value)
        return #(shape_key,shape_value)

    #ゲームの開始からの秒数(float)。
    def print_VMC_time(self,addr,vmc_time):
        #print(vmc_time)
        pass
    
    def modal(self, context, event):
        if event.type in {'ESC'}:
            self.server.shutdown()
            self.server.server_close()
            context.window_manager.event_timer_remove(self.timer)
            print("VMC client canceled")
            return {'FINISHED'}
        elif event.type == "TIMER":
            # do something
            pass

        return {'PASS_THROUGH'}


    def execute(self, context):
        self.armature_obj = context.active_object
        self.timer = context.window_manager.event_timer_add(0.01,window = context.window)
        context.window_manager.modal_handler_add(self)
        self.dispatcher = dispatcher.Dispatcher()
        self.dispatcher.map("/VMC/Ext/Root/Pos", self.print_VMC_Data_transform)
        self.dispatcher.map("/VMC/Ext/Bone/Pos", self.print_VMC_Data_transform)
        self.dispatcher.map("/VMC/Ext/Blend/Val",self.print_VMC_Data_blend_shape)
        self.dispatcher.map("/VMC/Ext/T", self.print_VMC_time)
        self.server = osc_server.ThreadingOSCUDPServer(("127.0.0.1",3333),self.dispatcher)
        self.server.timeout = 0.01
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.start()
        return {'RUNNING_MODAL'}

classes = [
    ICYP_OP_VMC_Client,
    ICYP_VMC_Client_PT_controller,
    ICYP_PT_VMC_Client_controller,
    Add_reqwire_humanbone_custom_propaty,
    Add_defined_humanbone_custom_propaty
]



def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if "__main__" == __name__:
    register()


