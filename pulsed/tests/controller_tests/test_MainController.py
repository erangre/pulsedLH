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
    PIMAX_STATUS_NORMAL, PIMAX_STATUS_PULSED, LASER_EMISSION_OFF, LASER_EMISSION_ON
from ...controller.epics_config import pulse_PVs, general_PVs, pulse_values, general_values, laser_PVs, laser_values, \
    lf_PVs, lf_values
from ...controller.utils import caput_lf

unittest_data_path = os.path.join(os.path.dirname(__file__), '../data')


class MainControllerTest(QtTest):
    def setUp(self):
        self.controller = MainController()
        self.widget = self.controller.widget

    def tearDown(self):
        del self.widget
        del self.controller
        gc.collect()

    def test_main_status_shows_correct_value(self):
        self.assertEqual(self.widget.main_status.text(), MAIN_STATUS_OFF)

        caput(general_PVs['laser_shutter_control'], general_values['laser_shutter_blocking'], wait=True)
        caput(pulse_PVs['BNC_run'], pulse_values['BNC_RUNNING'], wait=True)
        self.assertEqual(self.widget.main_status.text(), MAIN_STATUS_ON)
        caput(pulse_PVs['BNC_run'], pulse_values['BNC_STOPPED'], wait=True)
        caput(general_PVs['laser_shutter_control'], general_values['laser_shutter_clear'], wait=True)

    def test_laser_mode_status_shows_correct_value(self):
        self.assertEqual(self.widget.laser_ds_status.text(), LASER_STATUS_NORMAL)
        self.assertEqual(self.widget.laser_us_status.text(), LASER_STATUS_NORMAL)

        caput(laser_PVs['ds_enable_modulation'], 1, wait=True)
        caput(laser_PVs['us_enable_modulation'], 1, wait=True)
        time.sleep(0.5)

        self.assertEqual(self.widget.laser_ds_status.text(), LASER_STATUS_PULSED)
        self.assertEqual(self.widget.laser_us_status.text(), LASER_STATUS_PULSED)

        caput(laser_PVs['ds_disable_modulation'], 1, wait=True)
        caput(laser_PVs['us_disable_modulation'], 1, wait=True)

    def test_pimax_mode_status_shows_correct_value(self):
        caput_lf(lf_PVs['lf_set_experiment'], lf_values['PIMAX_normal'], wait=True)
        self.assertEqual(self.widget.pimax_status.text(), PIMAX_STATUS_NORMAL)
        caput_lf(lf_PVs['lf_set_experiment'], lf_values['PIMAX_pulsed'], wait=True)
        # self.controller.update_pimax_status()  # should be updated automatically in future
        self.assertEqual(self.widget.pimax_status.text(), PIMAX_STATUS_PULSED)

    def test_switch_to_mode_switch_tab_and_back_to_pulsed_heating_tab(self):
        self.controller.show_window()
        self.assertTrue(self.widget.pulsed_laser_heating_widget.isVisible())
        self.assertFalse(self.widget.mode_switch_widget.isVisible())
        self.widget.mode_switch_btn.click()
        self.assertFalse(self.widget.pulsed_laser_heating_widget.isVisible())
        self.assertTrue(self.widget.mode_switch_widget.isVisible())
        self.widget.pulsed_laser_heating_btn.click()
        self.assertTrue(self.widget.pulsed_laser_heating_widget.isVisible())
        self.assertFalse(self.widget.mode_switch_widget.isVisible())

    def test_laser_emission_status_shows_correct_value_on_startup(self):
        # need to find way to test this for changes. Feature works,
        # but not the test since emission cannot be controlled programmatically.
        self.assertEqual(self.widget.laser_ds_emission_status.text(), LASER_EMISSION_OFF)
        self.assertEqual(self.widget.laser_us_emission_status.text(), LASER_EMISSION_OFF)
