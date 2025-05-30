import pygame
from pygame.locals import *
from OpenGL.GL import *
import numpy as np
import ctypes
import glm
import sys
from PIL import Image
import random

# Importy własnych modułów
from camera import Camera
from shapes import create_cube, create_sphere

# Dla komputerów z linuxem
import os
os.environ["SDL_VIDEO_X11_FORCE_EGL"] = "1"
#Aby nie tworzył się folder pycache
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"



def load_shader(vertex_path, fragment_path):
    with open(vertex_path) as f:
        vertex_src = f.read()
    with open(fragment_path) as f:
        fragment_src = f.read()

    shader = glCreateProgram()
    vs = glCreateShader(GL_VERTEX_SHADER)
    fs = glCreateShader(GL_FRAGMENT_SHADER)

    glShaderSource(vs, vertex_src)
    glCompileShader(vs)
    if not glGetShaderiv(vs, GL_COMPILE_STATUS):
        raise RuntimeError(glGetShaderInfoLog(vs))

    glShaderSource(fs, fragment_src)
    glCompileShader(fs)
    if not glGetShaderiv(fs, GL_COMPILE_STATUS):
        raise RuntimeError(glGetShaderInfoLog(fs))

    glAttachShader(shader, vs)
    glAttachShader(shader, fs)
    glLinkProgram(shader)
    if not glGetProgramiv(shader, GL_LINK_STATUS):
        raise RuntimeError(glGetProgramInfoLog(shader))

    glDeleteShader(vs)
    glDeleteShader(fs)
    return shader


def load_texture(path, unit):
    img = Image.open(path).transpose(Image.FLIP_TOP_BOTTOM).convert("RGB")
    img_data = np.array(img, dtype=np.uint8)

    tex = glGenTextures(1)
    glActiveTexture(GL_TEXTURE0 + unit)
    glBindTexture(GL_TEXTURE_2D, tex)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.width, img.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
    glGenerateMipmap(GL_TEXTURE_2D)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    return tex


def main():
    pygame.init()

    # Set OpenGL context attributes before creating the window
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)

    # Utworzenie okna
    screen_width = 800
    screen_height = 600
    pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Sześciany i kule - Pygame")
    
    # Ukrycie kursora myszy i zamknięcie go w oknie
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)

    # Check OpenGL context
    print("OpenGL version:", glGetString(GL_VERSION).decode())

    glEnable(GL_DEPTH_TEST)
    
    # Ustawienie koloru tła (szary)
    glClearColor(0.2, 0.2, 0.2, 1.0)

    # Inicjalizacja kamery z prawidłowymi parametrami okna
    camera = Camera(screen_width, screen_height)

    # Load shaders
    shader = load_shader("shaders/vertex_shader.glsl", "shaders/fragment_shader.glsl")
    
    # Tworzenie obiektów geometrycznych
    cube_vao, cube_index_count = create_cube()
    sphere_vao, sphere_index_count = create_sphere()
    
    # Ładowanie tekstur
    textures = {
        "Ground_080": {
            "diffuse": load_texture("textures/Ground_080/Ground080_1K-JPG_Color.jpg", 0),
            "normal": load_texture("textures/Ground_080/Ground080_1K-JPG_NormalGL.jpg", 1)
        },
        "Rock_062": {
            "diffuse": load_texture("textures/Rock_062/Rock062_1K-JPG_Color.jpg", 2),
            "normal": load_texture("textures/Rock_062/Rock062_1K-JPG_NormalGL.jpg", 3)
        },
        "Fabric_048": {
            "diffuse": load_texture("textures/Fabric_048/Fabric048_1K-JPG_Color.jpg", 4),
            "normal": load_texture("textures/Fabric_048/Fabric048_1K-JPG_NormalGL.jpg", 5)
        }
    }
    
    # Losowe pozycje dla obiektów w scenie z mniejszym zakresem
    # Generujemy 6 losowych pozycji - 3 dla sześcianów i 3 dla kul
    positions = []
    for _ in range(6):
        x = random.uniform(-5.0, 5.0)  # Zmniejszony zakres z -10,10 do -5,5
        y = random.uniform(-3.0, 3.0)  # Zmniejszony zakres z -5,5 do -3,3
        z = random.uniform(-10.0, -5.0)  # Bliżej kamery
        positions.append(glm.vec3(x, y, z))
    
    # Przypisanie tekstur do obiektów
    texture_names = ["Ground_080", "Rock_062", "Fabric_048"]
    
    # Obiekty w scenie: sześciany i kule (bez rotacji)
    scene_objects = [
        {"type": "cube", "position": positions[0], "texture": texture_names[0]},
        {"type": "cube", "position": positions[1], "texture": texture_names[1]},
        {"type": "cube", "position": positions[2], "texture": texture_names[2]},
        {"type": "sphere", "position": positions[3], "texture": texture_names[0]},
        {"type": "sphere", "position": positions[4], "texture": texture_names[1]},
        {"type": "sphere", "position": positions[5], "texture": texture_names[2]}
    ]
    
    projection = glm.perspective(glm.radians(45.0), 800/600, 0.1, 100.0)

    clock = pygame.time.Clock()
    running = True
    
    while running:
        for e in pygame.event.get():
            if e.type == QUIT:
                running = False
            elif e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    running = False
                    pygame.mouse.set_visible(True)
                    pygame.event.set_grab(False)
            elif e.type == pygame.MOUSEMOTION:
                x, y = e.pos
                camera.process_mouse_movement(x, y)
        
        # Obsługa klawiatury
        keys = pygame.key.get_pressed()
        camera.process_keyboard(keys)
        
        # Aktualizacja macierzy widoku
        view = camera.get_view_matrix()
        
        # Czyszczenie bufora koloru i głębokości
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Konfiguracja shadera dla obiektów
        glUseProgram(shader)
        glUniformMatrix4fv(glGetUniformLocation(shader, "view"), 1, GL_FALSE, glm.value_ptr(view))
        glUniformMatrix4fv(glGetUniformLocation(shader, "projection"), 1, GL_FALSE, glm.value_ptr(projection))
        glUniform3f(glGetUniformLocation(shader, "lightPos"), 2.0, 5.0, 2.0)
        glUniform3f(glGetUniformLocation(shader, "viewPos"), camera.position.x, camera.position.y, camera.position.z)
        
        # Rysowanie obiektów
        for obj in scene_objects:
            # Wybór odpowiednich tekstur
            texture_name = obj["texture"]
            diffuse_tex = textures[texture_name]["diffuse"]
            normal_tex = textures[texture_name]["normal"]
            
            # Ustawiamy tekstury w shaderze
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, diffuse_tex)
            glUniform1i(glGetUniformLocation(shader, "diffuseMap"), 0)
            
            glActiveTexture(GL_TEXTURE1)
            glBindTexture(GL_TEXTURE_2D, normal_tex)
            glUniform1i(glGetUniformLocation(shader, "normalMap"), 1)
            
            # Tworzymy macierz modelu bez rotacji
            model = glm.mat4(1.0)
            model = glm.translate(model, obj["position"])
            
            # Stały rozmiar obiektów
            model = glm.scale(model, glm.vec3(1.0, 1.0, 1.0))
            
            glUniformMatrix4fv(glGetUniformLocation(shader, "model"), 1, GL_FALSE, glm.value_ptr(model))
            
            # Rysowanie odpowiedniego obiektu
            if obj["type"] == "cube":
                glBindVertexArray(cube_vao)
                glDrawElements(GL_TRIANGLES, cube_index_count, GL_UNSIGNED_INT, None)
            else:  # sphere
                glBindVertexArray(sphere_vao)
                glDrawElements(GL_TRIANGLES, sphere_index_count, GL_UNSIGNED_INT, None)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
