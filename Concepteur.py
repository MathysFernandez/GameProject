import logging


import pygame
import sys
import json
import os
from Files import config 
from Files import textures_manager
from Files import Lecteur_map as lecteur


nom_fichier_a_ouvrir = config.nom_fichier_a_ouvrir
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

# taille cellule
if largeur_grille > largeur_fenetre:
    taille_cellule = largeur_fenetre // largeur_grille
else:
    taille_cellule = hauteur_fenetre // hauteur_grille


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
    # Positionner en haut à gauche
    rect.topleft = (10, 0) 
    return surface, rect

# 3. Fonction pour mettre à jour les textures quand on zoome
def mettre_a_jour_textures_zoom(nouvelle_taille):
    # On vide l'ancien cache
    TEXTURES_ACTUELLES.clear()
    # On recrée les images à la bonne taille
    for id_texture, image_originale in TEXTURES_BASE.items():
        # L'optimisation est ici : on scale une fois pour toutes les 4 images
        TEXTURES_ACTUELLES[id_texture] = pygame.transform.scale(image_originale, (nouvelle_taille, nouvelle_taille))


# Création initiale de la surface et du rectangle du texte
lettre_surface, lettre_rect = creer_surface_texte(str(chosen_letter))

TEXTURES_ACTUELLES = {}
mettre_a_jour_textures_zoom(taille_cellule)

running = True
while running:
    # ---variables à réinitialiser---
    
    
    
    
    #deplacement vitesse
    vitesse = config.vitesse *5
    # FIN ---variables à réinitialiser---
    
    #touche pressé
    keys_pressed = pygame.key.get_pressed()
    
    # gestion évènements
    for event in pygame.event.get():
        # Si l'utilisateur clique sur la croix de fermeture
        if event.type == pygame.QUIT: 
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
                taille_cellule += 1
                mettre_a_jour_textures_zoom(taille_cellule)
            if event.button == 5 and taille_cellule >1:
                taille_cellule -= 1
                mettre_a_jour_textures_zoom(taille_cellule)
                
        
        if event.type == pygame.KEYDOWN:
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
                if largeur_grille > largeur_fenetre:
                    taille_cellule = largeur_fenetre // (largeur_grille + 2)
                else:
                    taille_cellule = hauteur_fenetre //  (hauteur_grille + 2)
            
            if event.key == pygame.K_F4 or event.key == pygame.K_KP_MINUS:
                lecteur.retirer(nom_fichier_a_ouvrir)
                if largeur_grille > largeur_fenetre:
                    taille_cellule = largeur_fenetre // (largeur_grille - 2)
                else:
                    taille_cellule = hauteur_fenetre //  (hauteur_grille - 2)
    
    #si le bouton gauche de la souris est maintenu enfoncé
    if mouse_left_button_held:
        # l'événement MOUSEBUTTONDOWN contient la position du clic:
        x, y = event.pos
        
        # position en nombre de cellules 
        cellular_x = int((x - camera_x )/ taille_cellule)
        cellular_y = int((y - camera_y )/ taille_cellule)
        
        # positionner les nouvelles tuiles (en focntion des textures choisis)
        lecteur.modifier_tile_dans_json(nom_fichier_a_ouvrir, cellular_y, cellular_x, chosen_letter)
        
        grille[cellular_y][cellular_x] = chosen_letter
        
    
    # Gestion évènement déplacement
    vitesse += vitesse * keys_pressed[pygame.K_LSHIFT]
    deplacement_x = (keys_pressed[pygame.K_d] or keys_pressed[pygame.K_RIGHT]) - (keys_pressed[pygame.K_q] or keys_pressed[pygame.K_LEFT])
    deplacement_y = (keys_pressed[pygame.K_s] or keys_pressed[pygame.K_DOWN]) - (keys_pressed[pygame.K_z] or keys_pressed[pygame.K_UP])
    
    #vitesse deplacement en diagonale réduit 
    if deplacement_x != 0 and deplacement_y != 0:
        vitesse *= config.multiplicateur_vitesse_diagonale
    
    #application du deplacement 
    deplacement_x *= vitesse
    deplacement_y *= vitesse
    
    # Appliquez le mouvement 
    camera_x -= deplacement_x
    camera_y -= deplacement_y
    
    
    
    
    
    
    # --- Rendu graphique de la scène ---
    
    # Dessiner la grille
    # Efface l'écran en le remplissant de noir. Cela supprime tous les dessins de la frame précédente.
    fenetre.fill((0, 0, 0))
    
    # --- Calculer la zone visible de la grille ---

    # Coordonnées monde du coin supérieur gauche de l'écran
    world_x_start_screen = -camera_x
    world_y_start_screen = -camera_y

    # Coordonnées monde du coin inférieur droit de l'écran
    world_x_end_screen = world_x_start_screen + largeur_fenetre
    world_y_end_screen = world_y_start_screen + hauteur_fenetre

    # Convertir ces coordonnées monde en indices de grille
    start_grid_x = int(world_x_start_screen // taille_cellule) -1 #+6
    end_grid_x = int(world_x_end_screen // taille_cellule) +1 #-5 # +1 

    start_grid_y = int(world_y_start_screen // taille_cellule) -1 #+2
    end_grid_y = int(world_y_end_screen // taille_cellule) +1 #-1 # +1 
    # S'assurer que les indices restent dans les limites de la grille réelle
    start_grid_x = max(0, start_grid_x)
    end_grid_x = min(largeur_grille, end_grid_x) # Ne pas dépasser largeur_grille - 1, mais range va jusqu'à end-1
    start_grid_y = max(0, start_grid_y)
    end_grid_y = min(hauteur_grille, end_grid_y) # Ne pas dépasser hauteur_grille - 1
    # --- Fin Calculer la zone visible de la grille ---



    # --- Dessiner uniquement les cellules visibles ---
    # OPTIMISATION : Si les cases sont minuscules, on en saute pour ne pas faire ramer le GPU	
    step = 1
    if taille_cellule < 5:
        step = 2  
    if taille_cellule < 3:
        step = 4 
    
    for y in range(start_grid_y, end_grid_y):
        for x in range(start_grid_x, end_grid_x):
            texture_id = grille[y][x]
            
            # SECURITÉ : On vérifie que l'ID existe bien dans nos textures chargées
            # et qu'il n'est pas None
            if texture_id is not None and texture_id in TEXTURES_ACTUELLES:
                    
                # Calcule la position de la cellule à l'écran
                screen_x = x * taille_cellule + camera_x
                screen_y = y * taille_cellule + camera_y

                # Crée un objet pygame.Rect pour la position à l'écran
                rect = pygame.Rect(screen_x, screen_y, taille_cellule, taille_cellule)

                # Dessine le contour du rectangle de la cellule
                #(Ces lignes sont souvent supprimées dans le jeu final pour ne dessiner que les textures)
                pygame.draw.rect(fenetre, couleur_cellule, rect)
                pygame.draw.rect(fenetre, couleur_grille, rect, 1)
                
                # Dessine la texture en fonction de la grille
                img = TEXTURES_ACTUELLES[texture_id]
                
                if step > 1:
                    taille_visuelle = taille_cellule * step
                    img = pygame.transform.scale(img, (taille_visuelle, taille_visuelle))
                
                
                if grille[y][x] is not None:
                    fenetre.blit(img, rect)
    # --- FIN Dessiner uniquement les cellules visibles ---
    
    
    
    fenetre.blit(lettre_surface, lettre_rect)
    # --- Fin Rendu graphique de la scène ---
    pygame.display.flip()
    horloge.tick(FPS)
pygame.quit()
sys.exit()  

