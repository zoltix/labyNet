import socket
import sys
import select

hote = "localhost"
port = 12800

connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_avec_serveur.connect((hote, port))
print("Connexion établie avec le serveur sur le port {}".format(port))

msg_a_envoyer = b""
while msg_a_envoyer != b"fin":
    msg_a_envoyer = input("> ")
    # Peut planter si vous tapez des caractères spéciaux
    msg_a_envoyer = msg_a_envoyer.encode()
    # On envoie le message
    connexion_avec_serveur.send(msg_a_envoyer)
    msg_recu = connexion_avec_serveur.recv(1024)
    print(msg_recu.decode()) # Là encore, peut planter s'il y a des accents
    socket_list = [connexion_avec_serveur]
    
    try:
        ready_to_read,ready_to_write,in_error = select.select(socket_list , [], [], 0.05)
    except select.error:
        pass
    for sock in ready_to_read:
        msg_recu = sock.recv(1024)


print("Fermeture de la connexion")
connexion_avec_serveur.close()