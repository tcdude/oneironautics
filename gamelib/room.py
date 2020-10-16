from panda3d import core

from .portal import Portal
from .util import load_shader_str


def process_vertex_data(vdata, read_only):
    if not read_only:
        texcoordw = core.GeomVertexWriter(vdata, 'texcoord.0')
    texcoord = core.GeomVertexReader(vdata, 'texcoord.0')
    vertex = core.GeomVertexReader(vdata, 'vertex')
    while not vertex.is_at_end():
        v = vertex.get_data3()
        t = texcoord.get_data2()
        if not read_only:
            t = texcoordw.set_data2(round(t[0], 0), round(t[1], 0))


def process_geom(geom):
    vdata = geom.modify_vertex_data()
    process_vertex_data(vdata, True)
    process_vertex_data(vdata, False)
    process_vertex_data(vdata, True)


def process_geom_node(geom_node):
    for i in range(geom_node.get_num_geoms()):
        geom = geom_node.modify_geom(i)
        process_geom(geom)


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

        for i in self.doors:
            i.set_transparency(core.TransparencyAttrib.M_alpha)
            i.set_alpha_scale(0.0)
            i.set_color(core.Vec4(0))
            for np in i.find_all_matches('**/+GeomNode'):
                geom_node = np.node()
                process_geom_node(geom_node)

        portal_vert_str = load_shader_str('portal.vert')
        portal_frag_str = load_shader_str('portal_heart_water.frag')
        portalshader = core.Shader.make(
            core.Shader.SL_GLSL,
            vertex=portal_vert_str,
            fragment=portal_frag_str,
        )
        for i in self.doors:
            i.set_shader(portalshader)
        self._active = False
        self.room_model.node().set_bounds(core.OmniBoundingVolume())
        self.room_model.node().set_final(True)

        for i in self.room_model.find_all_matches('**/Sun*/Sun*'):
            try:
                self.root.set_light(i)
            except AssertionError:
                pass

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
