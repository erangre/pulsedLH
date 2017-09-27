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
    lf_PVs, lf_values, pil3_PVs, pil3_values
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

    def test_switch_pimax_to_pulsed_and_back(self):
        self.assertEqual(caget(lf_PVs['lf_get_experiment'], as_string=True), lf_values['PIMAX_normal'])
        self.widget.mode_switch_widget.pimax_to_pulsed_btn.click()
        self.assertEqual(caget(lf_PVs['lf_get_experiment'], as_string=True), lf_values['PIMAX_pulsed'])
        self.assertEqual(caget(lf_PVs['lf_get_bg_file_name'], as_string=True), lf_values['PIMAX_pulsed_bg_file_name'])
        self.widget.mode_switch_widget.pimax_to_normal_btn.click()
        self.assertEqual(caget(lf_PVs['lf_get_experiment'], as_string=True), lf_values['PIMAX_normal'])
        self.assertEqual(caget(lf_PVs['lf_get_bg_file_name'], as_string=True), lf_values['PIMAX_normal_bg_file_name'])

    def test_switch_pilatus_to_pulsed_and_back(self):
        self.assertEqual(caget(pil3_PVs['trigger_mode']), pil3_values['trigger_internal'])
        self.widget.mode_switch_widget.pil3_pulsed.btn.click()
        self.assertEqual(caget(pil3_PVs['trigger_mode']), pil3_values['trigger_external_enable'])
        self.widget.mode_switch_widget.pil3_normal.btn.click()

    def test_switch_all_to_pulsed_and_back(self):
        self.assertTrue(self.widget.mode_switch_widget.ds_laser_normal_btn.isChecked())
        self.assertTrue(self.widget.mode_switch_widget.us_laser_normal_btn.isChecked())
        self.assertTrue(self.widget.mode_switch_widget.pimax_to_normal_btn.isChecked())
        self.assertTrue(self.widget.mode_switch_widget.pil3_to_normal_btn.isChecked())
        self.widget.mode_switch_widget.all_to_pulsed_btn.click()
        self.assertTrue(self.widget.mode_switch_widget.ds_laser_pulsed_btn.isChecked())
        self.assertTrue(self.widget.mode_switch_widget.us_laser_pulsed_btn.isChecked())
        self.assertTrue(self.widget.mode_switch_widget.pimax_to_pulsed_btn.isChecked())
        self.assertTrue(self.widget.mode_switch_widget.pil3_to_pulsed_btn.isChecked())
        self.widget.mode_switch_widget.all_to_normal_btn.click()
        self.assertTrue(self.widget.mode_switch_widget.ds_laser_normal_btn.isChecked())
        self.assertTrue(self.widget.mode_switch_widget.us_laser_normal_btn.isChecked())
        self.assertTrue(self.widget.mode_switch_widget.pimax_to_normal_btn.isChecked())
        self.assertTrue(self.widget.mode_switch_widget.pil3_to_normal_btn.isChecked())


