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


def sign(a):
    if a > 0:
        return 1
    if a < 0:
        return -1
    return 0


def calculate_oblique_matrix(projection_mat:core.LMatrix4f, clip_plane:core.Vec4):
    mat = core.LMatrix4f(projection_mat)
    mat_inv = core.LMatrix4f()
    mat_inv.invert_from(mat)
    #view_inv = core.LMatrix4f(view_mat)
    #view_inv.transpose_in_place()
    #clip_plane = view_inv.xform(clip_plane)

    #q = core.Vec4()
    #q.x = (sign(clip_plane.x) + mat[2][0]) / mat[0][0]
    #q.y = (sign(clip_plane.y) + mat[2][1]) / mat[1][1]
    #q.z = -1
    #q.w = (1 + mat[2][2]) / mat[3][2]

    q = mat.xform(core.Vec4(sign(clip_plane.x), sign(clip_plane.y), 1, 1))

    c = clip_plane * (2 / clip_plane.dot(q))

    mat[0][2] = c.x
    mat[1][2] = c.y
    mat[2][2] = c.z + 1
    mat[3][2] = c.w
    return mat


def clamp_angle(angle):
    while angle > 180:
        angle -= 180
    while angle < -180:
        angle += 180
    return angle
