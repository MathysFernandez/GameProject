import logging


import pygame
import sys
import json
import os
from Files import config 
from Files import textures_manager
from Files import Lecteur_map as lecteur

logger = logging.getLogger(__name__)

nom_fichier_a_ouvrir = lecteur.derniereSauvegarde()
nombre_texture = config.nombre_texture

pygame.init()

#horloge Interne
horloge = pygame.time.Clock()
FPS = config.FPS

# Dimension ecran
largeur_fenetre, hauteur_fenetre = config.get_dimensions()

# Créer la fenêtre
fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))

# récupérer grille
largeur_grille, hauteur_grille, grille = lecteur.chargerfichier(nom_fichier_a_ouvrir)

taille_cellule = config.taille_cellule



floor, mur, mur2, water_final = textures_manager.charger_texture(1, config.taille_frame)

TEXTURES_BASE = {
    -1: water_final,
    0: floor,
    1: mur,
    2: mur2
}

minimap_surface = pygame.Surface((largeur_grille, hauteur_grille))


# taille cellule
if largeur_grille > largeur_fenetre:
    taille_cellule = largeur_fenetre // largeur_grille
else:
    taille_cellule = hauteur_fenetre // hauteur_grille
if taille_cellule < 1:
    taille_cellule = 1


# Position initiale de la caméra
camera_x = 0
camera_y = 0

# Couleurs
couleur_grille = (100, 100, 100)
couleur_cellule = (200, 200, 200)

# ---Police---
BLANC = (255, 255, 255)

chosen_letter = 0


# Variable pour suivre l'état du bouton gauche
mouse_left_button_held = False

# Fonction pour rendre et positionner le texte
def creer_surface_texte(texte):
    police = pygame.font.SysFont('Arial', 50)
    surface = police.render(texte, True, BLANC)
    rect = surface.get_rect()
    rect.topleft = (10, 0) 
    return surface, rect

def mettre_a_jour_textures_zoom(nouvelle_taille):
    TEXTURES_ACTUELLES.clear()
    for id_texture, image_originale in TEXTURES_BASE.items():
        TEXTURES_ACTUELLES[id_texture] = pygame.transform.scale(image_originale, (nouvelle_taille, nouvelle_taille))

def mettre_a_jour_pixel_minimap(gx, gy, texture_id):
    if 0 <= gx < largeur_grille and 0 <= gy < hauteur_grille:
        if texture_id in TEXTURES_MINIMAP:
            micro_image = TEXTURES_MINIMAP[texture_id]
            minimap_surface.blit(micro_image, (gx, gy))

def recharger_donnees_carte():
    global largeur_grille, hauteur_grille, grille, minimap_surface
    largeur_grille, hauteur_grille, grille = lecteur.chargerfichier(nom_fichier_a_ouvrir)
    
    minimap_surface = pygame.Surface((largeur_grille, hauteur_grille))
    
    for y in range(hauteur_grille):
        for x in range(largeur_grille):
            id_actuel = grille[y][x]
            if id_actuel in TEXTURES_MINIMAP:
                 minimap_surface.blit(TEXTURES_MINIMAP[id_actuel], (x, y))

# Création initiale de la surface et du rectangle du texte
lettre_surface, lettre_rect = creer_surface_texte(str(chosen_letter))

TEXTURES_MINIMAP = {}
for id_tex, image_base in TEXTURES_BASE.items():
    #On reduit chaque image a 1 pixel
    TEXTURES_MINIMAP[id_tex] = pygame.transform.scale(image_base, (1, 1))
    
for y in range(hauteur_grille):
    for x in range(largeur_grille):
        id_actuel = grille[y][x]
        # On utilise TEXTURES_MINIMAP ici !
        if id_actuel in TEXTURES_MINIMAP:
             minimap_surface.blit(TEXTURES_MINIMAP[id_actuel], (x, y))

TEXTURES_ACTUELLES = {}
mettre_a_jour_textures_zoom(taille_cellule)

for y in range(hauteur_grille):
    for x in range(largeur_grille):
        mettre_a_jour_pixel_minimap(x, y, grille[y][x])

largeur_map_ecran = largeur_grille * taille_cellule
hauteur_map_ecran = hauteur_grille * taille_cellule
minimap_scale = pygame.transform.scale(minimap_surface, (largeur_map_ecran, hauteur_map_ecran))

taille_changement_de_mode_affichage = 20
grille_modifier = False

# On détecte si on veut voir TOUTE la carte 
mode_vue_globale = True



running = True
while running:
    # ---variables à réinitialiser---
    taille_cellule_change = False
    
    
        
    #deplacement vitesse
    vitesse = config.vitesse *5
    # FIN ---variables à réinitialiser---
    
    #touche pressé
    keys_pressed = pygame.key.get_pressed()
    
    # gestion évènements
    for event in pygame.event.get():
        # Si l'utilisateur clique sur la croix de fermeture
        if event.type == pygame.QUIT:
            if grille_modifier:
                lecteur.modifier_grille(nom_fichier_a_ouvrir, grille)
                logger.info("Sauvegarde de la Carte depuis le Concepteur")
            running = False
        
        # Si un bouton de la souris est pressé
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                mouse_left_button_held = True
                
                
        # Si un bouton de la souris est relâché
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == pygame.BUTTON_LEFT:
                mouse_left_button_held = False
            if event.button == 4:
                mode_vue_globale = False
                taille_cellule += 1
                taille_cellule_change = True
                mettre_a_jour_textures_zoom(taille_cellule)
            if event.button == 5:
                if taille_cellule > 1:
                    taille_cellule -= 1
                    taille_cellule_change = True
                    mettre_a_jour_textures_zoom(taille_cellule)
                else:
                    # Si on est déjà à 1 et qu'on dézoome encore -> On active la vue globale
                    mode_vue_globale = True
                
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_i:
                if grille_modifier:
                    lecteur.modifier_grille(nom_fichier_a_ouvrir, grille)
                    logger.info("Sauvegarde de la Carte depuis le Concepteur")
            # changer de choix de texture à positionner via le control left
            if event.key == pygame.K_LCTRL:
                if chosen_letter >= nombre_texture-1:
                    chosen_letter = 0
                else:
                    chosen_letter += 1
                
                lettre_surface, lettre_rect = creer_surface_texte(str(chosen_letter))
            
            #choix spécifique
            elif event.key == pygame.K_c:
                chosen_letter = 0
                lettre_surface, lettre_rect = creer_surface_texte(str(chosen_letter))
            elif event.key == pygame.K_m:
                chosen_letter = 1
                lettre_surface, lettre_rect = creer_surface_texte(str(chosen_letter))
            
            
            # changer de taille map
            if event.key == pygame.K_F3 or event.key == pygame.K_KP_PLUS:
                lecteur.ajouter(nom_fichier_a_ouvrir, 0)
                recharger_donnees_carte() 
                
                # Recalcul de la taille cellule comme tu le faisais
                if largeur_grille > largeur_fenetre:
                    # Attention à ne pas diviser par 0 si grille vide
                    taille_cellule = largeur_fenetre // (largeur_grille + 2) if largeur_grille > 0 else 10
                else:
                    taille_cellule = hauteur_fenetre //  (hauteur_grille + 2) if hauteur_grille > 0 else 10
                
                taille_cellule_change = True
                mettre_a_jour_textures_zoom(taille_cellule) # Important de remettre à jour les textures
            
            if event.key == pygame.K_F4 or event.key == pygame.K_KP_MINUS:
                lecteur.retirer(nom_fichier_a_ouvrir)
                recharger_donnees_carte() 
                
                if largeur_grille > largeur_fenetre:
                    taille_cellule = largeur_fenetre // (largeur_grille + 2) if largeur_grille > 0 else 10
                else:
                    taille_cellule = hauteur_fenetre //  (hauteur_grille + 2) if hauteur_grille > 0 else 10
                
                taille_cellule_change = True
                mettre_a_jour_textures_zoom(taille_cellule)
    
    #si le bouton gauche de la souris est maintenu enfoncé
    if mouse_left_button_held and taille_cellule > taille_changement_de_mode_affichage:
        # l'événement MOUSEBUTTONDOWN contient la position du clic:
        x, y = event.pos
        
        # position en nombre de cellules 
        cellular_x = int((x - camera_x )/ taille_cellule)
        cellular_y = int((y - camera_y )/ taille_cellule)
        if 0 <= cellular_y < hauteur_grille and 0 <= cellular_x < largeur_grille:
        # positionner les nouvelles tuiles (en focntion des textures choisis)
            grille[cellular_y][cellular_x] = chosen_letter
            mettre_a_jour_pixel_minimap(cellular_x, cellular_y, chosen_letter)
            grille_modifier = True
        
        
        
        
        
        if taille_cellule < 5: 
            taille_cellule_change = True
    
    # Gestion évènement déplacement
    vitesse += vitesse * keys_pressed[pygame.K_LSHIFT]
    deplacement_x = (keys_pressed[pygame.K_d] or keys_pressed[pygame.K_RIGHT]) - (keys_pressed[pygame.K_q] or keys_pressed[pygame.K_LEFT])
    deplacement_y = (keys_pressed[pygame.K_s] or keys_pressed[pygame.K_DOWN]) - (keys_pressed[pygame.K_z] or keys_pressed[pygame.K_UP])
    
    #vitesse deplacement en diagonale réduit 
    if deplacement_x != 0 and deplacement_y != 0:
        vitesse *= config.multiplicateur_vitesse_diagonale
    
    #application du deplacement
    if not mode_vue_globale:
        deplacement_x *= vitesse
        deplacement_y *= vitesse
        
    # Appliquez le mouvement 
    camera_x -= deplacement_x
    camera_y -= deplacement_y
    
    
    
    
    
    
    # --- Rendu graphique de la scène ---
    
    # Dessiner la grille
    # Efface l'écran en le remplissant de noir. Cela supprime tous les dessins de la frame précédente.
    fenetre.fill((0, 0, 0))
    

    
    # Coordonnées monde du coin supérieur gauche de l'écran
    world_x_start_screen = -camera_x
    world_y_start_screen = -camera_y

    # Coordonnées monde du coin inférieur droit de l'écran
    world_x_end_screen = world_x_start_screen + largeur_fenetre
    world_y_end_screen = world_y_start_screen + hauteur_fenetre
    
    if mode_vue_globale:
        
        #On calcule le ratio
        ratio_w = largeur_fenetre / largeur_grille
        ratio_h = hauteur_fenetre / hauteur_grille
        ratio = min(ratio_w, ratio_h) # On prend le plus petit pour que tout rentre
        
        new_w = int(largeur_grille * ratio)
        new_h = int(hauteur_grille * ratio)
        
        # redimensionnement
        map_ecrasée = pygame.transform.scale(minimap_surface, (new_w, new_h))
        
        #On centre l'image à l'écran (optionnel, pour faire joli)
        pos_x = (largeur_fenetre - new_w) // 2
        pos_y = (hauteur_fenetre - new_h) // 2
        
        fenetre.blit(map_ecrasée, (pos_x, pos_y))
    
    elif taille_cellule < taille_changement_de_mode_affichage:
        
        
        # Étirer la minimap (C'est rapide pour le GPU)
        # Note : pour encore plus de perfs, ne faire ce scale que si 'taille_cellule' change
        if taille_cellule_change :
            #Calculer la taille qu'aura la carte entière à l'écran
            largeur_map_ecran = largeur_grille * taille_cellule
            hauteur_map_ecran = hauteur_grille * taille_cellule
            minimap_scale = pygame.transform.scale(minimap_surface, (largeur_map_ecran, hauteur_map_ecran))
        
        #L'afficher à la position de la caméra
        fenetre.blit(minimap_scale, (camera_x, camera_y))
    else:
        # Convertir ces coordonnées monde en indices de grille
        start_grid_x = int(world_x_start_screen // taille_cellule) -1 #+6
        end_grid_x = int(world_x_end_screen // taille_cellule) +1 #-5 # +1 

        start_grid_y = int(world_y_start_screen // taille_cellule) -1 # +2
        end_grid_y = int(world_y_end_screen // taille_cellule) +1 #-1 # +1 
        # S'assurer que les indices restent dans les limites de la grille réelle
        start_grid_x = max(0, start_grid_x)
        end_grid_x = min(largeur_grille, end_grid_x) 
        start_grid_y = max(0, start_grid_y)
        end_grid_y = min(hauteur_grille, end_grid_y) 



        # --- Dessiner uniquement les cellules visibles ---
        for y in range(start_grid_y, end_grid_y):
            for x in range(start_grid_x, end_grid_x):
                texture_id = grille[y][x]
                
                # SECURITÉ : On vérifie que l'ID existe bien dans nos textures chargées
                # et qu'il n'est pas None
                if texture_id is not None and texture_id in TEXTURES_ACTUELLES:
                        
                    # Calcule la position de la cellule à l'écran
                    screen_x = x * taille_cellule + camera_x
                    screen_y = y * taille_cellule + camera_y

                    # Dessine la texture en fonction de la grille
                    img = TEXTURES_ACTUELLES[texture_id]
                    
                    fenetre.blit(img, (screen_x, screen_y))
    # --- FIN Dessiner uniquement les cellules visibles ---
    
    
    
    fenetre.blit(lettre_surface, lettre_rect)
    # --- Fin Rendu graphique de la scène ---
    pygame.display.flip()
    horloge.tick(FPS)
pygame.quit()
sys.exit()  

    