import math
import sys

from direct.showbase.ShowBase import ShowBase
import panda3d
from panda3d import core
import pman.shim

from gamelib import renderer
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
        #self.luttex = self.load_lut('lut.png')
        #self.render_pipeline = renderer.Pipeline(lut_texture=self.luttex)
        #self.render.set_shader_inputs(uv_shift=(0.0, 0.0))

    def load_lut(self, filename):
        path = panda3d.core.Filename(filename)
        vfs = panda3d.core.VirtualFileSystem.get_global_ptr()
        failed = (
            not vfs.resolve_filename(path, panda3d.core.get_model_path().value)
            or not path.is_regular_file()
        )
        if failed:
            raise RuntimeError('Failed to find file {}'.format(filename))

        image = panda3d.core.PNMImage(path)

        lutdim = 64
        xsize, ysize = image.get_size()
        tiles_per_row = xsize // lutdim
        num_rows = math.ceil(lutdim / tiles_per_row)
        ysize -= num_rows * lutdim

        texture = panda3d.core.Texture()
        texture.setup_3d_texture(
            lutdim, lutdim, lutdim,
            panda3d.core.Texture.T_unsigned_byte,
            panda3d.core.Texture.F_rgb8
        )

        for tileidx in range(lutdim):
            xstart = tileidx % tiles_per_row * lutdim
            ystart = tileidx // tiles_per_row * lutdim + ysize
            islice = panda3d.core.PNMImage(lutdim, lutdim, 3, 255)
            islice.copy_sub_image(image, 0, 0, xstart, ystart, lutdim, lutdim)
            # XXX should write these values out correctly when saving/embedding
            islice.flip(False, True, False)
            texture.load(islice, tileidx, 0)
        return texture

def main():
    app = GameApp()
    app.run()

if __name__ == '__main__':
    main()
