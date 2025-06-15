#version 330 core

// Wejścia do shadera - pobieramy pozycję, współrzędne tekstury, normalną i tangent
layout(location = 0) in vec3 aPos;       // pozycja wierzchołka
layout(location = 1) in vec2 aTexCoord;  // współrzędne tekstury
layout(location = 2) in vec3 aNormal;    // normalna wierzchołka
layout(location = 3) in vec3 aTangent;   // tangent

// Wyjścia do fragment shadera
out vec2 TexCoord;   // przekazujemy współrzędne tekstury
out vec3 FragPos;    // pozycja w świecie 
out mat3 TBN;        // macierz TBN do transformacji normalnych

// Macierze do przekształceń (model, widok, projekcja)
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

void main()
{
    // Liczymy tangent (T), normalną (N) i binormal (B) - potrzebne do macierzy TBN
    vec3 T = normalize(mat3(model) * aTangent);
    vec3 N = normalize(mat3(model) * aNormal);
    vec3 B = normalize(cross(N, T));
    TBN = mat3(T, B, N); // zapisujemy macierz TBN, żeby fragment shader mógł jej użyć

    FragPos = vec3(model * vec4(aPos, 1.0)); // liczymy pozycję wierzchołka w świecie
    TexCoord = aTexCoord; // przekazujemy dalej współrzędne tekstury
    gl_Position = projection * view * vec4(FragPos, 1.0); // końcowa pozycja na ekranie
}