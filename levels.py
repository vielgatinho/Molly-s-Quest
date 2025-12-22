import pygame
import random
from settings import *
from sprites import Platform, Enemy, Goal, Treat

class Level:
    def __init__(self, level_data):
        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.goals = pygame.sprite.Group()
        self.treats = pygame.sprite.Group()
        self.particles = pygame.sprite.Group()
        self.floating_texts = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        
        self.world_width = level_data.get('world_width', WORLD_WIDTH)
        self.time_limit = level_data.get('time_limit', 90)
        
        # Tworzenie platform
        for plat_data in level_data.get('platforms', []):
            # plat_data: (x, y, width, height)
            plat = Platform(*plat_data)
            self.platforms.add(plat)
            self.all_sprites.add(plat)
            
        # Tworzenie przeciwników
        for enemy_data in level_data.get('enemies', []):
            # enemy_data: (x, y)
            enemy = Enemy(*enemy_data)
            enemy.start_x = enemy_data[0]
            self.enemies.add(enemy)
            self.all_sprites.add(enemy)
            
        # Tworzenie celu
        if 'goal' in level_data:
            goal = Goal(*level_data['goal'])
            self.goals.add(goal)
            self.all_sprites.add(goal)

        # Tworzenie smaczków
        for treat_pos in level_data.get('treats', []):
            treat = Treat(*treat_pos)
            self.treats.add(treat)
            self.all_sprites.add(treat)

def generate_random_level(difficulty):
    """Generuje losowy poziom na podstawie trudności (numeru poziomu)."""
    # Zwiększamy świat i czas wraz z trudnością
    world_width = 2000 + (difficulty * 500)
    
    # Szanse zależne od poziomu trudności (rosną wraz z numerem poziomu)
    enemy_chance = 0.3 + (difficulty * 0.1)  # Np. poziom 0: 30%, poziom 4: 70%
    treat_chance = 0.6 + (difficulty * 0.05) # Np. poziom 0: 60%, poziom 4: 80%
    
    level_data = {
        'world_width': world_width,
        'time_limit': 90 + (difficulty * 15),
        'platforms': [],
        'enemies': [],
        'treats': [],
        'goal': (world_width - 150, SCREEN_HEIGHT - 110) # Cel zawsze na końcu
    }
    
    # Podłoga na całej długości poziomu
    level_data['platforms'].append((0, SCREEN_HEIGHT - 60, world_width, 60))
    
    # Generowanie losowych platform
    current_x = 200
    last_platform_y = SCREEN_HEIGHT - 60 # Zaczynamy od poziomu podłogi

    while current_x < world_width - 200:
        width = random.randint(100, 300)
        height = 20
        
        # Generowanie Y zależne od poprzedniej platformy (aby dało się wskoczyć)
        max_jump_up = 190
        max_drop_down = 300
        
        min_y = max(SCREEN_HEIGHT - 450, last_platform_y - max_jump_up)
        max_y = min(SCREEN_HEIGHT - 150, last_platform_y + max_drop_down)
        
        if min_y > max_y:
            min_y = max_y
            
        y = random.randint(min_y, max_y)
        
        # Obliczamy różnicę wysokości przed aktualizacją last_platform_y
        height_diff = last_platform_y - y
        last_platform_y = y

        level_data['platforms'].append((current_x, y, width, height))
        
        # Szansa na przeciwnika na platformie (jeśli jest wystarczająco szeroka)
        if width > 150 and current_x > 600 and random.random() < enemy_chance:
            level_data['enemies'].append((current_x + random.randint(20, width - 60), y - 60))
            
        # Szansa na smaczek nad platformą
        if random.random() < treat_chance:
            level_data['treats'].append((current_x + width // 2, y - 50))
            
        # Szansa na przeciwnika na podłodze
        # Unikamy spawnowania na samym początku (x < 600), żeby gracz nie zginął od razu
        if current_x > 600 and random.random() < enemy_chance:
            level_data['enemies'].append((current_x, SCREEN_HEIGHT - 120))
            
        # Obliczanie odstępu (gap) zależnie od różnicy wysokości
        if height_diff > 120: # Wysoki skok
            gap = random.randint(30, 150)
        elif height_diff > 0: # Mały skok w górę
            gap = random.randint(50, 220)
        else: # Skok w dół lub poziom
            gap = random.randint(100, 300)
            
        current_x += width + gap

    return level_data

# Tworzymy listę 5 poziomów o rosnącej trudności (indeksy 0-4)
LEVEL_LIST = [generate_random_level(i) for i in range(5)]