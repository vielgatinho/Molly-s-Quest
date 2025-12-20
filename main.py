import pygame
import sys

# Inicjalizacja Pygame
pygame.init()

# Ustawienia okna
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Molly's Quest")

# Kolory
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

from pygame.locals import (
    K_LEFT,
    K_RIGHT,
    K_SPACE,
    KEYDOWN,
    K_w,
    K_a,
    K_d,
    K_s,
)

# Stałe gry
GRAVITY = 0.8
JUMP_STRENGTH = 5

from pygame.locals import (
    K_LEFT,
    K_RIGHT,
    K_SPACE,
    KEYDOWN,
    K_w,
    K_a,
    K_d,
    K_s,
)

# Stałe gry
GRAVITY = 0.5
JUMP_STRENGTH = 18
PLATFORM_COLOR = (100, 200, 100) # Zielonkawy

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
        self.surf = pygame.Surface((30, 40))
        self.surf.fill(BLUE)
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 60))
        self.speed = 1
        self.velocity_y = 0
        self.on_ground = False

    def update(self, pressed_keys, platforms):
        # Ruch w poziomie
        if pressed_keys[K_LEFT] or pressed_keys[K_a]:
            self.rect.move_ip(-self.speed, 0)
        if pressed_keys[K_RIGHT] or pressed_keys[K_d]:
            self.rect.move_ip(self.speed, 0)

        # Ograniczenia ekranu (poziome)
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

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

    def jump(self):
        if self.on_ground:
            self.velocity_y = -JUMP_STRENGTH

    def draw(self, surface):
        surface.blit(self.surf, self.rect)

# Główna pętla gry
def main():
    player = Player()
    
    # Tworzenie platform
    platforms = pygame.sprite.Group()
    ground = Platform(0, SCREEN_HEIGHT - 20, SCREEN_WIDTH, 20)
    plat1 = Platform(100, SCREEN_HEIGHT - 120, 200, 20)
    plat2 = Platform(350, SCREEN_HEIGHT - 250, 150, 20)
    plat3 = Platform(50, SCREEN_HEIGHT - 400, 100, 20)
    platforms.add(ground, plat1, plat2, plat3)
    
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    all_sprites.add(platforms)

    running = True
    while running:
        # Obsługa zdarzeń
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    player.jump()

        # Pobranie wciśniętych klawiszy
        pressed_keys = pygame.key.get_pressed()
        
        # Aktualizacja gracza
        player.update(pressed_keys, platforms)

        # Rysowanie
        screen.fill(BLACK)
        for entity in all_sprites:
             screen.blit(entity.surf, entity.rect)

        # Aktualizacja wyświetlacza
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()