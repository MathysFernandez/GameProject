import pygame
import random
import logging
from pathlib import Path

# On récupère le logger existant ou on en crée un
logger = logging.getLogger(__name__)

class SoundManager:
    def __init__(self):
        # Initialisation du mixer avec une bonne qualité
        # On vérifie si le mixer n'est pas déjà initialisé pour éviter les erreurs
        if not pygame.mixer.get_init():
            try:
                # buffer=512 réduit le décalage entre le clic et le son
                pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            except Exception as e:
                logger.error(f"Erreur init mixer: {e}")
        
        # Gestion des canaux pour éviter que les SFX coupent la musique
        pygame.mixer.set_num_channels(32)
        
        # Chemins dynamiques (plus propre que os.path.join partout)
        self.base_path = Path(__file__).parent.parent / "Assets"
        self.bgm_path = self.base_path / "BGM"
        self.sfx_path = self.base_path / "SFX"

        # --- Chargement des sons ---
        self.sounds = {
            "clicks": self._load_folder(self.sfx_path / "button click SFX"),
            "wind": self._load_folder(self.sfx_path / "wind SFX"),
            "birds": self._load_folder(self.sfx_path / "birds SFX"),
            "grass": self._load_folder(self.sfx_path / "grass SFX"),
            "dash": self._load_folder(self.sfx_path / "dash SFX")
        }

        # --- Playlists Musiques ---
        self.playlists = {
            "menu": list((self.bgm_path / "in menu").glob("*.mp3")),
            "game": list((self.bgm_path / "in game").glob("*.mp3"))
        }

        # --- Variables de contrôle ---
        self.current_playlist_name = None # Important pour éviter le freeze
        self.last_step_time = 0
        self.step_delay = 350  # ms entre chaque bruit de pas
        
        # Timer pour l'ambiance (vent/oiseaux)
        self.next_ambiance_time = pygame.time.get_ticks() + random.randint(2000, 10000)

    def _load_folder(self, folder_path: Path) -> list:
        """Charge tous les fichiers audio d'un dossier donné."""
        loaded_sounds = []
        if folder_path.exists():
            # Supporte mp3 et wav
            files = list(folder_path.glob("*.mp3")) + list(folder_path.glob("*.wav"))
            
            for file in files:
                try:
                    sound = pygame.mixer.Sound(str(file))
                    sound.set_volume(0.4) 
                    loaded_sounds.append(sound)
                except pygame.error as e:
                    logger.error(f"Erreur chargement son {file}: {e}")
        else:
            logger.warning(f"Dossier introuvable: {folder_path}")
        
        return loaded_sounds

    def update_music(self, scene_name):
        """
        Lance la musique correspondant à la scène.
        CORRECTION FREEZE : On ne relance la musique que si la scène change vraiment.
        """
        target_playlist = "menu" if scene_name == "menu" else "game"

        # SI ON EST DÉJÀ SUR LA BONNE PLAYLIST, ON NE FAIT RIEN 
        # (C'est cette ligne qui empêche le jeu de recharger le son 60 fois par seconde et de freezer)
        if self.current_playlist_name == target_playlist:
            return

        # Sinon, on change la musique
        self.current_playlist_name = target_playlist
        
        if target_playlist not in self.playlists or not self.playlists[target_playlist]:
            logger.warning(f"Playlist vide ou inconnue : {target_playlist}")
            return

        if self.playlists[target_playlist]:
            music_file = random.choice(self.playlists[target_playlist])
            try:
                pygame.mixer.music.load(str(music_file))
                pygame.mixer.music.set_volume(0.2) 
                # loops=-1 veut dire "boucle infinie", pygame gère tout seul
                pygame.mixer.music.play(loops=-1, fade_ms=500) 
                logger.info(f"Musique lancée: {music_file.name}")
            except pygame.error as e:
                logger.error(f"Erreur lecture musique: {e}")

    def play_click(self):
        if self.sounds["clicks"]:
            random.choice(self.sounds["clicks"]).play()

    def play_footstep(self):
        """Joue un bruit de pas avec un cooldown pour éviter l'effet mitraillette."""
        now = pygame.time.get_ticks()
        if now - self.last_step_time > self.step_delay:
            if self.sounds["grass"]:
                snd = random.choice(self.sounds["grass"])
                snd.set_volume(0.2)
                snd.play()
                self.last_step_time = now

    def update_ambiance(self):
        """Gère les sons aléatoires (vent, oiseaux) pendant le jeu."""
        now = pygame.time.get_ticks()
        if now > self.next_ambiance_time:
            # Pile ou face : Vent ou Oiseau
            category = "birds" if random.random() > 0.2 else "wind"
            
            if self.sounds[category]:
                sound = random.choice(self.sounds[category])
                # Le vent peut être un peu plus fort, les oiseaux plus discrets
                vol = 0.1 if category == "wind" else 0.05
                sound.set_volume(vol)
                sound.play()
            
            # Prochain son dans 5 à 15 secondes
            self.next_ambiance_time = now + random.randint(5000, 15000)

            # --- NOUVELLES MÉTHODES ---

    def play_plant(self):
        """Son quand on plante"""
        if self.sounds["plant"]:
            snd = random.choice(self.sounds["plant"])
            snd.set_volume(0.3)
            snd.play()

    def play_harvest(self):
        """Son quand on récolte"""
        if self.sounds["harvest"]:
            snd = random.choice(self.sounds["harvest"])
            snd.set_volume(0.4)
            snd.play()

    def play_extinguish(self):
        """Son quand on éteint le feu (pshhht)"""
        if self.sounds["extinguish"]:
            snd = random.choice(self.sounds["extinguish"])
            snd.set_volume(0.4)
            snd.play()

    def play_fire_damage(self):
        """Son quand on brûle (avec délai)"""
        now = pygame.time.get_ticks()
        if now - self.last_damage_time > self.damage_delay:
            if self.sounds["fire_damage"]:
                snd = random.choice(self.sounds["fire_damage"])
                snd.set_volume(0.6)
                snd.play()
                self.last_damage_time = now