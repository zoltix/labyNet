# -*-coding:Utf-8 -*
u"""Module qui est le serveur de mon application"""
import socket
import sys
import threading

host = '127.0.0.1'
port = 46000

class ThreadReception(threading.Thread):
    """objet thread gérant la réception des messages"""
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.connexion = conn	     # réf. du socket de connexion
        self.terminated = False
    def stop(self):
        """fin de la thread """
        self.terminated = True
    def run(self):
        while not self.terminated:
            message_recu = self.connexion.recv(1024).decode("Utf8")
            print(message_recu )
            if not message_recu or message_recu.upper() == "FIN":
                break
            # Le thread <réception> se termine ici.
            # On force la fermeture du thread <émission> :
        print("Client arrêté. Connexion interrompue.")
        self.connexion.close()
        self.stop()

class ThreadEmission(threading.Thread):
    """objet thread gérant l'émission des messages"""
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.connexion = conn	     # réf. du socket de connexion
        self.terminated = False
    def stop(self):
        """fin de la thread """
        self.terminated = True
    def run(self):
        while not self.terminated:
            message_emis = input()
            self.connexion.send(message_emis.encode("Utf8"))
            if message_emis.upper() == "FIN":
                self.stop()
                break


# Programme principal - Établissement de la connexion :
connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    connexion.connect((host, port))
except socket.error:
    print("La connexion a échoué.")
    sys.exit()
print("Connexion établie avec le serveur.")

# Dialogue avec le serveur : on lance deux threads pour gérer
# indépendamment l'émission et la réception des messages :
th_E = ThreadEmission(connexion)
th_R = ThreadReception(connexion)
th_E.start()
th_R.start()

