#version 330 core
in vec2 TexCoord;
in vec3 FragPos;
in mat3 TBN;

uniform sampler2D diffuseMap;
uniform sampler2D normalMap;
uniform vec3 lightPos;
uniform vec3 viewPos;

out vec4 FragColor;

void main()
{
    vec3 normal = texture(normalMap, TexCoord).rgb;
    normal = normalize(normal * 2.0 - 1.0); // tangent space
    normal = normalize(TBN * normal);

    vec3 color = texture(diffuseMap, TexCoord).rgb;
    vec3 lightDir = normalize(lightPos - FragPos);
    float diff = max(dot(lightDir, normal), 0.0);

    vec3 viewDir = normalize(viewPos - FragPos);
    vec3 reflectDir = reflect(-lightDir, normal);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), 32.0);

    vec3 lighting = (0.1 + diff + spec) * color;
    FragColor = vec4(lighting, 1.0);
}
