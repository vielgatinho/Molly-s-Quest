import pygame
import json
import os

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

def load_leaderboard(filename="leaderboard.json"):
    """Wczytuje tabelę wyników z pliku JSON."""
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

def save_score_to_leaderboard(name, score, filename="leaderboard.json"):
    """Zapisuje wynik do tabeli. Aktualizuje wynik, jeśli nick istnieje i nowy wynik jest lepszy."""
    name = name.lower()
    data = load_leaderboard(filename)
    
    found = False
    for entry in data:
        if entry["name"].lower() == name:
            found = True
            # Aktualizuj tylko jeśli nowy wynik jest lepszy
            if score > entry["score"]:
                entry["score"] = score
                entry["name"] = name
            break
    
    if not found:
        data.append({"name": name, "score": score})
    
    # Sortowanie malejąco po wyniku
    data.sort(key=lambda x: x["score"], reverse=True)
    
    # Ograniczenie do np. top 10 (opcjonalne, ale dobre dla porządku)
    data = data[:10]
    
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
    except IOError as e:
        print(f"Błąd zapisu tabeli wyników: {e}")

def save_game_state(state, filename="savegame.json"):
    """Zapisuje stan gry do pliku JSON."""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=4)
        return True
    except IOError as e:
        print(f"Błąd zapisu gry: {e}")
        return False

def load_game_state(filename="savegame.json"):
    """Wczytuje stan gry z pliku JSON."""
    if not os.path.exists(filename):
        return None
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return None