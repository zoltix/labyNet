# -*-coding:Utf-8 -*
"""
Serveur pour les client du labyrinthe
 """
import socket
import sys
import threading
import os
import re
from carte import Carte
from labyrinthe import Labyrinthe

clear = lambda: os.system('cls')
HOST = '127.0.01'
PORT = 46000
conn_client = {}	# dictionnaire des connexions clients

class ThreadClient(threading.Thread):
    '''dérivation d'un objet thread pour gérer la connexion avec un client'''
    def __init__(self, conn, carte):
        threading.Thread.__init__(self)
        self.connexion = conn
        self.carte = carte
    def broadcast(self, message, soi_meme, client_name):
        """permet d'envoyer un messaga au client"""
        try:
            for cle in conn_client:
                if cle != client_name or soi_meme:  # ne pas le renvoyer à l'émetteur
                    message = message +"\n"+self.carte.afficher_carte()
                    conn_client[cle].send(message.encode("Utf8"))

        except ConnectionError as error_connection:
            print('Error conncetion: Le client a été retiré {}'.format(error_connection))
            del conn_client[client_name]	# supprimer son entrée dans le dictionnaire
 
    def run(self):
      # Dialogue avec le client :
        nom = self.getName()	    # Chaque thread possède un nom
        try:
            while 1:
                #reception du message
                msg_client = self.connexion.recv(1024).decode("Utf8")
                if not msg_client or msg_client.upper() == "FIN":
                    break
                message = "%s> %s" % (nom, msg_client)
                print(message)
                # Faire suivre le message à tous les autres clients :
                self.broadcast(msg_client, True, nom)
            # Fermeture de la connexion :
            self.connexion.close()	  # couper la connexion côté serveur
            del conn_client[nom]	# supprimer son entrée dans le dictionnaire
            print("Client %s déconnecté." % nom)
        except ConnectionError as error_connection:
            print('Error conncetion: Le client a été retiré {}'.format(error_connection))
            del conn_client[nom]	# supprimer son entrée dans le dictionnaire
      # Le thread se termine ici


def main():
    # Initialisation du serveur - Mise en place du socket :
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        mySocket.bind((HOST, PORT))
    except socket.error:
        print("La liaison du socket à l'adresse choisie a échoué.")
        sys.exit()
    print("Serveur prêt, en attente de requêtes ...")
    mySocket.listen(5)
    
    
    #choisir la carte.
    # On charge les cartes existantes
    clear()
    cartes = []
    for nom_fichier in os.listdir("cartes"):
        if nom_fichier.endswith(".txt"):
            chemin = os.path.join("cartes", nom_fichier)
            nom_carte = nom_fichier[:-3].lower()
            #charger la carte venant d'un fichier
            cartes.append(Carte.carte_from_file(chemin, nom_carte))
    # On affiche les cartes existantes
    print("Labyrinthes existants :")
    for i, carte in enumerate(cartes):
        print("  {} - {}".format(i + 1, carte.nom))
    #on Choisi la carte
    while True:
        resultat = input("Entrez un numéro de labyrinthe pour commencer à jouer : ")
        if resultat.isdigit() == True:
            if  int(resultat) > 0   and int(resultat) <= len(cartes):
                break
    clear()
    #charge la carte séléctionné
    carte = cartes[(int(resultat)-1)]
    jeux = Labyrinthe(carte)
    #si une partie encours/ a été sauvé
    chemin = os.path.join("cartes", (carte.nom +"pre"))
    if os.path.exists(chemin):
        key = ""
        exp = r"^[O]|[N]$"
        reg = re.compile(exp)
        while reg.search(key) is None:
            key = (input("Voulez continer la partie précédente(O/N)")).upper() or 'O'
        if key == 'O':
            clear()
            jeux = jeux.restaurer_labyrinthe()
        #Début du jeux

    # Attente et prise en charge des connexions demandées par les clients :
    while 1:
        connexion, adresse = mySocket.accept()
        # Créer un nouvel objet thread pour gérer la connexion :
        th = ThreadClient(connexion, carte)
        th.start()
        # Mémoriser la connexion dans le dictionnaire :
        it = th.getName()	  # identifiant du thread
        conn_client[it] = connexion
        print("Client %s connecté, adresse IP %s, port %s." %\
            (it, adresse[0], adresse[1]))
        # Dialogue avec le client :
        msg = "Vous êtes connecté. Envoyez vos messages.\n"
        msg = msg + carte.afficher_carte()
        connexion.send(msg.encode("Utf8"))
    
if __name__ == '__main__':
    main()
