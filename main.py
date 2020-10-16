import sys

from direct.showbase.ShowBase import ShowBase

from panda3d import core
import pman.shim
import simplepbr

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


class GameApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        pman.shim.init(self)
        simplepbr.init(
            use_emission_maps=False,
            max_lights=core.ConfigVariableInt('max-lights', 3).get_value(),
            enable_shadows=core.ConfigVariableBool('shadows-enabled', False).get_value(),
            msaa_samples=core.ConfigVariableInt('msaa-samples', 4).get_value(),
            exposure=core.ConfigVariableDouble('exposure', 0.9).get_value(),
        )
        self.disable_mouse()
        self.input = Input()
        self.accept('escape', sys.exit)
        self.accept('f1', self.toggle_wireframe)
        self.world = World()
        self.set_background_color(util.srgb_color(0x000000))


def main():
    app = GameApp()
    app.run()

if __name__ == '__main__':
    main()
