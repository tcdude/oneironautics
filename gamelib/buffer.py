from dataclasses import dataclass

from panda3d import core
import simplepbr


@dataclass
class BufferObject:
    buff:core.GraphicsBuffer
    tex:core.Texture
    cam:core.NodePath
    pipeline:simplepbr.Pipeline


_free_buffers:BufferObject = []


def get_buffer(render_node, buff_size=None, clear_color=0x000000):
    buff_size = buff_size or core.ConfigVariableInt('portal-buffer-size', 1024).get_value()
    if _free_buffers:
        bobj = _free_buffers.pop()
        bobj.pipeline.render_node = render_node
        bobj.cam.reparent_to(render_node)
        return bobj
    buff = base.win.make_texture_buffer('Room Buffer', buff_size, buff_size)
    buff.set_clear_color(clear_color)
    buff.set_sort(-100)
    tex = buff.get_texture()
    cam = base.make_camera(buff)
    cam.reparent_to(render_node)
    pipeline = simplepbr.init(
        render_node=render_node,
        window=buff,
        camera_node=cam,
        use_emission_maps=False,
        max_lights=core.ConfigVariableInt('max-lights', 3).get_value(),
        enable_shadows=core.ConfigVariableBool('shadows-enabled', False).get_value(),
        msaa_samples=core.ConfigVariableInt('msaa-samples', 4).get_value(),
        exposure=core.ConfigVariableDouble('exposure', 0.9).get_value(),
    )
    return BufferObject(buff, tex, cam, pipeline)


def release_buffer(buffer):
    _free_buffers.append(buffer)
