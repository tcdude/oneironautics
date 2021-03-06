from panda3d import core
import simplepbr

from . import buffer

BUFFER_SIZE = 1024


class Portal:
    def __init__(self, this_room, this_door, conn_room=None, conn_door=None):
        self.this_door = this_door
        self.this_room = this_room
        self.conn_door = conn_door
        self.conn_room = conn_room

        self.hinge = self.this_door.attach_new_node('hinge')
        self.hinge.set_h(180)
        self.outside_in = self.hinge.attach_new_node('lookin_in')

        self.buff = None

        self._active = False
        self.deactivate()
        self._collision_quad = core.CollisionPolygon(
            core.Point3(0.75, 0, 0), core.Point3(-0.75, 0, 0),
            core.Point3(-0.75, 0, 2.5), core.Point3(0.75, 0, 2.5))
        cnode = core.CollisionNode(f'{self.this_room.name}_{self.this_door.name}')
        cnode.add_solid(self._collision_quad)
        cnode.set_from_collide_mask(core.CollideMask.all_off())
        cnode.set_into_collide_mask(0x2)
        self.collider = self.this_door.attach_new_node(cnode)
        self.collider.set_pos(self.this_door, (0,0.05,0))
        self.collider.set_hpr(self.this_door, (0,0,0))
        #self.collider.show()
        self.collider.set_collide_mask(core.BitMask32(0x2))

    def activate(self):
        self._remove_buffer()
        self._active = True
        self.this_door.show()

    def deactivate(self):
        self._remove_buffer()
        self._active = False
        self.this_door.hide()

    def _remove_buffer(self):
        if self.buff is not None:
            self.buff.cam.node().set_active(False)
            buffer.release_buffer(self.buff)
            self.buff = None
            self.conn_room = None
            self.conn_door = None

    def connect_to(self, room, door):
        self._remove_buffer()
        self.conn_room = room
        self.conn_door = door
        self.buff = buffer.get_buffer(self.this_room.root)
        self.buff.cam.node().set_active(True)
        self.buff.cam.node().get_lens().set_fov(base.cam.node().get_lens().get_fov())
        for i in self.conn_door.find_all_texture_stages():
            self.conn_door.set_texture(i, self.buff.tex, 1)

    def update(self):
        if self._active or self.conn_room is None:
            return
        self.outside_in.set_quat(base.cam.get_quat(self.conn_door))
        self.outside_in.set_pos(base.cam.get_pos(self.conn_door))
        self.buff.cam.set_mat(self.hinge, self.outside_in.get_mat())
        return
