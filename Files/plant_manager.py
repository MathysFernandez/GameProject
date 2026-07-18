import pygame
import logging
import os
from Files import settings

logger = logging.getLogger(__name__)

# Classe des plantes avec ses caractéristique et ses fonctions
class PlantesManager:
    def __init__(self, taille_cellule):
        self.plantes = {} 
        self.taille_cellule = taille_cellule
        self.TEMPS_POUSSE = 2000
        self.STADE_MAX = 2
        self.POINTS_RECOLTE = 50
        
        self.textures = {}
        self.utiliser_textures = False
        
        try:
            img_0 = pygame.image.load(os.path.join("Assets", "plante_0.png")).convert_alpha()
            img_1 = pygame.image.load(os.path.join("Assets", "plante_1.png")).convert_alpha()
            img_2 = pygame.image.load(os.path.join("Assets", "plante_2.png")).convert_alpha()
            
            t = taille_cellule
            self.textures[0] = pygame.transform.scale(img_0, (t, t))
            self.textures[1] = pygame.transform.scale(img_1, (t, t))
            self.textures[2] = pygame.transform.scale(img_2, (t, t))
            self.utiliser_textures = True
        except Exception:
            self.utiliser_textures = False

        self.COULEURS = {0: (139, 69, 19), 1: (144, 238, 144), 2: (34, 139, 34)}

    # Augmenter l'etat 
    def update(self):
        current_time = pygame.time.get_ticks()
        for coord, data in self.plantes.items():
            if data["etat"] < self.STADE_MAX:
                if current_time - data["timer"] > self.TEMPS_POUSSE:
                    data["etat"] += 1
                    data["timer"] = current_time

    # Interaction avec collision 
    def interagir(self, player_x, player_y, collision_map_water, sound_manager=None):
        gx = int(player_x // self.taille_cellule)
        gy = int(player_y // self.taille_cellule)
        coord = (gx, gy)
        
        if coord in collision_map_water:
            return 0

        current_time = pygame.time.get_ticks()

        # Planter
        if coord not in self.plantes:
            self.plantes[coord] = {"etat": 0, "timer": current_time}
            # Son Plantation
            if sound_manager: sound_manager.play_plant() 
            logger.info(f"Le joueur à planté en {coord} ")
            return 0

        # Récolter
        else:
            if self.plantes[coord]["etat"] == self.STADE_MAX:
                del self.plantes[coord]
                # Son Récolte
                if sound_manager: sound_manager.play_harvest()
                logger.info(f"Le joueur à récolté en {coord} ")
                return self.POINTS_RECOLTE
            else:
                return 0

    # Dessiner les plantes en fonctions de l'état 
    def draw(self, fenetre, camera_x, camera_y, largeur_fen, hauteur_fen):
        for (gx, gy), data in self.plantes.items():
            screen_x = gx * self.taille_cellule + camera_x
            screen_y = gy * self.taille_cellule + camera_y

            if -self.taille_cellule < screen_x < largeur_fen and -self.taille_cellule < screen_y < hauteur_fen:
                etat = data["etat"]
                if self.utiliser_textures:
                    fenetre.blit(self.textures[etat], (screen_x, screen_y))
                    if etat == self.STADE_MAX:
                         r = pygame.Rect(screen_x, screen_y, self.taille_cellule, self.taille_cellule)
                         pygame.draw.rect(fenetre, (255, 255, 255), r, 2)
                else:
                    m = 20
                    r = pygame.Rect(screen_x+m, screen_y+m, self.taille_cellule-m*2, self.taille_cellule-m*2)
                    pygame.draw.rect(fenetre, self.COULEURS[etat], r, border_radius=8)