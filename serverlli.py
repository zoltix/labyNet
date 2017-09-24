import socket
import select


class Server:
    """"Class server """
    def __init__(self):
        print("inti")

    def start(self):
        """Démarre le serveur"""
        hote = ''
        port = 12800
        clients_connectes = []
        connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connexion_principale.bind((hote, port))
        connexion_principale.listen(5)
        clients_a_lire = []
        print("Le serveur écoute à présent sur le port {}".format(port))
        clients_a_lire.append(connexion_principale)

        serveur_lance = True

        while serveur_lance:
            # On va vérifier que de nouveaux clients ne demandent pas à se connecter
            # Pour cela, on écoute la connexion_principale en lecture
            # On attend maximum 50ms
            
            #connexions_demandees, wlist, xlist = select.select([connexion_principale],
            #    [], [], 0.05)
            
            #for connexion in connexions_demandees:
            #    connexion_avec_client, infos_connexion = connexion.accept()
                # On ajoute le socket connecté à la liste des clients
            #    clients_connectes.append(connexion_avec_client)
            
            # Maintenant, on écoute la liste des clients connectés
            # Les clients renvoyés par select sont ceux devant être lus (recv)
            # On attend là encore 50ms maximum
            # On enferme l'appel à select.select dans un bloc try
            # En effet, si la liste de clients connectés est vide, une exception
            # Peut être levée
            #clients_a_lire = []
            try:
                connexions, wlist, xlist = select.select(clients_a_lire,
                        [], [], 0.05)
            except select.error:
                pass
            for sock in connexions:
                # new connection request received
                if sock == connexion_principale:
                    sockfd, addr = connexion_principale.accept()
                    clients_a_lire.append(sockfd)
                    print("New connected client (%s, %s)" % addr)
                else:
                    try:
                        # On parcourt la liste des clients à lire
                        # Client est de type socket
                        msg_recu = sock.recv(1024)
                        # Peut planter si le message contient des caractères spéciaux
                        msg_recu = msg_recu.decode()
                        print("Reçu {}".format(msg_recu))
                        sock.send(b"5 / 5")
                        if msg_recu == "fin":
                            serveur_lance = False
                    except socket.error as err:
                        #perte de connexion
                        clients_a_lire.remove(sock)
                        print(err)


        print("Fermeture des connexions")
        for client in clients_connectes:
            client.close()

        connexion_principale.close()

if __name__ == '__main__':
    server = Server()
    server.start()  