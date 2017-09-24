# -*-coding:Utf-8 -*
"""
         Module pour définir les Obstacles
         Un seul fichier mais peux être splitté si la complexité l'exige.
"""
class Mur():
    "Class définition du Mur"
    name = 'Mur'
    symbole = 'o'
    bloquant = True
    fin = False
    description = 'ne peut être traversé'

class Porte():
    "Class définition du Porte"
    name = 'Porte'
    symbole = '.'
    bloquant = False
    fin = False
    description = 'porte sans arrêt'

class Sortie():
    "Class définition du Sortie"
    name = 'Sortie'
    symbole = 'U'
    bloquant = False
    fin = True
    description = 'Sortie du labyrinthe'

class Rien():
    "Class définition du Rien"
    name = 'Rien'
    symbole = ' '
    bloquant = False
    fin = False
    description = 'Sortie du labyrinthe'

class Robot():
    "Class définition du Robot"
    name = 'Robot'
    symbole = 'X'
    bloquant = True
    fin = False
    description = 'Robot Himself'

class Obstacle(object):
    "Class genérique Obstacle juste a but d'apprentissage"
    collection_obstacle = {"O":Mur(), ".":Porte(), "U":Sortie(), " ":Rien(), "X":Robot()}
