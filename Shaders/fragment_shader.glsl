#version 330

uniform vec3 Color;

in vec2 uv;
in vec3 normal;

out vec4 fragColor;

void main() {
    vec3 ambientLight = vec3(0.5, 0.5, 0.5);
    vec3 lightDir = normalize(vec3(1.0, 1.0, 1.0));
    float l = dot(normalize(normal), lightDir);
    vec3 diffuse = max(l, 0.0) * Color;
    vec3 ambient = ambientLight * Color;
    fragColor = vec4(diffuse + ambient, 1.0);
}