# -*- coding: utf8 -*-

import unittest
from qtpy import QtWidgets, QtCore
from qtpy.QtTest import QTest
import os

unittest_data_path = os.path.join(os.path.dirname(__file__), 'data')


class QtTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QtWidgets.QApplication.instance()
        if cls.app is None:
            cls.app = QtWidgets.QApplication([])


def delete_if_exists(data_path):
    if os.path.exists(data_path):
        os.remove(data_path)
