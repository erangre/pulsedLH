# -*- coding: utf8 -*-

import os
import gc
import time
import shutil
import numpy as np
from mock import MagicMock
from epics import caput, caget

from ..utility import QtTest

from qtpy import QtCore, QtWidgets
from qtpy.QtTest import QTest

from ...controller.MainController import MainController
from ...controller.MainController import MAIN_STATUS_OFF, MAIN_STATUS_ON, LASER_STATUS_NORMAL, LASER_STATUS_PULSED, \
    PIMAX_STATUS_NORMAL, PIMAX_STATUS_PULSED
from ...controller.epics_config import pulse_PVs, general_PVs, pulse_values, general_values, laser_PVs, laser_values, \
    lf_PVs, lf_values
from ...controller.utils import caput_lf

unittest_data_path = os.path.join(os.path.dirname(__file__), '../data')


class MainControllerTest(QtTest):
    def setUp(self):
        self.controller = MainController()

    def tearDown(self):
        del self.controller
        gc.collect()

    def test_main_status_shows_correct_value_on_startup(self):
        self.assertEqual(self.controller.widget.main_status.text(), MAIN_STATUS_OFF)

        caput(general_PVs['laser_shutter_control'], general_values['laser_shutter_blocking'], wait=True)
        caput(pulse_PVs['BNC'], pulse_values['BNC_RUNNING'], wait=True)

        self.controller.update_main_status()  # should be updated automatically in future
        self.assertEqual(self.controller.widget.main_status.text(), MAIN_STATUS_ON)
        caput(pulse_PVs['BNC'], pulse_values['BNC_STOPPED'], wait=True)
        caput(general_PVs['laser_shutter_control'], general_values['laser_shutter_clear'], wait=True)

    def test_laser_mode_status_shows_correct_value_on_startup(self):
        self.assertEqual(self.controller.widget.laser_ds_status.text(), LASER_STATUS_NORMAL)
        self.assertEqual(self.controller.widget.laser_us_status.text(), LASER_STATUS_NORMAL)

        caput(laser_PVs['ds_enable_modulation'], 1, wait=True)
        caput(laser_PVs['us_enable_modulation'], 1, wait=True)
        time.sleep(0.5)
        self.controller.update_laser_status()  # should be updated automatically in future

        self.assertEqual(self.controller.widget.laser_ds_status.text(), LASER_STATUS_PULSED)
        self.assertEqual(self.controller.widget.laser_us_status.text(), LASER_STATUS_PULSED)

        caput(laser_PVs['ds_disable_modulation'], 1, wait=True)
        caput(laser_PVs['us_disable_modulation'], 1, wait=True)

    def test_pimax_mode_status_shows_correct_value_on_startup(self):
        self.assertEqual(self.controller.widget.pimax_status.text(), PIMAX_STATUS_NORMAL)
        caput_lf(lf_PVs['lf_set_experiment'], lf_values['PIMAX_pulsed'], wait=True)
        self.controller.update_pimax_status()  # should be updated automatically in future
        self.assertEqual(self.controller.widget.pimax_status.text(), PIMAX_STATUS_PULSED)
