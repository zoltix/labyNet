# -*-coding:Utf-8 -*
"""
Serveur pour les client du labyrinthe
"""
import socket
import sys
import threading

HOST = '127.0.01'
PORT = 46000

class ThreadClient(threading.Thread):
    '''dérivation d'un objet thread pour gérer la connexion avec un client'''
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.connexion = conn

    def run(self):
      # Dialogue avec le client :
        nom = self.getName()	    # Chaque thread possède un nom
        try:
            while 1:
                msgClient = self.connexion.recv(1024).decode("Utf8")
                if not msgClient or msgClient.upper() == "FIN":
                    break
                message = "%s> %s" % (nom, msgClient)
                print(message)
                # Faire suivre le message à tous les autres clients :
                for cle in conn_client:
                    if cle != nom:	  # ne pas le renvoyer à l'émetteur
                        conn_client[cle].send(message.encode("Utf8"))
            # Fermeture de la connexion :
            self.connexion.close()	  # couper la connexion côté serveur
            del conn_client[nom]	# supprimer son entrée dans le dictionnaire
            print("Client %s déconnecté." % nom)
        except ConnectionError as error_connection:
            print('Error conncetion: Le client a été retiré {}'.format(error_connection))
            del conn_client[nom]	# supprimer son entrée dans le dictionnaire
      # Le thread se termine ici

# Initialisation du serveur - Mise en place du socket :
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
  mySocket.bind((HOST, PORT))
except socket.error:
  print("La liaison du socket à l'adresse choisie a échoué.")
  sys.exit()
print("Serveur prêt, en attente de requêtes ...")
mySocket.listen(5)
 
# Attente et prise en charge des connexions demandées par les clients :
conn_client = {}	# dictionnaire des connexions clients
while 1:
  connexion, adresse = mySocket.accept()
  # Créer un nouvel objet thread pour gérer la connexion :
  th = ThreadClient(connexion)
  th.start()
  # Mémoriser la connexion dans le dictionnaire :
  it = th.getName()	  # identifiant du thread
  conn_client[it] = connexion
  print("Client %s connecté, adresse IP %s, port %s." %\
     (it, adresse[0], adresse[1]))
  # Dialogue avec le client :
  msg ="Vous êtes connecté. Envoyez vos messages."
  connexion.send(msg.encode("Utf8"))