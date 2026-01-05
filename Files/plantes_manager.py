import pygame
import logging
import os
from Files import config

logger = logging.getLogger(__name__)

class PlantesManager:
    def __init__(self, taille_cellule):
        self.plantes = {} 
        self.taille_cellule = taille_cellule
        
        # --- Configuration ---
        self.TEMPS_POUSSE = 2000
        self.STADE_MAX = 2
        self.POINTS_RECOLTE = 50
        
        # --- Chargement des Textures ---
        self.textures = {}
        self.utiliser_textures = False
        
        try:
            # On essaie de charger les 3 images
            # convert_alpha() est important pour la transparence du PNG
            img_0 = pygame.image.load(os.path.join("Assets", "plante_0.png")).convert_alpha()
            img_1 = pygame.image.load(os.path.join("Assets", "plante_1.png")).convert_alpha()
            img_2 = pygame.image.load(os.path.join("Assets", "plante_2.png")).convert_alpha()
            
            # On redimensionne les images à la taille de la case (avec une petite marge pour faire joli)
            # On fait -20 pixels pour que la plante soit un peu plus petite que la case
            taille_img = taille_cellule 
            self.textures[0] = pygame.transform.scale(img_0, (taille_img, taille_img))
            self.textures[1] = pygame.transform.scale(img_1, (taille_img, taille_img))
            self.textures[2] = pygame.transform.scale(img_2, (taille_img, taille_img))
            
            self.utiliser_textures = True
            logger.info("Textures des plantes chargées avec succès.")
            
        except Exception as e:
            logger.warning(f"Impossible de charger les images de plantes ({e}). Utilisation des carrés de couleur.")
            self.utiliser_textures = False

        # --- Couleurs de secours (si pas d'images) ---
        self.COULEURS = {
            0: (139, 69, 19),   # Marron
            1: (144, 238, 144), # Vert clair
            2: (34, 139, 34)    # Vert foncé
        }

    def update(self):
        """Fait grandir les plantes."""
        current_time = pygame.time.get_ticks()
        for coord, data in self.plantes.items():
            if data["etat"] < self.STADE_MAX:
                if current_time - data["timer"] > self.TEMPS_POUSSE:
                    data["etat"] += 1
                    data["timer"] = current_time

    def interagir(self, player_x, player_y, collision_map_water, sound_manager=None):
        """Planter ou Récolter."""
        gx = int(player_x // self.taille_cellule)
        gy = int(player_y // self.taille_cellule)
        coord = (gx, gy)
        
        # --- MODIF: Vérifier si c'est de l'eau ---
        if coord in collision_map_water:
            return 0
        # -----------------------------------------

        current_time = pygame.time.get_ticks()

        # PLANTER
        if coord not in self.plantes:
            self.plantes[coord] = {"etat": 0, "timer": current_time}
            # logger.info(f"Plante ajoutée en {coord}")
            return 0

        # RÉCOLTER
        else:
            if self.plantes[coord]["etat"] == self.STADE_MAX:
                del self.plantes[coord]
                # logger.info(f"Plante récoltée ! +{self.POINTS_RECOLTE} pts")
                return self.POINTS_RECOLTE
            else:
                return 0

    def draw(self, fenetre, camera_x, camera_y, largeur_fen, hauteur_fen):
        """Affiche les plantes (Images ou Carrés)."""
        for (gx, gy), data in self.plantes.items():
            
            screen_x = gx * self.taille_cellule + camera_x
            screen_y = gy * self.taille_cellule + camera_y

            # Optimisation affichage
            if -self.taille_cellule < screen_x < largeur_fen and -self.taille_cellule < screen_y < hauteur_fen:
                
                etat = data["etat"]
                
                # --- OPTION 1 : AFFICHER L'IMAGE ---
                if self.utiliser_textures:
                    texture = self.textures[etat]
                    # Centrer un peu l'image si elle est plus petite (optionnel)
                    # Ici on l'affiche direct
                    fenetre.blit(texture, (screen_x, screen_y))
                    
                    # Petit cadre blanc si prête à récolter (pour bien voir)
                    if etat == self.STADE_MAX:
                         rect_indic = pygame.Rect(screen_x, screen_y, self.taille_cellule, self.taille_cellule)
                         pygame.draw.rect(fenetre, (255, 255, 255), rect_indic, 2)

                # --- OPTION 2 : AFFICHER LE CARRÉ (Secours) ---
                else:
                    marge = 20
                    rect = pygame.Rect(screen_x + marge, screen_y + marge, 
                                     self.taille_cellule - (marge*2), self.taille_cellule - (marge*2))
                    color = self.COULEURS[etat]
                    pygame.draw.rect(fenetre, color, rect, border_radius=8)
                    
                    if etat == self.STADE_MAX:
                        pygame.draw.rect(fenetre, (255, 255, 255), rect, 3)