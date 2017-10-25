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
    def __init__(self, position_x, position_y, symbole):
        self.name = 'default' #ne pas oublier de le mettre dans le constructeurS
        self.position_x = position_x
        self.position_y = position_y
        self.symbole = symbole

    @classmethod
    def construct_by_carte(cls, carte,symbole):
        """Constucteur avec surcharge """
        assert isinstance(carte, Carte)# astuce pour ide---pff longue recherche
        robot_x, robot_y = carte.robot_positiont_depart()
        return cls(robot_x, robot_y, symbole)

    @classmethod
    def construct_by_position(cls, position_x, position_y, symbole):
        """Constucteur avec surcharge """
        return cls(position_x, position_y, symbole)

