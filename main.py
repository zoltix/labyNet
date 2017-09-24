# -*-coding:Utf-8 -*
"""
C'est le démarage de l'application et l'initialisation
ex: py main.py
"""
import os
import re
from carte import Carte
from labyrinthe import Labyrinthe
#from roboc import Robot
clear = lambda: os.system('cls')
def main():
    """ Voici le début do mon programe pour jouer au labyrintheS"""
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
    jeux.start()

if __name__ == '__main__':
    main()
