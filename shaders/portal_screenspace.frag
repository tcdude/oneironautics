#version 130

in vec4 vtx_pos;
in vec2 l_texcoord;

uniform sampler2D p3d_Texture0;

out vec4 color;

void main() {
    vec2 uv = vtx_pos.xy / vtx_pos.w;
    uv = uv / 2.0f + 0.5f;
    color = texture(p3d_Texture0, uv);
}
