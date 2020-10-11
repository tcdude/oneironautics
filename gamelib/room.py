from panda3d import core

from .portal import Portal
from .util import load_shader_str


class Room:
    def __init__(self, room):
        self.root = core.NodePath('Room')
        self.room_model = room
        self.room_model.reparent_to(self.root)
        self.name = room.name
        
        self.doors = [
            i for i in self.room_model.find_all_matches('**/door*')
        ]
        self.portals = [
            Portal(self, i) for i in self.doors
        ]

        portal_vert_str = load_shader_str('portal.vert')
        portal_frag_str = load_shader_str('portal.frag')
        portalshader = core.Shader.make(
            core.Shader.SL_GLSL,
            vertex=portal_vert_str,
            fragment=portal_frag_str,
        )
        for i in self.doors:
            i.set_shader(portalshader)
        self._active = False

    def activate(self):
        self._active = True
        for i in self.portals:
            i.activate()

    def deactivate(self):
        self._active = False
        for i in self.portals:
            i.deactivate()

    def update(self):
        for i in self.portals:
            i.update()

    def __len__(self):
        return len(self.portals)

    def __getitem__(self, item):
        return self.portals[item]
