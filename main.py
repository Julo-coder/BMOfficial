import pygame
from pygame.locals import *
from OpenGL.GL import *
import numpy as np
import ctypes
import glm
import sys
from PIL import Image
import os
os.environ["SDL_VIDEO_X11_FORCE_EGL"] = "1"


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


def create_quad():
    # pos     tex     normal   tangent
    vertices = np.array([
        -1, -1, 0, 0, 0, 0, 0, 1, 1, 0, 0,
         1, -1, 0, 1, 0, 0, 0, 1, 1, 0, 0,
         1,  1, 0, 1, 1, 0, 0, 1, 1, 0, 0,
        -1,  1, 0, 0, 1, 0, 0, 1, 1, 0, 0,
    ], dtype=np.float32)

    indices = np.array([
        0, 1, 2, 2, 3, 0
    ], dtype=np.uint32)

    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)

    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    ebo = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

    stride = 11 * 4
    for i, size in enumerate([3, 2, 3, 3]):
        glVertexAttribPointer(i, size, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(sum([3, 2, 3, 3][:i]) * 4))
        glEnableVertexAttribArray(i)

    glBindVertexArray(0)
    return vao, len(indices)


def main():
    pygame.init()

    # Set OpenGL context attributes before creating the window
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)

    pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Bump Mapping - Pygame")

    # Check OpenGL context
    print("OpenGL version:", glGetString(GL_VERSION).decode())

    glEnable(GL_DEPTH_TEST)

    # Load shaders and resources
    shader = load_shader("shaders/vertex_shader.glsl", "shaders/fragment_shader.glsl")
    vao, index_count = create_quad()
    diffuse = load_texture("textures/Fabric048_1K-JPG_Color.jpg", 0)
    normal = load_texture("textures/Fabric048_1K-JPG_NormalGL.jpg", 1)
    model = glm.mat4(1.0)
    view = glm.lookAt(glm.vec3(0, 0, 3), glm.vec3(0, 0, 0), glm.vec3(0, 1, 0))
    projection = glm.perspective(glm.radians(45.0), 800/600, 0.1, 100.0)

    clock = pygame.time.Clock()
    running = True
    while running:
        for e in pygame.event.get():
            if e.type == QUIT:
                running = False

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glUseProgram(shader)
        glUniform1i(glGetUniformLocation(shader, "diffuseMap"), 0)
        glUniform1i(glGetUniformLocation(shader, "normalMap"), 1)
        glUniform3f(glGetUniformLocation(shader, "lightPos"), 1.2, 1.0, 2.0)
        glUniform3f(glGetUniformLocation(shader, "viewPos"), 0.0, 0.0, 3.0)
        glUniformMatrix4fv(glGetUniformLocation(shader, "model"), 1, GL_FALSE, glm.value_ptr(model))
        glUniformMatrix4fv(glGetUniformLocation(shader, "view"), 1, GL_FALSE, glm.value_ptr(view))
        glUniformMatrix4fv(glGetUniformLocation(shader, "projection"), 1, GL_FALSE, glm.value_ptr(projection))

        glBindVertexArray(vao)
        glDrawElements(GL_TRIANGLES, index_count, GL_UNSIGNED_INT, None)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
