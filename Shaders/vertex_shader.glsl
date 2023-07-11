#version 330

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

in vec3 in_position;
in vec3 in_normal;
in vec2 in_texcoord_0;

out vec2 uv;
out vec3 pos;
out vec3 normal;

void main() {
    mat4 m_view = view * model;
    vec4 p = m_view * vec4(in_position, 1.0);
    gl_Position = projection * p;
    normal = inverse(transpose(mat3(m_view))) * normalize(in_normal);
    pos = p.xyz;
    uv = in_texcoord_0;
}