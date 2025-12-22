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
    while current_x < world_width - 200:
        width = random.randint(100, 300)
        height = 20
        y = random.randint(SCREEN_HEIGHT - 450, SCREEN_HEIGHT - 150)
        
        level_data['platforms'].append((current_x, y, width, height))
        
        # Szansa na przeciwnika na platformie (jeśli jest wystarczająco szeroka)
        if width > 150 and random.random() < (0.5 * difficulty):
            level_data['enemies'].append((current_x + random.randint(20, width - 60), y - 60))
            
        # Szansa na smaczek nad platformą
        if random.random() < (0.6 * difficulty):
            level_data['treats'].append((current_x + width // 2, y - 50))
            
        # Przesuwamy się w prawo o szerokość platformy + losowy odstęp
        current_x += width + random.randint(100, 300)

    return level_data

# Tworzymy listę 5 poziomów o rosnącej trudności (indeksy 0-4)
LEVEL_LIST = [generate_random_level(i) for i in range(5)]