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
    def __init__(self, position_x, position_y):
        self.position_x = position_x
        self.position_y = position_y

    @classmethod
    def construct_by_carte(cls, carte):
        """Constucteur avec surcharge """
        assert isinstance(carte, Carte)# astuce pour ide---pff longue recherche
        robot_x, robot_y = carte.robot_positiont_depart()
        return cls(robot_x, robot_y)

    @classmethod
    def construct_by_position(cls, position_x, position_y):
        """Constucteur avec surcharge """
        return cls(position_x, position_y)
