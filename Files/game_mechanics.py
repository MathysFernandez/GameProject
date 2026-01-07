import pygame
try:
    from . import settings
except ImportError:
    import settings

def gerer_dash(events, temps_actuel, deplacement_x, deplacement_y, vitesse):
    # Vérifier si on peut lancer le dash
    # Que si le joueur est entrain de bouger ou que le cooldown du dash n'est pas fini
    if not settings.dash_actif and temps_actuel >= settings.dash_cooldown_fin:
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # On vérifie qu'il y a un mouvement (pour ne pas dasher sur place)
                if deplacement_x != 0 or deplacement_y != 0:
                    settings.dash_actif = True
                    settings.dash_fin_temps = temps_actuel + settings.dash_duree
                    settings.dash_cooldown_fin = temps_actuel + settings.dash_cooldown
                    
                    # On verrouille la direction du dash
                    dir_x = 0
                    if deplacement_x > 0: dir_x = 1
                    elif deplacement_x < 0: dir_x = -1
                    
                    dir_y = 0
                    if deplacement_y > 0: dir_y = 1
                    elif deplacement_y < 0: dir_y = -1
                    
                    settings.dash_dir = (dir_x, dir_y)
                break # Une seule action par frame

    # Appliquer l'effet du dash si actif
    if settings.dash_actif:
        if temps_actuel >= settings.dash_fin_temps:
            settings.dash_actif = False # Fin du dash
        else:
            deplacement_x = settings.dash_dir[0]
            deplacement_y = settings.dash_dir[1]
            
            # On applique le multiplicateur de vitesse
            vitesse *= settings.dash_vitesse

    return deplacement_x, deplacement_y, vitesse