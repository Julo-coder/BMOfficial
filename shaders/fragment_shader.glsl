#version 330 core

// Dane wejściowe z vertex shadera
in vec2 TexCoord;   // współrzędne tekstury
in vec3 FragPos;    // pozycja fragmentu w świecie
in mat3 TBN;        // macierz TBN do transformacji normalnych

// Tekstury i pozycje światła/kamery przekazywane z Pythona
uniform sampler2D diffuseMap; // tekstura koloru
uniform sampler2D normalMap;  // mapa normalnych 
uniform vec3 lightPos;        // pozycja światła
uniform vec3 viewPos;         // pozycja kamery

out vec4 FragColor; // końcowy kolor piksela

void main()
{
    // Pobieramy normalną z mapy normalnych i przeliczamy ją do zakresu [-1, 1]
    vec3 normal = texture(normalMap, TexCoord).rgb;
    normal = normalize(normal * 2.0 - 1.0);

    // Transformujemy normalną do przestrzeni świata za pomocą macierzy TBN
    normal = normalize(TBN * normal);

    // Pobieramy kolor z tekstury diffuse
    vec3 color = texture(diffuseMap, TexCoord).rgb;

    // Liczymy kierunek do światła i diffuse
    vec3 lightDir = normalize(lightPos - FragPos);
    float diff = max(dot(lightDir, normal), 0.0);

    // Liczymy specular (odbicie światła)
    vec3 viewDir = normalize(viewPos - FragPos);
    vec3 reflectDir = reflect(-lightDir, normal);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), 32.0);

    // Składamy końcowe oświetlenie (ambient + diffuse + specular)
    vec3 lighting = (0.1 + diff + spec) * color;
    FragColor = vec4(lighting, 1.0); // ustawiamy kolor piksela
}