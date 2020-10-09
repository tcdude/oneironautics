#version 130

uniform mat4 p3d_ModelViewProjectionMatrix;
uniform mat4 p3d_ModelViewMatrix;
uniform mat3 p3d_NormalMatrix;

in vec4 p3d_Vertex;
in vec3 p3d_Normal;
in vec2 p3d_MultiTexCoord0;

out vec4 vtx_pos;
out vec3 normal;
out vec2 l_texcoord;
out vec4 l_eye_position;

void main() {
    vtx_pos = p3d_ModelViewMatrix * p3d_Vertex;
    normal = normalize(p3d_NormalMatrix * p3d_Normal);
    l_texcoord = p3d_MultiTexCoord0;

    gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;
}
