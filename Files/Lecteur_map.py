import logging
import json
import os


logger = logging.getLogger(__name__)

def chargerfichier(nom : str) -> tuple[int, int, list]:
    fichier_charge_succes = False
    if nom [-5:] != ".json":
        nom += ".json"

    try:
        nom_fichier = os.path.join("Saves", nom)
        with open(nom_fichier, "r") as f:
            map_data = json.load(f)
        fichier_charge_succes = True
    except FileNotFoundError:
        logger.error(f"Erreur tentative 01: Le fichier de carte '{nom_fichier}' n'a pas été trouvé.")
    if not fichier_charge_succes:
        try:
            nom_fichier = os.path.join( "..","Saves", nom)
            with open(nom_fichier, "r") as f:
                map_data = json.load(f)
            fichier_charge_succes = True
        except FileNotFoundError:
            logger.error(f"Erreur tentative 02: Le fichier de carte '{nom_fichier}' n'a pas été trouvé.")

    if fichier_charge_succes:
        #Variables utile
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
        fichier_charge_succes = True
    except FileNotFoundError:
        logger.error(f"Erreur tentative 01: Le fichier de carte '{nom_fichier}' n'a pas été trouvé.")
        
    if not fichier_charge_succes:
        try:
            nom_fichier = os.path.join( "..","Saves", nom)
            with open(nom_fichier, "r") as f:
                map_data = json.load(f)
            fichier_charge_succes = True
        except FileNotFoundError:
            logger.error(f"Erreur tentative 02: Le fichier de carte '{nom_fichier}' n'a pas été trouvé.")
            
    tiles = map_data["tiles"]
    
    #Vérifier les limites des indices et modifier la valeur
    if 0 <= ligne < len(tiles):
        if 0 <= colonne < len(tiles[ligne]):
            tiles[ligne][colonne] = nouvelle_valeur_tile
            
            with open(nom_fichier, "w") as f:
                json.dump(map_data, f, indent=2)
        else:
            logger.error(f"Erreur : Indice de colonne ({colonne}) hors limites pour la ligne {ligne}.")
    else:
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
        fichier_charge_succes = True
    except FileNotFoundError:
        logger.error(f"Erreur tentative 01: Le fichier de carte '{nom_fichier}' n'a pas été trouvé.")
        
    if not fichier_charge_succes:
        try:
            nom_fichier = os.path.join( "..","Saves", nom)
            with open(nom_fichier, "r") as f:
                map_data = json.load(f)
        except FileNotFoundError:
            logger.error(f"Erreur tentative 02: Le fichier de carte '{nom_fichier}' n'a pas été trouvé.")
    
    tiles = map_data["tiles"]
    
    if tiles:
        nouvelles_lignes = []
        for ligne in tiles:
            nouvelle_ligne = [valeur_defaut] + ligne + [valeur_defaut]
            nouvelles_lignes.append(nouvelle_ligne)
        tiles = nouvelles_lignes

    if tiles:
        largeur_carte = len(tiles[0])
    else:
        largeur_carte = 2
        logger.warning("Avertissement: La carte 'tiles' était vide. Création d'une nouvelle ligne par défaut.")
        tiles = [[valeur_defaut]] # Initialise avec une seule tuile
        largeur_carte = 1


    nouvelle_ligne_bordure = [valeur_defaut] * largeur_carte

    tiles.insert(0, nouvelle_ligne_bordure)
    tiles.append(nouvelle_ligne_bordure)

    map_data["tiles"] = tiles
    map_data["height"] = len(tiles)
    map_data["width"] = len(tiles[0])

    try:
        with open(nom_fichier, "w") as f:
            json.dump(map_data, f, indent=4)
    except Exception as e:
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
        fichier_charge_succes = True
    except FileNotFoundError:
        logger.error(f"Erreur tentative 01: Le fichier de carte '{nom_fichier}' n'a pas été trouvé.")
        
    if not fichier_charge_succes:
        try:
            nom_fichier = os.path.join( "..","Saves", nom)
            with open(nom_fichier, "r") as f:
                map_data = json.load(f)
            fichier_charge_succes = True
        except FileNotFoundError:
            logger.error(f"Erreur tentative 02: Le fichier de carte '{nom_fichier}' n'a pas été trouvé.")
            
    tiles = map_data["tiles"]
    
    
    if len(tiles) >= 3: 
        tiles = tiles[1:-1] 
    else:
        logger.warning("La carte est trop petite pour retirer des lignes (moins de 3 lignes).")
    
    if tiles and len(tiles[0]) >= 3: 
        nouvelles_lignes = []
        for ligne in tiles:
            nouvelle_ligne = ligne[1:-1]
            nouvelles_lignes.append(nouvelle_ligne)
        tiles = nouvelles_lignes 
    elif tiles: 
        logger.warning("La carte est trop petite pour retirer des colonnes (moins de 3 colonnes).")
    
    map_data["tiles"] = tiles
    
    map_data["height"] = len(tiles)

    map_data["width"] = len(tiles[0]) if tiles else 0

    try:
        with open(nom_fichier, "w") as f: 
            json.dump(map_data, f, indent=4) 
    except Exception as e:
        logger.error(f"Erreur lors de la sauvegarde de la carte: {e}")




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
        "position_x": None,
        "position_y": None,
        "tiles" : grille
    }
    
    try:
        chemin = os.path.join("../Saves", name_json)
        
        with open(chemin,'w') as f:
            json.dump(contenu,f, indent=4)
        fichier_charge_succes = True
    except FileNotFoundError:
        logger.error(f"Erreur tentative 01: Le fichier de carte '{name}' n'a pas été trouvé.")
    
    if not fichier_charge_succes:
        try:
            chemin = os.path.join("Saves", name_json)
            
            with open(chemin,'w') as f:
                json.dump(contenu,f, indent=4)
            fichier_charge_succes = True
        except FileNotFoundError:
            logger.error(f"Erreur tentative 02: Le fichier de carte '{name}' n'a pas été trouvé.")
    if fichier_charge_succes:
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
        fichier_charge_succes = True
    except FileNotFoundError:
        logger.error(f"Erreur tentative 01: Le fichier de carte '{nom_fichier}' n'a pas été trouvé.")
        
    if not fichier_charge_succes:
        try:
            nom_fichier = os.path.join( "..","Saves", nom)
            with open(nom_fichier, "r") as f:
                map_data = json.load(f)
            fichier_charge_succes = True
        except FileNotFoundError:
            logger.error(f"Erreur tentative 02: Le fichier de carte '{nom_fichier}' n'a pas été trouvé.")
    
    # Remplacement des 'tiles' par la nouvelle grille
    map_data['tiles'] = grille
    
    with open(nom_fichier, "w") as f:
        json.dump(map_data, f, indent=4)
    logger.info(f"'{nom_fichier}' enregistrer")





def derniereSauvegarde() -> str or None:
    nom = "lastSave.json"
    fichier_charge_succes = False
    try:
        nom_fichier = os.path.join("Saves", nom)
        with open(nom_fichier, "r") as f:
            map_data = json.load(f)
        fichier_charge_succes = True
    except FileNotFoundError:
        logger.error(f"Erreur tentative 01: Le fichier de carte '{nom_fichier}' n'a pas été trouvé.")
        
    if not fichier_charge_succes:
        try:
            nom_fichier = os.path.join( "..","Saves", nom)
            with open(nom_fichier, "r") as f:
                map_data = json.load(f)
            fichier_charge_succes = True
        except FileNotFoundError:
            logger.error(f"Erreur tentative 02: Le fichier de carte '{nom_fichier}' n'a pas été trouvé.")
            
    if fichier_charge_succes:
        nom_sauvegarde = map_data.get("last_save_file")
        if nom_sauvegarde:
            return nom_sauvegarde
    return None



def dernierePosition() -> (int,int) or None:
    nom = "lastSave.json"
    fichier_charge_succes = False
    try:
        nom_fichier = os.path.join("Saves", nom)
        with open(nom_fichier, "r") as f:
            map_data = json.load(f)
        fichier_charge_succes = True
    except FileNotFoundError:
        logger.error(f"Erreur tentative 01: Le fichier de carte '{nom_fichier}' n'a pas été trouvé.")
        
    if not fichier_charge_succes:
        try:
            nom_fichier = os.path.join( "..","Saves", nom)
            with open(nom_fichier, "r") as f:
                map_data = json.load(f)
            fichier_charge_succes = True
        except FileNotFoundError:
            logger.error(f"Erreur tentative 02: Le fichier de carte '{nom_fichier}' n'a pas été trouvé.")
            
    if fichier_charge_succes:
        position_x = map_data.get("position_x")
        position_y = map_data.get("position_y")
        
        if position_x != None and position_y != None:
            return position_x, position_y
    return None

def dernierePositionDe(nom : str) -> (int,int) or None:
    if nom [-5:] != ".json":
        nom += ".json"
        
    fichier_charge_succes = False
    try:
        nom_fichier = os.path.join("Saves", nom)
        with open(nom_fichier, "r") as f:
            map_data = json.load(f)
        fichier_charge_succes = True
    except FileNotFoundError:
        logger.error(f"Erreur tentative 01: Le fichier de carte '{nom_fichier}' n'a pas été trouvé.")
        
    if not fichier_charge_succes:
        try:
            nom_fichier = os.path.join( "..","Saves", nom)
            with open(nom_fichier, "r") as f:
                map_data = json.load(f)
            fichier_charge_succes = True
        except FileNotFoundError:
            logger.error(f"Erreur tentative 02: Le fichier de carte '{nom_fichier}' n'a pas été trouvé.")
            
    if fichier_charge_succes:
        position_x = map_data.get("position_x")
        position_y = map_data.get("position_y")
        
        if position_x != None and position_y != None:
            return position_x, position_y
    return 0,0


def SetDerniereSauvegarde(nouvelle_sauvegarde):
    nom = "lastSave.json"
    fichier_charge_succes = False
    try:
        nom_fichier = os.path.join("Saves", nom)
        with open(nom_fichier, "r") as f:
            map_data = json.load(f)
        fichier_charge_succes = True
    except FileNotFoundError:
        logger.error(f"Erreur tentative 01: Le fichier de carte '{nom_fichier}' n'a pas été trouvé.")
        
    if not fichier_charge_succes:
        try:
            nom_fichier = os.path.join( "..","Saves", nom)
            with open(nom_fichier, "r") as f:
                map_data = json.load(f)
            fichier_charge_succes = True
        except FileNotFoundError:
            logger.error(f"Erreur tentative 02: Le fichier de carte '{nom_fichier}' n'a pas été trouvé.")
            
    if fichier_charge_succes:
        map_data["last_save_file"] = nouvelle_sauvegarde

        try:
            os.makedirs(os.path.dirname(nom_fichier), exist_ok=True)

            with open(nom_fichier, "w") as f:
                json.dump(map_data, f, indent=4)
            
        except IOError as e:
            logger.error(f"Erreur critique écriture config : {e}")

def SetDernierePosition(nouvelle_position_x : int, nouvelle_position_y : int):
    nom = "lastSave.json"
    fichier_charge_succes = False
    try:
        nom_fichier = os.path.join("Saves", nom)
        with open(nom_fichier, "r") as f:
            map_data = json.load(f)
        fichier_charge_succes = True
    except FileNotFoundError:
        logger.error(f"Erreur tentative 01: Le fichier de carte '{nom_fichier}' n'a pas été trouvé.")
        
    if not fichier_charge_succes:
        try:
            nom_fichier = os.path.join( "..","Saves", nom)
            with open(nom_fichier, "r") as f:
                map_data = json.load(f)
            fichier_charge_succes = True
        except FileNotFoundError:
            logger.error(f"Erreur tentative 02: Le fichier de carte '{nom_fichier}' n'a pas été trouvé.")
            
    if fichier_charge_succes:
        map_data["position_x"] = nouvelle_position_x
        map_data["position_y"] = nouvelle_position_y

        try:
            os.makedirs(os.path.dirname(nom_fichier), exist_ok=True)

            with open(nom_fichier, "w") as f:
                json.dump(map_data, f, indent=4)
            logger.info("Sauvegarde de la dernière position dans le LastSave.json")
            
        except IOError as e:
            logger.error(f"Erreur critique écriture config : {e}")
            
    

def SetDernierePositionDansCarte (nouvelle_position_x : int, nouvelle_position_y : int):
    nom = derniereSauvegarde()
    fichier_charge_succes = False
    try:
        nom_fichier = os.path.join("Saves", nom)
        with open(nom_fichier, "r") as f:
            map_data = json.load(f)
        fichier_charge_succes = True
    except FileNotFoundError:
        logger.error(f"Erreur tentative 01: Le fichier de carte '{nom_fichier}' n'a pas été trouvé.")
        
    if not fichier_charge_succes:
        try:
            nom_fichier = os.path.join( "..","Saves", nom)
            with open(nom_fichier, "r") as f:
                map_data = json.load(f)
            fichier_charge_succes = True
        except FileNotFoundError:
            logger.error(f"Erreur tentative 02: Le fichier de carte '{nom_fichier}' n'a pas été trouvé.")
            
    if fichier_charge_succes:
        map_data["position_x"] = nouvelle_position_x
        map_data["position_y"] = nouvelle_position_y

        try:
            os.makedirs(os.path.dirname(nom_fichier), exist_ok=True)

            with open(nom_fichier, "w") as f:
                json.dump(map_data, f, indent=4)
            
            logger.info("Sauvegarde de la dernière position dans la carte")
            
        except IOError as e:
            logger.error(f"Erreur critique écriture config : {e}")





def recupNomSauvegarde()-> list[str]:
    fichier_charge_succes = False
    liste_sauvegardes = []
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        dossier_saves = os.path.join(base_dir, "Saves")
        if os.path.exists(dossier_saves):
            fichier_charge_succes = True
    except FileNotFoundError:
        logger.error(f"Erreur tentative 01: impossible de charger l'arboresence")

    
    
    if not fichier_charge_succes:
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            dossier_saves = os.path.join(base_dir, "..", "Saves")
            if os.path.exists(dossier_saves):
                fichier_charge_succes = True
        except FileNotFoundError:
            logger.error(f"Erreur tentative 02: impossible de charger l'arboresence")
            return []
        
    if fichier_charge_succes:
        try:
            fichiers = os.listdir(dossier_saves)
            for f in fichiers:
                if f.endswith(".json") and f != "lastSave.json":
                    nom_propre = f[:-5] 
                    liste_sauvegardes.append(nom_propre)
                    
            return liste_sauvegardes

        except Exception as e:
            logger.error(f"Erreur lors de la lecture des sauvegardes : {e}")
            return []
    


#creation_fichier_X("test", 100)

#print(derniereSauvegarde())
#SetDerniereSauvegarde("test.json")
#print(derniereSauvegarde())
#print(dernierePositionDe("test"))
#SetDernierePosition(None, None)
#print(dernierePosition())

#x, y = dernierePosition()
#SetDernierePositionDansCarte (x, y)
#print(recupNomSauvegarde())