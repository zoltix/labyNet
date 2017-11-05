# -*-coding:Utf-8 -*
"""Ce fichier contient le code du Robot.
   comme sa position et ses attributs
   Pour la surcharge j'ai préféré utiliser @classmethod
"""
from carte import Carte
class  Robot:
    """
        caractèristique du Robot
    """
    def __init__(self, position_x, position_y, symbole, name, thread_name):
        self.name = name #ne pas oublier de le mettre dans le constructeurS
        self.thread_name_r = thread_name # nom de la thead
        self.position_x = position_x
        self.position_y = position_y
        self.symbole = symbole
        self.prev_position_x = position_x #mémorise la précédente position
        self.prev_position_y = position_y #mémorise la précédente position
        self.prev_symbole = " "
        self.index = 0

    @classmethod
    def construct_by_carte(cls, carte, symbole, name, thread_name):
        """Constucteur avec surcharge """
        assert isinstance(carte, Carte)# astuce pour ide---pff longue recherche
        robot_x, robot_y = carte.robot_positiont_depart()
        return cls(robot_x, robot_y, symbole, name, thread_name)

    @classmethod
    def construct_by_position(cls, position_x, position_y, symbole, name, thread_name):
        """Constucteur avec surcharge """
        return cls(position_x, position_y, symbole, name, thread_name)
