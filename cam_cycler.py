bl_info = {
    "name": "CamCycler",
    "author": "Zach",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "category": "3D View",
    "description": "Cycle through scene cameras and toggle camera view lock",
}

import bpy


class CAMCYCLER_OT_next_camera(bpy.types.Operator):
    bl_idname = "camcycler.next_camera"
    bl_label = "Next Camera"
    bl_description = "Look through the next camera in the scene"
    bl_options = {'REGISTER'}

    def execute(self, context):
        cameras = sorted(
            [obj for obj in context.scene.objects if obj.type == 'CAMERA'],
            key=lambda c: c.name,
        )
        if not cameras:
            self.report({'WARNING'}, "No cameras in scene")
            return {'CANCELLED'}

        current = context.scene.camera
        if current and current in cameras:
            idx = (cameras.index(current) + 1) % len(cameras)
        else:
            idx = 0

        context.scene.camera = cameras[idx]

        # Enter camera view if not already
        for area in context.screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                        if space.region_3d.view_perspective != 'CAMERA':
                            space.region_3d.view_perspective = 'CAMERA'
                        break
                break

        self.report({'INFO'}, f"Camera: {cameras[idx].name}")
        return {'FINISHED'}


class CAMCYCLER_OT_toggle_lock(bpy.types.Operator):
    bl_idname = "camcycler.toggle_lock"
    bl_label = "Toggle Camera Lock"
    bl_description = "Toggle lock that allows view navigation within the camera"
    bl_options = {'REGISTER'}

    def execute(self, context):
        space = context.space_data
        if space and space.type == 'VIEW_3D':
            space.lock_camera = not space.lock_camera
            state = "ON" if space.lock_camera else "OFF"
            self.report({'INFO'}, f"Camera lock: {state}")
            return {'FINISHED'}
        self.report({'WARNING'}, "Not in a 3D viewport")
        return {'CANCELLED'}


class CAMCYCLER_Preferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    def draw(self, context):
        layout = self.layout
        layout.label(text="Keymap:")
        col = layout.column()

        wm = bpy.context.window_manager
        kc = wm.keyconfigs.user
        km = kc.keymaps.get('3D View')
        if km:
            for kmi in km.keymap_items:
                if kmi.idname in (
                    CAMCYCLER_OT_next_camera.bl_idname,
                    CAMCYCLER_OT_toggle_lock.bl_idname,
                ):
                    col.context_pointer_set("keymap", km)
                    rna_keymap_ui.draw_kmi([], kc, km, kmi, col, 0)


addon_keymaps = []


# Lazy import — rna_keymap_ui ships with Blender but is not a top-level module
rna_keymap_ui = None


def _ensure_keymap_ui():
    global rna_keymap_ui
    if rna_keymap_ui is None:
        import rna_keymap_ui as _mod
        rna_keymap_ui = _mod


def register():
    _ensure_keymap_ui()

    bpy.utils.register_class(CAMCYCLER_OT_next_camera)
    bpy.utils.register_class(CAMCYCLER_OT_toggle_lock)
    bpy.utils.register_class(CAMCYCLER_Preferences)

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')

        kmi = km.keymap_items.new(
            CAMCYCLER_OT_next_camera.bl_idname,
            type='NUMPAD_0', value='PRESS', shift=True,
        )
        addon_keymaps.append((km, kmi))

        kmi = km.keymap_items.new(
            CAMCYCLER_OT_toggle_lock.bl_idname,
            type='L', value='PRESS', ctrl=True, shift=True,
        )
        addon_keymaps.append((km, kmi))


def unregister():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    bpy.utils.unregister_class(CAMCYCLER_Preferences)
    bpy.utils.unregister_class(CAMCYCLER_OT_toggle_lock)
    bpy.utils.unregister_class(CAMCYCLER_OT_next_camera)


if __name__ == "__main__":
    register()
