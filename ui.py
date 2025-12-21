import pygame
import sys
import math
from settings import *
from utils import load_image, load_font

def show_start_screen(screen):
    font = load_font('content/ui/pixel_font.otf', 55)
    
    background = load_image("content/textures/enviroment/background.png", (SCREEN_WIDTH, SCREEN_HEIGHT))
    if not background:
        background = pygame.Surface(screen.get_size())
        background.fill(SKY_BLUE)

    title_surf = load_image("content/ui/title.png")
    if title_surf:
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50))
    else:
        title_main = font.render(CAPTION, True, GOLD)
        title_shadow = font.render(CAPTION, True, BLACK)
        title_surf = pygame.Surface((title_main.get_width() + 2, title_main.get_height() + 2), pygame.SRCALPHA)
        title_surf.blit(title_shadow, (2, 2))
        title_surf.blit(title_main, (0, 0))
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50))

    start_surf = load_image("content/ui/press_key.png")
    if start_surf:
        if start_surf.get_width() > SCREEN_WIDTH - 60:
            ratio = (SCREEN_WIDTH - 60) / start_surf.get_width()
            new_height = int(start_surf.get_height() * ratio)
            start_surf = pygame.transform.scale(start_surf, (SCREEN_WIDTH - 60, new_height))
    else:
        start_main = font.render("Naciśnij dowolny klawisz, aby rozpocząć", True, GOLD)
        start_shadow = font.render("Naciśnij dowolny klawisz, aby rozpocząć", True, BLACK)
        start_surf = pygame.Surface((start_main.get_width() + 2, start_main.get_height() + 2), pygame.SRCALPHA)
        start_surf.blit(start_shadow, (2, 2))
        start_surf.blit(start_main, (0, 0))
    
    start_rect = start_surf.get_rect(center=(SCREEN_WIDTH / 2, title_rect.bottom + 50))

    screen.blit(background, (0,0))
    screen.blit(title_surf, title_rect)
    screen.blit(start_surf, start_rect)
    pygame.display.flip()

    pygame.time.wait(500) # Czekaj 0.5 sekundy
    pygame.event.clear()  # Wyczyść przypadkowe kliknięcia

    clock = pygame.time.Clock()
    waiting = True
    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                waiting = False
        
        # Animacja pulsowania (zmiana przezroczystości)
        alpha = (math.sin(pygame.time.get_ticks() * 0.005) + 1) * 127.5
        start_surf.set_alpha(int(alpha))

        screen.blit(background, (0,0))
        screen.blit(title_surf, title_rect)
        screen.blit(start_surf, start_rect)
        pygame.display.flip()

def show_end_screen(screen, message, score):
    font = load_font('content/ui/pixel_font.otf', 55)
    score_font = load_font('content/ui/pixel_font.otf', 35)
    
    background = pygame.Surface(screen.get_size()).convert()
    background.fill(BLACK)
    background = load_image("content/textures/enviroment/background_end.jpg", (SCREEN_WIDTH, SCREEN_HEIGHT))
    if not background:
        background = pygame.Surface(screen.get_size()).convert()
        background.fill(BLACK)
    
    text_shadow = font.render(message, True, BLACK)
    text_rect_shadow = text_shadow.get_rect(center=(SCREEN_WIDTH / 2 + 2, SCREEN_HEIGHT / 2 - 48))
    text = font.render(message, True, GOLD)
    text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50))
    
    score_shadow = score_font.render(f"Twój ostateczny wynik: {score}", True, BLACK)
    score_rect_shadow = score_shadow.get_rect(center=(SCREEN_WIDTH / 2 + 2, SCREEN_HEIGHT / 2 + 2))
    score_text = score_font.render(f"Twój ostateczny wynik: {score}", True, GOLD)
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

    restart_shadow = score_font.render("Naciśnij dowolny klawisz, aby zagrać ponownie", True, BLACK)
    restart_rect_shadow = restart_shadow.get_rect(center=(SCREEN_WIDTH / 2 + 2, SCREEN_HEIGHT / 2 + 52))
    restart_text = score_font.render("Naciśnij dowolny klawisz, aby zagrać ponownie", True, GOLD)
    restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50))

    screen.blit(background, (0,0))
    screen.blit(text_shadow, text_rect_shadow)
    screen.blit(text, text_rect)
    screen.blit(score_shadow, score_rect_shadow)
    screen.blit(score_text, score_rect)
    screen.blit(restart_shadow, restart_rect_shadow)
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
