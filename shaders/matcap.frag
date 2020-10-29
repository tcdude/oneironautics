#version 120

uniform sampler2D p3d_Texture0;
uniform sampler2D matcap;
uniform float hueshift;

varying vec3 vtx_pos;
varying vec4 vtx_color;
varying vec3 normal;
varying vec2 texcoord;
varying vec3 light;

vec3 rgb2hsv(vec3 c)
{
    vec4 K = vec4(0.0, -1.0 / 3.0, 2.0 / 3.0, -1.0);
    vec4 p = mix(vec4(c.bg, K.wz), vec4(c.gb, K.xy), step(c.b, c.g));
    vec4 q = mix(vec4(p.xyw, c.r), vec4(c.r, p.yzx), step(p.x, c.r));

    float d = q.x - min(q.w, q.y);
    float e = 1.0e-10;
    return clamp(vec3(abs(q.z + (q.w - q.y) / (6.0 * d + e)), d / (q.x + e), q.x), 0.0, 1.0);
}

vec3 hsv2rgb(vec3 c)
{
    vec4 K = vec4(1.0, 2.0 / 3.0, 1.0 / 3.0, 3.0);
    vec3 p = abs(fract(c.xxx + K.xyz) * 6.0 - K.www);
    return clamp(c.z * mix(K.xxx, clamp(p - K.xxx, 0.0, 1.0), c.y), 0.0, 1.0);
}


void main() {
    vec4 base_color = vtx_color * texture2D(p3d_Texture0, texcoord);
    base_color.rgb = rgb2hsv(smoothstep(0.0, 2.2, base_color.rgb));
    base_color.r = mod(base_color.r + hueshift, 1.0);
    base_color.rgb = hsv2rgb(base_color.rgb);
    vec3 n = normalize(normal);
    vec3 v = normalize(-vtx_pos.xyz);
    n = normalize(light + n + v);
    vec2 muv = n.xy * 0.5f + 0.5f;
    vec4 matcap_color = texture2D(matcap, vec2(1.0f - muv.x, muv.y));

    gl_FragColor = (base_color * (matcap_color * 2.0f)) * 2.2;
}