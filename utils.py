import pygame

def load_image(path, size=None):
    """Ładuje obrazek, konwertuje alpha i opcjonalnie skaluje."""
    try:
        img = pygame.image.load(path).convert_alpha()
        if size:
            img = pygame.transform.scale(img, size)
        return img
    except (pygame.error, FileNotFoundError) as e:
        print(f"Nie można załadować obrazka '{path}': {e}")
        return None

def load_font(path, size):
    """Ładuje czcionkę z pliku lub zwraca systemową w przypadku błędu."""
    try:
        return pygame.font.Font(path, size)
    except (pygame.error, FileNotFoundError) as e:
        print(f"Nie można załadować czcionki '{path}': {e}")
        return pygame.font.SysFont(None, size)

def load_sound(path):
    """Ładuje plik dźwiękowy."""
    try:
        return pygame.mixer.Sound(path)
    except (pygame.error, FileNotFoundError) as e:
        print(f"Nie można załadować dźwięku '{path}': {e}")
        return None