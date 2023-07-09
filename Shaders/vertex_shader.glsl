#version 330

uniform mat4 ModelViewProjection;
uniform mat4 Model;

in vec3 in_position;
in vec3 in_normal;
in vec2 in_texcoord_0;

out vec2 uv;
out vec3 normal;

void main() {
    gl_Position = ModelViewProjection * vec4(in_position, 1.0);
    uv = in_texcoord_0;
    normal = mat3(Model) * in_normal;
}