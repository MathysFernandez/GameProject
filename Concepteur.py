import logging
import pygame
import sys
import json
import os
from Files import config 
from Files import textures_manager
from Files import Lecteur_map as lecteur

# -------------------------------------------------
# Logging (même config que main.py)
# -------------------------------------------------
logging.basicConfig(
    level=logging.DEBUG,
    filename='game.log',
    filemode='a',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)
logger = logging.getLogger(__name__)

# -------------------------------------------------
# Initialisation
# -------------------------------------------------
nom_fichier_a_ouvrir = config.nom_fichier_a_ouvrir
nombre_texture = config.nombre_texture

pygame.init()
horloge = pygame.time.Clock()
FPS = config.FPS

largeur_fenetre, hauteur_fenetre = config.get_dimensions()
fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))

largeur_grille, hauteur_grille, grille = lecteur.chargerfichier(nom_fichier_a_ouvrir)

if largeur_grille > largeur_fenetre:
    taille_cellule = largeur_fenetre // largeur_grille
else:
    taille_cellule = hauteur_fenetre // hauteur_grille

camera_x = 0
camera_y = 0

couleur_grille = (100, 100, 100)
couleur_cellule = (200, 200, 200)

grille, collision_map_solid, collision_map_water = textures_manager.placer_texture(
    taille_cellule, largeur_grille, hauteur_grille, grille)

# -------------------------------------------------
# UI texte
# -------------------------------------------------
BLANC = (255, 255, 255)
chosen_letter = 0
police = pygame.font.SysFont('Arial', 50)

def creer_surface_texte(texte):
    surface = police.render(texte, True, BLANC)
    rect = surface.get_rect(topleft=(10, 0))
    return surface, rect

lettre_surface, lettre_rect = creer_surface_texte(str(chosen_letter))

mouse_left_button_held = False

# -------------------------------------------------
# Boucle principale
# -------------------------------------------------
fps = []                     # <-- collecte FPS
running = True
while running:
    # --- Ré-initialisation chaque frame (chargement map) ---
    largeur_grille, hauteur_grille, grille = lecteur.chargerfichier(nom_fichier_a_ouvrir)
    grille, collision_map_solid, collision_map_water = textures_manager.placer_texture(
        taille_cellule, largeur_grille, hauteur_grille, grille)

    vitesse = config.vitesse
    keys_pressed = pygame.key.get_pressed()

    # --- Événements ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
            mouse_left_button_held = True
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == pygame.BUTTON_LEFT:
                mouse_left_button_held = False
            if event.button == 4:   # molette haut
                taille_cellule += 1
            if event.button == 5:   # molette bas
                taille_cellule = max(1, taille_cellule - 1)

        if event.type == pygame.KEYDOWN:
            # texture choisie
            if event.key == pygame.K_LCTRL:
                chosen_letter = (chosen_letter + 1) % nombre_texture
                lettre_surface, lettre_rect = creer_surface_texte(str(chosen_letter))
            elif event.key == pygame.K_c:
                chosen_letter = 0
                lettre_surface, lettre_rect = creer_surface_texte(str(chosen_letter))
            elif event.key == pygame.K_m:
                chosen_letter = 1
                lettre_surface, lettre_rect = creer_surface_texte(str(chosen_letter))

            # agrandir / rétrécir map
            if event.key in (pygame.K_F3, pygame.K_KP_PLUS):
                lecteur.ajouter(nom_fichier_a_ouvrir, 0)
                taille_cellule = (largeur_fenetre // (largeur_grille + 2)) if largeur_grille > largeur_fenetre else (hauteur_fenetre // (hauteur_grille + 2))
            if event.key in (pygame.K_F4, pygame.K_KP_MINUS):
                lecteur.retirer(nom_fichier_a_ouvrir)
                taille_cellule = (largeur_fenetre // (largeur_grille - 2)) if largeur_grille > largeur_fenetre else (hauteur_fenetre // (hauteur_grille - 2))

    # --- Placement tuile avec clic gauche maintenu ---
    if mouse_left_button_held:
        x, y = pygame.mouse.get_pos()
        cellular_x = int((x - camera_x) / taille_cellule)
        cellular_y = int((y - camera_y) / taille_cellule)
        lecteur.modifier_tile_dans_json(nom_fichier_a_ouvrir, cellular_y, cellular_x, chosen_letter)

    # --- Déplacement caméra ---
    vitesse += vitesse * keys_pressed[pygame.K_LSHIFT]
    deplacement_x = (keys_pressed[pygame.K_d] or keys_pressed[pygame.K_RIGHT]) - \
                    (keys_pressed[pygame.K_q] or keys_pressed[pygame.K_LEFT])
    deplacement_y = (keys_pressed[pygame.K_s] or keys_pressed[pygame.K_DOWN]) - \
                    (keys_pressed[pygame.K_z] or keys_pressed[pygame.K_UP])
    if deplacement_x != 0 and deplacement_y != 0:
        vitesse *= config.multiplicateur_vitesse_diagonale
    deplacement_x *= vitesse
    deplacement_y *= vitesse
    camera_x -= deplacement_x
    camera_y -= deplacement_y

    # --- Rendu ---
    fenetre.fill((0, 0, 0))

    world_x_start = -camera_x
    world_y_start = -camera_y
    world_x_end = world_x_start + largeur_fenetre
    world_y_end = world_y_start + hauteur_fenetre

    start_grid_x = max(0, int(world_x_start // taille_cellule) - 1)
    end_grid_x = min(largeur_grille, int(world_x_end // taille_cellule) + 1)
    start_grid_y = max(0, int(world_y_start // taille_cellule) - 1)
    end_grid_y = min(hauteur_grille, int(world_y_end // taille_cellule) + 1)

    for y in range(start_grid_y, end_grid_y):
        for x in range(start_grid_x, end_grid_x):
            screen_x = x * taille_cellule + camera_x
            screen_y = y * taille_cellule + camera_y
            rect = pygame.Rect(screen_x, screen_y, taille_cellule, taille_cellule)
            pygame.draw.rect(fenetre, couleur_cellule, rect)
            pygame.draw.rect(fenetre, couleur_grille, rect, 1)
            if grille[y][x] is not None:
                fenetre.blit(grille[y][x], rect)

    fenetre.blit(lettre_surface, lettre_rect)

    # --- FPS en temps réel (uniquement en mode test) ---
    if config.test_fps:
        fps_text = police.render(f"FPS: {horloge.get_fps():.2f}", True, BLANC)
        fenetre.blit(fps_text, (10, 10))

    pygame.display.flip()
    horloge.tick(FPS)

    # --- Collecte FPS ---
    if config.test_fps:
        cur = horloge.get_fps()
        if cur > 0:
            fps.append(cur)

# -------------------------------------------------
# Fermeture – affichage stats FPS
# -------------------------------------------------
if config.test_fps and fps:
    avg = sum(fps) / len(fps)
    print(f"[Concepteur] moy : {avg:.2f}")
    print(f"[Concepteur] min : {min(fps):.2f}")
    print(f"[Concepteur] max : {max(fps):.2f}")
    logger.info(f"[Concepteur] moy : {avg:.2f}, min : {min(fps):.2f}, max : {max(fps):.2f}")

pygame.quit()
sys.exit()