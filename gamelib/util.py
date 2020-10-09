from panda3d import core

def srgb_color(color, alpha = 255):
    if isinstance(color, str):
        color = int(color.lstrip('#'), 16)

    return core.LColor(
        core.decode_sRGB_float((color >> 16) & 0xff),
        core.decode_sRGB_float((color >> 8) & 0xff),
        core.decode_sRGB_float(color & 0xff),
        alpha / 255.0)


def _add_shader_defines(shaderstr, defines):
    shaderlines = shaderstr.split('\n')

    for line in shaderlines:
        if '#version' in line:
            version_line = line
            break
    else:
        raise RuntimeError('Failed to find GLSL version string')
    shaderlines.remove(version_line)


    define_lines = [
        f'#define {define} {value}'
        for define, value in defines.items()
    ]

    return '\n'.join(
        [version_line]
        + define_lines
        + ['#line 1']
        + shaderlines
    )


def load_shader_str(shadername, defines=None):
    shaderpath = core.Filename.expand_from(f'$MAIN_DIR/shaders/{shadername}').to_os_specific()

    with open(shaderpath) as shaderfile:
        shaderstr = shaderfile.read()

    if defines is not None:
        shaderstr = _add_shader_defines(shaderstr, defines)

    return shaderstr
