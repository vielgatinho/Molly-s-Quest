import pygame
import sys
from settings import *
from sprites import Player, Particle, FloatingText
from levels import Level, LEVEL_LIST
from ui import show_start_screen, show_end_screen, show_pause_menu, show_main_menu, show_leaderboard, show_settings_menu
from utils import load_image, load_font, load_sound, save_score_to_leaderboard, load_leaderboard, save_game_state, load_game_state
from pygame.locals import K_SPACE, KEYDOWN, QUIT, K_ESCAPE

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(CAPTION)
        self.clock = pygame.time.Clock()
        
        self.music_volume = 0.5
        self.sfx_volume = 0.5
        
        self.load_assets()
        
        self.running = True
        self.current_level_index = 0
        self.total_score = 0
        self.lives = 3

    def load_assets(self):
        # Muzyka
        try:
            pygame.mixer.music.load('content/audio/background_music.mp3')
            pygame.mixer.music.set_volume(self.music_volume)
        except pygame.error:
            print("Nie można załadować pliku 'background_music.mp3'. Gra będzie bez muzyki.")

        # Dźwięki
        self.jump_sound = load_sound('content/audio/jump.mp3')
        if self.jump_sound: self.jump_sound.set_volume(self.sfx_volume)
        self.stomp_sound = load_sound('content/audio/stomp.mp3')
        if self.stomp_sound: self.stomp_sound.set_volume(self.sfx_volume)

        # Grafiki UI (ładowane raz)
        self.background_image = load_image("content/textures/enviroment/background2.png", (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.heart_img = load_image("content/ui/heart.png", (30, 30))
        
        self.score_label_img = load_image("content/ui/score.png")
        if self.score_label_img:
            target_h = 30
            scale = target_h / self.score_label_img.get_height()
            new_w = int(self.score_label_img.get_width() * scale)
            self.score_label_img = pygame.transform.scale(self.score_label_img, (new_w, target_h))

        self.time_label_img = load_image("content/ui/time.png")
        if self.time_label_img:
            target_h = 30
            scale = target_h / self.time_label_img.get_height()
            new_w = int(self.time_label_img.get_width() * scale)
            self.time_label_img = pygame.transform.scale(self.time_label_img, (new_w, target_h))
            
        self.font = load_font('content/ui/pixel_font.otf', 36)

    def play_music(self):
        try:
            pygame.mixer.music.play(-1)
        except pygame.error:
            pass

    def reset_game(self):
        self.current_level_index = 0
        self.total_score = 0
        self.lives = 3

    def run(self):
        while True: # Główna pętla aplikacji
            show_start_screen(self.screen)
            
            # Menu główne
            action = show_main_menu(self.screen)
            
            if action == 'quit':
                break
            elif action == 'leaderboard':
                data = load_leaderboard()
                show_leaderboard(self.screen, data)
                continue # Wróć do początku pętli (ekran startowy/menu)
            elif action == 'settings':
                self.music_volume, self.sfx_volume = show_settings_menu(self.screen, self.music_volume, self.sfx_volume)
                
                # Zastosuj zmiany
                pygame.mixer.music.set_volume(self.music_volume)
                if self.jump_sound: self.jump_sound.set_volume(self.sfx_volume)
                if self.stomp_sound: self.stomp_sound.set_volume(self.sfx_volume)
                
                continue
            elif action == 'load_game':
                state = load_game_state()
                if state:
                    self.current_level_index = state.get('level', 0)
                    self.total_score = state.get('score', 0)
                    self.lives = state.get('lives', 3)
                    self.play_music()
                else:
                    continue
            elif action == 'new_game':
                self.reset_game()
                self.play_music()

            # Pętla gry (poziomy)
            while self.current_level_index < len(LEVEL_LIST):
                if not pygame.mixer.music.get_busy():
                    self.play_music()

                level_data = LEVEL_LIST[self.current_level_index]
                result, score = self.run_level(level_data)
                
                if result == 'win':
                    score += self.lives * 300 # Bonus za zachowane życia
                    self.total_score = score
                    self.current_level_index += 1
                    if self.current_level_index < len(LEVEL_LIST):
                        # Automatyczny zapis po ukończeniu poziomu
                        save_game_state({
                            'level': self.current_level_index,
                            'score': self.total_score,
                            'lives': self.lives
                        })
                        # Tutaj można dodać ekran przejściowy, na razie używamy end_screen tylko na koniec gry
                        pass 
                    else:
                        player_name = show_end_screen(self.screen, "Wygrałeś całą grę!", self.total_score)
                        save_score_to_leaderboard(player_name, self.total_score)
                        break # Wróć do menu głównego
                elif result == 'died':
                    self.lives -= 1
                    if self.lives == 0:
                        player_name = show_end_screen(self.screen, "Koniec gry!", score)
                        save_score_to_leaderboard(player_name, score)
                        break # Wróć do menu głównego
                elif result == 'quit':
                    pygame.quit()
                    sys.exit()
        
        pygame.quit()
        sys.exit()

    def run_level(self, level_data):
        player = Player()
        level = Level(level_data)
        level.all_sprites.add(player)
        
        camera_x = 0
        score = self.total_score
        
        start_ticks = pygame.time.get_ticks()
        time_limit = level.time_limit

        running = True
        while running:
            self.clock.tick(60)
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    return 'quit', score
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        player.jump(self.jump_sound)
                    elif event.key == K_ESCAPE:
                        # Obsługa pauzy
                        pygame.mixer.music.pause()
                        pause_start = pygame.time.get_ticks()
                        
                        action = show_pause_menu(self.screen)
                        
                        pause_end = pygame.time.get_ticks()
                        # Korekta czasu gry o czas trwania pauzy, aby licznik czasu nie uciekł
                        start_ticks += (pause_end - pause_start) 
                        pygame.mixer.music.unpause()
                        
                        if action == 'quit':
                            return 'quit', score
                        elif action == 'save':
                            save_game_state({
                                'level': self.current_level_index,
                                'score': self.total_score,
                                'lives': self.lives
                            })

            seconds = (pygame.time.get_ticks() - start_ticks) / 1000
            remaining_time = time_limit - seconds
            
            if remaining_time <= 0:
                pygame.mixer.music.stop()
                return 'died', score

            pressed_keys = pygame.key.get_pressed()
            
            player.update(pressed_keys, level.platforms, level.world_width)
            level.enemies.update()
            level.goals.update()
            level.treats.update()
            level.particles.update()
            level.floating_texts.update()
            
            # Kolizje z przeciwnikami
            collided_enemy = pygame.sprite.spritecollideany(player, level.enemies)
            if collided_enemy:
                if player.velocity_y > 0 and player.rect.bottom < collided_enemy.rect.centery:
                    if self.stomp_sound:
                        self.stomp_sound.play()
                    collided_enemy.kill()
                    player.velocity_y = -10
                    score += 150
                    # Cząsteczki przy pokonaniu przeciwnika (czerwone)
                    for _ in range(15):
                        p = Particle(collided_enemy.rect.centerx, collided_enemy.rect.centery, RED)
                        level.particles.add(p)
                        level.all_sprites.add(p)
                    # Tekst z punktami
                    text = FloatingText(collided_enemy.rect.centerx, collided_enemy.rect.top, "+150", GOLD)
                    level.floating_texts.add(text)
                    level.all_sprites.add(text)
                else:
                    pygame.mixer.music.stop()
                    return 'died', score
            
            # Zbieranie smaczków
            collided_treats = pygame.sprite.spritecollide(player, level.treats, True)
            for treat in collided_treats:
                score += 50
                # Cząsteczki przy zebraniu smaczka (złote)
                for _ in range(10):
                    p = Particle(treat.rect.centerx, treat.rect.centery, GOLD)
                    level.particles.add(p)
                    level.all_sprites.add(p)
                # Tekst z punktami
                text = FloatingText(treat.rect.centerx, treat.rect.top, "+50", GOLD)
                level.floating_texts.add(text)
                level.all_sprites.add(text)

            # Cel
            if pygame.sprite.spritecollideany(player, level.goals):
                pygame.mixer.music.stop()
                return 'win', score

            # Kamera
            camera_x = player.rect.centerx - SCREEN_WIDTH / 2
            if camera_x < 0:
                camera_x = 0
            if camera_x > level.world_width - SCREEN_WIDTH:
                camera_x = level.world_width - SCREEN_WIDTH

            # Rysowanie
            if self.background_image:
                self.screen.blit(self.background_image, (0, 0))
            else:
                self.screen.fill(SKY_BLUE)
                
            for entity in level.all_sprites:
                shifted_rect = entity.rect.copy()
                shifted_rect.x -= camera_x
                self.screen.blit(entity.surf, shifted_rect)
                
            self.draw_ui(score, remaining_time)

            pygame.display.flip()

    def draw_ui(self, score, remaining_time):
        # Wynik
        if self.score_label_img:
            self.screen.blit(self.score_label_img, (10, 10))
            score_shadow = self.font.render(str(score), True, BLACK)
            self.screen.blit(score_shadow, (10 + self.score_label_img.get_width() + 12, 12))
            score_val = self.font.render(str(score), True, GOLD)
            self.screen.blit(score_val, (10 + self.score_label_img.get_width() + 10, 10))
        else:
            score_shadow = self.font.render(f'Wynik: {score}', True, BLACK)
            self.screen.blit(score_shadow, (12, 12))
            score_text = self.font.render(f'Wynik: {score}', True, GOLD)
            self.screen.blit(score_text, (10, 10))
        
        # Czas
        if self.time_label_img:
            self.screen.blit(self.time_label_img, (SCREEN_WIDTH - 180, 10))
            timer_shadow = self.font.render(str(int(remaining_time)), True, BLACK)
            self.screen.blit(timer_shadow, (SCREEN_WIDTH - 180 + self.time_label_img.get_width() + 12, 12))
            timer_val = self.font.render(str(int(remaining_time)), True, GOLD)
            self.screen.blit(timer_val, (SCREEN_WIDTH - 180 + self.time_label_img.get_width() + 10, 10))
        else:
            timer_shadow = self.font.render(f'Czas: {int(remaining_time)}', True, BLACK)
            self.screen.blit(timer_shadow, (SCREEN_WIDTH - 148, 12))
            timer_text = self.font.render(f'Czas: {int(remaining_time)}', True, GOLD)
            self.screen.blit(timer_text, (SCREEN_WIDTH - 150, 10))

        # Poziom (na środku)
        level_str = f"Poziom {self.current_level_index + 1}"
        level_shadow = self.font.render(level_str, True, BLACK)
        level_text = self.font.render(level_str, True, GOLD)
        level_rect = level_text.get_rect(midtop=(SCREEN_WIDTH // 2, 10))
        self.screen.blit(level_shadow, (level_rect.x + 2, level_rect.y + 2))
        self.screen.blit(level_text, level_rect)

        # Życia
        if self.heart_img:
            for i in range(self.lives):
                self.screen.blit(self.heart_img, (10 + i * 35, 50))