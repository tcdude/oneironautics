#version 130

in vec4 vtx_pos;
in vec2 l_texcoord;

uniform sampler2D p3d_Texture0;

out vec4 color;

void main() {
    vec2 uv = clamp(vtx_pos.xy / vtx_pos.w, 0.0f, 1.0f);
    vec4 tex_color = texture(p3d_Texture0, uv);
    color = tex_color;
}
