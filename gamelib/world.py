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

        self.active_room = None
        self.set_active_room(START_ROOM)

        self.mask = core.BitMask32(0x1)
        self.nav = self.active_room.room_model.find("**/nav*")
        #self.nav.hide()
        self.nav.set_collide_mask(self.mask)

        self.player = Player(self)

        base.taskMgr.add(self.update)

    def set_active_room(self, room_name):
        if self.active_room is not None:
            self.active_room.deactivate()
            self.active_room.root.detach()
        self.active_room = self.rooms[room_name]
        self.active_room.root.reparent_to(self.root)
        self.active_room.activate()

        # randomize portal connections
        rooms = list(self.rooms)
        rooms.pop(rooms.index(room_name))
        for i, room in enumerate(random.sample(rooms, len(self.active_room))):
            door = self.active_room.doors[i]
            doori = random.randrange(len(self.rooms[room].doors))
            portal = self.rooms[room][doori]
            portal.connect_to(self.active_room, door)

    def update(self, task):
        self.player.update()
        for i in self.rooms.values():
            i.update()
        return task.cont
