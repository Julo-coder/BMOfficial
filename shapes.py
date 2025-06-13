import numpy as np
from OpenGL.GL import *
import ctypes

def create_quad():
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

def create_cube():
    # Format: pozycja (3), tekstura (2), normalna (3), tangens (3)
    vertices = np.array([
        # Przednia ściana
        -0.5, -0.5,  0.5,  0.0, 0.0,  0.0, 0.0, 1.0,  1.0, 0.0, 0.0,
         0.5, -0.5,  0.5,  1.0, 0.0,  0.0, 0.0, 1.0,  1.0, 0.0, 0.0,
         0.5,  0.5,  0.5,  1.0, 1.0,  0.0, 0.0, 1.0,  1.0, 0.0, 0.0,
        -0.5,  0.5,  0.5,  0.0, 1.0,  0.0, 0.0, 1.0,  1.0, 0.0, 0.0,
        # Tylna ściana
        -0.5, -0.5, -0.5,  1.0, 0.0,  0.0, 0.0, -1.0, -1.0, 0.0, 0.0,
         0.5, -0.5, -0.5,  0.0, 0.0,  0.0, 0.0, -1.0, -1.0, 0.0, 0.0,
         0.5,  0.5, -0.5,  0.0, 1.0,  0.0, 0.0, -1.0, -1.0, 0.0, 0.0,
        -0.5,  0.5, -0.5,  1.0, 1.0,  0.0, 0.0, -1.0, -1.0, 0.0, 0.0,
        # Górna ściana
        -0.5,  0.5, -0.5,  0.0, 0.0,  0.0, 1.0, 0.0,  1.0, 0.0, 0.0,
         0.5,  0.5, -0.5,  1.0, 0.0,  0.0, 1.0, 0.0,  1.0, 0.0, 0.0,
         0.5,  0.5,  0.5,  1.0, 1.0,  0.0, 1.0, 0.0,  1.0, 0.0, 0.0,
        -0.5,  0.5,  0.5,  0.0, 1.0,  0.0, 1.0, 0.0,  1.0, 0.0, 0.0,
        # Dolna ściana
        -0.5, -0.5, -0.5,  0.0, 1.0,  0.0, -1.0, 0.0, 1.0, 0.0, 0.0,
         0.5, -0.5, -0.5,  1.0, 1.0,  0.0, -1.0, 0.0, 1.0, 0.0, 0.0,
         0.5, -0.5,  0.5,  1.0, 0.0,  0.0, -1.0, 0.0, 1.0, 0.0, 0.0,
        -0.5, -0.5,  0.5,  0.0, 0.0,  0.0, -1.0, 0.0, 1.0, 0.0, 0.0,
        # Prawa ściana
         0.5, -0.5, -0.5,  0.0, 0.0,  1.0, 0.0, 0.0,  0.0, 0.0, 1.0,
         0.5,  0.5, -0.5,  0.0, 1.0,  1.0, 0.0, 0.0,  0.0, 0.0, 1.0,
         0.5,  0.5,  0.5,  1.0, 1.0,  1.0, 0.0, 0.0,  0.0, 0.0, 1.0,
         0.5, -0.5,  0.5,  1.0, 0.0,  1.0, 0.0, 0.0,  0.0, 0.0, 1.0,
        # Lewa ściana
        -0.5, -0.5, -0.5,  1.0, 0.0, -1.0, 0.0, 0.0,  0.0, 0.0, -1.0,
        -0.5,  0.5, -0.5,  1.0, 1.0, -1.0, 0.0, 0.0,  0.0, 0.0, -1.0,
        -0.5,  0.5,  0.5,  0.0, 1.0, -1.0, 0.0, 0.0,  0.0, 0.0, -1.0,
        -0.5, -0.5,  0.5,  0.0, 0.0, -1.0, 0.0, 0.0,  0.0, 0.0, -1.0
    ], dtype=np.float32)
    
    indices = np.array([
        0, 1, 2, 2, 3, 0,     # Przód
        4, 5, 6, 6, 7, 4,     # Tył
        8, 9, 10, 10, 11, 8,  # Góra
        12, 13, 14, 14, 15, 12, # Dół
        16, 17, 18, 18, 19, 16, # Prawa
        20, 21, 22, 22, 23, 20  # Lewa
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

def create_sphere(stacks=20, sectors=20, radius=0.5):
    vertices = []
    indices = []
    
    for i in range(stacks + 1):
        V = i / stacks
        phi = V * np.pi
        
        for j in range(sectors + 1):
            U = j / sectors
            theta = U * 2 * np.pi
            
            x = radius * np.sin(phi) * np.cos(theta)
            y = radius * np.cos(phi)
            z = radius * np.sin(phi) * np.sin(theta)
            
            nx = x / radius
            ny = y / radius
            nz = z / radius
            
            tx = np.sin(phi) * np.sin(theta)
            ty = 0
            tz = -np.sin(phi) * np.cos(theta)

            # Normalizacja tangensa
            length = np.sqrt(tx*tx + ty*ty + tz*tz)
            if length > 0:
                tx /= length
                ty /= length
                tz /= length
            
            vertices.extend([x, y, z, U, V, nx, ny, nz, tx, ty, tz])
    
    for i in range(stacks):
        for j in range(sectors):
            first = i * (sectors + 1) + j
            second = first + sectors + 1
            
            indices.extend([first, second, first + 1])
            indices.extend([second, second + 1, first + 1])
    
    vertices = np.array(vertices, dtype=np.float32)
    indices = np.array(indices, dtype=np.uint32)
    
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