import sys

from direct.showbase.ShowBase import ShowBase

from panda3d import core
import pman.shim
from gamelib import simplematcap

from gamelib import util
from gamelib.world import World
from gamelib.input import Input

core.load_prc_file(
    core.Filename.expand_from('$MAIN_DIR/settings.prc')
)

USER_CONFIG_PATH = core.Filename.expand_from(
    '$MAIN_DIR/user.prc'
)
if USER_CONFIG_PATH.exists():
    core.load_prc_file(USER_CONFIG_PATH)


def load_shader_str(shadername, defines=None):
    shaderpath = core.Filename.expand_from(f'$MAIN_DIR/shaders/{shadername}').to_os_specific()

    with open(shaderpath) as shaderfile:
        shaderstr = shaderfile.read()
    return shaderstr


class GameApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        pman.shim.init(self)
        basic = core.Filename.expand_from('$MAIN_DIR/assets/textures/basic_1.exr')
        basic = self.loader.load_texture(basic)
        pipeline = simplematcap.init(basic, render_node=self.render, light_dir=core.Vec3(-1, -1, 0.5).normalized())

        fog = core.Fog("Fog Name")
        fog.set_color(0, 0, 0)
        fog.set_exp_density(0.06)
        self.render.set_fog(fog)
        self.disable_mouse()
        self.input = Input()
        self.accept('escape', sys.exit)
        self.accept('f1', self.toggle_wireframe)
        self.world = World(pipeline)
        self.set_background_color(util.srgb_color(0x000000))


def main():
    app = GameApp()
    app.run()

if __name__ == '__main__':
    main()
