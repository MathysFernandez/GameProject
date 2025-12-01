import pygame
import logging

# On crée un logger pour ce fichier.
# Le module logging sait que la configuration globale a déjà été faite.
logger = logging.getLogger(__name__)

#-1 water
#0 sol
#1 mur1
#2 mur2
#3 mur 3
def joueur_texture(taille_joueur : int, angle : int = 0): 
    joueur = pygame.image.load("Assets/joueur_1.png").convert_alpha()
    joueur = pygame.transform.scale(joueur, (taille_joueur, taille_joueur))
    joueur = pygame.transform.rotate(joueur, angle-90)
    return joueur

#divise l'image par 3 pour le sprite sheet du joueur

def texture_joueur(taille_joueur : int, angle : int = 0, num_img : int = 0):
# ---SpriteSheet joueur---
        # Charger l'image complète
        joueur_source = pygame.image.load("Assets/joueur_1.png").convert_alpha()
        
        # Rogner l'image
        #modifier num_img (y) pour la n ième image
        rect_rognage = pygame.Rect(0, num_img*25, 25, 25)
        joueur_rognee = joueur_source.subsurface(rect_rognage)
        
        # 3. Mettre à l'échelle la texture rognée (25x25) à la taille de la cellule
        joueur_final = pygame.transform.scale(joueur_rognee, (taille_joueur, taille_joueur))
        joueur_final = pygame.transform.rotate(joueur_final, angle-90)
        return joueur_final



def placer_texture(taille_cellule,largeur_grille,hauteur_grille, grille):
    try:
        floor = pygame.image.load("Assets/sol1.png").convert_alpha()
        floor = pygame.transform.scale(floor, (taille_cellule, taille_cellule))
        mur = pygame.image.load("Assets/pierre.png").convert_alpha()
        mur = pygame.transform.scale(mur, (taille_cellule, taille_cellule))
        mur2 = pygame.image.load("Assets/pierre_opt.png").convert_alpha()
        mur2 = pygame.transform.scale(mur2, (taille_cellule, taille_cellule))
        water = pygame.image.load("Assets/water1.png").convert_alpha()
        water = pygame.transform.scale(water, (taille_cellule, taille_cellule))
        
    except pygame.error as e:
        logger.info("Erreur lors du chargement des textures (texture_manager)")
        print("Erreur lors du chargement des textures (texture_manager)")
        pygame.quit()
        exit()
    
    # map de collision à tester la collisions (sans filtre)
    collision_map_solid = {}
    collision_map_water = {}
    
    for j in range(largeur_grille):
        for i in range(hauteur_grille):
            if grille[i][j] == 0 :
                grille[i][j] = floor
            elif grille[i][j] == 1 or grille[i][j] == 2:
                # --- murs ---
                if grille[i][j] == 1:
                    grille[i][j] = mur
                elif grille[i][j] == 2:
                    grille[i][j] = mur2
                    
                # Créer un rectangle représentant la position du mur dans le monde
                x = j * taille_cellule
                y = i * taille_cellule
                rect_mur = pygame.Rect(x, y, taille_cellule, taille_cellule)

                # Stocker le rectangle de collision dans notre map de collision par grille
                # On stocke le rect directement, c'est suffisant pour la collision
                collision_map_solid[(j, i)] = rect_mur # Clé (grid_x, grid_y)
                # --- FIN murs ---
            
            
            elif grille[i][j] == -1:
                # --- water ---
                grille[i][j] = water
                
                # Créer un rectangle représentant la position du mur dans le monde
                x = j * taille_cellule
                y = i * taille_cellule
                rect_water = pygame.Rect(x, y, taille_cellule, taille_cellule)

                # Stocker le rectangle de collision dans notre map de collision par grille
                # On stocke le rect directement, c'est suffisant pour la collision
                collision_map_water[(j, i)] = rect_water # Clé (grid_x, grid_y)
                # --- FIN water ---
            
    logger.info("placer_texture() effectué")        
    return grille, collision_map_solid, collision_map_water