import logging
import json
import os

# Récupérer le logger existant qui a été configuré dans le main.py
logger = logging.getLogger(__name__)

#charge le fichier <nom> et retourne <width>, <height> et <grille>
#-> tuple[int, int, int]
#indique les types d'éléments retournés
def chargerfichier(nom : str) -> tuple[int, int, list]:
    fichier_charge_succes = False
    if nom [-5:] != ".json":
        nom += ".json"
    #chemin d'accé différents en fonction de qui appel
    #Je devrais le changer pour le permmettre de l'appelé depuis n'importe ou
    try:
        nom_fichier = os.path.join("Saves", nom)
        with open(nom_fichier, "r") as f:
            map_data = json.load(f)
        #print("chargement tentative 1 succes")
        fichier_charge_succes = True
    except FileNotFoundError:
        print(f"Erreur tentative 01: Le fichier de carte '{nom_fichier}' n'a pas été trouvé.")
        logger.error(f"Erreur tentative 01: Le fichier de carte '{nom_fichier}' n'a pas été trouvé.")
    if not fichier_charge_succes:
        try:
            nom_fichier = os.path.join( "..","Saves", nom)
            with open(nom_fichier, "r") as f:
                map_data = json.load(f)
            #print("chargement tentative 2 succes")
            fichier_charge_succes = True
        except FileNotFoundError:
            print(f"Erreur tentative 02: Le fichier de carte '{nom_fichier}' n'a pas été trouvé.")
            logger.error(f"Erreur tentative 02: Le fichier de carte '{nom_fichier}' n'a pas été trouvé.")

    if fichier_charge_succes:
        #Variables utile
        # Récupérer les dimensions de la carte du JSON
        width = map_data['width']
        height = map_data['height']
        grille = map_data['tiles']
        logger.info("chargerfichier() effectué")
    return width, height, grille




#modifie une case spécifique de la grille <tiles> a l'emplacement <ligne> , <colonne> par <nouvelle_valeur_tile> dans le fichier <nom>
#spécifique au concepeteur de carte
# !!! trop lent pour la génération procédurale
def modifier_tile_dans_json(nom : str, ligne : int, colonne : int, nouvelle_valeur_tile : int):
    fichier_charge_succes = False
    if nom [-5:] != ".json":
        nom += ".json"
    try:
        nom_fichier = os.path.join("Saves", nom)
        with open(nom_fichier, "r") as f:
            map_data = json.load(f)
        #print("chargement tentative 1 succes")
        fichier_charge_succes = True
    except FileNotFoundError:
        print(f"Erreur tentative 01: Le fichier de carte '{nom_fichier}' n'a pas été trouvé.")
        logger.error(f"Erreur tentative 01: Le fichier de carte '{nom_fichier}' n'a pas été trouvé.")
        
    if not fichier_charge_succes:
        try:
            nom_fichier = os.path.join( "..","Saves", nom)
            with open(nom_fichier, "r") as f:
                map_data = json.load(f)
            #print("chargement tentative 2 succes")
        except FileNotFoundError:
            print(f"Erreur tentative 02: Le fichier de carte '{nom_fichier}' n'a pas été trouvé.")
            logger.error(f"Erreur tentative 02: Le fichier de carte '{nom_fichier}' n'a pas été trouvé.")
            
    tiles = map_data["tiles"]
    
    # Vérifier les limites des indices et modifier la valeur
    if 0 <= ligne < len(tiles):
        if 0 <= colonne < len(tiles[ligne]):
            tiles[ligne][colonne] = nouvelle_valeur_tile
            # 3. Sauvegarder le contenu mis à jour dans le fichier JSON
            
            with open(nom_fichier, "w") as f:
                json.dump(map_data, f, indent=2) # indent=4 pour une meilleure lisibilité
        else:
            print(f"Erreur : Indice de colonne ({colonne}) hors limites pour la ligne {ligne}.")
            logger.error(f"Erreur : Indice de colonne ({colonne}) hors limites pour la ligne {ligne}.")
    else:
        print(f"Erreur : Indice de ligne ({ligne}) hors limites.")
        logger.error(f"Erreur : Indice de ligne ({ligne}) hors limites.")



#ajoute une colonne de chaque coté et une ligne de chaque coté
def ajouter(nom :str, valeur_defaut :int):
    
    if nom [-5:] != ".json":
        nom += ".json"
    
    fichier_charge_succes = False
    try:
        nom_fichier = os.path.join("Saves", nom) 
        with open(nom_fichier, "r") as f:
            map_data = json.load(f)
        #print("chargement tentative 1 succes")
        fichier_charge_succes = True
    except FileNotFoundError:
        print(f"Erreur tentative 01: Le fichier de carte '{nom_fichier}' n'a pas été trouvé.")
        logger.error(f"Erreur tentative 01: Le fichier de carte '{nom_fichier}' n'a pas été trouvé.")
        
    if not fichier_charge_succes:
        try:
            nom_fichier = os.path.join( "..","Saves", nom)
            with open(nom_fichier, "r") as f:
                map_data = json.load(f)
            #print("chargement tentative 2 succes")
        except FileNotFoundError:
            print(f"Erreur tentative 02: Le fichier de carte '{nom_fichier}' n'a pas été trouvé.")
            logger.error(f"Erreur tentative 02: Le fichier de carte '{nom_fichier}' n'a pas été trouvé.")
    
    tiles = map_data["tiles"]
    
    if tiles:
        nouvelles_lignes = []
        for ligne in tiles:
            # Ajoute une tuile par défaut au début et à la fin de chaque ligne existante
            nouvelle_ligne = [valeur_defaut] + ligne + [valeur_defaut]
            nouvelles_lignes.append(nouvelle_ligne)
        tiles = nouvelles_lignes # Met à jour la liste des tuiles avec les colonnes ajoutées

    # --- Étape 2 : Ajouter une ligne en haut et en bas ---
    # Récupérez la largeur actuelle de la carte après l'ajout des colonnes
    if tiles:
        largeur_carte = len(tiles[0])
    else:
        # Si tiles était vide au départ, définissez une largeur par défaut
        largeur_carte = 2 # Une colonne à gauche + une colonne à droite si la carte était vide
        # Si 'tiles' est vide, nous pourrions initialiser une grille de taille 1x1
        print("Avertissement: La carte 'tiles' était vide. Création d'une nouvelle ligne par défaut.")
        logger.warning("Avertissement: La carte 'tiles' était vide. Création d'une nouvelle ligne par défaut.")
        tiles = [[valeur_defaut]] # Initialise avec une seule tuile
        largeur_carte = 1



    # Créez une nouvelle ligne remplie de la valeur par défaut pour les bordures
    nouvelle_ligne_bordure = [valeur_defaut] * largeur_carte

    # Ajoutez la nouvelle ligne en haut
    tiles.insert(0, nouvelle_ligne_bordure)
    # Ajoutez la nouvelle ligne en bas
    tiles.append(nouvelle_ligne_bordure)

    # --- Mettre à jour map_data avec les nouvelles tuiles ---
    map_data["tiles"] = tiles
    #la nouvelle hauteur est le nombre de lignes
    map_data["height"] = len(tiles)
    #la nouvelle largeur est le nombre de colonnes dans la première ligne '
    map_data["width"] = len(tiles[0])

    # --- Sauvegarder la carte modifiée ---
    try:
        with open(nom_fichier, "w") as f: # Utilisez "w" pour l'écriture
            json.dump(map_data, f, indent=4) # indent=4 pour une meilleure "lisibilité"
    except Exception as e:
        print(f"Erreur lors de la sauvegarde de la carte: {e}")
        logger.error(f"Erreur lors de la sauvegarde de la carte: {e}")



#retire une colonne de chaque coté et une ligne de chaque coté
def retirer(nom):
    if nom [-5:] != ".json":
        nom += ".json"
    
    fichier_charge_succes = False
    try:
        nom_fichier = os.path.join("Saves", nom)
        with open(nom_fichier, "r") as f:
            map_data = json.load(f)
        #print("chargement tentative 1 succes")
        fichier_charge_succes = True
    except FileNotFoundError:
        print(f"Erreur tentative 01: Le fichier de carte '{nom_fichier}' n'a pas été trouvé.")
        logger.error(f"Erreur tentative 01: Le fichier de carte '{nom_fichier}' n'a pas été trouvé.")
        
    if not fichier_charge_succes:
        try:
            nom_fichier = os.path.join( "..","Saves", nom)
            with open(nom_fichier, "r") as f:
                map_data = json.load(f)
            #print("chargement tentative 2 succes")
        except FileNotFoundError:
            print(f"Erreur tentative 02: Le fichier de carte '{nom_fichier}' n'a pas été trouvé.")
            logger.error(f"Erreur tentative 02: Le fichier de carte '{nom_fichier}' n'a pas été trouvé.")
            
    tiles = map_data["tiles"]
    
    # --- Retirer une ligne en haut et en bas ---
    if len(tiles) >= 3: #au moins 3 lignes pour pouvoir en supprimer 2 et qu'il en reste 1
        tiles = tiles[1:-1] #supprime la première (index 0) et la dernière ligne
    else:
        print("La carte est trop petite pour retirer des lignes (moins de 3 lignes).")
        logger.warning("La carte est trop petite pour retirer des lignes (moins de 3 lignes).")
        #on suppose qu'on ne retire que si c'est possible.
    
    # --- Retirer une colonne à gauche et à droite de chaque ligne ---
    if tiles and len(tiles[0]) >= 3: # S'il y a des lignes et au moins 3 colonnes
        nouvelles_lignes = []
        for ligne in tiles:
            # Supprime le premier (index 0) et le dernier élément de chaque ligne
            nouvelle_ligne = ligne[1:-1]
            nouvelles_lignes.append(nouvelle_ligne)
        tiles = nouvelles_lignes # Met à jour la liste des tuiles avec les colonnes retirées
    elif tiles: #s'il y a des lignes mais moins de 3 colonnes
        print("La carte est trop petite pour retirer des colonnes (moins de 3 colonnes).")
        logger.warning("La carte est trop petite pour retirer des colonnes (moins de 3 colonnes).")
    # --- Mettre à jour map_data avec les nouvelles tuiles ---
    map_data["tiles"] = tiles
    # La nouvelle hauteur est le nombre de lignes 
    map_data["height"] = len(tiles)
    # La nouvelle largeur est le nombre de colonnes dans la première ligne  
    map_data["width"] = len(tiles[0]) if tiles else 0 # Gère le cas où la carte est devenue vide

    # ---Sauvegarder la carte modifiée ---
    try:
        with open(nom_fichier, "w") as f: #utilise "w" pour l'écriture (écrase le contenu)
            json.dump(map_data, f, indent=4) # indent=4  pour une meilleure "lisibilité"
    except Exception as e:
        print(f"Erreur lors de la sauvegarde de la carte: {e}")
        logger.error(f"Erreur lors de la sauvegarde de la carte: {e}")




#creer ou remplace le fichier (produit un tiles de taille <taille> par <taille> de 0)
#produit une grille de 0 dans le fichier <name>
def creation_fichier_X(name : str, taille : int):
    fichier_charge_succes = False
    if name[-5:] != ".json":
        name_json = name + ".json"
    else:
        name_json = name
        name = name[:-5]
    
    
    
    grille = [[0 for _ in range (taille)] for _ in range(taille)]
    
    contenu = {
        "name" : name,
        "width" : taille,
        "height" : taille,
        "tiles" : grille
    }
    
    try:
        chemin = os.path.join("../Saves", name_json)
        
        with open(chemin,'w') as f:
            json.dump(contenu,f, indent=4)
        fichier_charge_succes = True
    except FileNotFoundError:
        print(f"Erreur tentative 01: Le fichier de carte '{name}' n'a pas été trouvé.")
        logger.error(f"Erreur tentative 01: Le fichier de carte '{name}' n'a pas été trouvé.")
    
    if not fichier_charge_succes:
        try:
            chemin = os.path.join("Saves", name_json)
            
            with open(chemin,'w') as f:
                json.dump(contenu,f, indent=4)
            fichier_charge_succes = True
        except FileNotFoundError:
            print(f"Erreur tentative 02: Le fichier de carte '{name}' n'a pas été trouvé.")
            logger.error(f"Erreur tentative 02: Le fichier de carte '{name}' n'a pas été trouvé.")
    if fichier_charge_succes:
        print(name + " a été creer")
        logger.info(f" '{name}' a été creer")

    


#modifie l'ensemble de la grille du fichier 
def modifier_grille(nom : str, grille : list):
    if nom [-5:] != ".json":
        nom += ".json"
    
    fichier_charge_succes = False
    try:
        nom_fichier = os.path.join("Saves", nom)
        with open(nom_fichier, "r") as f:
            map_data = json.load(f)
        #print("chargement tentative 1 succes")
        fichier_charge_succes = True
    except FileNotFoundError:
        print(f"Erreur tentative 01: Le fichier de carte '{nom_fichier}' n'a pas été trouvé.")
        logger.error(f"Erreur tentative 01: Le fichier de carte '{nom_fichier}' n'a pas été trouvé.")
        
    if not fichier_charge_succes:
        try:
            nom_fichier = os.path.join( "..","Saves", nom)
            with open(nom_fichier, "r") as f:
                map_data = json.load(f)
            #print("chargement tentative 2 succes")
        except FileNotFoundError:
            print(f"Erreur tentative 02: Le fichier de carte '{nom_fichier}' n'a pas été trouvé.")
            logger.error(f"Erreur tentative 02: Le fichier de carte '{nom_fichier}' n'a pas été trouvé.")
    
    # Remplacement des 'tiles' par la nouvelle grille
    map_data['tiles'] = grille
    
    with open(nom_fichier, "w") as f:
        json.dump(map_data, f, indent=4) # indent=4 pour une meilleure lisibilité
    print(f"'{nom_fichier}' enregistrer")
    logger.info(f"'{nom_fichier}' enregistrer")


    
#creer ou réinitialise un fichier json avec tel nom avec un tiles de X par X de 0
#creation_fichier_X("map_generation_procedural", 100)