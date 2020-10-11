from panda3d import core


class Portal:
    def __init__(self, this_room, this_door, conn_room=None, conn_door=None):
        self.this_door = this_door
        self.this_room = this_room
        self.conn_door = conn_door
        self.conn_room = conn_room
        self.buff = base.win.make_texture_buffer('Room Buffer', 1024, 1024)

        self.mytex = self.buff.get_texture()
        self.mytex.set_wrap_u(core.Texture.WM_clamp)
        self.mytex.set_wrap_v(core.Texture.WM_clamp)
        self.buff.set_sort(-100)
        self.cam = base.make_camera(self.buff)
        self.cam.reparent_to(self.this_room.root)

        self.hinge = self.this_door.attach_new_node('hinge')
        self.hinge.set_h(180)
        self.outside_in = self.hinge.attach_new_node('lookin_in')

        self._active = False
        self.deactivate()
        self._collision_quad = core.CollisionPolygon(
            core.Point3(0.75, 0, 0), core.Point3(-0.75, 0, 0),
            core.Point3(-0.75, 0, 2.5), core.Point3(0.75, 0, 2.5))
        cnode = core.CollisionNode(f'{self.this_room.name}_{self.this_door.name}')
        cnode.add_solid(self._collision_quad)
        self.collider = self.this_door.attach_new_node(cnode)
        self.collider.set_pos(self.this_door, (0,0.05,0))
        self.collider.set_hpr(self.this_door, (0,0,0))
        #self.collider.show()
        self.collider.set_collide_mask(core.BitMask32(0x2))

    def activate(self):
        self.cam.node().set_active(False)
        self._active = True
        self.this_door.show()

    def deactivate(self):
        self.cam.node().set_active(True)
        self.cam.node().get_lens().set_fov(base.cam.node().get_lens().get_fov())
        self._active = False
        self.this_door.hide()

    def connect_to(self, room, door):
        self.conn_room = room
        self.conn_door = door
        for i in self.conn_door.find_all_texture_stages():
            self.conn_door.set_texture(i, self.mytex, 1)

    def update(self):
        if self._active or self.conn_room is None:
            return
        self.outside_in.set_quat(base.camera.get_quat(self.conn_door))
        self.outside_in.set_pos(base.camera.get_pos(self.conn_door))
        quat = self.outside_in.get_quat(self.this_door)
        self.cam.set_quat(self.this_door, quat)
        direction = self.outside_in.get_pos(self.conn_door)
        direction.x = max(-0.75, min(0.75, direction.x))
        self.cam.set_pos(self.this_door, (-direction.x, 0, 2.5))
