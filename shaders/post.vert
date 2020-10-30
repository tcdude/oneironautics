#version 130

uniform mat4 p3d_ModelViewProjectionMatrix;
uniform mat4 p3d_ModelViewMatrix;

in vec4 p3d_Vertex;

out vec2 texcoord;


void main() {
    texcoord = p3d_Vertex.xz / 2.0 + 0.5;

    gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;
}
