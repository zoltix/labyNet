# -*-coding:Utf-8 -*
"""Ce fichier contient le code du container de robot.
    amélioration possible rendre la classe itérable
"""
class Robots:
    """ classe qui contient tous les robots qui sont entrain de jouer """
    def __init__(self):
        self.robots = {}
    def ajouter_robot(self, robot):
        """ ajouter un robot"""
        self.robots[robot.name] = robot
    def enlever_robot(self, robot):
        """ enlever un robot """
        self.robots.pop(robot)
    def get_robot_thread_name(self, thread_name):
        """ obtenir un robot par le nom de la thread"""
        for name, robot in self.robots.items():
            if robot.thread_name_r == thread_name:
                return robot
    def get_robot_name(self, joueur):
        """ obtenir un robot par le nom de la thread"""
        return self.robots[joueur]
