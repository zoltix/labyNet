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
        if bool(self.robots):
            robot.index = len (self.robots)+1
        else:
            robot.index = 1
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
    def get_robot_index(self, inedex):
        """ obtenir un robot par l'index"""
        for name, robot in self.robots.items():
            if robot.index == inedex:
                return robot
    def next_robot(self, joueur):
        """ le prochain robot a pouvoir jouer"""
        if joueur == "":#option de démarage par défaut
            return self.get_robot_index(1) # et donc il retourne le premier robot
        robot = self.get_robot_name(joueur)
        if robot.index >= len(self.robots):
            robot = self.get_robot_index(1)
        else:
            robot = self.get_robot_index(robot.index+1)
        return robot
