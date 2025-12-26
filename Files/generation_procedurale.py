try:
    # Pour l'importation relative (lorsque le script est appelé par main.py)
    from . import Lecteur_map as lecteur
except ImportError:
    # Pour l'importation directe (lorsque le script est exécuté seul)
    import Lecteur_map as lecteur

try:
    # Pour l'importation relative (lorsque le script est appelé par main.py)
    from . import config
except ImportError:
    # Pour l'importation directe (lorsque le script est exécuté seul)
    import config


import random
import time

import logging

logger = logging.getLogger(__name__)


nom_fichier_a_ouvrir = lecteur.derniereSauvegarde()
nombre_texture = config.nombre_texture
multiplicateur_sol = config.multiplicateur_sol
nombre_répétition = config.nombre_répétition
nombre_répétition_water = config.nombre_répétition_water
multiplicateur_point_apparition_water = config.multiplicateur_point_apparition_water

#taille de la nouvelle génération
taille = config.taille_nouvelle_generation



#retourne 2 listes : la population, et le poid de chacun
#cela permet ensuite de faire random.choices
def listes(nombre_texture : int) -> list:
    if nombre_texture < 1:
        print("Le nombre_texture de texture doit etre au moins 1")
    
    poid_sol = (nombre_texture -1) * multiplicateur_sol
    population = []
    poids = []
    for i in range (nombre_texture):
        population.append(i)
        
        if i == 0:
            poids.append(poid_sol) # Poids spécial pour la texture 0
        
        #...
        
        else:
            poids.append(1)
    logger.info("listes() effectué")
    return population, poids



#génère de l'eau sur la carte
def generation_water(largeur_grille : int, hauteur_grille : int, grille : list, nombre_répétition_water : int =1,multiplicateur_point_apparition_water : int =1) -> list:
    for nb in range (nombre_répétition_water):
        grille_suivante = [row[:] for row in grille]
        for x in range (1, largeur_grille -1):
            for y in range (1, hauteur_grille -1):
                valeur_actu = grille[x][y]
                
                #si première boucle:
                if nb == 0:
                    #Parcourir les voisins
                    if valeur_actu == 0:
                        if random.randint(0,1000) < (1 * multiplicateur_point_apparition_water):
                            for dx in [-1, 0, 1]:  #Décalages pour l'axe X
                                for dy in [-1, 0, 1]:  #décalages pour l'axe Y
                                    #calculer les coordonnées du voisin
                                    x_voisin = x + dx
                                    y_voisin = y + dy
                                    voisin = grille[x_voisin][y_voisin]
                                    if voisin == 0 and random.randint(0,100) < 15:
                                        grille_suivante[x_voisin][y_voisin] = -1
                
                #si pas première boucle:
                elif nb != 0:    
                    #Parcourir les voisins
                    if valeur_actu == -1:
                        for dx in [-1, 0, 1]:  #Décalages pour l'axe X
                            for dy in [-1, 0, 1]:  #décalages pour l'axe Y
                                #calculer les coordonnées du voisin
                                x_voisin = x + dx
                                y_voisin = y + dy
                                voisin = grille[x_voisin][y_voisin]
                                if voisin == 0 and random.random() < 0.30 :
                                    grille_suivante[x_voisin][y_voisin] = -1
                                
        grille = grille_suivante
    print("génération water terminé")
    logger.info("generation_water() effectué")
    return grille

#genère de nouveaux type de mur à la place du mur de base
def generation_type_mur(largeur_grille : int, hauteur_grille : int, grille : list, nombre_répétition : int) -> list:
    for nb in range (nombre_répétition):
        grille_suivante = [row[:] for row in grille]
        for x in range (largeur_grille):
            for y in range (hauteur_grille):
                voisin_mur_type_1 = 0
                
                if x >= 1 and y >= 1 and x < largeur_grille -1  and y < hauteur_grille -1 :
                    valeur_actu = grille[x][y]
                    
                    #Parcourir les voisins
                    #permets de rapprocher des éléments
                    for dx in [-1, 0, 1]:  #Décalages pour l'axe X
                        for dy in [-1, 0, 1]:  #décalages pour l'axe Y
                            # Si pas la valeur actuelle
                            if not (dx == 0 and dy == 0):
                                #calculer les coordonnées du voisin
                                x_voisin = x + dx
                                y_voisin = y + dy
                                voisin = grille[x_voisin][y_voisin]
                                
                                if voisin == 1:
                                    voisin_mur_type_1 += 1
                                
                                    
                    #si une cellule est un mur :
                    if valeur_actu == 1 and voisin_mur_type_1 > 5 and nombre_texture > 2 and nb < (nombre_répétition -2) :
                        if random.random() > 0.98:
                            grille_suivante[x][y] = 2
                    
                    #si le mur est un mur 2 alors mettre un mur 2 sur l'une ou plusieures des cases alentour
                    if valeur_actu == 2:
                        for i in range(3):
                            x_alea = x + random.randint(-1,1)
                            y_alea = y + random.randint(-1,1)
                            if x_alea == x or y_alea == y:
                                grille_suivante[x_alea][y_alea] = 2

        grille = grille_suivante
    print("génération type mur terminé")
    logger.info("generation_type_mur() effectué")
    return grille

#supprime les mur solitaire
def generation_voisin_mur(largeur_grille : int, hauteur_grille : int, grille : list) -> list:
    
    grille_suivante = [row[:] for row in grille]
    for x in range (largeur_grille):
        for y in range (hauteur_grille):
            voisin_mur = 0
            if x >= 1 and y >= 1 and x < largeur_grille -1  and y < hauteur_grille -1 :
                valeur_actu = grille[x][y]
                if valeur_actu != 0:
                    #Parcourir les voisins
                    for dx in [-1, 0, 1]:  #Décalages pour l'axe X
                        for dy in [-1, 0, 1]:  #décalages pour l'axe Y
                            # Si pas la valeur actuelle
                            if ((dx == 0 and dy != 0) or (dx != 0 and dy == 0)) :
                                x_voisin = x + dx
                                y_voisin = y + dy
                                voisin = grille[x_voisin][y_voisin]
                                
                                if voisin != 0:
                                    voisin_mur += 1
                    if voisin_mur == 0:
                        grille_suivante[x][y] = 0
    grille = grille_suivante
    print("génération suppression mur solitaire terminé")
    logger.info("generation_voisin_mur() effectué")
    return grille



#automate cellular sur sol et mur
#seulement 0 et 1
# mur = 1
# sol = 0
def generation_mur(largeur_grille : int, hauteur_grille : int, grille : list, nombre_répétition : int) -> list:
    for _ in range (nombre_répétition):
        grille_suivante = [row[:] for row in grille]
        for x in range (largeur_grille):
            for y in range (hauteur_grille):
                voisin_mur = 0
                
                if x >= 1 and y >= 1 and x < largeur_grille -1  and y < hauteur_grille -1 :
                    valeur_actu = grille[x][y]
                    
                    #Parcourir les voisins
                    #permets de rapprocher des éléments
                    for dx in [-1, 0, 1]:  #Décalages pour l'axe X
                        for dy in [-1, 0, 1]:  #décalages pour l'axe Y
                            # Si pas la valeur actuelle
                            if not (dx == 0 and dy == 0):
                                #calculer les coordonnées du voisin
                                x_voisin = x + dx
                                y_voisin = y + dy
                                voisin = grille[x_voisin][y_voisin]
                                
                                if voisin != 0:
                                    voisin_mur += 1
                                    
                    #si une cellule est un mur :
                    #si elle a moins de X voisins murs, elle devient sol (0)
                    if valeur_actu != 0 and voisin_mur < 3: #3 c'est très bien
                        grille_suivante[x][y] = 0
                    
                    #si une cellule est un sol (0) :
                    # si elle a plus de X voisins murs, elle devient mur (X)
                    elif valeur_actu == 0 and voisin_mur > 3: #3 c'est très bien
                        grille_suivante[x][y] = 1

        grille = grille_suivante                
                    
    print("génération mur terminé")
    logger.info("generation_mur() effectué")
    return grille

#génération bordure de carte
def generation_limite(largeur_grille : int, hauteur_grille : int, grille : list) -> list:
    for x in range (largeur_grille):
        grille[x][0] = 1
        grille[x][hauteur_grille-1] = 1
        
    for y in range (1, hauteur_grille -1):
        grille[0][y] = 1
        grille[largeur_grille-1][y] = 1
    print("génération limite carte terminé")
    logger.info("generation_limite() effectué")
    return grille




def generation(nom : str, nombre_texture : int = 2, taille : int = 100):
    #gestion du nom en fonction de la présence ou non de l'extension
    if nom [-5:] != ".json":
        nom += ".json"
    #nombres défini le nombre_texturede valeur à intégrer dans la génération procédurale
    #2 = des 0 et des 1
    #3 = des 0 et des 1 et des 2
    #4 = des 0 et des 1 et des 2 et des 3
    #etc...
    
    #creer ou réinitialise un fichier json avec tel nom avec un tiles de X par X de 0 
    lecteur.creation_fichier_X(nom, taille)
    
    #récupérer grille
    largeur_grille, hauteur_grille, grille = lecteur.chargerfichier(nom_fichier_a_ouvrir)
    
    #récupère les 2 premiers paramètres de random.choice
    population, poids = listes(2)
    
    #génération aléatoire
    for x in range (largeur_grille):
        for y in range (hauteur_grille):
            #liste éléments, poids de chacun, nombre_texture d'éléments pris aux hasard
            result = random.choices(population, poids, k=1)[0]
            grille[x][y] = result
    
    
    # ---génération procédurale---
    # génération des murs
    grille = generation_mur(largeur_grille, hauteur_grille, grille, 9)
    # génération suppression des murs en trop en les remplacants par du sol
    grille = generation_voisin_mur(largeur_grille, hauteur_grille, grille)
    
    if nombre_texture > 2:
        #modifie les murs en plusieurs textures de mur différentes
        grille = generation_type_mur(largeur_grille, hauteur_grille, grille, nombre_répétition)
    
    #génération de l'eau
    grille = generation_water(largeur_grille, hauteur_grille, grille, nombre_répétition_water, multiplicateur_point_apparition_water)
    
    #génération bordure de carte
    grille = generation_limite(largeur_grille, hauteur_grille, grille)
    
    print("génération limite carte terminé")
    logger.info("generation_limite() effectué")
    
    #sauvegarde la grille sur le fichier
    lecteur.modifier_grille(nom_fichier_a_ouvrir, grille)
    
if __name__ == "__main__":
    generation(nom_fichier_a_ouvrir, nombre_texture, taille)