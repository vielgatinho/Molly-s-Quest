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
        self.surf = pygame.Surface((width, height))
        self.surf.fill(PLATFORM_COLOR)
        self.rect = self.surf.get_rect(topleft=(x, y))

# Klasa gracza
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        try:
            # Spróbuj załadować obrazek gracza
            self.surf = pygame.image.load("content/textures/player.png").convert_alpha()
        except (pygame.error, FileNotFoundError):
            # Jeśli obrazek się nie załaduje, użyj fioletowego kwadratu
            print("Nie można załadować obrazka 'player.png', używam domyślnego kwadratu.")
            self.surf = pygame.Surface((30, 40))
            self.surf.fill(PURPLE)
        
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 60))
        self.speed = PLAYER_SPEED
        self.velocity_y = 0
        self.on_ground = False

    def update(self, pressed_keys, platforms, world_width):
        # Ruch w poziomie
        if pressed_keys[K_LEFT] or pressed_keys[K_a]:
            self.rect.move_ip(-self.speed, 0)
        if pressed_keys[K_RIGHT] or pressed_keys[K_d]:
            self.rect.move_ip(self.speed, 0)

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
                if self.rect.bottom > plat.rect.top:
                    self.rect.bottom = plat.rect.top
                    self.velocity_y = 0
                    self.on_ground = True

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

# Klasa przeciwnika
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        try:
            # Spróbuj załadować obrazek przeciwnika
            self.surf = pygame.image.load("content/textures/enemy.png").convert()
            self.surf.set_colorkey(WHITE, RLEACCEL) # Ustaw biały jako kolor przezroczysty
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
