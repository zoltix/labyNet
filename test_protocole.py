# -*-coding:Utf-8 -*
"""
    module de test pour la classe protocole
 """
import unittest
from protocole import Protocole

class ProtocoleTest(unittest.TestCase):
    """proceédure de test """
    def setUp(self):
        pass


    def test_protocole_execute_chat(self):
        """Test du protocole de communictaion chat"""
        proto = Protocole()
        self.assertEqual(proto.execute("chat:testChar"), "chat")

    def test_protocole_execute_ordr(self):
        """Test du protocole de communictaion ordr"""
        proto = Protocole()
        self.assertEqual(proto.execute("ordr:testChar"), "ordr")

    def test_protocole_execute_info(self):
        """Test du protocole de communictaion info"""
        proto = Protocole()
        self.assertEqual(proto.execute("info:testChar"), "info")

    def test_protocole_execute_help(self):
        """Test du protocole de communictaion info"""
        proto = Protocole()
        self.assertEqual(proto.execute("help:testChar"), "help")

    def test_protocole_execute_fin(self):
        """Test du protocole de communictaion info"""
        proto = Protocole()
        self.assertEqual(proto.execute("fin_:testChar"), "quitter")
