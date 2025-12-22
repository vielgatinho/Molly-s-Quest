import pygame
import math
from pygame.locals import (
    K_LEFT,
    K_RIGHT,
    K_a,
    K_d,
    RLEACCEL
)
from settings import *
from utils import load_image

# Klasa platform
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        
        try:
            # Ładowanie tekstury trawy (używamy load_image, ale bez skalowania tutaj, bo robimy to niżej dynamicznie)
            texture = load_image("content/textures/enviroment/grass.png")
            
            # Skalowanie tekstury do większego rozmiaru (np. 60px wysokości) zamiast ściskania do 'height'
            target_height = 60
            scale_factor = target_height / texture.get_height()
            new_width = int(texture.get_width() * scale_factor)
            texture = pygame.transform.scale(texture, (new_width, target_height))
            
            self.surf = pygame.Surface((width, target_height), pygame.SRCALPHA)
            
            # Kafelkowanie (powielanie) tekstury na całej szerokości
            for i in range(0, width, new_width):
                self.surf.blit(texture, (i, 0))
                
        except (AttributeError, pygame.error): # AttributeError jeśli texture jest None
            # Jeśli nie uda się załadować tekstury, użyj koloru
            self.surf = pygame.Surface((width, height))
            self.surf.fill(PLATFORM_COLOR)
            
        self.rect = self.surf.get_rect(topleft=(x, y))

# Klasa gracza
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self._load_frames()
        
        self.surf = self.idle_frames[0] # Start with idle frame
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 150))
        
        self.speed = PLAYER_SPEED
        self.velocity_y = 0
        self.on_ground = False
        
        # Animation state
        self.walking = False
        self.direction = 1 # 1 for right, -1 for left
        self.last_anim_update = pygame.time.get_ticks()
        self.walk_frame_index = 0
        self.idle_frame_index = 0

    def _load_frames(self):
        player_size = (90, 60)
        
        # Load idle frames
        self.idle_frames = []
        for i in range(1, 5):
            frame = load_image(f"content/textures/player/player_idle{i}.png", player_size)
            if frame: self.idle_frames.append(frame)

        if not self.idle_frames:
            # Fallback if idle frames are missing
            fallback = pygame.Surface(player_size)
            fallback.fill(PURPLE)
            self.idle_frames = [fallback]

        # Load jump frame
        # Używamy jednej klatki skoku, aby uniknąć problemów z migotaniem
        self.jump_frame = load_image("content/textures/player/player_jump.png", player_size)
        if not self.jump_frame:
            self.jump_frame = load_image("content/textures/player/player_jump.png", player_size)
        if not self.jump_frame:
            self.jump_frame = self.idle_frames[0]


        # Load walking frames
        self.walk_frames = []
        for i in range(1, 10):
            frame = load_image(f"content/textures/player/player_walk{i}.png", player_size)
            if frame: self.walk_frames.append(frame)

        if not self.walk_frames:
            # Use idle if walk frames are missing
            self.walk_frames = [self.idle_frames[0]]

    def update(self, pressed_keys, platforms, world_width):
        self.walking = False
        # Ruch w poziomie
        if pressed_keys[K_LEFT] or pressed_keys[K_a]:
            self.rect.move_ip(-self.speed, 0)
            self.direction = -1
            self.walking = True
        if pressed_keys[K_RIGHT] or pressed_keys[K_d]:
            self.rect.move_ip(self.speed, 0)
            self.direction = 1
            self.walking = True

        # Ograniczenie ruchu do granic świata
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > world_width:
            self.rect.right = world_width

        # Grawitacja i ruch w pionie
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y
        self.on_ground = False # Resetuj przed sprawdzaniem kolizji

        # Kolizje z platformami (pionowe)
        collided_platforms = pygame.sprite.spritecollide(self, platforms, False)
        for plat in collided_platforms:
            if self.velocity_y > 0: # Spadanie
                if self.rect.bottom < plat.rect.centery:
                    self.rect.bottom = plat.rect.top + 20
                    self.velocity_y = 0
                    self.on_ground = True
        
        self._animate()

    def _animate(self):
        now = pygame.time.get_ticks()
        
        # Determine which frame to use
        if not self.on_ground:
            original_frame = self.jump_frame
        elif self.walking:
            if now - self.last_anim_update > WALK_ANIMATION_SPEED:
                self.last_anim_update = now
                self.walk_frame_index = (self.walk_frame_index + 1) % len(self.walk_frames)
            original_frame = self.walk_frames[self.walk_frame_index]
        else: # Idle
            # Użyj niestandardowych czasów dla animacji bezczynności
            current_duration = IDLE_ANIMATION_TIMINGS[self.idle_frame_index]
            if now - self.last_anim_update > current_duration:
                self.last_anim_update = now
                self.idle_frame_index = (self.idle_frame_index + 1) % len(self.idle_frames)
            original_frame = self.idle_frames[self.idle_frame_index]
            
        # Flip frame if necessary and update self.surf
        if self.direction == -1: # Left
            self.surf = pygame.transform.flip(original_frame, True, False)
        else: # Right
            self.surf = original_frame

    def jump(self, jump_sound=None):
        if self.on_ground:
            if jump_sound:
                jump_sound.play()
            self.velocity_y = -JUMP_STRENGTH

    def draw(self, surface):
        surface.blit(self.surf, self.rect)

# Klasa celu
class Goal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.frames = []
        # Ładowanie klatek animacji bazy
        for i in range(1, 3):
            img = load_image(f"content/textures/enviroment/base{i}.png", (160, 100))
            if img:
                self.frames.append(img)
        
        # Fallback jeśli nie znaleziono klatek animacji
        if not self.frames:
            img = load_image("content/textures/enviroment/base.png", (160, 160))
            if img:
                self.frames.append(img)
            else:
                surf = pygame.Surface((50, 50))
                surf.fill(GOLD)
                self.frames.append(surf)
        
        self.current_frame = 0
        self.surf = self.frames[0]
        self.last_update = pygame.time.get_ticks()

        # Dopasowanie do ziemi
        if self.surf.get_height() <= 160:
            self.rect = self.surf.get_rect(bottomleft=(x, y + 50 + 30))
        else:
            self.rect = self.surf.get_rect(topleft=(x, y))

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > GOAL_ANIMATION_SPEED:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.surf = self.frames[self.current_frame]

# Klasa smaczka (punkty)
class Treat(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.surf = load_image("content/textures/enviroment/treat.png", (60, 30))
        if not self.surf:
            self.surf = pygame.Surface((20, 20))
            self.surf.fill((255, 165, 0)) # Pomarańczowy
        self.rect = self.surf.get_rect(center=(x, y))
        self.start_y = y
        self.timer = 0

    def update(self):
        self.timer += 0.1
        offset = math.sin(self.timer) * 5 # Amplituda 5 pikseli
        self.rect.centery = self.start_y + offset

# Klasa przeciwnika
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self._load_frames()
        self.surf = self.frames[0]
        self.rect = self.surf.get_rect(topleft=(x, y + 20))
        self.x = float(self.rect.x)
        self.speed = ENEMY_SPEED
        self.direction = 1 # 1 for right, -1 for left
        self.start_x = x

        # Animation
        self.last_anim_update = pygame.time.get_ticks()
        self.anim_frame_index = 0

    def _load_frames(self):
        self.frames = []
        for i in range(1, 5):
            path = f"content/textures/enemy/enemy{i}.png"
            img = load_image(path, (60, 60))
            if img: self.frames.append(img)
        
        if not self.frames:
            # Fallback, jeśli nie załadowano żadnej klatki
            fallback = pygame.Surface((60, 60))
            fallback.fill(RED)
            self.frames = [fallback]

    def _animate(self):
        now = pygame.time.get_ticks()
        if now - self.last_anim_update > ENEMY_ANIMATION_SPEED:
            self.last_anim_update = now
            self.anim_frame_index = (self.anim_frame_index + 1) % len(self.frames)
        
        original_frame = self.frames[self.anim_frame_index]
        
        if self.direction == -1:
            self.surf = pygame.transform.flip(original_frame, True, False)
        else:
            self.surf = original_frame

    def update(self):
        self.x += self.speed * self.direction
        self.rect.x = int(self.x)
        # Prosta AI: zawróć na krawędzi
        if self.rect.x > self.start_x + 100 or self.rect.x < self.start_x:
            self.direction *= -1
        
        self._animate()
