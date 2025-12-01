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





pygame.init()
angle_voulu = 0
angle = 0

# ---instancier variable par défaut---
nom_fichier_a_ouvrir = config.nom_fichier_a_ouvrir
Titre = config.Titre


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

# récupérer grille avec les valeur en int
largeur_grille, hauteur_grille, grille = lecteur.chargerfichier(nom_fichier_a_ouvrir)

# Calculer les coordonnées mondiales du centre de la grille
# C'est la position "idéale" du joueur dans le monde
centre_grille_x_monde = (largeur_grille // 2) * taille_cellule
centre_grille_y_monde = (hauteur_grille // 2) * taille_cellule

# Couleurs
couleur_grille = (100, 100, 100)
couleur_cellule = (200, 200, 200)


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





# -- joueur en cercle nouveauté ---
position_player_x = centre_grille_x_monde + 100
position_player_y = centre_grille_y_monde + 100

rayon_joueur = taille_joueur / 2
# -- FIN joueur en cercle nouveauté ---



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


# Création de la fonction de collision cercle-rectangle
def collision_cercle_rect(centre_cercle : (int, int), rayon_cercle : int, rect):
    # Trouver le point le plus proche sur le rectangle par rapport au centre du cercle
    closest_x = max(rect.left, min(centre_cercle[0], rect.right))
    closest_y = max(rect.top, min(centre_cercle[1], rect.bottom))

    #Calculer la distance entre le centre du cercle et ce point
    distance_x = centre_cercle[0] - closest_x
    distance_y = centre_cercle[1] - closest_y

    distance_squared = (distance_x ** 2) + (distance_y ** 2)
    
    # Si la distance au carré est inférieure au rayon au carré, il y a collision
    if distance_squared < (rayon_cercle ** 2):
        # On calcule la distance réelle (sans le carré)
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
grille, collision_map_solid, collision_map_water = textures_manager.placer_texture(taille_cellule, largeur_grille, hauteur_grille, grille)


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
def menu_scene(events, largeur_fenetre, hauteur_fenetre): # <-- Ajout de 'events'
    fenetre.fill(BLACK)
    #nombre de bouton
    nb_BT = 4
    compteur_BT = 0
    
    #result = draw_button(text, x, y, w, h, color, hover_color, action_name)
    result = draw_button("Game", (largeur_fenetre - BT_width) // 2 ,(hauteur_fenetre  - BT_height ) // 2 -100 -25 *nb_BT + compteur_BT * 100,  BT_width ,  BT_height, BLUE, DARK_BLUE, "jeu")
    compteur_BT += 1
    if result:
        return result
    result = draw_button("Charger", (largeur_fenetre - BT_width) // 2 ,(hauteur_fenetre  - BT_height ) // 2 -100 -25 *nb_BT + compteur_BT * 100,  BT_width ,  BT_height, BLUE, DARK_BLUE, "quit")
    
    compteur_BT += 1
    if result:
        return result
    result = draw_button("Save", (largeur_fenetre - BT_width) // 2 ,(hauteur_fenetre  - BT_height ) // 2 -100 -25 *nb_BT + compteur_BT * 100,  BT_width ,  BT_height, BLUE, DARK_BLUE, "quit")
    
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

# +++ DÉBUT AJOUT MENU PAUSE +++
def dessiner_menu_pause(largeur_fenetre, hauteur_fenetre):
    """
    Dessine l'overlay sombre et les boutons du menu pause.
    Cette fonction est appelée DEPUIS jeu_scene.
    Elle utilise les variables globales : fenetre, font, WHITE, BLUE, DARK_BLUE, BT_width, BT_height
    et la fonction draw_button.
    """

# 1. Effet translucide lors de la pause
    overlay = pygame.Surface((largeur_fenetre, hauteur_fenetre), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150)) # Noir avec 150/255 d'opacité
    fenetre.blit(overlay, (0, 0))

# 2. Dessiner le titre "Pause"
    titre_surf = font.render("Pause", True, WHITE)
    titre_rect = titre_surf.get_rect(center=(largeur_fenetre // 2, hauteur_fenetre // 2 - 150))
    fenetre.blit(titre_surf, titre_rect)

# 3. Dessiner les boutons
    action_reprise = draw_button("Reprendre", 
                                (largeur_fenetre - BT_width) // 2, 
                                (hauteur_fenetre - BT_height) // 2 - 50, 
                                BT_width, BT_height, BLUE, DARK_BLUE, "resume")

    action_menu = draw_button("Retour au Menu", 
                              (largeur_fenetre - BT_width) // 2, 
                              (hauteur_fenetre - BT_height) // 2 + 60, 
                              BT_width, BT_height, BLUE, DARK_BLUE, "menu")

# 4. Retourner l'action du bouton si un est cliqué
    if action_reprise:
        return action_reprise
    if action_menu:
        return action_menu
    
    return None
# +++ FIN AJOUT MENU PAUSE +++

# Boucle principale avec gestion de scène
def run(largeur_fenetre, hauteur_fenetre):
    
    current_scene = "menu"
    fps = []
    
    #Journal - Info démarage  jeu
    logger.info("lancement jeu")
    logger.info("run() effectué")
    
    """
    # --- Si on veut une génération avant de jouer ---
    # Nombre de texture différente (sans compté l'eau)
    nombre_texture = config.nombre_texture
    
    #taille de la nouvelle génération
    taille = config.taille_nouvelle_generation

    generation.generation(nom_fichier_a_ouvrir, nombre_texture, taille)
    # --- FIN Si on veut une génération avant de jouer ---
    """
    
    while True:
        # COLLECTE UNIQUE de TOUS les événements pour cette frame
        events = pygame.event.get() 
        keys_pressed = pygame.key.get_pressed()
        # Traitement des événements globaux (comme quitter le jeu depuis n'importe quelle scène)
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # 2. Détecter l'événement de redimensionnement de la fenêtre
            elif event.type == pygame.VIDEORESIZE:
                # Récupérer les nouvelles dimensions
                largeur_fenetre = event.w
                hauteur_fenetre = event.h
                
                
                
                # Mettre à jour la taille de la surface d'affichage de Pygame
                # C'est important pour que Pygame puisse redimensionner le "canvas" interne.
                fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre), pygame.RESIZABLE)
                
        # Appel de la scène actuelle, en lui passant TOUS les événements collectés
        if current_scene == "menu":
            current_scene = menu_scene(events, largeur_fenetre, hauteur_fenetre) 
        if current_scene == "jeu":
            current_scene = jeu_scene(events, camera_x, camera_y) 
        
        # Gestion des changements de scène (quit est déjà traité au-dessus, mais c'est bien de l'avoir ici aussi)
        if current_scene == "quit":
            if config.test_fps:
                result = 0
                for i in range(len(fps)):
                    result += fps[i]
                print("moy : ",result / len(fps))
                print("min : ", min(fps))
                print("max : ", max(fps))
                logger.info(f"moy : {result / len(fps)}, min : {min(fps)}, max : {max(fps)}")
            logger.info("fermeture jeu")
            pygame.quit()
            sys.exit()
        
        #si on veut tester plus tard le nombre de fps moyen, min, max
        if config.test_fps:
            fps_one = horloge.get_fps()
            if fps_one > 0:
                fps.append(fps_one)
        
        pygame.display.flip()
        horloge.tick(FPS)

















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
    
    global angle_voulu
    global angle
    global position_player_x
    global position_player_y
    global joueur_vie_actuelle
    global joueur_etat
    global joueur_score
    global jeu_est_en_pause
    
    
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


    # --- Dessiner uniquement les cellules visibles ---
    for y in range(start_grid_y, end_grid_y):
        for x in range(start_grid_x, end_grid_x):
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
            if grille[y][x] is not None:
                fenetre.blit(grille[y][x], rect)
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
    
    
    # ---gère la hitbox pour la rotation du rect---
    joueur = textures_manager.joueur_texture(config.taille_joueur, angle)
    
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
    score_surf = font.render(f"Score: {joueur_score}", True, WHITE)
    score_rect = score_surf.get_rect(topright=(largeur_fenetre - 10, 10))
    fenetre.blit(score_surf, score_rect)
    # +++ FIN AFFICHAGE SCORE (UI) +++
    
    # +++ DÉBUT AJOUT AFFICHAGE BARRE DE VIE (UI) +++
    
    # Barre de vie en haut à gauche
    #barre_pos_x = 10
    #barre_pos_y = 10
    #barre_largeur = 200
    #barre_hauteur = 20
    
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




run(largeur_fenetre, hauteur_fenetre)
