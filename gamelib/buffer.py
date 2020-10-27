from dataclasses import dataclass

from panda3d import core
import simplematcap


@dataclass
class BufferObject:
    buff:core.GraphicsBuffer
    tex:core.Texture
    cam:core.NodePath
    pipeline:simplematcap.Pipeline


_free_buffers:BufferObject = []


def get_buffer(render_node, buff_size=None, clear_color=core.Vec4(0, 0, 0, 1)):
    buff_size = buff_size or core.ConfigVariableInt('portal-buffer-size', 1024).get_value()
    if _free_buffers:
        bobj = _free_buffers.pop()
        bobj.pipeline.render_node = render_node
        bobj.cam.reparent_to(render_node)
        return bobj
    basic = core.Filename.expand_from('$MAIN_DIR/assets/textures/basic_1.exr')
    basic = loader.load_texture(basic)
    buff = base.win.make_texture_buffer('Room Buffer', buff_size, buff_size)
    buff.set_clear_color(clear_color)
    buff.set_clear_color_active(True)
    buff.set_sort(-100)
    tex = buff.get_texture()
    cam = base.make_camera(buff)
    cam.reparent_to(render_node)
    pipeline = simplematcap.init(
        basic,
        render_node=render_node,
        light_dir=core.Vec3(-1, -1, 0.5).normalized()
    )
    return BufferObject(buff, tex, cam, pipeline)


def release_buffer(buffer):
    _free_buffers.append(buffer)
