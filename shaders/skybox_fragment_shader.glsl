#version 330 core
out vec4 FragColor;

in vec3 TexCoords;

void main()
{    
    // Proste niebo - gradient od niebieskiego do białego
    float t = TexCoords.y * 0.5 + 0.5;  // Przeskalowanie wysokości od -1,1 do 0,1
    vec3 topColor = vec3(0.1, 0.4, 0.8);  // Niebieski
    vec3 bottomColor = vec3(0.8, 0.9, 1.0);  // Jaśniejszy niebieski/biały
    FragColor = vec4(mix(bottomColor, topColor, t), 1.0);
}
