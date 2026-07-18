import pygame
import random
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# Classe pour la gestion du son
class SoundManager:
    # Initialiser le son 
    def __init__(self):
        # Initialisation du mixer
        if not pygame.mixer.get_init():
            try:
                # Parametre de son
                pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            except Exception as e:
                logger.error(f"Erreur init mixer: {e}")
        
        pygame.mixer.set_num_channels(32)
        
        # Chemins des dossiers 
        self.base_path = Path(__file__).parent.parent / "Assets"
        self.bgm_path = self.base_path / "BGM"
        self.sfx_path = self.base_path / "SFX"



        # --- Chargement des sons ---
        self.sounds = {
            # Dossiers (Sons aléatoires)
            "clicks": self._load_folder(self.sfx_path / "button click SFX"),
            "wind": self._load_folder(self.sfx_path / "wind SFX"),
            "birds": self._load_folder(self.sfx_path / "birds SFX"),
            "grass": self._load_folder(self.sfx_path / "grass SFX"),
            "dash": self._load_folder(self.sfx_path / "dash SFX"),
            
            # Fichiers Uniques (Sons précis selon l'arborescence)
            "plant": self._load_file(self.sfx_path / "plant SFX" / "seeding.mp3", volume=0.8),
            "harvest": self._load_file(self.sfx_path / "plant SFX" / "harvest.mp3"),
            "fire_damage": self._load_file(self.sfx_path / "fire SFX" / "burning.mp3"),
            "extinguish": self._load_file(self.sfx_path / "fire SFX" / "extinguish.mp3")
        }

        # Playlists Musique
        self.playlists = {
            "menu": list((self.bgm_path / "in menu").glob("*.mp3")),
            "game": list((self.bgm_path / "in game").glob("*.mp3"))
        }

        self.current_playlist_name = None
        
        # Cooldowns
        self.last_step_time = 0
        self.step_delay = 350
        self.last_damage_time = 0
        # 1 seconde entre chaque bruit de brûlure (1000 milisecondes)
        self.damage_delay = 1000
        self.next_ambiance_time = pygame.time.get_ticks() + random.randint(2000, 10000)




    # Charger tout un dossier de sons.
    def _load_folder(self, folder_path: Path) -> list:
        loaded_sounds = []
        if folder_path.exists():
            files = list(folder_path.glob("*.mp3")) + list(folder_path.glob("*.wav"))
            for file in files:
                try:
                    s = pygame.mixer.Sound(str(file))
                    s.set_volume(0.4)
                    loaded_sounds.append(s)
                except Exception as e:
                    logger.error(f"Erreur son {file}: {e}")
        return loaded_sounds



    # Charger un fichier son unique.
    def _load_file(self, file_path: Path, volume: float = 0.5):
        if file_path.exists():
            try:
                s = pygame.mixer.Sound(str(file_path))
                s.set_volume(0.5)
                return s
            except Exception as e:
                logger.error(f"Erreur chargement fichier {file_path}: {e}")
        else:
            logger.warning(f"Fichier introuvable : {file_path}")
        return None




    # --- Début Méthodes de jeu ---

    # Son quand on clique avec la souris
    def play_click(self):
        if self.sounds["clicks"]: random.choice(self.sounds["clicks"]).play()

    # Son quand on se déplace
    def play_footstep(self):
        now = pygame.time.get_ticks()
        if now - self.last_step_time > self.step_delay:
            if self.sounds["grass"]:
                random.choice(self.sounds["grass"]).play()
                self.last_step_time = now



    # --- Début Jouer X son ---
    def play_plant(self):
        if self.sounds["plant"]: self.sounds["plant"].play()

    def play_harvest(self):
        if self.sounds["harvest"]: self.sounds["harvest"].play()

    def play_extinguish(self):
        if self.sounds["extinguish"]: self.sounds["extinguish"].play()

    def play_fire_damage(self):
        now = pygame.time.get_ticks()
        if now - self.last_damage_time > self.damage_delay:
            if self.sounds["fire_damage"]:
                self.sounds["fire_damage"].play()
                self.last_damage_time = now
    # --- Fin Jouer X son ---


    # Varier la musique
    def update_music(self, scene_name):
        target = "menu" if scene_name == "menu" else "game"
        if self.current_playlist_name == target: return
        
        self.current_playlist_name = target
        if self.playlists[target]:
            m = random.choice(self.playlists[target])
            try:
                pygame.mixer.music.load(str(m))
                pygame.mixer.music.set_volume(0.2)
                pygame.mixer.music.play(-1, fade_ms=500)
            except: pass

    # Varier l'ambiance
    def update_ambiance(self):
        now = pygame.time.get_ticks()
        if now > self.next_ambiance_time:
            cat = "birds" if random.random() > 0.2 else "wind"
            if self.sounds[cat]:
                s = random.choice(self.sounds[cat])
                s.set_volume(0.05 if cat == "birds" else 0.1)
                s.play()
            self.next_ambiance_time = now + random.randint(5000, 15000)
    
    # --- Fin Méthodes de jeu ---