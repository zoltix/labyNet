# -*-coding:Utf-8 -*
"""
         Module pour parmettre de partager des valeur entre les thread
         avec l'utilisation des setter et getter
"""
class ParamThread:
    """ class pour partager les paramètre entre les """
    def __init__(self, thread_name):
        self.set_thread_name(thread_name)
        self.terminated = False
        self.on_peux_jouper = False
        #self.set_dernier_joueur("")
    @classmethod
    def construct_by_name_thread(cls, thread_name):
        """pour construire la class avec le nom de la thread"""
        return cls(thread_name)
    def get_thread_name(self):
        """obtenir la valeur du nom de la thread"""
        return self.__thread_name
    def set_thread_name(self, thread_name):
        """changer la valeur de la thread(seulement a l'initisaltion de la thread)"""
        self.__thread_name = thread_name
    threadName = property(get_thread_name, set_thread_name)
