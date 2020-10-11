#version 130

in vec4 vtx_pos;
in vec2 l_texcoord;

uniform sampler2D p3d_Texture0;

out vec4 color;

void main() {
    // Switch between entire texture for fake version and screen space version
    vec2 uv = vec2(1.0f) - l_texcoord // vtx_pos.xy / vtx_pos.w;
    vec4 tex_color = texture(p3d_Texture0, uv);
    color = tex_color;
}
