# -*-coding:Utf-8 -*
"""
         Ce fichier contient le code principal du jeu.
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
        assert isinstance(carte, Carte)# astuce pour ide pour intellisence---pff longue recherche
        self.carte = carte
        self._chemin = os.path.join("cartes", (self.carte.nom +"pre"))
        #attention pour chargement après sauvegarde
        self.robot = Robot.construct_by_position(self.carte.coord_debut_x, self.carte.coord_debut_y)
        #self._position_robot_x, self._position_robot_y = \
        #   self.carte.coord_debut_x, self.carte.coord_debut_y
        self.precedent_position = PrecentePosition(" ")

    def _move(self, step_x, step_y):
        """ mouvement du robot """
        try:
            if len(self.carte.grille) > (self.robot.position_y + step_y) \
            and (self.robot.position_y + step_y) >= 0:
                if len(self.carte.grille[self.robot.position_y + step_y]) >\
                (self.robot.position_x + step_x) \
                and (self.robot.position_x + step_x) >= 0:
                    if Obstacle.collection_obstacle.get( \
                        self.carte.grille[self.robot.position_y+ step_y][self.robot.position_x + step_x]).fin:
                        os.remove(self._chemin)
                        return 2 #on retourne  c'est fini voir _STATUS_Mouvement
                        #delete fichier de sauvegarde
                    else:
                        pass
                    if  not Obstacle.collection_obstacle.get(\
                             self.carte.grille[self.robot.position_y + step_y][self.robot.position_x + step_x]).bloquant:
                        # restauration du précédent symbole
                        self.carte.grille[self.robot.position_y][self.robot.position_x] \
                                   = self.precedent_position.pre_obstacle
                        # sauvegarde du symbole qui va être écrasé par le robot (X)
                        self.precedent_position.pre_obstacle \
                                     = self.carte.grille[self.robot.position_y + step_y][self.robot.position_x + step_x]
                        #mettre le robot a sa nouvelle place avec le symbole dans la collection
                        self.carte.grille[self.robot.position_y + step_y][self.robot.position_x + step_x] \
                                    = Obstacle.collection_obstacle['X'].symbole 
                        self.carte.coord_debut_x, self.carte.coord_debut_y  \
                                    = self.robot.position_x + step_x, self.robot.position_y + step_y
                        self.robot.position_x, self.robot.position_y  \
                                    = self.robot.position_x + step_x, self.robot.position_y + step_y
                        #self.carte.enregistre_partie()
                        self.enregistrer_labyrinthe()
                        return 0 # on retourne on continue voir _STATUS_Mouvement
                    else:
                        return 1 #on retourne on continue voir _STATUS_Mouvement
                else:
                    return 1 #on retourne on continue voir _STATUS_Mouvement
            else:
                return 1 #on retourne on continue voir _STATUS_Mouvement
        except:
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

    def _help(self):
        """Afficher l'aide"""
        #self.carte.afficher_carte()
        return 5
    
    def _nord(self):
        return self._move(step_x=0, step_y=-1)

    def _est(self):
        return self._move(step_x=1, step_y=0)

    def _sud(self):
        return self._move(step_x=0, step_y=1)

    def _ouest(self):
        return self._move(step_x=-1, step_y=0)

    def _quitter(self):
        return 3 #on retourne le code voir _STATUS_Mouvement

    def _defaut(self):
        return 4

    def start(self):
        """Debut ou continue la partie"""
        #test = Obstacle.collection_obstacle.get(" ")t
        #xxx = test.bloquant
        #test = Obstacle.collection_obstacle.get("0")
        #xxx = test.bloquant
        self.carte.afficher_carte()
        while True:
            key = ""
            exp = r"^([\d]*)([NESOQH])$"
            reg = re.compile(exp)
            while reg.search(key) is None:
                key = (input("Commade (H)elp:")).upper()
            _nombre_de_pas = reg.match(key).group(1)
            if _nombre_de_pas == '':
                nombre_de_pas = 1
            else:
                nombre_de_pas = int(_nombre_de_pas)
            _commande = reg.match(key).group(2)
            os.system('cls')
            #if key in "NESOQH" and len(key) > 0 and len(key) <= 1:
            switch_dict = { #equivalent switch en C
                'N':self._nord,
                'E':self._est,
                'S':self._sud,
                'O':self._ouest,
                'Q':self._quitter,
                'H':self._help
            }
            func = switch_dict.get(_commande, self._defaut) # avec valeur par defaut
            for x in range(nombre_de_pas):
                #self.clear()
                os.system('cls')
                result = func()
                self.carte.afficher_carte()
                #stope la boucle dans le cas que le mouvement est annulé(mur,...)
                if result >= 1:
                    break # c'est la fin du pas à pas
                #Pour un genre de petite animationS
                if x > 0:
                    time.sleep(0.5)
            print("{}".format(Labyrinthe._STATUS_Mouvement[result]))
            if result == 3 or result == 2:
                break # c'est la fin du jeux
        return
