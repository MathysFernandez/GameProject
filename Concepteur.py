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

#récupère la grille avec les emplacements de texture
grille, collision_map_solid, collision_map_water = textures_manager.placer_texture(taille_cellule, largeur_grille, hauteur_grille, grille)



# ---Police---
BLANC = (255, 255, 255)

chosen_letter = 0


# Fonction pour rendre et positionner le texte
def creer_surface_texte(texte):
    police = pygame.font.SysFont('Arial', 50)
    surface = police.render(texte, True, BLANC)
    rect = surface.get_rect()
    # Positionner en haut à gauche
    rect.topleft = (10, 0) 
    return surface, rect

# Création initiale de la surface et du rectangle du texte
lettre_surface, lettre_rect = creer_surface_texte(str(chosen_letter))

# Variable pour suivre l'état du bouton gauche
mouse_left_button_held = False

running = True
while running:
    # ---variables à réinitialiser---
    # récupérer grille
    largeur_grille, hauteur_grille, grille = lecteur.chargerfichier(nom_fichier_a_ouvrir)
    
    #récupère la grille avec les emplacements de texture
    grille, collision_map_solid, collision_map_water = textures_manager.placer_texture(taille_cellule, largeur_grille, hauteur_grille, grille)

    #deplacement vitesse
    vitesse = config.vitesse
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
            if event.button == 5:
                taille_cellule -= 1
                
        
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
            #...
            
            
            
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
    
    # Dessiner la grille
    fenetre.fill((0, 0, 0))
    
    for y in range(hauteur_grille):
            for x in range(largeur_grille):
                # Calcule la position de la cellule à l'écran
                screen_x = x * taille_cellule + camera_x
                screen_y = y * taille_cellule + camera_y

                # Crée un objet pygame.Rect pour la position à l'écran
                rect = pygame.Rect(screen_x, screen_y, taille_cellule, taille_cellule)

                # Dessine le contour du rectangle de la cellule
                pygame.draw.rect(fenetre, couleur_cellule, rect)
                pygame.draw.rect(fenetre, couleur_grille, rect, 1)

                # Dessine la texture en fonction de la grille
                if grille[y][x] is not None:
                    fenetre.blit(grille[y][x], rect)
    
    
    if grille[y][x] is not None:
        fenetre.blit(grille[y][x], rect)
    
    fenetre.blit(lettre_surface, lettre_rect)
    
    pygame.display.flip()
    horloge.tick(FPS)
pygame.quit()
sys.exit()  

