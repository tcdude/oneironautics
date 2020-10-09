#version 130

in vec4 vtx_pos;
in vec3 normal;
in vec2 l_texcoord;
in vec3 l_tangent;
in vec3 l_bitangent;
in vec4 l_eye_position;

uniform sampler2D normal_map;
uniform sampler2D gloss_map;
uniform vec4 p3d_ColorScale;
uniform sampler2D p3d_Texture0;
uniform struct {
  vec4 ambient;
  vec4 diffuse;
  vec4 emission;
  vec3 specular;
  float shininess;

  // These properties are new in 1.10.
  vec4 baseColor;
  float roughness;
  float metallic;
  float refractiveIndex;
} p3d_Material;

uniform struct {
  vec4 ambient;
} p3d_LightModel;

uniform struct p3d_LightSourceParameters {
  // Primary light color.
  vec4 color;

  // Light color broken up into components, for compatibility with legacy shaders.
  vec4 ambient;
  vec4 diffuse;
  vec4 specular;

  // View-space position.  If w=0, this is a directional light, with
  // the xyz being -direction.
  vec4 position;

  // Spotlight-only settings
  vec3 spotDirection;
  float spotExponent;
  float spotCutoff;
  float spotCosCutoff;

  // Individual attenuation constants
  float constantAttenuation;
  float linearAttenuation;
  float quadraticAttenuation;

  // constant, linear, quadratic attenuation in one vector
  vec3 attenuation;

  // Shadow map for this light source
  sampler2DShadow shadowMap;

  // Transforms view-space coordinates to shadow map coordinates
  mat4 shadowViewMatrix;
} p3d_LightSource[1];

out vec4 color;

void main() {
    /*vec4 normal_val = texture(normal_map, l_texcoord);
    vec4 gloss_val = texture(gloss_map, l_texcoord);

    vec3 ts_normal = (normal_val.xyz * 2.0) - 1.0;
    vec3 ts_eye_normal = normal.xyz * ts_normal.z;
    ts_eye_normal += l_tangent * ts_normal.x;
    ts_eye_normal += l_bitangent * ts_normal.y;
    ts_eye_normal = normalize(ts_eye_normal);

    vec4 tot_ambient = vec4(0.0);
    vec4 tot_diffuse = vec4(0.0);
    vec4 tot_specular = vec4(0.0);
    float shininess = p3d_Material.shininess;
    tot_ambient += p3d_LightModel.ambient;

    vec4 l_color = p3d_LightSource[0].color;
    vec4 l_specular = p3d_LightSource[0].color;
    vec3 l_vec = p3d_LightSource[0].position.xyz;
    l_color *= clamp(dot(ts_eye_normal, l_vec), 0.0, 1.0);
    tot_diffuse += l_color;
    vec3 l_half = normalize(l_vec - vec3(0.0, 1.0, 0.0));
    l_specular *= pow(clamp(dot(ts_eye_normal, l_half), 0.0, 1.0), shininess);
    tot_specular += l_specular;

    color = vec4(0.0);
    color += tot_ambient;
    color += tot_diffuse;
    color.rgb *= tex_color.rgb;
    color *= p3d_ColorScale;
    tot_specular *= vec4(p3d_Material.specular, shininess);
    tot_specular *= gloss_val.a;
    color.rgb = color.rgb + tot_specular.rgb;
    color = color / (color + 1.0);
    color = color * 1.000001;
    color.a = 1.0;*/
    vec2 uv = clamp(vtx_pos.xy / vtx_pos.w, 0.0f, 1.0f);
    vec4 tex_color = texture(p3d_Texture0, uv);
    color = tex_color;
    //color.rg = uv;
    //color.b = 0.0f;
    color.a = 1.0f;
}
