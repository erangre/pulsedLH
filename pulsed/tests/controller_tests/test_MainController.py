# -*- coding: utf8 -*-

import os
import gc
import shutil
import numpy as np
from mock import MagicMock
from epics import caput, caget

from ..utility import QtTest

from qtpy import QtCore, QtWidgets
from qtpy.QtTest import QTest

from ...controller.MainController import MainController
from ...controller.MainController import MAIN_STATUS_OFF, MAIN_STATUS_ON
from ...controller.epics_config import pulse_PVs, general_PVs, pulse_values, general_values

unittest_data_path = os.path.join(os.path.dirname(__file__), '../data')


class MainControllerTest(QtTest):
    def setUp(self):
        self.controller = MainController()

    def tearDown(self):
        del self.controller
        gc.collect()

    def test_status_shows_correct_value_on_startup(self):
        self.assertEqual(self.controller.widget.main_status.text(), MAIN_STATUS_OFF)

        caput(general_PVs['laser_shutter_control'], general_values['laser_shutter_blocking'], wait=True)
        caput(pulse_PVs['BNC'], pulse_values['BNC_RUNNING'], wait=True)

        self.controller.update_main_status()
        self.assertEqual(self.controller.widget.main_status.text(), MAIN_STATUS_ON)
        caput(pulse_PVs['BNC'], pulse_values['BNC_STOPPED'], wait=True)
        caput(general_PVs['laser_shutter_control'], general_values['laser_shutter_clear'], wait=True)

