import os

from panda3d import core


__all__ = [
    'init',
    'Pipeline'
]


def _load_shader_str(shaderpath):
    shader_dir = core.Filename.expand_from(f'$MAIN_DIR/shaders/')

    with open(os.path.join(shader_dir, shaderpath)) as shaderfile:
        shaderstr = shaderfile.read()

    return shaderstr


class Pipeline:
    def __init__(
            self,
            default_matcap:core.Texture,
            *,
            render_node:core.NodePath = None,
            light_dir:core.Vec3 = None,
            hueshift:core.Vec3 = None,
    ):
        self._default_matcap = default_matcap

        if render_node is None:
            render_node = base.render

        if light_dir is None:
            self._light_dir = core.PTA_float(core.Vec3(-1).normalized())
        else:
            self._light_dir = core.PTA_float(light_dir.normalized())

        if hueshift is None:
            hueshift = core.Vec3(0)

        self._hueshift = hueshift

        self._render_node = render_node

        # Do not force power-of-two textures
        core.Texture.set_textures_power_2(core.ATS_none)

        # Matcap Shader
        self._recompile_matcap()

    @property
    def default_matcap(self) -> core.Texture:
        return self._default_matcap

    @default_matcap.setter
    def default_matcap(self, value:core.Texture) -> None:
        self._default_matcap = value
        self._recompile_matcap()

    @property
    def render_node(self) -> core.NodePath:
        return self._render_node

    @render_node.setter
    def render_node(self, value:core.NodePath) -> None:
        self._render_node = value
        self._recompile_matcap()

    @property
    def light_dir(self) -> core.Vec3:
        return core.Vec3(*[i for i in self._light_dir])

    @light_dir.setter
    def light_dir(self, value:core.Vec3) -> None:
        for i, j in enumerate(value.normalized()):
            self._light_dir[i] = j
        self._recompile_matcap()

    @property
    def hueshift(self) -> core.Vec3:
        return self._hueshift

    @hueshift.setter
    def hueshift(self, value:core.Vec3) -> None:
        self._hueshift = value
        self._recompile_matcap()

    def _recompile_matcap(self):
        matcap_vert_str = _load_shader_str('matcap.vert')
        matcap_frag_str = _load_shader_str('matcap.frag')
        matcapshader = core.Shader.make(
            core.Shader.SL_GLSL,
            vertex=matcap_vert_str,
            fragment=matcap_frag_str,
        )
        self._render_node.set_shader(matcapshader)
        self._render_node.set_shader_input('matcap', self._default_matcap)
        self._render_node.set_shader_input('light_dir', self._light_dir)
        self._render_node.set_shader_input('hueshift', self._hueshift)


def init(default_matcap:core.Texture, *, render_node:core.NodePath = None, light_dir:core.Vec3 = None, hueshift:core.Vec3 = None):
    '''Initialize the Matcap render pipeline
    :param default_matcap: The default matcap to apply
    :type default_matcap: `panda3d.core.Texture`
    :param render_node: The node to attach the shader too, defaults to `base.render` if `None`
    :type render_node: `panda3d.core.NodePath`
    :param light_dir: The light direction, which will be used to apply the matcap, defaults to
        `Vec3(-0.57735, -0.57735, -0.57735)`
    :type light_dir: `panda3d.core.Vec3`
    '''

    return Pipeline(default_matcap, render_node=render_node, light_dir=light_dir, hueshift=hueshift)
