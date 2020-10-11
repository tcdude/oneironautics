#version 130

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

void main() {
    // Switch between entire texture for fake version and screen space version
    vec2 uv = vec2(1.0f) - l_texcoord; // vtx_pos.xy / vtx_pos.w;
    //uv = normalize(noised(uv + osg_FrameTime).yz);
    vec4 tex_color = texture(p3d_Texture0, uv);
    color = tex_color;
}
