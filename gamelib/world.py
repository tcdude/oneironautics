import random

from panda3d import core
from direct.showbase.DirectObject import DirectObject

from .player import Player
from .room import Room


START_ROOM = 'room_a'


class World(DirectObject):
    def __init__(self):
        super().__init__()
        self.root = base.render.attach_new_node('World')
        rooms = loader.load_model('assets/models/rooms.blend')
        self.room_models = {i.name: i for i in rooms.find_all_matches('**/room*')}
        for i in self.room_models.values():
            i.clear_transform()
        self.rooms = {i: Room(self.room_models[i]) for i in self.room_models}

        self.mask = core.BitMask32(0x1)
        self.nav = None

        self.active_room = None
        self.set_active_room(START_ROOM)

        self.player = Player(self)
        self.last_teleport = 0

        base.taskMgr.add(self.update)

    def set_active_room(self, room_name):
        if self.active_room is not None:
            self.active_room.deactivate()
            self.active_room.root.detach_node()
            self.nav.set_collide_mask(0x0)
        self.active_room = self.rooms[room_name]
        self.active_room.root.reparent_to(self.root)
        self.active_room.activate()
        self.nav = self.active_room.room_model.find("**/nav*")
        #self.nav.hide()
        self.nav.set_collide_mask(self.mask)

        # randomize portal connections
        rooms = list(self.rooms)
        rooms.pop(rooms.index(room_name))
        for i, room in enumerate(random.sample(rooms, len(self.active_room))):
            door = self.active_room.doors[i]
            doori = random.randrange(len(self.rooms[room].doors))
            portal = self.rooms[room][doori]
            portal.connect_to(self.active_room, door)
            self.accept(f'into-{self.active_room[i].collider.name}', self.teleport)
            self.active_room[i].collider.set_python_tag('portal', portal)
            self.active_room[i].collider.set_python_tag('door', doori)

    def teleport(self, coll_entry):
        t = globalClock.frame_time
        if t - self.last_teleport < 0.5:
            return
        self.last_teleport = t
        np = coll_entry.get_into_node_path()
        self.set_active_room(np.get_python_tag('portal').this_room.name)
        door = self.active_room.doors[np.get_python_tag('door')]

        self.player.root.set_mat(render, door.get_mat(render))
        self.player.pivot.clear_transform()
        #self.player.update()
        #self.player.xyh_inertia = core.Vec3(0)
        print('teleport', door.get_hpr(render), self.player.root.get_pos(render),
            self.player.root.get_hpr(render), self.player.root.get_pos(door),
            self.player.root.get_hpr(door))
        self.player.teleported = True

    def update(self, task):
        self.player.update()
        for i in self.rooms.values():
            i.update()
        return task.cont
