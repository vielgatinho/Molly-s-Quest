import pygame
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

# Definicje poziomów
LEVEL_1 = {
    'world_width': 2000,
    'time_limit': 90,
    'platforms': [
        (0, SCREEN_HEIGHT - 60, 2000, 60),
        (100, SCREEN_HEIGHT - 160, 200, 20),
        (350, SCREEN_HEIGHT - 290, 150, 20),
        (550, SCREEN_HEIGHT - 440, 100, 20),
        (800, SCREEN_HEIGHT - 190, 200, 20),
        (1100, SCREEN_HEIGHT - 340, 150, 20),
        (1400, SCREEN_HEIGHT - 240, 100, 20),
        (1600, SCREEN_HEIGHT - 390, 100, 20),
    ],
    'enemies': [
        (400, SCREEN_HEIGHT - 290 - 60),
        (850, SCREEN_HEIGHT - 190 - 60),
    ],
    'treats': [
        (200, SCREEN_HEIGHT - 160 - 40),
        (600, SCREEN_HEIGHT - 440 - 40),
        (1200, SCREEN_HEIGHT - 340 - 40),
    ],
    'goal': (2000 - 100, SCREEN_HEIGHT - 60 - 50)
}

LEVEL_2 = {
    'world_width': 2500,
    'time_limit': 120,
    'platforms': [
        (0, SCREEN_HEIGHT - 60, 2500, 60), # Dłuższa podłoga
        (200, SCREEN_HEIGHT - 190, 200, 20),
        (500, SCREEN_HEIGHT - 340, 200, 20),
        (900, SCREEN_HEIGHT - 440, 150, 20),
        (1300, SCREEN_HEIGHT - 290, 200, 20),
        (1700, SCREEN_HEIGHT - 390, 150, 20),
        (2100, SCREEN_HEIGHT - 240, 200, 20),
    ],
    'enemies': [
        (550, SCREEN_HEIGHT - 340 - 60),
        (1350, SCREEN_HEIGHT - 290 - 60),
        (2150, SCREEN_HEIGHT - 240 - 60),
    ],
    'treats': [
        (300, SCREEN_HEIGHT - 190 - 40),
        (1000, SCREEN_HEIGHT - 440 - 40),
        (1400, SCREEN_HEIGHT - 290 - 40),
        (1800, SCREEN_HEIGHT - 390 - 40),
    ],
    'goal': (2500 - 100, SCREEN_HEIGHT - 60 - 50)
}

LEVEL_LIST = [LEVEL_1, LEVEL_2]