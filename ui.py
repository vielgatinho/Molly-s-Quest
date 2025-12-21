import pygame
import sys
from settings import *

def show_start_screen(screen):
    font = pygame.font.SysFont(None, 55)
    
    try:
        background = pygame.image.load("content/textures/enviroment/background.png").convert()
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    except (pygame.error, FileNotFoundError):
        background = pygame.Surface(screen.get_size())
        background.fill(SKY_BLUE)

    try:
        title_surf = pygame.image.load("content/ui/title.png").convert_alpha()
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50))
    except (pygame.error, FileNotFoundError):
        title_surf = font.render(CAPTION, True, WHITE)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50))

    start_text = font.render("Naciśnij dowolny klawisz, aby rozpocząć", True, WHITE)
    start_rect = start_text.get_rect(center=(SCREEN_WIDTH / 2, title_rect.bottom + 50))

    screen.blit(background, (0,0))
    screen.blit(title_surf, title_rect)
    screen.blit(start_text, start_rect)
    pygame.display.flip()

    pygame.time.wait(500) # Czekaj 0.5 sekundy
    pygame.event.clear()  # Wyczyść przypadkowe kliknięcia

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

    pygame.time.wait(500) # Czekaj 0.5 sekundy
    pygame.event.clear()  # Wyczyść przypadkowe kliknięcia

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                waiting = False
