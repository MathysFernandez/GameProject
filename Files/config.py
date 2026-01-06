import pygame
import logging
import math

#----- Jeu -----
Titre = "GameProject"
#2 c'est bien
vitesse = 4
vitesse_rotation = 5
FPS = 60
#entre 0 et 1
multiplicateur_vitesse_diagonale = math.sqrt(2)
SCORE_OBJECTIF = 2000
#----- Fin Jeu -----



#----- taille -----
taille_cellule = 70
taille_joueur = 56
taille_frame = 25
taille_BT_w = 500
taille_BT_h = 50
#----- Fin taille -----



#----- Animation -----
duree_animation_joueur = 20
#----- Fin Animation -----



#----- Generation -----
taille_nouvelle_generation = 2000
# nombre de dechet par carte
nombre_de_dechets = 50
nombre_texture = 3

# Gère la quantité de sol
# 8 à 10 sur 12 c'est bien 
multiplicateur_sol = 10/12 * nombre_texture

# Gère la quantité de points d'eau
#7  c'est bien
multiplicateur_point_apparition_water = 7

#nombre de couche de génération procédurale
nombre_répétition = 4

#nombre de couche de génération d'eau
#8 c'est bien
nombre_répétition_water = 9
#----- Fin Generation -----



#----- Mode test -----
test_fps = False
test_vie = False
mod_test_score = False
#----- Fin Mode test -----



#----- GamePlay -----
dash_actif = False
dash_dir = (0, 0)
dash_fin_temps = 0
dash_cooldown_fin = 0

dash_duree =  200        
dash_cooldown = 1000   
dash_vitesse =  3  

joueur_vie_max = 100
joueur_vie_actuelle = 100 
joueur_etat = "vivant" 
#----- Fin GamePlay -----




#----- Vérification -----
if vitesse >= taille_cellule:
    vitesse = 2

if nombre_texture < 2:
    nombre_texture = 2

if test_fps:
    FPS = 1000
#----- Fin Vérification -----




#----- Fonctions -----
def get_dimensions():
    largeur_fen = pygame.display.Info().current_w
    hauteur_fen = pygame.display.Info().current_h - 60
    return largeur_fen, hauteur_fen
#----- Fin Fonctions -----


