import pygame
from pygame.locals import *
import glm
import math

class Camera:
    def __init__(self, window_width=800, window_height=600):
        self.position = glm.vec3(0, 0, 3)
        self.front = glm.vec3(0, 0, -1)
        self.up = glm.vec3(0, 1, 0)
        self.right = glm.vec3(0, 0, 0)
        self.world_up = glm.vec3(0, 1, 0)
        
        # Kąty Eulera
        self.yaw = -90.0
        self.pitch = 0.0
        
        # Parametry kamery
        self.movement_speed = 0.05
        self.sensitivity = 0.3  # Wysoka czułość dla lepszej responsywności
        
        # Parametry okna
        self.window_width = window_width
        self.window_height = window_height
        self.center_x = window_width // 2
        self.center_y = window_height // 2
        
        # Poprzednia pozycja myszy
        self.last_x = self.center_x
        self.last_y = self.center_y
        self.first_mouse = True
        
        # Sterowanie resetowaniem myszy przy krawędzi
        self.border_threshold = 50  # odległość od krawędzi, przy której resetujemy mysz
        self.should_reset_mouse = True
        
        self.update_camera_vectors()
    
    def get_view_matrix(self):
        return glm.lookAt(self.position, self.position + self.front, self.up)
    
    def process_keyboard(self, keys):
        if keys[K_w]:
            self.position += self.movement_speed * self.front
        if keys[K_s]:
            self.position -= self.movement_speed * self.front
        if keys[K_a]:
            self.position -= self.right * self.movement_speed
        if keys[K_d]:
            self.position += self.right * self.movement_speed
        if keys[K_SPACE]:
            self.position.y += self.movement_speed
        if keys[K_LSHIFT]:
            self.position.y -= self.movement_speed
    
    def process_mouse_movement(self, x_pos, y_pos):
        if self.first_mouse:
            self.last_x = x_pos
            self.last_y = y_pos
            self.first_mouse = False
            return
        
        # Sprawdzamy, czy mysz jest blisko krawędzi ekranu
        near_edge = (x_pos < self.border_threshold or 
                     x_pos > self.window_width - self.border_threshold or
                     y_pos < self.border_threshold or 
                     y_pos > self.window_height - self.border_threshold)
        
        # Obliczamy przesunięcie myszy
        x_offset = x_pos - self.last_x
        y_offset = self.last_y - y_pos  # Odwrócone, ponieważ współrzędne y rosną od góry do dołu
        
        # Jeśli mysz jest blisko krawędzi, resetujemy jej pozycję
        if near_edge and self.should_reset_mouse:
            pygame.mouse.set_pos(self.center_x, self.center_y)
            self.last_x = self.center_x
            self.last_y = self.center_y
            # Ustawiamy flagę, żeby nie resetować myszy w następnej klatce
            self.should_reset_mouse = False
            return  # Pomijamy aktualizację kamery w tej klatce
        else:
            self.should_reset_mouse = True
            self.last_x = x_pos
            self.last_y = y_pos
        
        # Stosujemy czułość
        x_offset *= self.sensitivity
        y_offset *= self.sensitivity
        
        # Aktualizujemy kąty Eulera
        self.yaw += x_offset
        self.pitch += y_offset
        
        # Ograniczenie kąta pionowego
        if self.pitch > 89.0:
            self.pitch = 89.0
        if self.pitch < -89.0:
            self.pitch = -89.0
            
        self.update_camera_vectors()
    
    def update_camera_vectors(self):
        front = glm.vec3(0, 0, 0)
        front.x = math.cos(glm.radians(self.yaw)) * math.cos(glm.radians(self.pitch))
        front.y = math.sin(glm.radians(self.pitch))
        front.z = math.sin(glm.radians(self.yaw)) * math.cos(glm.radians(self.pitch))
        
        self.front = glm.normalize(front)
        self.right = glm.normalize(glm.cross(self.front, self.world_up))
        self.up = glm.normalize(glm.cross(self.right, self.front))