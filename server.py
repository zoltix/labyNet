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
from paramThread import ParamThread

clear = lambda: os.system('cls')
HOST = '127.0.01'
PORT = 46000
conn_client = {}	# dictionnaire des connexions clients

class ThreadClient(threading.Thread):
    '''dérivation d'un objet thread pour gérer la connexion avec un client'''
    def __init__(self, conn, jeux):
        threading.Thread.__init__(self)
        self.connexion = conn
        self.jeux = jeux
        self.joueur = ""
    def broadcast(self, message, soi_meme, client_name):
        """permet d'envoyer un messaga au client
           message = message 
           soi_même similaire a un echo
           client_name  pour ecoho
        """
        try:
            for cle in conn_client:
                if cle != client_name or soi_meme:  # ne pas le renvoyer à l'émetteur
                    message_a_envoyer = message #+"\n"+self.jeux.carte.afficher_carte()
                    conn_client[cle].send(message_a_envoyer.encode("Utf8"))

        except ConnectionError as error_connection:
            print('Error conncetion: Le client a été retiré {}'.format(error_connection))
            #self.jeux.robots.pop(self.joueur)  pas correcte 
            del conn_client[client_name]	# supprimer son entrée dans le dictionnaire
    def send_message(self, message, client_name):
        """envoie un message uniquement a un clien"""
        #message = message +"\n"+self.carte.afficher_carte()
        conn_client[client_name].send(message.encode("Utf8"))
    
    def _whoim(self):
        return "whoim"
    def run(self):
      # Dialogue avec le client :
        thread_name = self.getName()	    # Chaque thread possède un thread_name
        try:
            while 1:
                #reception du message
                msg_client = self.connexion.recv(1024).decode("Utf8")
                if not msg_client or msg_client.upper() == "FIN":
                    break
                if msg_client.upper() == "WHOIM":
                    self.send_message(("whoim:"+thread_name), thread_name)
                    self.broadcast(self.jeux.carte.afficher_carte(), True, thread_name)
                if msg_client.startswith("ordr:"):
                    #""" action dans le labyrinthe"""
                    if self.jeux.dernier_joueur == self.joueur:
                        self.send_message("c'est est pas ton tour" , thread_name)
                    else:
                        lst_ordr = msg_client[4:].split(',')
                        if lst_ordr[1] == 'move':
                            self.jeux.move(int(lst_ordr[2]), int(lst_ordr[3]), self.joueur)
                            self.jeux.dernier_joueur = self.joueur
                        if lst_ordr[1] == 'build':
                            if lst_ordr[2] == 'M': 
                                self.jeux.porte_en_mur(int(lst_ordr[3]),int(lst_ordr[4]), self.joueur)
                            if lst_ordr[2] == 'P':
                                self.jeux.mur_en_porte(int(lst_ordr[3]),int(lst_ordr[4]), self.joueur)

                            self.jeux.dernier_joueur = self.joueur
                        #x= lst_ordr[1]
                        #y= lst_ordr[2]
                        self.broadcast(self.jeux.carte.afficher_carte(), True, thread_name)
                else:
                    message = "%s> %s" % (thread_name, msg_client)
                    print(message)
                    # Faire suivre le message à tous les autres clients :
                    #self.broadcast(msg_client, True, thread_name)
            # Fermeture de la connexion :
            self.connexion.close()	  # couper la connexion côté serveur
            self.jeux.enlever_robot(self.joueur)  
            del conn_client[thread_name]	# supprimer son entrée dans le dictionnaire
            print("Client %s déconnecté." % thread_name)
        except ConnectionError as error_connection:
            print('Error conncetion: Le client a été retiré {}'.format(error_connection))
            self.jeux.enlever_robot(self.joueur)  
            del conn_client[thread_name]	# supprimer son entrée dans le dictionnaire
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
    carte.clean_robot()
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
        #attendre de la connexion
        connexion, adresse = mySocket.accept()
        #choix du symbole du symbole du robot
        #jeux.ajouter_robot("P")
        th = ThreadClient(connexion, jeux)
        thread_name = th.getName()	  # identifiant du thread
        if bool(jeux.robots):
            for item in list(jeux.robots):
                print('************* robot ****************')
                print('nom du robot {}'.format(item))
                print('symbole du robot {}'.format(jeux.robots[item].symbole))
                print('thread du robot {}'.format(jeux.robots[item].thread_name_r))
                #test toujours valide 
                if conn_client[jeux.robots[item].thread_name_r].fileno() < 0:
                      jeux.enlever_robot(item)  
                      jeux.ajouter_robot(jeux.robots[item].symbole, item, thread_name)
                else:
                    if len(jeux.robots) < 2:
                        if jeux.robots[item].symbole == "X": 
                            joueur = "joueur2"
                            jeux.ajouter_robot("x", joueur, thread_name)
                        elif jeux.robots[item].symbole == "x":
                            joueur = "joueur1"
                            jeux.ajouter_robot("X", joueur, thread_name)
                    else:
                        pass
        else:
            joueur = "joueur1"
            jeux.ajouter_robot("X", joueur, thread_name)

        # Créer un nouvel objet thread pour gérer la connexion :
        th.joueur = joueur
        th.start()
        # Mémoriser la connexion dans le dictionnaire :
        conn_client[thread_name] = connexion
        print("Client %s connecté, adresse IP %s, port %s." %\
            (thread_name, adresse[0], adresse[1]))
        # Dialogue avec le client :
        msg = "Vous êtes connecté. Envoyez vos messages.\n"
        msg = msg + jeux.carte.afficher_carte()
        #message de bienvenue sur le serveur
        connexion.send(msg.encode("Utf8"))
    
if __name__ == '__main__':
    main()
