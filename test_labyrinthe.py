# -*-coding:Utf-8 -*
"""
    module de test pour la classe labyrinthe
 """
import unittest
from carte import Carte
from labyrinthe import Labyrinthe

class TestCarte(unittest.TestCase):
    """proceédure de test """
    def setUp(self):
        self.grille = 'OOOOOOOOOO\nO O    O O\nO . OO   O\nO O O   XO\nO OOOO O.O\nO O O    U\nO OOOOOO.O\nO O      O\nO O OOOOOO\nO . O    O\nOOOOOOOOOO '
        self.carte = Carte('test', self.grille)
        #simulation d'une grille pour instancier un carte

    def test_obtenir_STATUS_Mouvement_0(self):
        """Testing code de retour"""
        #jeux = Labyrinthe(self.carte)
        self.assertEqual(Labyrinthe._STATUS_Mouvement.get(0), 'Bientôt arrivé Courage')

    def test_obtenir_STATUS_Mouvement_1(self):
        """Testing code de retour"""
        #jeux = Labyrinthe(self.carte)
        self.assertEqual(Labyrinthe._STATUS_Mouvement.get(1), 'Vous ne pouvez pas aller là bas')
    
    def test_obtenir_STATUS_Mouvement_2(self):
        """Testing code de retour"""
        #jeux = Labyrinthe(self.carte)
        self.assertEqual(Labyrinthe._STATUS_Mouvement.get(2), 'Félicitations ! Vous avez gagné !')

    def test_ajout_robot(self):
        """test d'ajout d'un robot"""
        jeux = Labyrinthe(self.carte)
        # Check not thrown une exception
        jeux.ajouter_robot("X", "joueur", "thread_name")
        