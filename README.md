# labyNet
labyrinthe Client Server Activité_partie 4 pour "Apprenez à programmer en Python" 
Ceci est une version qui fonctionne avec beaucoup de buggs
Le code est posté sur https://github.com/zoltix/labyNet
Testé sur: windows 10 build 1709 et Ubuntu(16.04)
Version de Python 3.6.2
	sur ubuntu installattion 16,04:
		sudo add-apt-repository ppa:jonathonf/python-3.6
		sudo apt-get update
		sudo apt-get install python3.6	
1) Lancer le serveur
	python serever.py
		Choisir la carte(prison ou facile)
2) Lancer autant de client que vous le voulez
	python client.py
   		une fois les clients démarés, Il faudra taper sur C pour commencer la partie.

Il y une vidéo comme démo "demo_linux.mkv"

Bug:
	Perte de connexion. 
	Gestion de sortie des clients
	Arrêter le serveur
