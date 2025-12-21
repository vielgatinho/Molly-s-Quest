import pygame
from settings import *
from sprites import Platform, Enemy, Goal

class Level:
    def __init__(self, level_data):
        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.goals = pygame.sprite.Group()
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

# Definicje poziomów
LEVEL_1 = {
    'world_width': 2000,
    'time_limit': 90,
    'platforms': [
        (0, SCREEN_HEIGHT - 20, 2000, 20),
        (100, SCREEN_HEIGHT - 120, 200, 20),
        (350, SCREEN_HEIGHT - 250, 150, 20),
        (550, SCREEN_HEIGHT - 400, 100, 20),
        (800, SCREEN_HEIGHT - 150, 200, 20),
        (1100, SCREEN_HEIGHT - 300, 150, 20),
        (1400, SCREEN_HEIGHT - 200, 100, 20),
        (1600, SCREEN_HEIGHT - 350, 100, 20),
    ],
    'enemies': [
        (400, SCREEN_HEIGHT - 250 - 30),
        (850, SCREEN_HEIGHT - 150 - 30),
    ],
    'goal': (2000 - 100, SCREEN_HEIGHT - 20 - 50)
}

LEVEL_2 = {
    'world_width': 2500,
    'time_limit': 120,
    'platforms': [
        (0, SCREEN_HEIGHT - 20, 2500, 20), # Dłuższa podłoga
        (200, SCREEN_HEIGHT - 150, 200, 20),
        (500, SCREEN_HEIGHT - 300, 200, 20),
        (900, SCREEN_HEIGHT - 400, 150, 20),
        (1300, SCREEN_HEIGHT - 250, 200, 20),
        (1700, SCREEN_HEIGHT - 350, 150, 20),
        (2100, SCREEN_HEIGHT - 200, 200, 20),
    ],
    'enemies': [
        (550, SCREEN_HEIGHT - 300 - 30),
        (1350, SCREEN_HEIGHT - 250 - 30),
        (2150, SCREEN_HEIGHT - 200 - 30),
    ],
    'goal': (2500 - 100, SCREEN_HEIGHT - 20 - 50)
}

LEVEL_LIST = [LEVEL_1, LEVEL_2]