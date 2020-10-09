import sys

from direct.showbase.ShowBase import ShowBase
import panda3d
import pman.shim

from gamelib import util
from gamelib.world import World


panda3d.core.load_prc_file(
    panda3d.core.Filename.expand_from('$MAIN_DIR/settings.prc')
)


class GameApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        pman.shim.init(self)
        self.disable_mouse()
        self.accept('escape', sys.exit)
        self.world = World()
        self.set_background_color(util.srgb_color(0x292931))


def main():
    app = GameApp()
    app.run()

if __name__ == '__main__':
    main()
