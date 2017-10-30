# -*-coding:Utf-8 -*
"""
    module de test pour la classe labyrinthe
 """
import unittest
from carte import Carte

class Labyrinthe(unittest.TestCase):
    """proceédure de test """
    def setUp(self):
        #simulation d'une grille pour instancier un carte
        self.grille = 'OOOOOOOOOO\nO O    O O\nO . OO   O\nO O O   XO\nO OOOO O.O\nO O O    U\nO OOOOOO.O\nO O      O\nO O OOOOOO\nO . O    O\nOOOOOOOOOO '

    def test_obtenir_position(self):
        """Testing mouvement de carte"""
        carte = Carte('test', self.grille)
        x_pos, y_pos = carte.robot_positiont_depart()
        self.assertEqual(x_pos, 8)
        self.assertEqual(y_pos, 3)

    
