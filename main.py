import pygame
import sys
from settings import *
from sprites import Player, Platform, Goal, Enemy
from ui import show_start_screen, show_end_screen
from levels import Level, LEVEL_LIST

# Inicjalizacja Pygame
pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(CAPTION)

from pygame.locals import (
    K_SPACE,
    KEYDOWN,
)

def main():
    show_start_screen(screen)
    try:
        pygame.mixer.music.load('content/audio/background_music.mp3')
        pygame.mixer.music.play(-1) # Odtwarzaj w pętli
    except pygame.error:
        print("Nie można załadować pliku 'background_music.mp3'. Gra będzie bez muzyki.")
        
    try:
        jump_sound = pygame.mixer.Sound('content/audio/jump.wav')
    except pygame.error:
        print("Nie można załadować pliku 'jump.wav'. Efekt dźwiękowy skoku nie będzie odtwarzany.")
        jump_sound = None
    except FileNotFoundError:
        print("Plik 'jump.wav' nie został znaleziony. Efekt dźwiękowy skoku nie będzie odtwarzany.")
        jump_sound = None
        
    try:
        stomp_sound = pygame.mixer.Sound('content/audio/stomp.wav')
    except pygame.error:
        print("Nie można załadować pliku 'stomp.wav'. Efekt dźwiękowy pokonania przeciwnika nie będzie odtwarzany.")
        stomp_sound = None
    except FileNotFoundError:
        print("Plik 'stomp.wav' nie został znaleziony. Efekt dźwiękowy pokonania przeciwnika nie będzie odtwarzany.")
        stomp_sound = None

    current_level_index = 0
    total_score = 0
    lives = 3

    while current_level_index < len(LEVEL_LIST):
        if not pygame.mixer.music.get_busy():
            try:
                pygame.mixer.music.play(-1)
            except pygame.error:
                pass

        level_data = LEVEL_LIST[current_level_index]
        result, score = game_loop(jump_sound, stomp_sound, level_data, total_score, lives)
        
        if result == 'win':
            score += lives * 300 # Bonus za zachowane życia
            total_score = score
            current_level_index += 1
            if current_level_index < len(LEVEL_LIST):
                show_end_screen(screen, f"Poziom {current_level_index} ukończony!", total_score)
            else:
                show_end_screen(screen, "Wygrałeś całą grę!", total_score)
                current_level_index = 0
                total_score = 0
                lives = 3
                show_start_screen(screen)
        elif result == 'died':
            lives -= 1
            if lives == 0:
                show_end_screen(screen, "Koniec gry!", score)
                current_level_index = 0
                total_score = 0
                lives = 3
                show_start_screen(screen)
            # Jeśli życia > 0, pętla wykona się ponownie dla tego samego poziomu (restart)
        elif result == 'quit':
            break

def game_loop(jump_sound, stomp_sound, level_data, start_score, lives):
    player = Player()
    level = Level(level_data)
    level.all_sprites.add(player)
    
    try:
        background_image = pygame.image.load("content/textures/enviroment/background.png").convert()
        background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    except (pygame.error, FileNotFoundError):
        print("Nie można załadować tła 'background.png'.")
        background_image = None

    try:
        heart_img = pygame.image.load("content/ui/heart.png").convert_alpha()
        heart_img = pygame.transform.scale(heart_img, (30, 30))
    except (pygame.error, FileNotFoundError):
        heart_img = None

    camera_x = 0
    score = start_score
    font = pygame.font.SysFont(None, 36)
    
    clock = pygame.time.Clock()
    start_ticks = pygame.time.get_ticks() # Początkowy czas
    time_limit = level.time_limit

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
            return 'died', score

        pressed_keys = pygame.key.get_pressed()
        
        player.update(pressed_keys, level.platforms, level.world_width)
        level.enemies.update()
        
        collided_enemy = pygame.sprite.spritecollideany(player, level.enemies)
        if collided_enemy:
            if player.velocity_y > 0 and player.rect.bottom < collided_enemy.rect.centery:
                if stomp_sound:
                    stomp_sound.play()
                collided_enemy.kill()
                player.velocity_y = -10
                score += 150
            else:
                pygame.mixer.music.stop()
                return 'died', score
        
        # Zbieranie smaczków
        collided_treats = pygame.sprite.spritecollide(player, level.treats, True)
        for treat in collided_treats:
            score += 50

        if pygame.sprite.spritecollideany(player, level.goals):
            pygame.mixer.music.stop()
            return 'win', score

        camera_x = player.rect.centerx - SCREEN_WIDTH / 2
        if camera_x < 0:
            camera_x = 0
        if camera_x > level.world_width - SCREEN_WIDTH:
            camera_x = level.world_width - SCREEN_WIDTH

        if background_image:
            screen.blit(background_image, (0, 0))
        else:
            screen.fill(SKY_BLUE)
            
        for entity in level.all_sprites:
            shifted_rect = entity.rect.copy()
            shifted_rect.x -= camera_x
            screen.blit(entity.surf, shifted_rect)
            
        score_text = font.render(f'Wynik: {score}', True, BLACK)
        screen.blit(score_text, (10, 10))
        
        timer_text = font.render(f'Czas: {int(remaining_time)}', True, BLACK)
        screen.blit(timer_text, (SCREEN_WIDTH - 150, 10))

        if heart_img:
            for i in range(lives):
                screen.blit(heart_img, (10 + i * 35, 50))

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()