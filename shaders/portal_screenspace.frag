#version 130

in vec4 vtx_pos;
in vec2 l_texcoord;

uniform sampler2D p3d_Texture0;

out vec4 color;

float dist(vec2 p, float r) {
    vec2 a = abs(p - 0.5f);
    float d = max(a.x, a.y) - (0.5f - r);
    d = clamp(d, 0.0f, r) / r;
    return d;
}


void main() {
    vec2 uv = vtx_pos.xy / vtx_pos.w;
    uv = uv / 2.0f + 0.5f;
    vec4 fgcolor = texture(p3d_Texture0, uv);
    vec4 bgcolor = vec4(0.0f);
    color = mix(fgcolor, bgcolor, dist(l_texcoord, 0.01));
}
