import pygame
try:
    from . import config
except ImportError:
    import config

def gerer_dash(events, temps_actuel, deplacement_x, deplacement_y, vitesse):
    """
    Gère l'activation et l'effet du dash.
    Met à jour les variables globales de config pour l'état du dash.
    Retourne les nouvelles valeurs de deplacement et vitesse.
    """
    
    # 1. Vérifier si on veut et peut lancer un dash
    # Condition : pas déjà actif, cooldown terminé, et le joueur est en train de bouger
    if not config.dash_actif and temps_actuel >= config.dash_cooldown_fin:
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # On vérifie qu'il y a un mouvement (pour ne pas dasher sur place)
                if deplacement_x != 0 or deplacement_y != 0:
                    config.dash_actif = True
                    config.dash_fin_temps = temps_actuel + config.dash_duree
                    config.dash_cooldown_fin = temps_actuel + config.dash_cooldown
                    
                    # On verrouille la direction du dash
                    # On normalise juste le sens (-1, 0, ou 1)
                    dir_x = 0
                    if deplacement_x > 0: dir_x = 1
                    elif deplacement_x < 0: dir_x = -1
                    
                    dir_y = 0
                    if deplacement_y > 0: dir_y = 1
                    elif deplacement_y < 0: dir_y = -1
                    
                    config.dash_dir = (dir_x, dir_y)
                break # Une seule action par frame

    # 2. Appliquer l'effet du dash si actif
    if config.dash_actif:
        if temps_actuel >= config.dash_fin_temps:
            config.dash_actif = False # Fin du dash
        else:
            # On écrase le mouvement du joueur par la direction verrouillée du dash
            deplacement_x = config.dash_dir[0]
            deplacement_y = config.dash_dir[1]
            
            # On applique le multiplicateur de vitesse
            vitesse *= config.dash_vitesse

    return deplacement_x, deplacement_y, vitesse