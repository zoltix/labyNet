# -*-coding:Utf-8 -*
"""
ce module défin un language de communictation entre les client et le serveur
ce qui permet de faire du chat et donner des ordres dans le labyrinthe.
 """

class Protocole:
    """class qui définit la communictation"""
    def __init__(self):
        pass
    def _chat(self):
        return 'chat'
    def _ordr(self):
        return 'ordr'
    def _info(self):
        return 'info'
    def _help(self):
        return 'help'
    def _quitter(self):
        return 'quitter'
    def _defaut(self):
        return 'defaut'
    def execute(self, message):
        """traitement du message """
        instruction = message[0:5]
        switch_dict = { #equivalent switch en C
            'chat:':self._chat,
            'ordr:':self._ordr,
            'info:':self._info,
            'help:':self._help,
            'fin_:':self._quitter,
            }
        func = switch_dict.get(instruction, self._defaut) # avec valeur par defaut
        ret = func()
        return ret

# t_test = Protocole()
# t_test.execute("chat:auie")
