import argparse
import threading
import math
from math import radians
from . import dispatcher,osc_server
from mathutils import Quaternion,Vector
import bpy


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
        return True

    def draw(self, context):
        self.layout.operator(ICYP_OP_VMC_Client.bl_idname)
        return

class ICYP_OP_VMC_Client(bpy.types.Operator):
    bl_idname = "icyp.vmc_client"
    bl_label = "TEST Client"
    bl_description = "start vmc client"
    bl_options = {'REGISTER', 'UNDO'}

    _axis_tranlation_quatanion =  Quaternion(Vector([0,0,0]),radians(180)) @ Quaternion(Vector([1,0,0]),radians(-90))
    server = None
    dispatcher = None
    def print_VMC_Data_transform(self,addr, bone_name, loc_x, loc_y, loc_z, qua_x, qua_y, qua_z, qua_w):
        print(addr, bone_name, loc_x, loc_y, loc_z, qua_x, qua_y, qua_z, qua_w)
        if bone_name is not str \
            or loc_y is not float or loc_y is not float or loc_z is not float\
            or qua_x is not float or qua_y is not float or qua_z is not float or qua_w is not float:
            raise ValueError("unexpected input in vmc capture")
        loc = (loc_x, loc_y, loc_z)
        quat = (qua_x, qua_y, qua_z, qua_w) @ self._axis_tranlation_quatanion
        return #(bone_name, loc, quat)

    def print_VMC_Data_blend_shape(self,addr,shape_key,shape_value):
        if shape_key is not str or shape_value is not float:
            raise ValueError("unexpected input in vmc capture")
        print(addr,shape_key,shape_value)
        return #(shape_key,shape_value)

    #ゲームの開始からの秒数(float)。
    def print_VMC_time(self,addr,vmc_time):
        print(vmc_time)

    def modal(self, context, event):
        if event.type == 'LEFTMOUSE':
            self.server.shutdown()
            self.server.server_close()
            context.window_manager.event_timer_remove(self.timer)
            print("VMC client closed")
            return {'FINISHED'}

        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            self.server.shutdown()
            self.server.server_close()
            context.window_manager.event_timer_remove(self.timer)
            print("VMC client canceled")
            return {'CANCELLED'}
        elif event.type == "TIMER":
            # do something
            print("modal running")
            pass

        return {'PASS_THROUGH'}


    def execute(self, context):
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
    ICYP_VMC_Client_PT_controller
]



def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if "__main__" == __name__:
    register()


