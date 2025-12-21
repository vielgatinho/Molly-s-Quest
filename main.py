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
GRAVITY = 0.5
JUMP_STRENGTH = 15
PLATFORM_COLOR = (139, 69, 19) # Brązowy
WORLD_WIDTH = 2000 # Szerokość świata gry

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
            self.surf = pygame.image.load("player.png").convert()
            self.surf.set_colorkey((255, 255, 255), pygame.RLEACCEL) # Ustaw biały jako kolor przezroczysty
        except pygame.error:
            # Jeśli obrazek się nie załaduje, użyj fioletowego kwadratu
            print("Nie można załadować obrazka 'player.png', używam domyślnego kwadratu.")
            self.surf = pygame.Surface((30, 40))
            self.surf.fill((128, 0, 128)) # Fioletowy
        except FileNotFoundError:
            print("Plik 'player.png' nie został znaleziony, używam domyślnego kwadratu.")
            self.surf = pygame.Surface((30, 40))
            self.surf.fill((128, 0, 128)) # Fioletowy
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 60))
        self.speed = 5
        self.velocity_y = 0
        self.on_ground = False

    def update(self, pressed_keys, platforms):
        # Ruch w poziomie
        if pressed_keys[K_LEFT] or pressed_keys[K_a]:
            self.rect.move_ip(-self.speed, 0)
        if pressed_keys[K_RIGHT] or pressed_keys[K_d]:
            self.rect.move_ip(self.speed, 0)

        # Ograniczenie ruchu do granic świata
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WORLD_WIDTH:
            self.rect.right = WORLD_WIDTH

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
        self.surf.fill((255, 215, 0)) # Złoty
        self.rect = self.surf.get_rect(topleft=(x, y))

# Klasa przeciwnika
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        try:
            # Spróbuj załadować obrazek przeciwnika
            self.surf = pygame.image.load("enemy.png").convert()
            self.surf.set_colorkey((255, 255, 255), pygame.RLEACCEL) # Ustaw biały jako kolor przezroczysty
        except pygame.error:
            # Jeśli obrazek się nie załaduje, użyj czerwonego kwadratu
            print("Nie można załadować obrazka 'enemy.png', używam domyślnego kwadratu.")
            self.surf = pygame.Surface((30, 30))
            self.surf.fill((255, 0, 0)) # Czerwony
        except FileNotFoundError:
            print("Plik 'enemy.png' nie został znaleziony, używam domyślnego kwadratu.")
            self.surf = pygame.Surface((30, 30))
            self.surf.fill((255, 0, 0)) # Czerwony
        self.rect = self.surf.get_rect(topleft=(x, y))
        self.x = float(self.rect.x)
        self.speed = 2.5
        self.direction = 1 # 1 for right, -1 for left

    def update(self):
        self.x += self.speed * self.direction
        self.rect.x = int(self.x)
        # Prosta AI: zawróć na krawędzi (to wymaga dopracowania w zależności od platformy)
        # Na razie prosty przykład, zawraca po przejściu 100 pikseli
        if self.rect.x > self.start_x + 100 or self.rect.x < self.start_x:
            self.direction *= -1
def show_start_screen(screen):
    font = pygame.font.SysFont(None, 55)
    
    background = pygame.Surface(screen.get_size()).convert()
    background.fill(BLACK)
    
    title_text = font.render("Molly's Quest", True, WHITE)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50))

    start_text = font.render("Naciśnij dowolny klawisz, aby rozpocząć", True, WHITE)
    start_rect = start_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50))

    screen.blit(background, (0,0))
    screen.blit(title_text, title_rect)
    screen.blit(start_text, start_rect)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                waiting = False

def show_end_screen(screen, message, score):
    font = pygame.font.SysFont(None, 55)
    score_font = pygame.font.SysFont(None, 35)
    
    background = pygame.Surface(screen.get_size()).convert()
    background.fill(BLACK)
    
    text = font.render(message, True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50))
    
    score_text = score_font.render(f"Twój ostateczny wynik: {score}", True, WHITE)
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

    restart_text = score_font.render("Naciśnij dowolny klawisz, aby zagrać ponownie", True, WHITE)
    restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50))

    screen.blit(background, (0,0))
    screen.blit(text, text_rect)
    screen.blit(score_text, score_rect)
    screen.blit(restart_text, restart_rect)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                waiting = False

def main():
    show_start_screen(screen)
    try:
        pygame.mixer.music.load('background_music.mp3')
        pygame.mixer.music.play(-1) # Odtwarzaj w pętli
    except pygame.error:
        print("Nie można załadować pliku 'background_music.mp3'. Gra będzie bez muzyki.")
        
    try:
        jump_sound = pygame.mixer.Sound('jump.wav')
    except pygame.error:
        print("Nie można załadować pliku 'jump.wav'. Efekt dźwiękowy skoku nie będzie odtwarzany.")
        jump_sound = None
    except FileNotFoundError:
        print("Plik 'jump.wav' nie został znaleziony. Efekt dźwiękowy skoku nie będzie odtwarzany.")
        jump_sound = None
        
    try:
        stomp_sound = pygame.mixer.Sound('stomp.wav')
    except pygame.error:
        print("Nie można załadować pliku 'stomp.wav'. Efekt dźwiękowy pokonania przeciwnika nie będzie odtwarzany.")
        stomp_sound = None
    except FileNotFoundError:
        print("Plik 'stomp.wav' nie został znaleziony. Efekt dźwiękowy pokonania przeciwnika nie będzie odtwarzany.")
        stomp_sound = None

    while True:
        game_loop(jump_sound, stomp_sound)

def game_loop(jump_sound, stomp_sound):
    player = Player()
    
    # Tworzenie platform
    platforms = pygame.sprite.Group()
    ground = Platform(0, SCREEN_HEIGHT - 20, WORLD_WIDTH, 20)
    plat1 = Platform(100, SCREEN_HEIGHT - 120, 200, 20)
    plat2 = Platform(350, SCREEN_HEIGHT - 250, 150, 20)
    plat3 = Platform(550, SCREEN_HEIGHT - 400, 100, 20)
    plat4 = Platform(800, SCREEN_HEIGHT - 150, 200, 20)
    plat5 = Platform(1100, SCREEN_HEIGHT - 300, 150, 20)
    plat6 = Platform(1400, SCREEN_HEIGHT - 200, 100, 20)
    plat7 = Platform(1600, SCREEN_HEIGHT - 350, 100, 20)
    platforms.add(ground, plat1, plat2, plat3, plat4, plat5, plat6, plat7)

    # Tworzenie celu
    goal = Goal(WORLD_WIDTH - 100, SCREEN_HEIGHT - 20 - 50)
    goals = pygame.sprite.Group()
    goals.add(goal)

    # Tworzenie przeciwników
    enemy1 = Enemy(400, SCREEN_HEIGHT - 250 - 30) # Na platformie plat2
    enemy1.start_x = 400 
    enemy2 = Enemy(850, SCREEN_HEIGHT - 150 - 30) # Na platformie plat4
    enemy2.start_x = 850
    enemies = pygame.sprite.Group()
    enemies.add(enemy1, enemy2)
    
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    all_sprites.add(platforms)
    all_sprites.add(enemies)
    all_sprites.add(goals)
    
    camera_x = 0
    score = 0
    font = pygame.font.SysFont(None, 36)
    
    clock = pygame.time.Clock()
    start_ticks = pygame.time.get_ticks() # Początkowy czas
    time_limit = 90 # Limit czasu w sekundach

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    player.jump(jump_sound)

        seconds = (pygame.time.get_ticks() - start_ticks) / 1000 # Obliczanie ile sekund minęło
        remaining_time = time_limit - seconds
        
        if remaining_time <= 0:
            pygame.mixer.music.stop()
            show_end_screen(screen, "Koniec czasu!", score)
            running = False

        pressed_keys = pygame.key.get_pressed()
        
        player.update(pressed_keys, platforms)
        enemies.update()
        
        score += 1

        collided_enemy = pygame.sprite.spritecollideany(player, enemies)
        if collided_enemy:
            if player.velocity_y > 0 and player.rect.bottom < collided_enemy.rect.centery:
                if stomp_sound:
                    stomp_sound.play()
                collided_enemy.kill()
                player.velocity_y = -10
                score += 100
            else:
                pygame.mixer.music.stop()
                show_end_screen(screen, "Koniec gry!", score)
                running = False
        
        if pygame.sprite.spritecollideany(player, goals):
            pygame.mixer.music.stop()
            show_end_screen(screen, "Wygrałeś! Gratulacje!", score)
            running = False

        camera_x = player.rect.centerx - SCREEN_WIDTH / 2
        if camera_x < 0:
            camera_x = 0
        if camera_x > WORLD_WIDTH - SCREEN_WIDTH:
            camera_x = WORLD_WIDTH - SCREEN_WIDTH

        screen.fill((135, 206, 235))
        for entity in all_sprites:
            shifted_rect = entity.rect.copy()
            shifted_rect.x -= camera_x
            screen.blit(entity.surf, shifted_rect)
            
        score_text = font.render(f'Wynik: {score}', True, BLACK)
        screen.blit(score_text, (10, 10))
        
        timer_text = font.render(f'Czas: {int(remaining_time)}', True, BLACK)
        screen.blit(timer_text, (SCREEN_WIDTH - 150, 10))

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()