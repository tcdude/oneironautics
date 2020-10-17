import random

from panda3d import core
from direct.showbase.DirectObject import DirectObject

from .player import Player
from .room import Room


START_ROOM = 'starterella'


class World(DirectObject):
    def __init__(self):
        super().__init__()
        self.root = base.render.attach_new_node('World')

        room_names = [
            'cylinderella',
            'looperella',
            'plusserella',
            'spherella',
            'spirella',
            'starterella',
            'stepperella',
        ]
        self.rooms = {}
        for room_name in room_names:
            room_filename = 'models/rooms/'+room_name+'.bam'
            room_model = loader.load_model(room_filename)
            room_model.name = room_name
            room_model.clear_transform()
            self.rooms[room_name] = Room(room_model)

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
        self.active_room.root.clear_transform()
        self.active_room.room_model.clear_transform()
        door_mat = door.get_mat(render)
        door_mat_inv = core.LMatrix4f(door_mat)
        #print('invert', door_mat_inv.invert_in_place())
        self.active_room.room_model.clear_transform()
        self.active_room.room_model.set_mat(render, door_mat_inv)

        self.player.pivot.clear_transform()
        base.cam.clear_transform()
        self.player.root.clear_transform()
        self.player.root_target.clear_transform()
        #if not door.get_mat(render).is_identity():
        #    print(door.get_mat(render))
        #print(door.get_mat(render).is_identity(), self.player.root.get_mat(render).is_identity())
        self.player.teleported = True

    def update(self, task):
        self.player.update()
        for i in self.rooms.values():
            i.update()
        return task.cont
