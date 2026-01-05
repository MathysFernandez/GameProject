import logging

import pygame
import math
import json
import os
import sys
from Files import config
from Files import textures_manager
from Files import Lecteur_map as lecteur
from Files import generation_procedurale as generation
from Files import gameplay
from Files.sound_manager import SoundManager



# Configuration simple du logger pour écrire dans le fichier game.log
logging.basicConfig(
    level=logging.DEBUG,
    filename='game.log',
    filemode='a',  # 'a' pour ajouter les nouvelles lignes à la fin du fichier
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    encoding='utf-8' # Ajout de l'encodage pour les caractères accentués
)

# Créer un logger pour ce module
logger = logging.getLogger(__name__)


"""
Niveaux de notes les plus courants :
logger.info("") : Pour les informations générales ("Le joueur est entré dans la zone X").

logger.warning("") : Pour les avertissements ("La vie du joueur est basse !").

logger.error("") : Pour les erreurs graves qui empêchent quelque chose de fonctionner correctement.

logger.debug("") : Pour les détails de débogage que tu n'utilises que quand tu cherches un bug.
Si tu as mis level=logging.INFO à l'étape 1, ces messages ne seront même pas écrits, ce qui est très pratique pour ne pas surcharger le fichier.
"""



"""
# Au début de ton jeu
logger.info("Le jeu a démarré !")

# Quand un monstre est créé
logger.info("Un monstre a été créé à la position (150, 200).")

# Quand le joueur gagne
logger.info("Félicitations ! Le joueur a gagné !")

# Quand il y a un problème (par exemple, un fichier manquant)
logger.error("Erreur ! Le fichier 'textures/sword.png' est introuvable.")
"""
logger.info("Lancement")




pygame.init()
angle_voulu = 0
angle = 0

# ---instancier variable par défaut---
Titre = config.Titre


nom_fichier_a_ouvrir = lecteur.derniereSauvegarde()
# récupérer grille avec les valeur en int
try:
    largeur_grille, hauteur_grille, grille = lecteur.chargerfichier(nom_fichier_a_ouvrir)
except:
    nom_fichier_a_ouvrir = "Par_Defaut.json"
    largeur_grille, hauteur_grille, grille = lecteur.chargerfichier(nom_fichier_a_ouvrir)

#horloge Interne
horloge = pygame.time.Clock()
FPS = config.FPS

# Fenêtre
largeur_fenetre, hauteur_fenetre = config.get_dimensions()

pygame.display.set_caption("Menu de jeux")

#système pygame permettant d'ajuster la taille de la fenetre a volonté
flags = pygame.RESIZABLE
# Créer la fenêtre
fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre), flags)
# Définit le titre de la fenêtre
pygame.display.set_caption(Titre)

#compteur pour changer de spritesheet
compteur_animation = 0
interv = config.duree_animation_joueur


# Couleurs
WHITE = (255, 255, 255)
BLUE = (0, 102, 204)
DARK_BLUE = (0, 51, 102)
BLACK = (0, 0, 0)

#taille bouton
BT_width = config.taille_BT_w
BT_height = config.taille_BT_h

# Dimensions de la grille
taille_cellule = config.taille_cellule



# Calculer les coordonnées mondiales du centre de la grille
# C'est la position "idéale" du joueur dans le monde
centre_grille_x_monde = (largeur_grille // 2) * taille_cellule
centre_grille_y_monde = (hauteur_grille // 2) * taille_cellule



# Position initiale de la caméra
camera_x = 0
camera_y = 0


# --- Ajout du joueur ---
# Dimensions et couleur du joueur
taille_joueur = config.taille_joueur
#couleur_joueur = (255, 255, 0) # Bleu

# Position initiale du joueur au centre de l'écran (ne bouge pas par rapport à la fenêtre)
joueur_x_fixe = (largeur_fenetre - taille_joueur) // 2
joueur_y_fixe = (hauteur_fenetre - taille_joueur) // 2
# --- Fin Ajout du joueur ---


# Texture Joueur 2
texture_eau2 = textures_manager.texture_num_2_water(taille_cellule, config.taille_frame)



#dimension monde
monde_largeur_px = largeur_grille * taille_cellule
monde_hauteur_px = hauteur_grille * taille_cellule
position_valide = False

pos_save = lecteur.dernierePosition()

if pos_save:
    x, y = pos_save
    if 0 <= x <= monde_largeur_px and 0 <= y <= monde_hauteur_px:
        position_player_x = x
        position_player_y = y
        position_valide = True
        logger.info(f"Position chargée (Valide) : {int(position_player_x)}, {int(position_player_y)}")
    else:
        logger.error(f"ATTENTION : Position sauvegardée hors limites ({x}, {y}). Réinitialisation.")

if not position_valide:
    position_player_x = centre_grille_x_monde + 100
    position_player_y = centre_grille_y_monde + 100
    lecteur.SetDernierePosition(position_player_x, position_player_y)

rayon_joueur = taille_joueur / 2



# +++ DÉBUT AJOUT BARRE DE VIE ---

# Variables pour l'état et la vie du joueur
joueur_vie_max = config.joueur_vie_max
joueur_vie_actuelle = config.joueur_vie_actuelle# On peut choisir le pourcentage de vie de départ ici
joueur_etat = config.joueur_etat # Peut être "vivant" ou "mort"


# +++ AJOUT SCORE +++
joueur_score = 0
# +++ FIN AJOUT SCORE +++

# +++ AJOUT ETAT DE PAUSE +++
jeu_est_en_pause = False
# +++ FIN AJOUT ETAT DE PAUSE +++

barre_largeur = 70  
barre_hauteur = 15
# Définir les couleurs Vie et game over
COULEUR_FOND_BARRE = (100, 100, 100) # Gris foncé
COULEUR_VIE = (0, 255, 0)         # Vert
COULEUR_CONTOUR = (255, 255, 255) # Blanc
compt_anim_eau = 0



floor, mur, mur2, water_final, water_final2, dechet1, dechet2, feu_final = textures_manager.charger_texture(taille_cellule, config.taille_frame)

TEXTURES_BASE = {
    -1: water_final,
    0: floor,
    1: mur,
    2: mur2,
    3: dechet1,
    4: feu_final
}




def retirer_vie(quantite):

    global joueur_vie_actuelle, joueur_etat
    
    if joueur_etat == "vivant":
        joueur_vie_actuelle -= quantite
        
        if joueur_vie_actuelle <= 0:
            joueur_vie_actuelle = 0
            joueur_etat = "mort"
            logger.warning("Le joueur est mort.")
        else:
            logger.info(f"Le joueur a perdu {quantite} PV. Vie restante : {joueur_vie_actuelle}")

def ajouter_vie(quantite):

    global joueur_vie_actuelle
    
    if joueur_etat == "vivant":
        joueur_vie_actuelle += quantite
        if joueur_vie_actuelle > joueur_vie_max:
            joueur_vie_actuelle = joueur_vie_max
        logger.info(f"Le joueur a gagné {quantite} PV. Vie restante : {joueur_vie_actuelle}")

# +++ FIN AJOUT BARRE DE VIE +++

# +++ AJOUT SCORE +++
def ajouter_score(quantite):
    """Ajoute un montant au score du joueur."""
    global joueur_score
    
    joueur_score += quantite
    logger.info(f"Le joueur a gagné {quantite} points. Score total : {joueur_score}")

# +++ FIN AJOUT SCORE +++


# Création de la fonction de collision entre cercle et rectangle
def collision_cercle_rect(centre_cercle : (int, int), rayon_cercle : int, rect):
    # Trouvé le point le plus proche sur le rectangle par rapport au centre du cercle
    closest_x = max(rect.left, min(centre_cercle[0], rect.right))
    closest_y = max(rect.top, min(centre_cercle[1], rect.bottom))

    #Calculer la distance entre le centre du cercle et ce .
    distance_x = centre_cercle[0] - closest_x
    distance_y = centre_cercle[1] - closest_y

    distance_squared = (distance_x ** 2) + (distance_y ** 2)
    
    #Si la distance au carré est inférieure au rayon au carré, il y a collision
    if distance_squared < (rayon_cercle ** 2):
        # on calcule la distance reelle (sans le carré)
        distance = math.sqrt(distance_squared)
        # On détermine la quantité d'intersection
        overlap = rayon_cercle - distance
        
        # On calcule le vecteur de déplacement pour sortir de la collision
        # Si la distance est zéro, cela signifie que le centre est dans le coin.
        # On donne une petite valeur pour éviter la division par zéro.
        if distance == 0:
            push_x = overlap
            push_y = overlap
        else:
            push_x = (distance_x / distance) * overlap
            push_y = (distance_y / distance) * overlap
            
        return True, (push_x, push_y)
    
    return False, (0, 0)


# -- FIN joueur en cercle nouveauté ---











#récupère la grille avec les emplacements de texture
grille, collision_map_solid, collision_map_water, collision_map_dechet = textures_manager.placer_texture(taille_cellule, largeur_grille, hauteur_grille, grille, False, config.taille_frame)


# Police
font = pygame.font.SysFont(None, 50)



# Bouton classique
def draw_button(text, x, y, w, h, color, hover_color, action_name):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(fenetre, hover_color, (x, y, w, h))
        if click[0] == 1:
            return action_name
    else:
        pygame.draw.rect(fenetre, color, (x, y, w, h))

    text_surf = font.render(text, True, WHITE)
    text_rect = text_surf.get_rect(center=(x + w // 2, y + h // 2))
    fenetre.blit(text_surf, text_rect)
    return None

# Menu principal
# La fonction menu_scene doit aussi prendre les événements en paramètre
def menu_scene(events, largeur_fenetre, hauteur_fenetre) -> str: # <-- Ajout de 'events'
    fenetre.fill(BLACK)
    #nombre de bouton
    nb_BT = 4
    compteur_BT = 0
    
    #result = draw_button(text, x, y, w, h, color, hover_color, action_name)
    result = draw_button("Game", (largeur_fenetre - BT_width) // 2 ,(hauteur_fenetre  - BT_height ) // 2 -100 -25 *nb_BT + compteur_BT * 100,  BT_width ,  BT_height, BLUE, DARK_BLUE, "jeu")
    compteur_BT += 1
    if result:
        return result
    result = draw_button("Charger", (largeur_fenetre - BT_width) // 2 ,(hauteur_fenetre  - BT_height ) // 2 -100 -25 *nb_BT + compteur_BT * 100,  BT_width ,  BT_height, BLUE, DARK_BLUE, "charger")
    
    compteur_BT += 1
    if result:
        return result
    result = draw_button("New game", (largeur_fenetre - BT_width) // 2 ,(hauteur_fenetre  - BT_height ) // 2 -100 -25 *nb_BT + compteur_BT * 100,  BT_width ,  BT_height, BLUE, DARK_BLUE, "nouvelle partie")
    
    compteur_BT += 1
    if result:
        return result
    result = draw_button("Quit", (largeur_fenetre - BT_width) // 2 ,(hauteur_fenetre  - BT_height ) // 2 -100 -25*nb_BT + compteur_BT * 100,  BT_width ,  BT_height, BLUE, DARK_BLUE, "quit")
    if result:
        return result
    
    # Gérer les événements spécifiques au menu ici si nécessaire (ex: touches clavier)
    for event in events: # <-- Utilisation des événements passés en paramètre
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: # Exemple : quitter le menu avec ESC
                print("ESC pressée dans le menu")
                return "quit"

    return "menu"



def menu_scene_chargement(events, largeur_fenetre, hauteur_fenetre):
    fenetre.fill(BLACK)
    
    nomsDesSauvegardes = lecteur.recupNomSauvegarde()
    nb_BT = len(nomsDesSauvegardes)
    compteur_BT = 0
    
    mouse_click = pygame.mouse.get_pressed()
    action_a_faire = None
    
    
    
    for i in range (nb_BT):
        result = draw_button(nomsDesSauvegardes[i], (largeur_fenetre - BT_width) // 2 ,(hauteur_fenetre  - BT_height ) // 2 -100 -25 *nb_BT + compteur_BT * 100,  BT_width ,  BT_height, BLUE, DARK_BLUE, nomsDesSauvegardes[i])
        compteur_BT += 1
        if result:
            action_a_faire = result
            
    validation_finale = False
    
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: 
                validation_finale = True
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "menu"

    if action_a_faire and validation_finale:
        return action_a_faire

    return "charger"


def formulaire(fenetre, events, nom_actuel, taille_actuelle, champ_actif):
    largeur, hauteur = fenetre.get_size()
    font = pygame.font.SysFont(None, 32)
    #font.render(text, True, WHITE)
    
    rect_nom = pygame.Rect(largeur // 2 - 100, hauteur // 2 - 80, 200, 40)
    rect_taille = pygame.Rect(largeur // 2 - 100, hauteur // 2 + 20, 200, 40)
    rect_btn_valider = pygame.Rect(largeur // 2 - 100, hauteur // 2 + 100, 200, 50)
    rect_btn_retour = pygame.Rect(largeur // 2 - 100, hauteur // 2 + 160, 200, 50)

    action_a_retourner = None

    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if rect_nom.collidepoint(event.pos):
                champ_actif = "nom"
            elif rect_taille.collidepoint(event.pos):
                champ_actif = "taille"
            elif rect_btn_valider.collidepoint(event.pos):
                action_a_retourner = "valider"
            elif rect_btn_retour.collidepoint(event.pos):
                action_a_retourner = "retour"
            else:
                champ_actif = None

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                action_a_retourner = "retour"
            
            if champ_actif == "nom":
                if event.key == pygame.K_BACKSPACE:
                    nom_actuel = nom_actuel[:-1]
                else:
                    nom_actuel += event.unicode
                    
            elif champ_actif == "taille":
                if event.key == pygame.K_BACKSPACE:
                    taille_actuelle = taille_actuelle[:-1]
                elif event.unicode.isnumeric(): 
                    taille_actuelle += event.unicode

    fenetre.fill((30, 30, 30))

    couleur = (0, 100, 255) if champ_actif == "nom" else (100, 100, 100)
    pygame.draw.rect(fenetre, couleur, rect_nom, 2)
    fenetre.blit(font.render(nom_actuel, True, (255, 255, 255)), (rect_nom.x + 5, rect_nom.y + 10))
    fenetre.blit(font.render("Nom :", True, (255, 255, 255)), (rect_nom.x - 70, rect_nom.y + 10))

    couleur = (0, 100, 255) if champ_actif == "taille" else (100, 100, 100)
    pygame.draw.rect(fenetre, couleur, rect_taille, 2)
    fenetre.blit(font.render(taille_actuelle, True, (255, 255, 255)), (rect_taille.x + 5, rect_taille.y + 10))
    fenetre.blit(font.render("Taille :", True, (255, 255, 255)), (rect_taille.x - 80, rect_taille.y + 10))

    pygame.draw.rect(fenetre, (0, 200, 0), rect_btn_valider)
    fenetre.blit(font.render("CRÉER", True, (255, 255, 255)), (rect_btn_valider.x + 60, rect_btn_valider.y + 15))

    pygame.draw.rect(fenetre, (200, 0, 0), rect_btn_retour)
    fenetre.blit(font.render("RETOUR", True, (255, 255, 255)), (rect_btn_retour.x + 55, rect_btn_retour.y + 15))

    return nom_actuel, taille_actuelle, champ_actif, action_a_retourner



def menu_scene_nouvelle_carte(events, largeur_fenetre, hauteur_fenetre, nom_actuel, champ_actif, taille_actuelle, position_player_x, position_player_y):
    fenetre.fill(BLACK)
    
    nom_actuel, taille_actuelle, champ_actif, action_a_retourner = formulaire(fenetre, events, nom_actuel, taille_actuelle, champ_actif)
    if action_a_retourner == "valider":
        global grille, collision_map_solid, collision_map_water, collision_map_dechet, nom_fichier_a_ouvrir, largeur_grille, hauteur_grille
        generation.generation(nom_actuel, config.nombre_texture, int(taille_actuelle))
        lecteur.SetDernierePositionDansCarte(position_player_x, position_player_y)
        lecteur.SetDerniereSauvegarde(nom_actuel+".json")
        x, y = lecteur.dernierePositionDe(nom_actuel)
        lecteur.SetDernierePosition(x,y)
        nom_fichier_a_ouvrir = nom_actuel
        largeur_grille, hauteur_grille, grille = lecteur.chargerfichier(nom_fichier_a_ouvrir)
        grille, collision_map_solid, collision_map_water, collision_map_dechet = textures_manager.placer_texture(taille_cellule, largeur_grille, hauteur_grille, grille, False, config.taille_frame)
        return nom_actuel, champ_actif, taille_actuelle, "jeu"
    
    if action_a_retourner == "retour":
        return nom_actuel, champ_actif, taille_actuelle, "menu"
        
    return nom_actuel, champ_actif, taille_actuelle, "nouvelle partie"



# +++ DÉBUT AJOUT MENU PAUSE +++
def dessiner_menu_pause(largeur_fenetre, hauteur_fenetre):
    
    overlay = pygame.Surface((largeur_fenetre, hauteur_fenetre), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150)) # Noir avec 150/255 d'opacité
    fenetre.blit(overlay, (0, 0))

    titre_surf = font.render("Pause", True, WHITE)
    titre_rect = titre_surf.get_rect(center=(largeur_fenetre // 2, hauteur_fenetre // 2 - 150))
    fenetre.blit(titre_surf, titre_rect)

    action_reprise = draw_button("Reprendre", 
                                (largeur_fenetre - BT_width) // 2, 
                                (hauteur_fenetre - BT_height) // 2 - 50, 
                                BT_width, BT_height, BLUE, DARK_BLUE, "resume")

    action_menu = draw_button("Retour au Menu", 
                              (largeur_fenetre - BT_width) // 2, 
                              (hauteur_fenetre - BT_height) // 2 + 60, 
                              BT_width, BT_height, BLUE, DARK_BLUE, "menu")
    if action_reprise:
        return action_reprise
    if action_menu:
        return action_menu
    
    return None
# +++ FIN AJOUT MENU PAUSE +++

















# Jeu
def jeu_scene(events, camera_x, camera_y): # <-- Ajout de 'events' (pour la gestion des évènements)
    #Gère la logique et le rendu de la scène de jeu principale

    #Args:
        #events (list): Liste des événements Pygame collectés depuis la boucle principale.
        #camera_x (int): Position X  actuelle de la caméra.
        #camera_y (int): Position Y actuelle de la caméra.

    #Returns:
        #str: Le nom de la scène suivante ("jeu" pour rester, "menu" pour retourner au menu)
    
    
    #variables à réinitialiser à chaque boucle:
    #deplacement vitesse
    vitesse = config.vitesse
    
    global angle_voulu, angle, position_player_x, position_player_y, joueur_vie_actuelle, joueur_etat, joueur_score, jeu_est_en_pause, compt_anim_eau, champ_actif, nom_actuel, taille_actuelle, compteur_animation, interv, grille
    
    # Stocke la position du joueur et de la caméra AVANT tout calcul de mouvement
    # Utile pour la détection de collision afin de pouvoir "revenir en arrière" (en focntion des axes)
    ancienne_position_x = position_player_x
    ancienne_position_y = position_player_y
    ancienne_camera_x = camera_x
    ancienne_camera_y = camera_y
    
    largeur_fenetre, hauteur_fenetre = fenetre.get_size()
    
    
    # --- Gestion des événements spécifiques à la scène de jeu ---
    # Parcourt les événements collectés une seule fois par la boucle principale du jeu.
    for event in events: # <-- Utilisation des événements passés en paramètre, PLUS DE pygame.event.get() ici
        # Détecte n'importe quelle touche pressée
        if event.type == pygame.KEYDOWN:
            
            # --- Gestion PAUSE (P) et QUITTER (ESC) ---
            
            # Ajout d'une détection pour ESC pour revenir au menu, comme indiqué dans le texte d'aide
           # if event.key == pygame.K_SPACE:
            #    return
            if event.key == pygame.K_ESCAPE:
                if jeu_est_en_pause:
                    jeu_est_en_pause = False # Si en pause, ESC quitte la pause
                else:
                    # Sinon, ESC quitte le jeu pour le menu (comportement original)
                    joueur_vie_actuelle = 100# On peut choisir le pourcentage de vie de départ ici
                    joueur_etat = "vivant" # Peut être "vivant" ou "mort"
                    joueur_score = 0 #score commençant à 0
                    jeu_est_en_pause = False # S'assurer de réinitialiser
                    return "menu" # <-- Changement ici pour revenir au menu
            
            if event.key == pygame.K_p:
                jeu_est_en_pause = not jeu_est_en_pause # Inverse l'état de pause
                logger.info(f"Jeu mis en pause: {jeu_est_en_pause}")

            # --- FIN GESTION PAUSE ---
            
            # Si le jeu est en pause, on ignore les autres touches de test (H, J, K)
            if jeu_est_en_pause:
                continue # Passe à l'événement suivant
            
            # --- Touches de test (ne s'activent pas durant une pause)
            if config.test_vie:
            # +++ TEST PERDRE DE LA VIE (Appuyez sur H) +++
                if event.key == pygame.K_h:
                    # Press H pour perdre 10 PV (pour tester)
                    retirer_vie(10)
            # +++ FIN TEST +++
                
            # +++ TEST AJOUTER VIE (Appuyez sur J) +++
                if event.key == pygame.K_j:
                    # Press H pour perdre 10 PV (pour tester)
                    ajouter_vie(10)
            # +++ FIN TEST +++
            
            # +++ TEST AJOUTER SCORE (Appuyez sur K) +++
                if event.key == pygame.K_k:
                    # Press K pour gagner 10 points (pour tester)
                    ajouter_score(10)
            # +++ FIN TEST +++
    
    
    # +++ TOUTE LA LOGIQUE DU JEU NE S'EXÉCUTE QUE SI ON N'EST PAS EN PAUSE +++

    # --- Gestion du déplacement du joueur par les touches ---
    # Obtient l'état actuel de toutes les touches du clavier (quelles touches sont pressées).
    keys_pressed = pygame.key.get_pressed()
    # Modifie la vitesse du joueur si la touche 'Maj Gauche' (LSHIFT) est pressée.
    vitesse += vitesse * (keys_pressed[pygame.K_LSHIFT] *0.5)
    deplacement_x = (keys_pressed[pygame.K_d] or keys_pressed[pygame.K_RIGHT]) - (keys_pressed[pygame.K_q] or keys_pressed[pygame.K_LEFT])
    deplacement_y = (keys_pressed[pygame.K_s] or keys_pressed[pygame.K_DOWN]) - (keys_pressed[pygame.K_z] or keys_pressed[pygame.K_UP])
    
    # --- Ajout du dash ---
    temps_actuel = pygame.time.get_ticks()
    # On utilise 'events' pour détecter la touche Espace
    deplacement_x, deplacement_y, vitesse = gameplay.gerer_dash(events, temps_actuel, deplacement_x, deplacement_y, vitesse)
    # --- Déplacer dans un nouveau fichier en tant que fonction --
    if deplacement_x != 0 and deplacement_y != 0:
        vitesse /= config.multiplicateur_vitesse_diagonale
    
    deplacement_x *= vitesse
    deplacement_y *= vitesse
    
    
    #Calcule la cellule actuelle du joueur pour vérifier s'il est dans l'eau.
    #On utilise le centre du joueur pour une vérification plus précise
    player_gx = int(position_player_x // taille_cellule)
    player_gy = int(position_player_y // taille_cellule)




    #Vérifie si le joueur est sur un bloc d'eau 
    if (player_gx, player_gy) in collision_map_water:
        deplacement_x *= 0.7
        deplacement_y *= 0.7
    
    #Vérifie si le joueur est sur un bloc de dechet
    if (player_gx, player_gy) in collision_map_dechet:
        grille[player_gy][player_gx] = 0
        del collision_map_dechet[(player_gx, player_gy)]
        ajouter_score(10)
    
    if joueur_etat == "vivant" and jeu_est_en_pause == False:
        # Appliquez le mouvement désiré au joueur sur X
        position_player_x += deplacement_x
        
    
    # --- Détection de collision sur l'axe X (Optimisé par grille) ---
    # Optimisation de la détection de collision : Seules les cellules à proximité du joueur sont vérifiées
    # Calcule la plage des indices de grille (min_gx à max_gx) que le joueur pourrait toucher
    # après son déplacement sur l'axe X. Une marge de +/- 1 cellule est ajoutée (-1 pour min, +1 pour max)
    # pour s'assurer de ne rater aucune collision, même avec des mouvements rapides ou aux bords des cellules.
    min_gx = int((position_player_x - rayon_joueur) // taille_cellule) -1
    max_gx = int((position_player_x + rayon_joueur) // taille_cellule) +1
    min_gy = int((position_player_y - rayon_joueur) // taille_cellule) -1 # Inclure Y pour avoir la zone de vérification
    max_gy = int((position_player_y + rayon_joueur) // taille_cellule) +1
    
    
    # Limiter les indices aux bords de la grille
    # S'assure que les indices calculés restent dans les limites valides de la grille
    min_gx = max(0, min_gx)
    max_gx = min(largeur_grille - 1, max_gx)
    min_gy = max(0, min_gy)
    max_gy = min(hauteur_grille - 1, max_gy)
    
    
    # Parcourt uniquement les cellules de la grille potentiellement en collision avec le joueur.
    for y_grid in range(min_gy, max_gy + 1):
        for x_grid in range(min_gx, max_gx + 1):
            # Vérifie si la cellule actuelle (x_grid, y_grid) est un bloc de collision.
            if (x_grid, y_grid) in collision_map_solid:
                # Récupère l'objet Rect représentant le bloc de collision.
                bloc_rect = collision_map_solid[(x_grid, y_grid)] 
                
                # Utiliser la nouvelle fonction de collision qui retourne un vecteur
                collision, (push_x, push_y) = collision_cercle_rect((position_player_x, position_player_y), rayon_joueur, bloc_rect)
                
                # Utilise notre nouvelle fonction de collision
                if collision:
                    # Correction sur l'axe X : on applique le déplacement push_x
                    position_player_x += push_x
                    # On annule le déplacement sur l'axe X pour cette frame
                    deplacement_x = 0
        
    
    if joueur_etat == "vivant" and jeu_est_en_pause == False:
        # --- Application du mouvement et détection de collision (axe Y) ---
        # Applique le déplacement calculé à la position Y du joueur.
        position_player_y += deplacement_y
    
    # Optimisation de la détection de collision : Seules les cellules à proximité du joueur sont vérifiées
    # Calcule la plage des indices de grille (min_gx à max_gx) que le joueur pourrait toucher
    # après son déplacement sur l'axe X. Une marge de +/- 1 cellule est ajoutée (-1 pour min, +1 pour max)
    # pour s'assurer de ne rater aucune collision, même avec des mouvements rapides ou aux bords des cellules
    min_gx = int((position_player_x - rayon_joueur) // taille_cellule) -1
    max_gx = int((position_player_x + rayon_joueur) // taille_cellule) +1
    min_gy = int((position_player_y - rayon_joueur) // taille_cellule) -1 # Inclure Y pour avoir la zone de vérification
    max_gy = int((position_player_y + rayon_joueur) // taille_cellule) +1
    
    # S'assure que les indices calculés restent dans les limites valides de la grille.
    min_gx = max(0, min_gx)
    max_gx = min(largeur_grille - 1, max_gx)
    min_gy = max(0, min_gy)
    max_gy = min(hauteur_grille - 1, max_gy)
    
    # Parcourt les cellules potentiellement en collision pour l'axe Y.
    for y_grid in range(min_gy, max_gy + 1):
        for x_grid in range(min_gx, max_gx + 1):
            if (x_grid, y_grid) in collision_map_solid:
                bloc_rect = collision_map_solid[(x_grid, y_grid)]

                collision, (push_x, push_y) = collision_cercle_rect((position_player_x, position_player_y), rayon_joueur, bloc_rect)

                if collision:
                    # Correction sur l'axe Y : on applique le déplacement push_y
                    position_player_y += push_y
                    # On annule le déplacement sur l'axe Y pour cette frame
                    deplacement_y = 0
    
    # --- FIN Déplacer dans un nouveau fichier en tant que fonction --
    
    
    
    
    
    
    
    
    
    

    # --- Mise à jour de la caméra ---
    # La caméra est ajustée de manière à ce que le joueur reste "fixe" au centre de l'écran
    camera_x = joueur_x_fixe - position_player_x # joueur_x_fixe est le centre X de l'écran pour le joueur
    camera_y = joueur_y_fixe - position_player_y # joueur_y_fixe est le centre Y de l'écran pour le joueur
    
    
    
    
    
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

    
    #test anim 1 ou 2 pour l'eau
    anim = 1
    if compt_anim_eau <= 50:
        anim = 1
    elif 50 < compt_anim_eau < 100:
        anim = 2
    else :
        anim = 1
        compt_anim_eau = 0
    compt_anim_eau += 1
    
    """
    print("nom: "+nom_fichier_a_ouvrir)
    print("largeur: "+ str(largeur_grille))
    print("hauteur: "+ str(hauteur_grille))
    """
    
    # --- Dessiner uniquement les cellules visibles ---
    for y in range(start_grid_y, end_grid_y):
        for x in range(start_grid_x, end_grid_x):
            texture_id = grille[y][x]
            
            if texture_id is not None and texture_id in TEXTURES_BASE: 
                # Calcule la position de la cellule à l'écran
                screen_x = x * taille_cellule + camera_x
                screen_y = y * taille_cellule + camera_y
                
                if texture_id == -1 and anim == 2:
                    img = water_final2
                elif texture_id == 3 and anim == 2:
                    img = dechet2
                else:
                    # Dessine la texture en fonction de la grille
                    img = TEXTURES_BASE[texture_id]
                    
                fenetre.blit(img, (screen_x, screen_y))

    # --- FIN Dessiner uniquement les cellules visibles ---
    
    #détermine l'angle de direction du joueur
    ##0 degrés = droite, 90 degrés = haut
    
    if deplacement_x != 0:
        if deplacement_x < 0 and deplacement_y < 0:
            angle_voulu = 135
        elif deplacement_x < 0 and deplacement_y > 0:
            angle_voulu = 225
        elif deplacement_x > 0 and deplacement_y > 0:
            angle_voulu = 315
        elif deplacement_x > 0 and deplacement_y < 0:
            angle_voulu = 45
        elif deplacement_x > 0 and deplacement_y == 0:
            angle_voulu = 0
        elif deplacement_x < 0 and deplacement_y == 0:
            angle_voulu = 180
    else:
        if deplacement_y > 0:
            angle_voulu = 270
        elif deplacement_y < 0:
            angle_voulu = 90
    if joueur_etat == "vivant" and jeu_est_en_pause == False:
        #permet de tourner le joueur dans la direction voulu seulement lors des déplacements du joueurs 
        if (deplacement_x !=0 or deplacement_y !=0) and angle != angle_voulu:
            if angle >= 360:
                angle -= 360
            if angle <0:
                angle += 360
            if (angle_voulu - angle) % 360 <= 180:
                angle += config.vitesse_rotation
            else:
                angle -= config.vitesse_rotation
    
    
    
    # le joueur_1 et joueur_2 correspondent à l'animation de marche, joueur_0 est l'affichage du joueur quand il est immobile
    joueur_0 = textures_manager.texture_joueur(config.taille_joueur, angle, 0)
    joueur_1 = textures_manager.texture_joueur(config.taille_joueur, angle, 1)
    joueur_2 = textures_manager.texture_joueur(config.taille_joueur, angle, 2)
    
    joueur = joueur_0
    
    
    if deplacement_x == 0 and deplacement_y == 0:
        joueur = joueur_0
        compteur_animation = 0
    
    elif 0 <= compteur_animation <= interv:
        joueur = joueur_1
        compteur_animation += 1
    elif interv < compteur_animation <= interv*2:
        joueur = joueur_2
        compteur_animation += 1
    elif compteur_animation > interv*2:
        joueur = joueur_1
        compteur_animation = 0
    
    
    
    
    # Correction : Calculer la position d'affichage du joueur sur l'écran
    #en utilisant ses coordonnées monde (position_player_x, position_player_y)
    screen_x = position_player_x + camera_x
    screen_y = position_player_y + camera_y

    # Créer un nouveau Rect à partir de la surface tournée, centré sur la position d'affichage
    # Nous utilisons 'screen_x' et 'screen_y' pour le positionnement.
    rect_rotate = joueur.get_rect(center=(screen_x, screen_y))
    # ---FIN gère la hitbox pour la rotation du rect---
    
    
    
    
    # --- Dessiner le joueur ---
    fenetre.blit(joueur, rect_rotate)
    # --- Fin Dessiner le joueur ---
    
    # --- Affichage des FPS en temps réel si test_fps est activé ---
    if config.test_fps:
        fps_text = font.render(f"FPS: {horloge.get_fps():.2f}", True, WHITE)
        fenetre.blit(fps_text, (10, 10))
    # --- Fin Affichage des FPS ---
    
    
    
    # +++ DÉBUT AFFICHAGE SCORE (UI) +++
    score_prec = -1
    score_surf = None

    if joueur_score != score_prec:
        score_surf = font.render(f"Score: {joueur_score}", True, WHITE)
        score_rect = score_surf.get_rect(topright=(largeur_fenetre - 10, 10))
    fenetre.blit(score_surf, score_rect)
    # +++ FIN AFFICHAGE SCORE (UI) +++
    
    
    
    # +++ DÉBUT AJOUT AFFICHAGE BARRE DE VIE (UI) +++
    
    # Barre de vie au dessus du joueur

    barre_pos_x = largeur_fenetre // 2 - (barre_largeur) +7
    barre_pos_y = hauteur_fenetre // 2 - barre_hauteur - config.taille_joueur *1.2

    # Calculer le pourcentage de vie pour la barre
    ratio_vie = joueur_vie_actuelle / joueur_vie_max
    largeur_vie_actuelle = barre_largeur * ratio_vie

    

    # Dessiner le fond de la barre (la vie perdue)
    pygame.draw.rect(fenetre, COULEUR_FOND_BARRE, (barre_pos_x, barre_pos_y, barre_largeur, barre_hauteur))
    
    # Dessiner la vie actuelle par-dessus
    if largeur_vie_actuelle > 0:
        pygame.draw.rect(fenetre, COULEUR_VIE, (barre_pos_x, barre_pos_y, largeur_vie_actuelle, barre_hauteur))
    
    # Dessiner un contour pour que ce soit plus joli
    pygame.draw.rect(fenetre, COULEUR_CONTOUR, (barre_pos_x, barre_pos_y, barre_largeur, barre_hauteur), 2) # 2 = épaisseur
    
    # Si le joueur est mort, on peut afficher un message "GAME OVER"
    if joueur_etat == "mort":
        # Nous utilisons la police globale déjà chargée (font)
        mort_surf = font.render("GAME OVER", True, (255, 0, 0)) # Rouge
        # On utilise les variables globales largeur_fenetre et hauteur_fenetre pour centrer
        mort_rect = mort_surf.get_rect(center=(largeur_fenetre // 2, hauteur_fenetre // 2))
        fenetre.blit(mort_surf, mort_rect)
    
    # +++ DÉBUT GESTION AFFICHAGE DU MENU PAUSE (LE BON CODE) +++
    if jeu_est_en_pause:
        # On récupère les dimensionss 
        largeur_fenetre, hauteur_fenetre = fenetre.get_size()
        
        action = dessiner_menu_pause(largeur_fenetre, hauteur_fenetre)
        
        if action == "resume":
            jeu_est_en_pause = False 
            
        elif action == "menu":
            # Réinitialiser l'état du joueur avant de retourner au menu
            joueur_vie_actuelle = 100
            joueur_etat = "vivant"
            joueur_score = 0
            jeu_est_en_pause = False 
            return "menu" # <-- C'est ça qui retourne au menu
    # +++ FIN GESTION AFFICHAGE DU MENU PAUSE +++
    
    return "jeu"

sound_manager = SoundManager()

def run(largeur_fenetre, hauteur_fenetre):
    global nom_fichier_a_ouvrir, largeur_grille, hauteur_grille, grille, collision_map_solid, collision_map_water, collision_map_dechet, position_player_x, position_player_y
                
    current_scene = "menu"
    fps = []
    
    champ_actif = None
    
    logger.info("Lancement du jeu")
    champ_actif = None
    nom_actuel = "Par_Defaut"
    taille_actuelle = "50"
    
    while True:
        events = pygame.event.get()
        keys_pressed = pygame.key.get_pressed()

        for event in events:
            if event.type == pygame.QUIT:
                lecteur.SetDernierePosition(position_player_x, position_player_y)
                print("Sauvegarde de la dernière position dans le LastSave.json")
                
                x, y = lecteur.dernierePosition()
                lecteur.SetDernierePositionDansCarte(x,y)
                print("Sauvegarde de la dernière position dans la carte")
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                largeur_fenetre = event.w
                hauteur_fenetre = event.h
                fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre), pygame.RESIZABLE)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Clic gauche
                    sound_manager.play_click()

        sound_manager.update_music(current_scene)

        if current_scene == "menu":
            current_scene = menu_scene(events, largeur_fenetre, hauteur_fenetre)

        elif current_scene == "jeu":
            # On capture la position AVANT la frame
            prev_x, prev_y = position_player_x, position_player_y
            
            # On lance la frame de jeu
            current_scene = jeu_scene(events, camera_x, camera_y)
            
            # On compare avec la position APRÈS pour le son de pas
            if (position_player_x != prev_x or position_player_y != prev_y) and joueur_etat == "vivant" and not jeu_est_en_pause:
                sound_manager.play_footstep()
            
            # Gestion de l'ambiance (Oiseaux / Vent)
            if not jeu_est_en_pause and joueur_etat == "vivant":
                sound_manager.update_ambiance()
        
        elif current_scene == "charger":
            current_scene = menu_scene_chargement(events, largeur_fenetre, hauteur_fenetre)
            if current_scene != "charger" and current_scene != "jeu" and current_scene != "menu":
                
                lecteur.SetDernierePositionDansCarte(position_player_x, position_player_y)
                lecteur.SetDerniereSauvegarde(current_scene +".json")
                x, y = lecteur.dernierePositionDe(current_scene)
                lecteur.SetDernierePosition(x,y)
                current_scene = "jeu"
                
                nom_fichier_a_ouvrir = lecteur.derniereSauvegarde()
                largeur_grille, hauteur_grille, grille = lecteur.chargerfichier(nom_fichier_a_ouvrir)
                grille, collision_map_solid, collision_map_water, collision_map_dechet = textures_manager.placer_texture(taille_cellule, largeur_grille, hauteur_grille, grille, False, config.taille_frame)
                position_player_x, position_player_y = lecteur.dernierePosition()
        
        elif current_scene == "nouvelle partie":
            nom_actuel, champ_actif, taille_actuelle, current_scene = menu_scene_nouvelle_carte(events, largeur_fenetre, hauteur_fenetre, nom_actuel, champ_actif, taille_actuelle, position_player_x, position_player_y)
            position_player_x, position_player_y = lecteur.dernierePosition()
            
        if current_scene == "quit":
            lecteur.SetDernierePosition(position_player_x, position_player_y)
            print("Sauvegarde de la dernière position dans le LastSave.json")
            
            x, y = lecteur.dernierePosition()
            lecteur.SetDernierePositionDansCarte(x,y)
            print("Sauvegarde de la dernière position dans la carte")
            
            logger.info("Fermeture du jeu")
            pygame.quit()
            sys.exit()

        # Afficher FPS si test activé
        if config.test_fps:
            tick = horloge.get_fps()
            if tick > 0: fps.append(tick)

        pygame.display.flip()
        horloge.tick(FPS)
    
    return "jeu"

run(largeur_fenetre, hauteur_fenetre)
