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


class ModeSwitchControllerTest(QtTest):
    def setUp(self):
        self.main_controller = MainController()
        self.controller = self.main_controller.mode_switch_controller
        self.widget = self.controller.widget

    def tearDown(self):
        del self.controller
        del self.widget
        del self.main_controller
        gc.collect()

    def test_switch_ds_laser_mode_to_pulsed_and_back(self):
        self.assertEqual(caget(laser_PVs['ds_modulation_status']), laser_values['modulation_disabled'])
        self.widget.mode_switch_widget.ds_laser_pulsed_btn.click()
        self.assertEqual(caget(laser_PVs['ds_modulation_status']), laser_values['modulation_enabled'])
        self.widget.mode_switch_widget.ds_laser_normal_btn.click()
        self.assertEqual(caget(laser_PVs['ds_modulation_status']), laser_values['modulation_disabled'])

    def test_switch_us_laser_mode_to_pulsed_and_back(self):
        self.assertEqual(caget(laser_PVs['us_modulation_status']), laser_values['modulation_disabled'])
        self.widget.mode_switch_widget.us_laser_pulsed_btn.click()
        self.assertEqual(caget(laser_PVs['us_modulation_status']), laser_values['modulation_enabled'])
        self.widget.mode_switch_widget.us_laser_normal_btn.click()
        self.assertEqual(caget(laser_PVs['us_modulation_status']), laser_values['modulation_disabled'])
