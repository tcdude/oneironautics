from panda3d import core
from direct.showbase.DirectObject import DirectObject

from .player import Player
from .room import Room
from .util import load_shader_str, calculate_oblique_matrix, sign


class World(DirectObject):
    def __init__(self):
        super().__init__()
        self.root = base.render.attach_new_node('World')
        self.room = Room()
        rooms = loader.load_model('assets/models/rooms.blend')
        self.rooms = rooms.find('**/room_a')
        self.rooms.reparent_to(self.root)
        self.root.clear_light()
        self.door = self.rooms.find('**/door*')
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

        self.mask = core.BitMask32(0x1)
        self.nav = self.rooms.find("**/nav*")
        #self.nav.hide()
        self.nav.set_collide_mask(self.mask)

        base.taskMgr.add(self.update)

        self.player = Player(self)

        fov = base.cam.node().get_lens().get_fov()
        print(fov, self.room.cam.node().get_lens().get_fov())
        self.room.cam.node().get_lens().set_fov(fov)

        # Trying to achieve oblique near plane clipping with a custom lens...
        #self.rclens = core.MatrixLens()
        #self.rclens.user_mat = self.room.cam.node().get_lens().get_projection_mat()
        #self.room.cam.node().set_lens(self.rclens)
        #self.room.cam.node().get_lens().set_near_far(0.001, 100000)

        # Enable to see the output from the room cam
        #cmk = core.CardMaker('mycard')
        #cmk.set_frame(0, 1, 0, 1)
        #self.debug_view = base.aspect2d.attach_new_node(cmk.generate())
        #self.debug_view.set_texture(self.room.mytex)
        self.hinge = self.door.attach_new_node('the hinge')
        self.hinge.set_h(180)
        self.outside = self.hinge.attach_new_node('the other side')

    def update(self, task):
        self.player.update()
        self.stupid_fake_portal()

        # Matrix transform attempt
        #quat = base.camera.get_quat(self.door)
        #self.room.cam.set_quat(self.room.portal_in, quat)
        #mat = base.camera.get_mat(self.door)
        #self.room.cam.set_mat(self.room.portal_in, mat)

        # Hinged Node attempt
        #self.outside.set_pos(base.camera.get_pos(self.door))
        #self.outside.set_quat(base.camera.get_quat(self.door))
        #quat = self.outside.get_quat(self.door)
        #self.room.cam.set_quat(self.room.door, quat)
        #loc = self.outside.get_mat(self.door)
        #self.room.cam.set_mat(self.room.door, loc)

        #self.set_near_clip_plane()
        return task.cont

    def stupid_fake_portal(self):
        self.outside.set_pos(base.camera.get_pos(self.door))
        self.outside.set_quat(base.camera.get_quat(self.door))
        quat = self.outside.get_quat(self.door)
        self.room.cam.set_quat(self.room.door, quat)
        direction = self.outside.get_pos(self.door)
        direction.x = max(-0.75, min(0.75, direction.x))
        self.room.cam.set_pos(self.room.door, (-direction.x, 0, 2.5))

    def set_near_clip_plane(self):
        fw = self.room.door.get_quat(self.room.root).get_forward()
        camvec = self.room.cam.get_pos(self.room.door)
        dot = sign(fw.dot(camvec))

        world_cam_mat = self.room.cam.get_mat(self.room.root)
        cam_space_pos = world_cam_mat.xform(self.room.door.get_pos(self.room.root))
        cam_space_normal = world_cam_mat.xform(fw) * dot
        cam_space_dst = -cam_space_pos.dot(cam_space_normal)# + 0.05

        self.rclens.user_mat = calculate_oblique_matrix(
            base.cam.node().get_lens().get_projection_mat(),
            core.Vec4(cam_space_normal.x, cam_space_normal.y, cam_space_normal.z, cam_space_dst))
