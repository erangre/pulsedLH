# -*- coding: utf8 -*-

import os
import gc
import shutil
import numpy as np
from mock import MagicMock

from ..utility import QtTest

from qtpy import QtCore, QtWidgets
from qtpy.QtTest import QTest

from ...controller.MainController import MainController
from ...controller.MainController import MAIN_STATUS_OFF

unittest_data_path = os.path.join(os.path.dirname(__file__), '../data')


class MainControllerTest(QtTest):
    def setUp(self):
        self.controller = MainController()

    def tearDown(self):
        del self.controller
        gc.collect()

    def test_status_shows_off_on_startup(self):
        self.assertEqual(self.controller.widget.main_status.text(), MAIN_STATUS_OFF)
