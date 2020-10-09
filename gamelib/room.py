from panda3d import core


class Room:
    def __init__(self):
        self.root = core.NodePath('Room')
        self.buff = base.win.make_texture_buffer('Room Buffer', 2048, 2048)

        self.mytex = self.buff.get_texture()
        self.mytex.set_wrap_u(core.Texture.WM_clamp)
        self.mytex.set_wrap_v(core.Texture.WM_clamp)
        self.buff.set_sort(-100)
        self.cam = base.make_camera(self.buff)
        self.cam.reparent_to(self.root)
        self.cam.set_r(180)
        rooms = loader.load_model('assets/rooms.blend')
        self.room = rooms.find('**/room_b')
        self.room.reparent_to(self.root)
        self.room.clear_light()
        self.room.set_pos(0, 0, 0)
        self.door = self.room.find('**/door*')
        self.door.hide()
        self.door_focus = self.door.attach_new_node('door focus')
        self.door_focus.set_pos(0, 0, 1.5)
