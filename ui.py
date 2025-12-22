import pygame
import sys
import math
from settings import *
from utils import load_image, load_font, load_game_state
from pygame.locals import K_RETURN, K_BACKSPACE, KEYDOWN

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
    """Wyświetla ekran końcowy i pozwala wpisać nick. Zwraca wpisany nick."""
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

    input_info_shadow = score_font.render("Wpisz swój nick i naciśnij ENTER:", True, BLACK)
    input_info_rect_shadow = input_info_shadow.get_rect(center=(SCREEN_WIDTH / 2 + 2, SCREEN_HEIGHT / 2 + 62))
    input_info_text = score_font.render("Wpisz swój nick i naciśnij ENTER:", True, GOLD)
    input_info_rect = input_info_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 60))

    screen.blit(background, (0,0))
    screen.blit(text_shadow, text_rect_shadow)
    screen.blit(text, text_rect)
    screen.blit(score_shadow, score_rect_shadow)
    screen.blit(score_text, score_rect)
    screen.blit(input_info_shadow, input_info_rect_shadow)
    screen.blit(input_info_text, input_info_rect)
    pygame.display.flip()

    pygame.time.wait(500) # Czekaj 0.5 sekundy
    pygame.event.clear()  # Wyczyść przypadkowe kliknięcia

    player_name = ""
    waiting = True
    clock = pygame.time.Clock()

    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    if len(player_name) > 0: # Wymuś wpisanie czegokolwiek
                        return player_name
                elif event.key == K_BACKSPACE:
                    player_name = player_name[:-1]
                else:
                    # Limit długości nicku
                    if len(player_name) < 12 and event.unicode.isprintable():
                        player_name += event.unicode
        
        # Odświeżanie wpisywanego tekstu
        # Czyścimy fragment ekranu pod napisem zachęcającym
        screen.blit(background, (0, SCREEN_HEIGHT / 2 + 90), pygame.Rect(0, SCREEN_HEIGHT / 2 + 90, SCREEN_WIDTH, 100))
        
        name_surf = score_font.render(player_name + "_", True, WHITE)
        name_rect = name_surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 110))
        screen.blit(name_surf, name_rect)
        
        pygame.display.flip()
    return player_name

def show_pause_menu(screen):
    """Wyświetla menu pauzy i zwraca akcję ('continue', 'save', 'quit')."""
    # Zrób zrzut ekranu gry
    background_snapshot = screen.copy()
    
    # Przyciemnienie
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(150) # Półprzezroczystość (0-255)
    overlay.fill(BLACK)
    background_snapshot.blit(overlay, (0, 0))
    
    font = load_font('content/ui/pixel_font.otf', 50)
    
    # Przyciski (jako prostokąty do detekcji myszy)
    center_x = SCREEN_WIDTH // 2
    continue_rect = pygame.Rect(0, 0, 300, 60)
    continue_rect.center = (center_x, SCREEN_HEIGHT // 2 - 60)
    
    save_rect = pygame.Rect(0, 0, 300, 60)
    save_rect.center = (center_x, SCREEN_HEIGHT // 2)
    
    quit_rect = pygame.Rect(0, 0, 300, 60)
    quit_rect.center = (center_x, SCREEN_HEIGHT // 2 + 60)
    
    clock = pygame.time.Clock()
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 'continue'
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Lewy przycisk myszy
                    if continue_rect.collidepoint(mouse_pos):
                        return 'continue'
                    if save_rect.collidepoint(mouse_pos):
                        return 'save'
                    if quit_rect.collidepoint(mouse_pos):
                        return 'quit'
        
        # Rysowanie tła (zrzut gry + przyciemnienie)
        screen.blit(background_snapshot, (0, 0))
        
        # Rysowanie przycisków
        for rect, text in [(continue_rect, "Kontynuuj"), (save_rect, "Zapisz grę"), (quit_rect, "Wyjdź")]:
            color = GOLD
            if rect.collidepoint(mouse_pos):
                color = WHITE # Podświetlenie po najechaniu
            
            # Cień tekstu
            shadow_surf = font.render(text, True, BLACK)
            shadow_rect = shadow_surf.get_rect(center=(rect.centerx + 2, rect.centery + 2))
            screen.blit(shadow_surf, shadow_rect)
            
            # Tekst
            text_surf = font.render(text, True, color)
            text_rect = text_surf.get_rect(center=rect.center)
            screen.blit(text_surf, text_rect)
            
        pygame.display.flip()
        clock.tick(60)

def show_main_menu(screen):
    """Wyświetla menu główne z opcjami."""
    background = load_image("content/textures/enviroment/background.png", (SCREEN_WIDTH, SCREEN_HEIGHT))
    if not background:
        background = pygame.Surface(screen.get_size())
        background.fill(SKY_BLUE)

    font = load_font('content/ui/pixel_font.otf', 45)
    
    save_exists = load_game_state() is not None
    
    # Konfiguracja przycisków: (Tekst, Akcja, Czy aktywny)
    buttons = [
        {"text": "NOWA GRA", "action": "new_game", "active": True},
        {"text": "WCZYTAJ GRĘ", "action": "load_game", "active": save_exists},
        {"text": "TABELA WYNIKÓW", "action": "leaderboard", "active": True},
        {"text": "USTAWIENIA", "action": "settings", "active": True},
        {"text": "WYJDŹ", "action": "quit", "active": True}
    ]
    
    button_rects = []
    center_x = SCREEN_WIDTH // 2
    start_y = SCREEN_HEIGHT // 2 - 80
    gap = 60
    
    # Przygotowanie prostokątów przycisków
    for i, btn in enumerate(buttons):
        text_surf = font.render(btn["text"], True, WHITE)
        rect = text_surf.get_rect(center=(center_x, start_y + i * gap))
        rect.inflate_ip(40, 20) # Powiększ obszar kliknięcia
        button_rects.append((rect, btn))

    clock = pygame.time.Clock()
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for rect, btn in button_rects:
                        if btn["active"] and rect.collidepoint(mouse_pos):
                            return btn["action"]
        
        screen.blit(background, (0, 0))
        
        for rect, btn in button_rects:
            color = (100, 100, 100) # Szary dla nieaktywnych
            if btn["active"]:
                color = GOLD
                if rect.collidepoint(mouse_pos):
                    color = WHITE # Podświetlenie
            
            # Cień tekstu
            shadow_surf = font.render(btn["text"], True, BLACK)
            shadow_rect = shadow_surf.get_rect(center=(rect.centerx + 2, rect.centery + 2))
            screen.blit(shadow_surf, shadow_rect)
            
            # Tekst
            text_surf = font.render(btn["text"], True, color)
            text_rect = text_surf.get_rect(center=rect.center)
            screen.blit(text_surf, text_rect)
            
        pygame.display.flip()
        clock.tick(60)

def show_leaderboard(screen, data):
    """Wyświetla tabelę wyników."""
    background = load_image("content/textures/enviroment/background.png", (SCREEN_WIDTH, SCREEN_HEIGHT))
    if not background:
        background = pygame.Surface(screen.get_size())
        background.fill(SKY_BLUE)
        
    title_font = load_font('content/ui/pixel_font.otf', 50)
    entry_font = load_font('content/ui/pixel_font.otf', 35)
    
    screen.blit(background, (0, 0))
    
    # Tytuł
    title = title_font.render("TABELA WYNIKÓW", True, GOLD)
    title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 80))
    screen.blit(title, title_rect)
    
    # Lista wyników
    start_y = 160
    for i, entry in enumerate(data):
        text = f"{i+1}. {entry['name']} - {entry['score']}"
        surf = entry_font.render(text, True, WHITE)
        rect = surf.get_rect(center=(SCREEN_WIDTH // 2, start_y + i * 40))
        screen.blit(surf, rect)
        
    if not data:
        info = entry_font.render("Brak wyników", True, (200, 200, 200))
        screen.blit(info, info.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))

    # Instrukcja powrotu
    back_text = entry_font.render("Naciśnij ESC, aby wrócić", True, GOLD)
    back_rect = back_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60))
    screen.blit(back_text, back_rect)
    
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    waiting = False
        pygame.time.Clock().tick(60)

def show_settings_menu(screen, music_vol, sfx_vol):
    """Wyświetla menu ustawień (głośność). Zwraca (music_vol, sfx_vol)."""
    background = load_image("content/textures/enviroment/background.png", (SCREEN_WIDTH, SCREEN_HEIGHT))
    if not background:
        background = pygame.Surface(screen.get_size())
        background.fill(SKY_BLUE)
        
    font = load_font('content/ui/pixel_font.otf', 45)
    small_font = load_font('content/ui/pixel_font.otf', 30)
    
    center_x = SCREEN_WIDTH // 2
    
    # Paski głośności
    bar_width = 300
    bar_height = 30
    
    music_rect = pygame.Rect(0, 0, bar_width, bar_height)
    music_rect.center = (center_x, SCREEN_HEIGHT // 2 - 50)
    
    sfx_rect = pygame.Rect(0, 0, bar_width, bar_height)
    sfx_rect.center = (center_x, SCREEN_HEIGHT // 2 + 50)
    
    back_rect = pygame.Rect(0, 0, 200, 50)
    back_rect.center = (center_x, SCREEN_HEIGHT - 100)
    
    dragging_music = False
    dragging_sfx = False
    
    clock = pygame.time.Clock()
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return music_vol, sfx_vol
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if back_rect.collidepoint(mouse_pos):
                        return music_vol, sfx_vol
                    
                    if music_rect.collidepoint(mouse_pos):
                        dragging_music = True
                        val = (mouse_pos[0] - music_rect.x) / music_rect.width
                        music_vol = max(0.0, min(1.0, val))
                        
                    if sfx_rect.collidepoint(mouse_pos):
                        dragging_sfx = True
                        val = (mouse_pos[0] - sfx_rect.x) / sfx_rect.width
                        sfx_vol = max(0.0, min(1.0, val))
                        
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging_music = False
                    dragging_sfx = False
        
        # Obsługa przeciągania
        if dragging_music:
            val = (mouse_pos[0] - music_rect.x) / music_rect.width
            music_vol = max(0.0, min(1.0, val))
        
        if dragging_sfx:
            val = (mouse_pos[0] - sfx_rect.x) / sfx_rect.width
            sfx_vol = max(0.0, min(1.0, val))
            
        screen.blit(background, (0, 0))
        
        # Tytuł
        title = font.render("USTAWIENIA", True, GOLD)
        title_rect = title.get_rect(center=(center_x, 80))
        screen.blit(title, title_rect)
        
        # Rysowanie pasków
        for rect, vol, label_text in [(music_rect, music_vol, "Muzyka"), (sfx_rect, sfx_vol, "Efekty")]:
            label = small_font.render(f"{label_text}: {int(vol * 100)}%", True, WHITE)
            screen.blit(label, (rect.x, rect.y - 35))
            
            pygame.draw.rect(screen, BLACK, rect, 2) # Obramowanie
            pygame.draw.rect(screen, (100, 100, 100), rect) # Tło
            
            fill_width = int(rect.width * vol)
            fill_rect = pygame.Rect(rect.x, rect.y, fill_width, rect.height)
            pygame.draw.rect(screen, GOLD, fill_rect)
        
        # Przycisk powrotu
        color = WHITE if back_rect.collidepoint(mouse_pos) else GOLD
        back_surf = font.render("POWRÓT", True, color)
        screen.blit(back_surf, back_surf.get_rect(center=back_rect.center))
        
        pygame.display.flip()
        clock.tick(60)
