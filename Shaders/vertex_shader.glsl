#version 330

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

in vec3 in_position;
in vec3 in_normal;
in vec2 in_texcoord_0;

out vec2 uv;
out vec3 normal;

void main() {
    gl_Position = projection * view * model * vec4(in_position, 1.0);
    uv = in_texcoord_0;
    normal = mat3(model) * in_normal;
}