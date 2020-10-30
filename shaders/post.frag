#version 130

uniform sampler2D p3d_Texture0;
uniform sampler2D depth;
//uniform sampler2D bg;
uniform float blur;

in vec2 texcoord;

out vec4 color;


vec3 rgb2hsv(vec3 c)
{
    vec4 K = vec4(0.0, -1.0 / 3.0, 2.0 / 3.0, -1.0);
    vec4 p = mix(vec4(c.bg, K.wz), vec4(c.gb, K.xy), step(c.b, c.g));
    vec4 q = mix(vec4(p.xyw, c.r), vec4(c.r, p.yzx), step(p.x, c.r));

    float d = q.x - min(q.w, q.y);
    float e = 1.0e-10;
    return clamp(vec3(abs(q.z + (q.w - q.y) / (6.0 * d + e)), d / (q.x + e), q.x), 0.0, 1.0);
}


void main() {
    vec2 pixel = vec2(1.0, 1.0) / textureSize(p3d_Texture0, 0).xy;
    vec2 sharp = pixel * blur;

    vec4 out_tex = texture2D(p3d_Texture0, texcoord);
    sharp *= out_tex.a;
    float d = texture2D(depth, texcoord).x;
    sharp *= 0.2 + pow(d * 0.7, 2.0);

    //Hardcoded blur
    out_tex += texture2D(p3d_Texture0, texcoord + vec2(-0.326212,-0.405805) * sharp);
    out_tex += texture2D(p3d_Texture0, texcoord + vec2(-0.840144, -0.073580) * sharp);
    out_tex += texture2D(p3d_Texture0, texcoord + vec2(-0.695914, 0.457137) * sharp);
    out_tex += texture2D(p3d_Texture0, texcoord + vec2(-0.203345, 0.620716) * sharp);
    out_tex += texture2D(p3d_Texture0, texcoord + vec2(0.962340, -0.194983) * sharp);
    out_tex += texture2D(p3d_Texture0, texcoord + vec2(0.473434, -0.480026) * sharp);
    out_tex += texture2D(p3d_Texture0, texcoord + vec2(0.519456, 0.767022) * sharp);
    out_tex += texture2D(p3d_Texture0, texcoord + vec2(0.185461, -0.893124) * sharp);
    out_tex += texture2D(p3d_Texture0, texcoord + vec2(0.507431, 0.064425) * sharp);
    out_tex += texture2D(p3d_Texture0, texcoord + vec2(0.896420, 0.412458) * sharp);
    out_tex += texture2D(p3d_Texture0, texcoord + vec2(-0.321940, -0.932615) * sharp);
    out_tex += texture2D(p3d_Texture0, texcoord + vec2(-0.791559, -0.597705) * sharp);
    out_tex /= 13.0;

    out_tex.a = 1.0;

    //vec4 bgc = texture2D(bg, texcoord);
    //float d = 1.0 - clamp(texture2D(depth, texcoord).x, 0.0, 1.0);
    //vec3 hsv = rgb2hsv(smoothstep(0.0, 2.2, out_tex.rgb));
    //if (hsv.z < 0.000000001) {
    //    out_tex.rgb = bgc.rgb * 0.1;
    //}
    //c.rgb = mix(c.rgb, bgc.rgb, d < 0.1 ? 1.0 : 0.0);
    //color = vec4(vec3(d), 1.0);

    color = out_tex;
}
