import sys

from direct.showbase.ShowBase import ShowBase

import panda3d
from panda3d.core import WindowProperties
import pman.shim

from gamelib import util
from gamelib.world import World
from gamelib.input import Input

panda3d.core.load_prc_file(
    panda3d.core.Filename.expand_from('$MAIN_DIR/settings.prc')
)

USER_CONFIG_PATH = panda3d.core.Filename.expand_from(
    '$MAIN_DIR/user.prc'
)
if USER_CONFIG_PATH.exists():
    panda3d.core.load_prc_file(USER_CONFIG_PATH)


class GameApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        pman.shim.init(self)
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
