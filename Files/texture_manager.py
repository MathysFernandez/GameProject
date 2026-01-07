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
    
def texture_feu(taille_cellule : int, num_img : int = 0):
# ---Animation feu---
        # Charger l'image complète
        feu_source = pygame.image.load("Assets/solfeu.png").convert_alpha()
        
        # Rogner l'image
        #modifier num_img (y) pour la n ième image
        rect_rognage = pygame.Rect(0, num_img*25, 25, 25)
        feu_rognee = feu_source.subsurface(rect_rognage)
        
        # 3. Mettre à l'échelle la texture rognée (25x25) à la taille de la cellule
        feu_final = pygame.transform.scale(feu_rognee, (taille_cellule, taille_cellule))
        return feu_final






def texture_num_2_water(taille_cellule : int = 25, taille_frame : int = 25):
    # ---SpriteSheet eau 2 ---
    
    # Charger l'image complète
    water_source = pygame.image.load("Assets/water1.png").convert_alpha()
    
    # Rogner l'image
    rect_rognage2 = pygame.Rect(0, taille_frame, taille_frame, taille_frame)
    water_rognee2 = water_source.subsurface(rect_rognage2)
    
    # Mettre à l'échelle la texture rognée à la taille de la cellule
    water_final2 = pygame.transform.scale(water_rognee2, (taille_cellule, taille_cellule))
    
    return water_final2
    # ---SpriteSheet eau 2 ---


def texture_num_2_dechet(taille_cellule : int = 25, taille_frame : int = 25):
    
    # Charger l'image complète
    dechet = pygame.image.load("Assets/dechet.png").convert_alpha()
    
    # Rogner l'image
    rect_rognage = pygame.Rect(0, taille_frame, taille_frame, taille_frame)
    dechet_rognee = dechet.subsurface(rect_rognage)
    
    # Mettre à l'échelle la texture rognée à la taille de la cellule
    dechetfinal = pygame.transform.scale(dechet_rognee, (taille_cellule, taille_cellule))
    
    return dechetfinal


def charger_texture(taille_cellule, taille_frame: int = 25):
    try:
        floor = pygame.image.load("Assets/sol1.png").convert_alpha()
        floor = pygame.transform.scale(floor, (taille_cellule, taille_cellule))
        mur = pygame.image.load("Assets/pierre.png").convert_alpha()
        mur = pygame.transform.scale(mur, (taille_cellule, taille_cellule))
        mur2 = pygame.image.load("Assets/pierre_opt.png").convert_alpha()
        mur2 = pygame.transform.scale(mur2, (taille_cellule, taille_cellule))
        
        feu_source = pygame.image.load("Assets/solfeu.png").convert_alpha()
        # Chaque frame fait 25x25. On se déplace de 25px verticalement par image.
        rect_rognage = pygame.Rect(0, 0, 25, 25)
        feu_rognee = feu_source.subsurface(rect_rognage)
        feu_final = pygame.transform.scale(feu_rognee, (taille_cellule, taille_cellule))
        
        rect_rognage = pygame.Rect(0, taille_frame, taille_frame, taille_frame)
        feu_rognee2 = feu_source.subsurface(rect_rognage)
        feu_final2 = pygame.transform.scale(feu_rognee2, (taille_cellule, taille_cellule))
        
        # ---SpriteSheet dechet---
        # img 1
        dechet = pygame.image.load("Assets/dechet.png").convert_alpha()
    
        # Rogner l'image
        rect_rognage = pygame.Rect(0, 0, taille_frame, taille_frame)
        dechet_rognee = dechet.subsurface(rect_rognage)
        
        # Mettre à l'échelle la texture rognée à la taille de la cellule
        dechet1 = pygame.transform.scale(dechet_rognee, (taille_cellule, taille_cellule))
        
        # ----------------------------------------------------------
        
        # img 2
        dechet = pygame.image.load("Assets/dechet.png").convert_alpha()
    
        # Rogner l'image
        rect_rognage = pygame.Rect(0, taille_frame, taille_frame, taille_frame)
        dechet_rognee = dechet.subsurface(rect_rognage)
        
        # Mettre à l'échelle la texture rognée à la taille de la cellule
        dechet2 = pygame.transform.scale(dechet_rognee, (taille_cellule, taille_cellule))
        # ---FIn SpriteSheet dechet---
        
        
        
        
        # ---SpriteSheet eau---
        # Charger l'image complète
        water_source = pygame.image.load("Assets/water1.png").convert_alpha()
        # Rogner l'image
        
        #modifier y pour la deuxième image
        rect_rognage = pygame.Rect(0, 0, taille_frame, taille_frame)
        water_rognee = water_source.subsurface(rect_rognage)
        
        # Mettre à l'échelle la texture rognée à la taille de la cellule
        water_final = pygame.transform.scale(water_rognee, (taille_cellule, taille_cellule))
        # ---FIN SpriteSheet eau---
        
        
        # Rogner l'image
        rect_rognage2 = pygame.Rect(0, taille_frame, taille_frame, taille_frame)
        water_rognee2 = water_source.subsurface(rect_rognage2)
        
        # Mettre à l'échelle la texture rognée à la taille de la cellule
        water_final2 = pygame.transform.scale(water_rognee2, (taille_cellule, taille_cellule))
    
        
        
        
    except pygame.error as e:
        logger.error("Erreur lors du chargement des textures (texture_manager)")
        pygame.quit()
        exit()
    return floor, mur, mur2, water_final, water_final2, dechet1, dechet2, feu_final, feu_final2





def placer_texture(taille_cellule,largeur_grille,hauteur_grille, grille, avecBasseResolution : bool = False,  taille_frame : int = 25):
    
    floor, mur, mur2, water_final, water_final2, dechet1, dechet2, feu_final, feu_final2 = charger_texture(taille_cellule, taille_frame)
    
    # map de collision à tester la collisions
    collision_map_solid = {}
    collision_map_water = {}
    collision_map_dechet = {}
    collision_map_fire = {}
    
    for j in range(largeur_grille):
        for i in range(hauteur_grille):
            valeur_case = grille[i][j]
            
            x = j * taille_cellule
            y = i * taille_cellule
            
            # Génération des collisions basée sur la valeur (le nombre)
            if valeur_case == 1 or valeur_case == 2: # Murs
                rect_mur = pygame.Rect(x, y, taille_cellule, taille_cellule)
                collision_map_solid[(j, i)] = rect_mur
            
            elif valeur_case == -1: # Eau
                rect_water = pygame.Rect(x, y, taille_cellule, taille_cellule)
                collision_map_water[(j, i)] = rect_water
                
            elif valeur_case == 3: #déchet
                rect_dechet = pygame.Rect(x, y, taille_cellule, taille_cellule)
                collision_map_dechet[(j, i)] = rect_dechet
            
            elif valeur_case == 4: #feu
                collision_map_fire[(j, i)] = pygame.Rect(x, y, taille_cellule, taille_cellule)
            
    logger.info("placer_texture() effectué")
    return grille, collision_map_solid, collision_map_water, collision_map_dechet, collision_map_fire