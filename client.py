# -*-coding:Utf-8 -*
"""Module qui est le serveur de mon application"""
import socket
import sys
import threading
import re
import os
from paramThread import ParamThread

class ThreadReception(threading.Thread):
    """objet thread gérant la réception des messages"""
    def __init__(self, conn, CLIENT_NANE):
        threading.Thread.__init__(self)
        self.client_name = CLIENT_NANE
        self.connexion = conn	     # réf. du socket de connexion
        #self.terminated = False
    @staticmethod
    def clear():
        """Statique methode pour netoyer l'écran"""
        os.system('cls')
    def stop(self):
        """fin de la thread """
        self.client_name.terminated = True
    def run(self):
        while not self.client_name.terminated:
            message_recu = self.connexion.recv(1024).decode("Utf8")
            ThreadReception.clear()
            print(message_recu)
            print("(H) pour afficher l'aide ou commande pour un déplacement:")
            if not message_recu or message_recu.upper() == "FIN" or message_recu.find(' FIN ') != -1:
                self.client_name.terminated = True
                break
            if message_recu.upper().startswith("WHOIM:"):
                self.client_name.set_thread_name(message_recu[6:])
            # Le thread <réception> se termine ici.
            # On force la fermeture du thread <émission> :
        print("Client arrêté. Connexion interrompue.")
        self.connexion.close()
        self.stop()
        sys.exit(0)

class ThreadEmission(threading.Thread):
    """objet thread gérant l'émission des messages"""
    clear = lambda: os.system('cls') #clear console peut être creer une classe outil
    def __init__(self, conn, CLIEN_NANE):
        self.client_name = CLIEN_NANE
        threading.Thread.__init__(self)
        self.connexion = conn	     # réf. du socket de connexion
        #self.terminated = False
        self.direction =''
        self.commande = ''
    def stop(self):
        """fin de la thread """
        self.client_name.terminated = True

    def _help(self):
        """Afficher l'aide"""
        #self.carte.afficher_carte()
        message_emis = 'help:'
        return message_emis

    def _nord(self):
        step_x, step_y = self.convert_cardinalite('N')
        message_emis = "ordr:{},move,{},{}".format(self.client_name.get_thread_name(), step_y, step_x)
        return message_emis

    def _est(self):
        step_x, step_y = self.convert_cardinalite('E')
        message_emis = "ordr:{},move,{},{}".format(self.client_name.get_thread_name(), step_y, step_x)
        return message_emis

    def _sud(self):
        step_x, step_y = self.convert_cardinalite('S')
        message_emis = "ordr:{},move,{},{}".format(self.client_name.get_thread_name(), step_y, step_x)
        return message_emis

    def _ouest(self):
        step_x, step_y = self.convert_cardinalite('O')
        message_emis = "ordr:{},move,,{},{}".format(self.client_name.get_thread_name(), step_y, step_x)
        return message_emis

    def convert_cardinalite(self, direction):
        """Conver les cardinalité en x et y"""
        if direction == 'N':
            step_x = -1
            step_y = 0
        if direction == 'E':
            step_x = 0
            step_y = 1
        if direction == 'S':
            step_x = 1
            step_y = 0
        if direction == 'O':
            step_x = 0
            step_y = -1
        return  step_x, step_y

    def _murer(self):
        step_x, step_y = self.convert_cardinalite(self.direction)
        message_emis = "ordr:{},build,M,{},{}".format(self.client_name.get_thread_name(), step_y, step_x)
        return message_emis

    def _percer(self):
        step_x, step_y = self.convert_cardinalite(self.direction)
        message_emis = "ordr:{},build,P,{},{}".format(self.client_name.get_thread_name(), step_y , step_x)
        return message_emis

    def _commencer(self):
        message_emis = "ordr:{},C".format(self.client_name.get_thread_name())
        return message_emis


    def _quitter(self):
        return "FIN" #on retourne le code voir _STATUS_Mouvement

    def _defaut(self):
        return "UNKNOW"

    def _whoim(self):
        self.connexion.send("WHOIM".encode("Utf8"))

        return "whoim"


    def run(self):
        #self._whoim()

        while not self.client_name.terminated:
            key = ""
            exp = r"^([CPMNESOQH])([NESO]?)$"
            reg = re.compile(exp)
            while reg.search(key) is None:
                key = (input("Commade (Q)uitter:")).upper()
            _direction = reg.match(key).group(2)
            self.direction = _direction
            _commande = reg.match(key).group(1)
            self.commande = _commande
            switch_dict = { #equivalent switch en C
                'C':self._commencer,
                'N':self._nord,
                'E':self._est,
                'S':self._sud,
                'O':self._ouest,
                'M':self._murer,
                'P':self._percer,
                'Q':self._quitter,
                'H':self._help
            }
            if not self.client_name.terminated:
                func = switch_dict.get(_commande, self._defaut) # avec valeur par defaut
                message_emis = func()
                #message_emis = input()
                self.connexion.send(func().encode("Utf8"))
            if message_emis.upper() == "FIN" or self.client_name.terminated:
                self.stop()
                break

def main():
    """  Programme principal - Établissement de la connexion : """
    host = '127.0.0.1'
    port = 46000
    connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        connexion.connect((host, port))
    except socket.error:
        print("La connexion a échoué.")
        sys.exit()
    print("Connexion établie avec le serveur.")

    # Dialogue avec le serveur : on lance deux threads pour gérer
    # indépendamment l'émission et la réception des messages :
    client_name = ParamThread("unknow")
    th_e = ThreadEmission(connexion, client_name)
    th_r = ThreadReception(connexion, client_name)
    th_r.start()
    th_e.start()
    


if __name__ == '__main__':
    main()
