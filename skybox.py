import numpy as np
from OpenGL.GL import *
import ctypes
import os

def ensure_shader_files_exist():
    """Sprawdź czy pliki shaderów skyboxa istnieją, jeśli nie - utwórz je"""
    
    if os.path.exists("shaders/skybox_vertex_shader.glsl") and os.path.exists("shaders/skybox_fragment_shader.glsl"):
        print("Pliki shaderów skyboxa już istnieją")
        return True
    
    # Jeśli brakuje któregokolwiek pliku, utwórz oba
    print("Brakuje plików shaderów skyboxa, tworzę...")
    
    # Vertex shader
    vertex_shader = """#version 330 core
layout (location = 0) in vec3 aPos;

uniform mat4 projection;
uniform mat4 view;

out vec3 TexCoords;

void main()
{
    TexCoords = aPos;
    vec4 pos = projection * view * vec4(aPos, 1.0);
    gl_Position = pos.xyww;
}
"""
    
    # Fragment shader
    fragment_shader = """#version 330 core
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
"""
    
    # Upewnij się, że folder shaders istnieje
    if not os.path.exists("shaders"):
        os.makedirs("shaders")
    
    # Zapisz pliki shaderów tylko jeśli ich nie ma
    try:
        if not os.path.exists("shaders/skybox_vertex_shader.glsl"):
            with open("shaders/skybox_vertex_shader.glsl", "w") as f:
                f.write(vertex_shader)
        
        if not os.path.exists("shaders/skybox_fragment_shader.glsl"):
            with open("shaders/skybox_fragment_shader.glsl", "w") as f:
                f.write(fragment_shader)
                
        print("Utworzono brakujące pliki shaderów skyboxa")
        return True
    except Exception as e:
        print(f"Błąd podczas tworzenia plików shaderów: {e}")
        return False

def create_skybox():
    """Tworzenie VAO dla skyboxa"""
    
    # Sprawdź czy pliki shaderów istnieją - ale nie twórz nowych jeśli już istnieją
    ensure_shader_files_exist()
    
    # Zwiększone rozmiary skyboxa - większy skybox będzie lepiej widoczny
    vertices = np.array([
        # positions          
        -100.0,  100.0, -100.0,  # Znacznie zwiększone rozmiary skyboxa
        -100.0, -100.0, -100.0,
         100.0, -100.0, -100.0,
         100.0, -100.0, -100.0,
         100.0,  100.0, -100.0,
        -100.0,  100.0, -100.0,

        -100.0, -100.0,  100.0,
        -100.0, -100.0, -100.0,
        -100.0,  100.0, -100.0,
        -100.0,  100.0, -100.0,
        -100.0,  100.0,  100.0,
        -100.0, -100.0,  100.0,

         100.0, -100.0, -100.0,
         100.0, -100.0,  100.0,
         100.0,  100.0,  100.0,
         100.0,  100.0,  100.0,
         100.0,  100.0, -100.0,
         100.0, -100.0, -100.0,

        -100.0, -100.0,  100.0,
        -100.0,  100.0,  100.0,
         100.0,  100.0,  100.0,
         100.0,  100.0,  100.0,
         100.0, -100.0,  100.0,
        -100.0, -100.0,  100.0,

        -100.0,  100.0, -100.0,
         100.0,  100.0, -100.0,
         100.0,  100.0,  100.0,
         100.0,  100.0,  100.0,
        -100.0,  100.0,  100.0,
        -100.0,  100.0, -100.0,

        -100.0, -100.0, -100.0,
        -100.0, -100.0,  100.0,
         100.0, -100.0, -100.0,
         100.0, -100.0, -100.0,
        -100.0, -100.0,  100.0,
         100.0, -100.0,  100.0
    ], dtype=np.float32)
    
    skybox_vao = glGenVertexArrays(1)
    skybox_vbo = glGenBuffers(1)
    
    glBindVertexArray(skybox_vao)
    glBindBuffer(GL_ARRAY_BUFFER, skybox_vbo)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * 4, ctypes.c_void_p(0))
    
    return skybox_vao, 36  # 36 wierzchołków (6 ścian * 2 trójkąty * 3 wierzchołki)