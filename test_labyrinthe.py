import unittest
from carte import Carte

class labyrinthe(unittest.TestCase):
    """proceédure de test """
    def setUp(self):
        self.grille = 'OOOOOOOOOO\nO O    O O\nO . OO   O\nO O O   XO\nO OOOO O.O\nO O O    U\nO OOOOOO.O\nO O      O\nO O OOOOOO\nO . O    O\nOOOOOOOOOO '
    
    def test_obtenir_position(self):
        carte =Carte('test', self.grille)
        x, y = carte.robot_positiont_depart()
        self.assertEqual(x, 8)
        self.assertEqual(y, 3)

    