import pygame
import logging


Titre = "GameProject"
taille_cellule = 100
taille_joueur = 54

#2 c'est bien
vitesse = 2
if vitesse >= taille_cellule:
    vitesse = 2
FPS = 60
taille_BT_w = 200
taille_BT_h = 50
nombre_texture = 3
nom_fichier_a_ouvrir = 'map_generation_procedural'
vitesse_rotation = 5
test_fps = False

if test_fps:
    FPS = 1000
#taille de la nouvelle génération
taille_nouvelle_generation = 200

#entre 0 et 1
multiplicateur_vitesse_diagonale = 0.71


if nombre_texture < 2:
    nombre_texture = 2


# Gère la quantité de sol
# 7 ou 8 sur 12 c'est mal
multiplicateur_sol = 8/12 * nombre_texture

# Gère la quantité de points d'eau
#entre 2 et 15
#7  c'est bien
multiplicateur_point_apparition_water = 7

#nombre de couche de génération procédurale
nombre_répétition = 4

#nombre de couche de génération d'eau
#propagation de l'eau
#entre 5 et 20
#8 c'est bien
nombre_répétition_water = 8

def get_dimensions():
    largeur_fen = pygame.display.Info().current_w
    hauteur_fen = pygame.display.Info().current_h - 60
    return largeur_fen, hauteur_fen

joueur_vie_max = 100
joueur_vie_actuelle = 100 # On peut choisir le pourcentage de vie de départ ici
joueur_etat = "vivant" # Peut être "vivant" ou "mort"
test_vie = True