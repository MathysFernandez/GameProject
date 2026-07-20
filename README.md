# GameProject
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

![exemple_generation](https://github.com/user-attachments/assets/5fb52f79-63a1-4b11-be58-4c1a9555c37d)


## Project Overview 

**_GameProject_** is a Pygame game where you explore a vast world from a top-down view.    
Our goal is to deliver an immersive and engaging experience where every interaction and challenge brings you closer to victory.
Game development is simplified thanks to the integration of a dedicated map editor (`conceptor.py`).   

---
## Project Architecture     
> Information on project files and directory structure

### Structure
GameProject/   
├── Assets/             
├── Files/    
├── image_pou_gitlab/      
├── Saves/                    
├── .gitignore     
├── CHANGELOG     
├── conceptor.py       
├── game.log     
├── requirement.txt         
├── LICENSE    
├── main.py      
└── README.md
   

###  Content



* [main.py]()
: The main game file, contains the game loop with the menu, game, etc. scenes.   

* [conceptor.py]()
: Developer tool to modify the game map.   

* [LICENSE]()
: Legal document defining what others can do with the code.     

* [CHANGELOG]()
: Document that lists major changes chronologically.   

* [requirement.txt]()
: Essential text file that lists all external software dependencies.

* [Files/]()
: Directory containing all python files.

* [Files/game_mechanics.py]()
: Handles everything related to `gameplay` (dash, etc...).   

* [Files/map_loader.py]()
: Reads and modifies the JSON file. 

* [Files/plant_manager.py]()
: Plant management (planting and harvesting). 

* [Files/settings.py]()
: Configuration file for screen dimensions, title, etc.    

* [Files/procedural_generation.py]()
: File allowing, as its name suggests, to generate a map (mainly Cellular Automata).    

* [Files/sound_manager.py]()
: Handles sound effects and music.

* [Files/texture_manager.py]()
:  Manages loading and scaling of textures, as well as preparing the grid and collision data.  

* [Assets/]()
: Contains all game assets (images, sounds, piskel, etc.)   

* [Saves/]()
: Contains all game maps (JSON files).  

* [Saves/LastSave]()
: Manages the last loaded map and the last positions   

* [.gitignore]()
: Specifies the files and directories that Git should ignore and not track, to prevent them from being accidentally added to commits. (Ex: .log files)

* [game.log]()
: Logs activity in the game, conceptor, and important game functions to help with debugging.





---



## World Creation

**Goal**:
>  To ensure rapid and efficient development

The GameProject includes a custom-built map editor, named conceptor. This internal tool was designed specifically to facilitate world layout.   
Rather than manually coding every map element or having a completely procedural map, ̀conceptor.py` offers an interface to quickly visualize, place, and organize the various components of the game world.

### Editor Controls:

* <kbd>Z</kbd>,<kbd>Q</kbd>,<kbd>S</kbd>,<kbd>D</kbd>: to move the map
* <kbd>clic Gauche</kbd>: to place textures (can be held down)
* <kbd>M</kbd>: wall texture mode
* <kbd>C</kbd>: floor texture mode
* <kbd>L-Ctrl</kbd>: change texture mode
* <kbd>F3</kbd>/<kbd>+</kbd>: add columns/rows
* <kbd>F4</kbd>/<kbd>-</kbd>: remove columns/rows
* <kbd>molette</kbd>: zoom

---




## Quick Start

> To clone the project, install dependencies, and run the game locally:

Clone this repository in bash:

```bash
git clone https://github.com/MathysFernandez/GameProject.git
```

install dependencies:

* [Python (the latest version)](https://www.python.org/downloads/)
* Pygame width the command `pip install pygame`

Launch the game with:\
`main.py`

Launch the editor mode with::\
`concepetor.py`


---
## Authors

| <a href="https://github.com/MathysFernandez"> <img src="https://avatars.githubusercontent.com/u/90396790?s=96&v=4?width=800" width="64" height="64"> </a> | **Name :** _Fernandez Mathys_ <br> **GitLab :** [mon profil](https://github.com/MathysFernandez) |
|:----------------------------------------------------------------------------------------------------------------------------------:|:----------------------------------------------------------------------------------------------------:|

| <a href="https://gitlab.univ-lr.fr/tsoilihi"> <img src="https://gitlab.univ-lr.fr/uploads/-/system/user/avatar/2486/avatar.png?width=800" width="64" height="64"> </a> | **Nom :** _Soilihi Timeo_ <br> **GitLab :** [mon profil](https://gitlab.univ-lr.fr/tsoilihi) |
|:----------------------------------------------------------------------------------------------------------------------------------:|:----------------------------------------------------------------------------------------------------:|

| <a href="https://gitlab.univ-lr.fr/rlamou01"> <img src="https://gitlab.univ-lr.fr/uploads/-/system/user/avatar/3019/avatar.png?width=800" width="64" height="64"> </a> | **Nom :** _Lamoureux Robin_ <br> **GitLab :** [mon profil](https://gitlab.univ-lr.fr/rlamou01) |
|:----------------------------------------------------------------------------------------------------------------------------------:|:----------------------------------------------------------------------------------------------------:|

| <a href="https://gitlab.univ-lr.fr/tpinet"> <img src="https://gitlab.univ-lr.fr/uploads/-/system/user/avatar/3021/avatar.png?width=800" width="64" height="64"> </a> | **Nom :** _Pinet Theo_ <br> **GitLab :** [mon profil](https://gitlab.univ-lr.fr/tpinet) |
|:----------------------------------------------------------------------------------------------------------------------------------:|:----------------------------------------------------------------------------------------------------:|



---
## Pour plus d'information
Aller sur la page [Home](https://github.com/MathysFernandez/GameProject/wiki) de notre projet
