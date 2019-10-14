import bpy

humanoid_requires= [
    "hips","spine","chest","neck","head",
    "leftUpperLeg","leftLowerLeg","leftFoot",
    "rightUpperLeg","rightLowerLeg","rightFoot",
    "leftUpperArm","leftLowerArm","leftHand",
    "rightUpperArm","rightLowerArm","rightHand"
]
humanoid_defines =  [
    "jaw",
    "leftEye","rightEye",
    "leftShoulder","rightShoulder",
    "upperChest",
    "leftToes","rightToes",

    "leftThumbProximal","leftThumbIntermediate","leftThumbDistal","leftIndexProximal",
    "leftIndexIntermediate","leftIndexDistal","leftMiddleProximal","leftMiddleIntermediate",
    "leftMiddleDistal","leftRingProximal","leftRingIntermediate","leftRingDistal",
    "leftLittleProximal","leftLittleIntermediate","leftLittleDistal",
    
    "rightThumbProximal","rightThumbIntermediate","rightThumbDistal",
    "rightIndexProximal","rightIndexIntermediate","rightIndexDistal",
    "rightMiddleProximal","rightMiddleIntermediate","rightMiddleDistal",
    "rightRingProximal","rightRingIntermediate","rightRingDistal",
    "rightLittleProximal","rightLittleIntermediate","rightLittleDistal"
            ]

class ICYP_PT_VMC_Client_controller(bpy.types.Panel):
    bl_idname = "ICYP_PT_VM_Client_bone_panel_controller"
    bl_label = "humanoid helper"
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
        self.layout.separator()
        abox = self.layout.row(align=False).box()
        abox.label(text="Armature Help")

        reqbox = abox.box()
        reqrow = reqbox.row()
        reqrow.label(text = "Humanoid Reqwire Bones")
        for req in humanoid_requires:
            if req in context.active_object.data:
                reqbox.prop_search(context.active_object.data, f'[\"{req}\"]', context.active_object.data, "bones", text=req)
            else:
                reqbox.operator(Add_reqwire_humanbone_custom_propaty.bl_idname,text = f"Add {req} propaty")
        defbox = abox.box()
        defbox.label(text="Humanoid option Bones")
        for defs in humanoid_defines:
            if defs in context.active_object.data:
                defbox.prop_search(context.active_object.data, f'[\"{defs}\"]', context.active_object.data, "bones", text=defs)
            else:
                defbox.operator(Add_defined_humanbone_custom_propaty.bl_idname,text = f"Add {defs} propaty")     

        return
        

class Add_reqwire_humanbone_custom_propaty(bpy.types.Operator):
    bl_idname = "icyp.add_humanoid_req_humanbone_prop"
    bl_label = "Add humanoid reqwire"
    bl_description = ""
    bl_options = {'REGISTER', 'UNDO'}
    
    
    def execute(self, context):
        arm = bpy.data.armatures[bpy.context.active_object.data.name]
        for req in humanoid_requires:
            if req not in arm:
                arm[req] = ""
        return {"FINISHED"}

class Add_defined_humanbone_custom_propaty(bpy.types.Operator):
    bl_idname = "icyp.add_humanoid_def_humanbone_prop"
    bl_label = "Add humanoid require"
    bl_description = ""
    bl_options = {'REGISTER', 'UNDO'}
    
    
    def execute(self, context):
        arm = bpy.data.armatures[bpy.context.active_object.data.name]
        for d in humanoid_defines:
            if d not in arm:
                arm[d] = ""
        return {"FINISHED"}