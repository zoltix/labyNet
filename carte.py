# -*-coding:Utf-8 -*
"""Ce module contient la classe Carte."""
import os
class Carte:
    """Objet de transition entre un fichier et un labyrinthe."""
    def __init__(self, nom, chaine):
        self.nom = nom
        self.grille = [[str(x) for x in line] for line in chaine.splitlines()] #list 2 dimensions.
        self.coord_debut_x, self.coord_debut_y = self.robot_positiont_depart()

    @classmethod
    def carte_from_file(cls, chemin, nom_carte):
        """ initialise la classe a partir d'un fichier """
        with open(chemin, "r") as fichier:
            contenu = fichier.read()
        return cls(nom_carte, contenu)

    def __repr__(self):
        "affiche la carte par défaut"
        return "<Carte {}>".format(self.nom)

    def enregistre_partie(self):
        "sauvegarde le fichier sur disque"
        chemin = os.path.join("cartes", (self.nom +"pre"))
        with open(chemin, "w") as fichier:
            fichier.write('\n'.join(map(''.join, self.grille)))

    def afficher_carte(self):
        """ Afficher la carte en cours"""
        print('\n'.join(map(''.join, self.grille))) #si liste a deux dimension
        #print('\n'.join(''.join(s) for s in grille)) #
        #print(*self.grille, sep='\n') # is chaine de caratère

    def robot_positiont_depart(self):
        """ obtenir les cordonnée de départ"""
        for coord_y, line in enumerate(self.grille):
            #print(coord_x)
            coord_x = [pos for pos, char in enumerate(line) if char == 'X']
            if coord_x:
                self.coord_debut_y = coord_y
                self.coord_debut_x = coord_x[0]
                #print("Position du robot au Départ est X {} Y {} ".format(
                #    self.coord_x, self.coord_y))
                break
        return  self.coord_debut_x, self.coord_debut_y
