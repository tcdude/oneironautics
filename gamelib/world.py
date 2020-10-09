from panda3d import core
from direct.showbase.DirectObject import DirectObject

from .room import Room
from .util import load_shader_str

SPEED = 300
CAM_SPEED = 800


class World(DirectObject):
    def __init__(self):
        super().__init__()
        self.root = base.render.attach_new_node('World')
        self.room = Room()
        rooms = loader.load_model('assets/rooms.blend')
        self.rooms = rooms.find('**/room_a')
        self.rooms.reparent_to(self.root)
        self.root.clear_light()
        self.door = self.rooms.find('**/door*')
        self.door_focus = self.door.attach_new_node('door focus')
        self.door_focus.set_pos(0, 0, 1.5)

        for i in self.door.find_all_texture_stages():
            self.door.set_texture(i, self.room.mytex, 1)

        portal_vert_str = load_shader_str('portal.vert')
        portal_frag_str = load_shader_str('portal.frag')
        portalshader = core.Shader.make(
            core.Shader.SL_GLSL,
            vertex=portal_vert_str,
            fragment=portal_frag_str,
        )
        self.door.set_shader(portalshader)

        self.rooms.set_pos(0, 0, 0)
        base.camera.reparent_to(self.root)
        base.camera.set_pos(0, 5, 2)
        base.camera.look_at(self.door)

        self.accept('w-repeat', self.move, [core.Vec3(0, 1, 0)])
        self.accept('s-repeat', self.move, [core.Vec3(0, -1, 0)])
        self.accept('a-repeat', self.move, [core.Vec3(-1, 0, 0)])
        self.accept('d-repeat', self.move, [core.Vec3(1, 0, 0)])
        self.accept('arrow_up-repeat', self.move, [core.Vec3(0, 0, 1)])
        self.accept('arrow_down-repeat', self.move, [core.Vec3(0, 0, -1)])
        self.accept('arrow_left-repeat', self.rotate, [1])
        self.accept('arrow_right-repeat', self.rotate, [-1])

        fov = base.cam.node().get_lens().get_fov()
        print(fov, self.room.cam.node().get_lens().get_fov())
        self.room.cam.node().get_lens().set_fov(fov)
        base.taskMgr.add(self.update)

    def move(self, direction):
        base.camera.set_pos(base.camera, direction * SPEED * globalClock.dt)

    def rotate(self, direction):
        base.camera.set_h(base.camera, direction * CAM_SPEED * globalClock.dt)

    def update(self, task):
        loc = base.camera.get_mat(self.door_focus)
        self.room.cam.set_mat(self.room.door_focus, loc)
        return task.cont
