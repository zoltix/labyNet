# -*-coding:Utf-8 -*
"""
    module de test pour la classe protocole
 """
import unittest
import socket
from client import ThreadEmission
from paramThread import ParamThread


class ProtocoleTest(unittest.TestCase):
    """proceédure de test """
    def setUp(self):
        self.client_name = ParamThread("unknow")
    def test_client_cardinalite_nord(self):
        """ Test la convesion des cardinalité"""
        connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        th_e = ThreadEmission(connexion, self.client_name)
        x_pos, y_pos = th_e.convert_cardinalite("N")
        result = [x_pos, y_pos]
        nord = [-1, 0]
        self.assertListEqual(nord, result)
        connexion.close()
    def test_client_cardinalite_est(self):
        """ Test la convesion des cardinalité"""
        connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        th_e = ThreadEmission(connexion, self.client_name)
        x_pos, y_pos = th_e.convert_cardinalite("E")
        result = [x_pos, y_pos]
        est = [0, 1]
        self.assertListEqual(est, result)
        connexion.close()
    def test_client_cardinalite_sud(self):
        """ Test la convesion des cardinalité"""
        connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        th_e = ThreadEmission(connexion, self.client_name)
        x_pos, y_pos = th_e.convert_cardinalite("S")
        result = [x_pos, y_pos]
        sud = [1, 0]
        self.assertListEqual(sud, result)
        connexion.close()
    def test_client_cardinalite_ouest(self):
        """ Test la convesion des cardinalité"""
        connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        th_e = ThreadEmission(connexion, self.client_name)
        x_pos, y_pos = th_e.convert_cardinalite("O")
        result = [x_pos, y_pos]
        ouest = [0, -1]
        self.assertListEqual(ouest, result)
        connexion.close()
