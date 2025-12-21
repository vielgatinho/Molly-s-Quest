import pygame
from pygame.locals import (
    K_LEFT,
    K_RIGHT,
    K_a,
    K_d,
    RLEACCEL
)
from settings import *

# Klasa platformy
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        
        try:
            # Ładowanie i skalowanie tekstury trawy
            texture = pygame.image.load("content/textures/enviroment/grass.png").convert_alpha()
            
            # Skalowanie tekstury do większego rozmiaru (np. 60px wysokości) zamiast ściskania do 'height'
            target_height = 60
            scale_factor = target_height / texture.get_height()
            new_width = int(texture.get_width() * scale_factor)
            texture = pygame.transform.scale(texture, (new_width, target_height))
            
            self.surf = pygame.Surface((width, target_height), pygame.SRCALPHA)
            
            # Kafelkowanie (powielanie) tekstury na całej szerokości
            for i in range(0, width, new_width):
                self.surf.blit(texture, (i, 0))
                
        except (pygame.error, FileNotFoundError):
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
        # Helper function to load and scale images
        def load_and_scale(path, size):
            try:
                img = pygame.image.load(path).convert_alpha()
                return pygame.transform.scale(img, size)
            except (pygame.error, FileNotFoundError):
                print(f"Nie można załadować obrazka '{path}'.")
                return None

        player_size = (90, 60)
        
        # Load idle frames
        self.idle_frames = []
        idle1 = load_and_scale("content/textures/player/player_idle1.png", player_size)
        idle2 = load_and_scale("content/textures/player/player_idle2.png", player_size)
        idle3 = load_and_scale("content/textures/player/player_idle3.png", player_size)
        idle4 = load_and_scale("content/textures/player/player_idle4.png", player_size)

        if idle1 and idle2 and idle3 and idle4:
            self.idle_frames = [idle1, idle2, idle3, idle4]
        else:
            # Fallback if idle frames are missing
            fallback = pygame.Surface(player_size)
            fallback.fill(PURPLE)
            self.idle_frames = [fallback]

        # Load jump frame
        # Używamy jednej klatki skoku, aby uniknąć problemów z migotaniem
        self.jump_frame = load_and_scale("content/textures/player/player_jump.png", player_size)
        if not self.jump_frame:
            self.jump_frame = load_and_scale("content/textures/player/player_jump.png", player_size)
        if not self.jump_frame:
            self.jump_frame = self.idle_frames[0]


        # Load walking frames
        self.walk_frames = []
        walk1 = load_and_scale("content/textures/player/player_walk1.png", player_size)
        walk2 = load_and_scale("content/textures/player/player_walk2.png", player_size)
        walk3 = load_and_scale("content/textures/player/player_walk3.png", player_size)
        walk4 = load_and_scale("content/textures/player/player_walk4.png", player_size)
        walk5 = load_and_scale("content/textures/player/player_walk5.png", player_size)
        walk6 = load_and_scale("content/textures/player/player_walk6.png", player_size)



        if walk1 and walk2 and walk3 and walk4 and walk5 and walk6:
            self.walk_frames = [walk1, walk2, walk3, walk4, walk5, walk6]
        else:
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
        self.surf = pygame.Surface((50, 50))
        self.surf.fill(GOLD)
        self.rect = self.surf.get_rect(topleft=(x, y))

# Klasa smaczka (punkty)
class Treat(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        try:
            self.surf = pygame.image.load("content/textures/treat.png").convert_alpha()
            self.surf = pygame.transform.scale(self.surf, (30, 30))
        except (pygame.error, FileNotFoundError):
            self.surf = pygame.Surface((20, 20))
            self.surf.fill((255, 165, 0)) # Pomarańczowy
        self.rect = self.surf.get_rect(center=(x, y))

# Klasa przeciwnika
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        try:
            # Spróbuj załadować obrazek przeciwnika
            self.surf = pygame.image.load("content/textures/enemy.png").convert_alpha()
        except (pygame.error, FileNotFoundError):
            # Jeśli obrazek się nie załaduje, użyj czerwonego kwadratu
            print("Nie można załadować obrazka 'enemy.png', używam domyślnego kwadratu.")
            self.surf = pygame.Surface((30, 30))
            self.surf.fill(RED)
        self.rect = self.surf.get_rect(topleft=(x, y))
        self.x = float(self.rect.x)
        self.speed = ENEMY_SPEED
        self.direction = 1 # 1 for right, -1 for left
        self.start_x = x

    def update(self):
        self.x += self.speed * self.direction
        self.rect.x = int(self.x)
        # Prosta AI: zawróć na krawędzi
        if self.rect.x > self.start_x + 100 or self.rect.x < self.start_x:
            self.direction *= -1
