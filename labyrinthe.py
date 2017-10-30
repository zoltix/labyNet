# -*-coding:Utf-8 -*
"""
         Ce fichier contient le code principal du jeu...
"""
import os
import time
import sys
import pickle
import re
from carte import Carte
from obstacle import Obstacle
from robot import Robot

class PrecentePosition:
    """Memoriser la précédente position"""
    def __init__(self, pre_obstacle):
        self.pre_obstacle = pre_obstacle

class Labyrinthe:
    """Ce module contient la classe Jeux et mouvement."""
    clear = lambda: os.system('cls') #clear console peut être creer une classe outil
    #Ce sont les différents status après le mouvement du robot pour le ruturn
    #de la méthode _move
    _STATUS_Mouvement = {0:'Bientôt arrivé Courage',\
                         1:'Vous ne pouvez pas aller là bas',\
                         2:'Félicitations ! Vous avez gagné !',\
                         3:'A Bientôt, la partie a été savegardé pour plus tard',\
                         4:'Ce n\'est pas la bonne valeur',\
                         5:'(N) déplacer vers le nord\n'\
                            '(E) déplacer vers l''est\n'\
                            '(S) déplacer vers le sud\n'\
                            '(O) déplacer vers l\'ouest\n'\
                            '(Q) sauvegarder et quitter\n'\
                            '*(1-10)(N|E|S|O) plusieurs steps \n ex: (5N) bouge 5 fois vers le nord'}

    def __init__(self, carte):
        """Avec un robot en stand alone"""
        assert isinstance(carte, Carte)# astuce pour ide pour intellisence---pff longue recherche
        self.carte = carte
        self._chemin = os.path.join("cartes", (self.carte.nom +"pre"))
        self.robots = {}
        #self.robots[joueur] = Robot.construct_by_position(self.carte.coord_debut_x, self.carte.coord_debut_y, 'X')
        #attention pour chargement après sauvegarde
        #self.robot = Robot.construct_by_position(self.carte.coord_debut_x, self.carte.coord_debut_y)
        #self._position_robot_x, self._position_robot_y = \
        #   self.carte.coord_debut_x, self.carte.coord_debut_y
        self.precedent_position = PrecentePosition(" ")
        self.dernier_joueur = ""

    #@classmethod
    #def 
    def ajouter_robot(self, symbole, joueur, thread_name):
        """ Ajourter un robot """
        x, y = self.carte.robot_random_position(symbole) #make a random posisition
        self.robots[joueur] = Robot.construct_by_position(x, y, symbole, thread_name)
    def enlever_robot(self, joueur):
        """"Remove robot"""
        self.carte.grille[self.robots[joueur].position_y][self.robots[joueur].position_x] = ' '
        self.robots.pop(joueur)
    
    def porte_en_mur(self, step_x, step_y, joueur):
        """"transforme porte en mur"""
        #check if porte
        if self.carte.grille[self.robots[joueur].position_y + step_y][self.robots[joueur].position_x + step_x] \
                == Obstacle.collection_obstacle.get(".").symbole:
            self.carte.grille[self.robots[joueur].position_y + step_y][self.robots[joueur].position_x + step_x] \
                                    = Obstacle.collection_obstacle.get("O").symbole

    def mur_en_porte(self, step_x, step_y, joueur):
        """"transforme mur en porte """
        #check if mur
        if self.carte.grille[self.robots[joueur].position_y + step_y][self.robots[joueur].position_x + step_x] \
                    == Obstacle.collection_obstacle.get("O").symbole:
            self.carte.grille[self.robots[joueur].position_y + step_y][self.robots[joueur].position_x + step_x] \
                                    = Obstacle.collection_obstacle.get(".").symbole


    def move(self, step_x, step_y, joueur):
        """ to expose the methode mouvement (pour conserver le code d
        origine)
        """
        return self._move(step_x, step_y, joueur)

    def _move(self, step_x, step_y, joueur):
        """ mouvement du robot """
        try:
            if len(self.carte.grille) > ( self.robots[joueur].position_y + step_y) \
            and (self.robots[joueur].position_y + step_y) >= 0:
                if len(self.carte.grille[self.robots[joueur].position_y + step_y]) >\
                (self.robots[joueur].position_x + step_x) \
                and (self.robots[joueur].position_x + step_x) >= 0:
                    if Obstacle.collection_obstacle.get( \
                        self.carte.grille[self.robots[joueur].position_y+ step_y][self.robots[joueur].position_x + step_x]).fin:
                        os.remove(self._chemin)
                        return 2 #on retourne  c'est fini voir _STATUS_Mouvement
                        #delete fichier de sauvegarde
                    else:
                        pass
                    if  not Obstacle.collection_obstacle.get(\
                             self.carte.grille[self.robots[joueur].position_y + step_y][self.robots[joueur].position_x + step_x]).bloquant:
                        # restauration du précédent symbole
                        self.carte.grille[self.robots[joueur].position_y][self.robots[joueur].position_x] \
                                   = self.robots[joueur].prev_symbole
                        # sauvegarde du symbole qui va être écrasé par le robot (X)
                        self.robots[joueur].prev_symbole \
                                     = self.carte.grille[self.robots[joueur].position_y + step_y][self.robots[joueur].position_x + step_x]
                        #mettre le robot a sa nouvelle place avec le symbole dans la collection
                        self.carte.grille[self.robots[joueur].position_y + step_y][self.robots[joueur].position_x + step_x] \
                                    = self.robots[joueur].symbole #Obstacle.collection_obstacle['X'].symbole 
                        #self.carte.coord_debut_x, self.carte.coord_debut_y  \
                        #             = self.robots[joueur].position_x + step_x, self.robots[joueur].position_y + step_y
                        self.robots[joueur].position_x, self.robots[joueur].position_y  \
                                    = self.robots[joueur].position_x + step_x, self.robots[joueur].position_y + step_y
                        #self.carte.enregistre_partie()
                        self.enregistrer_labyrinthe()
                        return 0 # on retourne on continue voir _STATUS_Mouvement
                    else:
                        return 1 #on retourne on continue voir _STATUS_Mouvement
                else:
                    return 1 #on retourne on continue voir _STATUS_Mouvement
            else:
                return 1 #on retourne on continue voir _STATUS_Mouvement
        except Exception:
            e = sys.exc_info()[0]
            print("aie aie encore un insecte électrocuté\n{}".format(e))

    def enregistrer_labyrinthe(self):
        """Enregistrer le status du labyrinthe"""
        with open(self._chemin, 'wb') as fichier:
            mon_pickler = pickle.Pickler(fichier)
            mon_pickler.dump(self)

    def restaurer_labyrinthe(self):
        """Restaurer le status du labyrinthe"""
        with open(self._chemin, 'rb') as fichier:
            mon_depickler = pickle.Unpickler(fichier)
            # Lecture des objets contenus dans le fichier...
            ret = mon_depickler.load()
            return ret

    
