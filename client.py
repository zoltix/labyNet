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
    def __init__(self, conn, CLIEN_NANE):
        threading.Thread.__init__(self)
        self.client_name = CLIEN_NANE
        self.connexion = conn	     # réf. du socket de connexion
        self.terminated = False
    def stop(self):
        """fin de la thread """
        self.terminated = True
    def run(self):
        while not self.terminated:
            message_recu = self.connexion.recv(1024).decode("Utf8")
            print(self.client_name.get_thread_name())
            print(message_recu)
            if not message_recu or message_recu.upper() == "FIN":
                break
            if message_recu.upper().startswith("WHOIM:"):
                self.client_name.set_thread_name(message_recu)
            # Le thread <réception> se termine ici.
            # On force la fermeture du thread <émission> :
        print("Client arrêté. Connexion interrompue.")
        self.connexion.close()
        self.stop()

class ThreadEmission(threading.Thread):
    """objet thread gérant l'émission des messages"""
    clear = lambda: os.system('cls') #clear console peut être creer une classe outil
    def __init__(self, conn, CLIEN_NANE):
        self.client_name = CLIEN_NANE
        threading.Thread.__init__(self)
        self.connexion = conn	     # réf. du socket de connexion
        self.terminated = False
    def stop(self):
        """fin de la thread """
        self.terminated = True

    def _help(self):
        """Afficher l'aide"""
        #self.carte.afficher_carte()
        return 5

    def _nord(self):
        message_emis = "ordr:Client,0,-1"
        return message_emis

    def _est(self):
        message_emis = "ordr:Client,1,0"
        return message_emis

    def _sud(self):
        message_emis = "ordr:Client,0,1"
        return message_emis

    def _ouest(self):
        message_emis = "ordr:Client,-1,0"
        return message_emis

    def _quitter(self):
        return "FIN" #on retourne le code voir _STATUS_Mouvement

    def _defaut(self):
        return "UNKNOW"

    def _whoim(self):
        self.connexion.send("WHOIM".encode("Utf8"))
        return "whoim"


    def run(self):
        self._whoim()

        while not self.terminated:
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
            switch_dict = { #equivalent switch en C
                'N':self._nord,
                'E':self._est,
                'S':self._sud,
                'O':self._ouest,
                'Q':self._quitter,
                'H':self._help
            }
            func = switch_dict.get(_commande, self._defaut) # avec valeur par defaut
            message_emis = func()
            #message_emis = input()
            self.connexion.send(func().encode("Utf8"))
            if message_emis.upper() == "FIN":
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
    th_e.start()
    th_r.start()


if __name__ == '__main__':
    main()
