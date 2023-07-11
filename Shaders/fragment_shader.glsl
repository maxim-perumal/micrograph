#version 330

uniform mat4 ModelViewProjection;
uniform vec3 Color;

in vec2 uv;
in vec3 pos;
in vec3 normal;

out vec4 fragColor;

void main() {
    vec3 ambientLight = vec3(0.5, 0.5, 0.5);
    vec3 lightDir = normalize(vec3(1.0, 1.0, 1.0));
    float shininess = 16.0;

    vec3 P = pos;    // Position vector
    vec3 N = normalize(normal);             // Normal vector
    vec3 V = normalize(-P);                 // View direction
    vec3 L = normalize(lightDir - P);       // Light direction
    vec3 R = reflect(-L, N);                // Reflection of the light direction based on normal vector
    float dotLN = max(dot(L, N), 0.0);      // Dot product between L and N
    float dotRV = max(dot(R, V), 0.0);      // Dot product between R and V

    // Ambiant light
    vec3 ambient = ambientLight * Color;    // Compute ambient light

    // Diffuse light
    vec3 diffuse = dotLN * Color;           // Compute diffuse light

    // Specular light
    vec3 specular = max(0.0, pow(dotRV, shininess)) * Color;    // Compute specular
    
    fragColor = vec4(ambient + diffuse + specular, 1.0);    // Compute final pixel color
}