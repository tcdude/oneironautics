#version 130
#define TAU 6.28318530718
#define MAX_ITER 5

in vec4 vtx_pos;
in vec2 l_texcoord;

uniform sampler2D p3d_Texture0;
uniform float osg_FrameTime;

out vec4 color;

// from iq - https://www.shadertoy.com/view/XdXBRH
vec2 hash(in vec2 x)// replace this by something better
{
    const vec2 k=vec2(.3183099,.3678794);
    x=x*k+k.yx;
    return-1.+2.*fract(16.*k*fract(x.x*x.y*(x.x+x.y)));
}

// from iq - https://www.shadertoy.com/view/XdXBRH
vec3 noised(in vec2 p)
{
    vec2 i=floor(p);
    vec2 f=fract(p);

    vec2 u=f*f*f*(f*(f*6.-15.)+10.);
    vec2 du=30.*f*f*(f*(f-2.)+1.);

    vec2 ga=hash(i+vec2(0.,0.));
    vec2 gb=hash(i+vec2(1.,0.));
    vec2 gc=hash(i+vec2(0.,1.));
    vec2 gd=hash(i+vec2(1.,1.));

    float va=dot(ga,f-vec2(0.,0.));
    float vb=dot(gb,f-vec2(1.,0.));
    float vc=dot(gc,f-vec2(0.,1.));
    float vd=dot(gd,f-vec2(1.,1.));

    return vec3(va+u.x*(vb-va)+u.y*(vc-va)+u.x*u.y*(va-vb-vc+vd),// value
    ga+u.x*(gb-ga)+u.y*(gc-ga)+u.x*u.y*(ga-gb-gc+gd)+// derivatives
    du*(u.yx*(va-vb-vc+vd)+vec2(vb,vc)-va));
}

float heart2D( vec2 p )
{
    p *= 0.5;
    p.x = abs(p.x);
    p.y = -0.15 -p.y*1.2 + p.x*(1.0-p.x);
    return length(p) - 0.4;
}


void main() {
    // Switch between entire texture for fake version and screen space version
    vec2 uv = vec2(1.0f) - l_texcoord; // vtx_pos.xy / vtx_pos.w;
    //float a = clamp(sign(heart2D(uv * 2.0f - 1.0f)), -1.0f, 0.0f) * -1.0f;//clamp(sign(length(l_texcoord - 0.5f) - 0.5f), -1.0f, 0.0f) * -1.0f;
    float a = heart2D(uv * 2.0f - 1.0f);
    //vec3 n = normalize(noised(uv + osg_FrameTime * 0.3));
    vec2 d = normalize(noised(uv + osg_FrameTime * 0.1).yz);
    uv = smoothstep(0.0f, 1.0f, uv + d * 0.05);
    vec4 tex_color = texture(p3d_Texture0, uv);
    //tex_color.rgb += n / 3.0f;
    //tex_color.rgb /= 1.3f;
    //tex_color.rgb += clamp(vec3(pow(n.x, 0.5f)), 0.0f, 1.0f);
    //tex_color.rgb = smoothstep(0.0f, 1.0f, tex_color.rgb);
    vec4 bgcolor = vec4(0.0f);
    color = mix(tex_color, bgcolor, clamp(a / 0.03f, 0.0f, 1.0f)); // * a;
    float time = osg_FrameTime * 0.5f + 23.0f;
    vec2 p = mod(uv * TAU, TAU) - 250.0;
    vec2 i = vec2(p);
    float c = 1.0;
	float inten = .005;

	for (int n = 0; n < MAX_ITER; n++)
	{
		float t = time * (1.0 - (3.5 / float(n+1)));
		i = p + vec2(cos(t - i.x) + sin(t + i.y), sin(t - i.y) + cos(t + i.x));
		c += 1.0/length(vec2(p.x / (sin(i.x+t)/inten),p.y / (cos(i.y+t)/inten)));
	}
	c /= float(MAX_ITER);
	c = 1.17-pow(c, 1.4);
	vec3 colour = vec3(pow(abs(c), 8.0));
    colour = clamp(colour + color.rgb, 0.0, 1.0);

    color = vec4(colour, color.a);
    //color.a = a;
}
