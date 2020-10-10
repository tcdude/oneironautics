from panda3d import core


class Room:
    def __init__(self):
        self.root = core.NodePath('Room')
        self.root.set_shader_auto(True)
        self.buff = base.win.make_texture_buffer('Room Buffer', 2048, 2048)

        self.mytex = self.buff.get_texture()
        self.mytex.set_wrap_u(core.Texture.WM_clamp)
        self.mytex.set_wrap_v(core.Texture.WM_clamp)
        self.buff.set_sort(-100)
        self.cam = base.make_camera(self.buff)
        self.cam.reparent_to(self.root)
        rooms = loader.load_model('assets/models/rooms.blend')
        self.room = rooms.find('**/room_b')
        self.room.reparent_to(self.root)
        self.room.clear_light()
        self.door = self.room.find('**/door*')
        self.portal_in = self.door.attach_new_node('portal')
        self.portal_in.set_h(180)
