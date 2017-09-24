
# -*-coding:Utf-8 -*
"""Module qui est le serveur de mon application"""
import socket
import select

class Server:
    """"Class server """
    def __init__(self):
        self.hote = ''
        self.port = 12800
        self.clients_connecte = []
        self.connexion_principale = socket.socket()
    def bind(self):
        """attache le socket pour la connexion"""
        self.connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connexion_principale.bind((self.hote, self.port))
        self.connexion_principale.listen(5)
        print("Le serveur écoute à présent sur le port {}".format(self.port))
        self.clients_connecte.append(self.connexion_principale)
    def broacastMessage(self,message):
        for sock in self.clients_connecte: #list toutes les connections
            if sock != self.connexion_principale: #and sock != lui-même pour éviter un echo
                try:

                    sock.send(("Tout le monde me reçois").encode())
                except Exception as e :
                     print(e)




    def start(self):
        """Démarre le serveur"""
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
            #clients_connecte = []
            try:
                connexions, _wlist, _xlist = select.select(self.clients_connecte, [], [], 0.05)
            except select.error:
                pass
            for sock in connexions:
                # new connection request received
                if sock == self.connexion_principale:
                    sockfd, addr = self.connexion_principale.accept()
                    self.clients_connecte.append(sockfd)
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
                        self.broacastMessage("auie")
                    except socket.error as err:
                        #perte de connexion
                        sock.close()
                        self.clients_connecte.remove(sock)
                        print(err)


        print("Fermeture des connexions")
        for client in self.clients_connecte:
            client.close()

        self.connexion_principale.close()

if __name__ == '__main__':
    server = Server()
    server.bind()
    server.start()  