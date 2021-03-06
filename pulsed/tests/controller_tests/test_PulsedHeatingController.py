# -*- coding: utf8 -*-

import os
import gc
import time
import shutil
import numpy as np
from mock import MagicMock
from epics import caput, caget

from ..utility import QtTest, enter_value_into_text_field

from qtpy import QtCore, QtWidgets
from qtpy.QtTest import QTest

from ...controller.MainController import MainController
from ...controller.MainController import MAIN_STATUS_OFF, MAIN_STATUS_ON, LASER_STATUS_NORMAL, LASER_STATUS_PULSED, \
    PIMAX_STATUS_NORMAL, PIMAX_STATUS_PULSED
from ...controller.epics_config import pulse_PVs, general_PVs, pulse_values, general_values, laser_PVs, laser_values, \
    lf_PVs, lf_values
from ...controller.utils import caput_lf

unittest_data_path = os.path.join(os.path.dirname(__file__), '../data')


class PulsedHeatingControllerTest(QtTest):
    def setUp(self):
        self.main_controller = MainController()
        self.controller = self.main_controller.pulsed_heating_controller
        self.widget = self.controller.widget

    def tearDown(self):
        del self.controller
        del self.widget
        del self.main_controller
        gc.collect()

    def test_zero_btn(self):
        self.helper_set_lasers_to_ten_percent()
        self.widget.zero_btn.click()
        self.assertAlmostEqual(caget(laser_PVs['ds_laser_percent']), 0.0, places=3)
        self.assertAlmostEqual(caget(laser_PVs['us_laser_percent']), 0.0, places=3)

    def test_ten_percent_btn(self):
        self.assertAlmostEqual(caget(laser_PVs['ds_laser_percent']), 0.0, places=3)
        self.assertAlmostEqual(caget(laser_PVs['us_laser_percent']), 0.0, places=3)
        self.helper_set_lasers_to_ten_percent()
        self.assertAlmostEqual(caget(laser_PVs['ds_laser_percent']), 10.0, places=3)
        self.assertAlmostEqual(caget(laser_PVs['us_laser_percent']), 10.0, places=3)
        self.helper_set_lasers_to_zero_percent()

    def helper_set_lasers_to_ten_percent(self):
        self.widget.ten_percent_btn.click()

    def helper_set_lasers_to_zero_percent(self):
        self.widget.zero_btn.click()

    def test_set_laser_percent_step(self):
        self.assertAlmostEqual(caget(laser_PVs['ds_laser_percent_tweak']), 0.1, places=3)
        self.assertAlmostEqual(caget(laser_PVs['us_laser_percent_tweak']), 0.1, places=3)
        enter_value_into_text_field(self.widget.laser_percent_tweak_le, '0.2')
        self.assertAlmostEqual(caget(laser_PVs['ds_laser_percent_tweak']), 0.2, places=3)
        self.assertAlmostEqual(caget(laser_PVs['us_laser_percent_tweak']), 0.2, places=3)
        enter_value_into_text_field(self.widget.laser_percent_tweak_le, '0.1')

    def test_increase_and_decrease_ds(self):
        step = 0.2
        enter_value_into_text_field(self.widget.laser_percent_tweak_le, str(step))
        self.assertAlmostEqual(caget(laser_PVs['ds_laser_percent']), 0.0, places=3)
        self.widget.ds_increase_percent_btn.click()
        time.sleep(0.1)
        self.assertAlmostEqual(caget(laser_PVs['ds_laser_percent']), step, places=3)
        self.widget.ds_decrease_percent_btn.click()
        time.sleep(0.1)
        self.assertAlmostEqual(caget(laser_PVs['ds_laser_percent']), 0.0, places=3)

    def test_increase_and_decrease_us(self):
        step = 0.2
        enter_value_into_text_field(self.widget.laser_percent_tweak_le, str(step))
        self.assertAlmostEqual(caget(laser_PVs['us_laser_percent']), 0.0, places=3)
        self.widget.us_increase_percent_btn.click()
        time.sleep(0.1)
        self.assertAlmostEqual(caget(laser_PVs['us_laser_percent']), step, places=3)
        self.widget.us_decrease_percent_btn.click()
        time.sleep(0.1)
        self.assertAlmostEqual(caget(laser_PVs['us_laser_percent']), 0.0, places=3)

    def test_increase_and_decrease_both(self):
        step = 0.2
        enter_value_into_text_field(self.widget.laser_percent_tweak_le, str(step))
        self.assertAlmostEqual(caget(laser_PVs['us_laser_percent']), 0.0, places=3)
        self.assertAlmostEqual(caget(laser_PVs['ds_laser_percent']), 0.0, places=3)
        self.widget.both_increase_percent_btn.click()
        time.sleep(0.1)
        self.assertAlmostEqual(caget(laser_PVs['us_laser_percent']), step, places=3)
        self.assertAlmostEqual(caget(laser_PVs['ds_laser_percent']), step, places=3)
        self.widget.both_decrease_percent_btn.click()
        time.sleep(0.1)
        self.assertAlmostEqual(caget(laser_PVs['us_laser_percent']), 0.0, places=3)
        self.assertAlmostEqual(caget(laser_PVs['ds_laser_percent']), 0.0, places=3)

    def test_run_without_measurement(self):
        """
        Real run should change BNC mode to burst and make sure laser shutter is open before starting pulses
        :return: 
        """
        self.assertEqual(caget(pulse_PVs['BNC_run']), pulse_values['BNC_STOPPED'])
        self.widget.start_pulse_btn.click()
        time.sleep(0.1)
        self.assertEqual(caget(general_PVs['laser_shutter_status']), general_values['laser_shutter_clear'])
        self.assertEqual(caget(pulse_PVs['BNC_mode']), pulse_values['BNC_BURST'])
        self.assertEqual(caget(pulse_PVs['BNC_run']), pulse_values['BNC_RUNNING'])

    def test_stop_btn(self):
        self.widget.start_pulse_btn.click()
        time.sleep(0.1)
        self.assertEqual(caget(pulse_PVs['BNC_run']), pulse_values['BNC_RUNNING'])
        self.widget.stop_pulse_btn.click()
        time.sleep(0.1)
        self.assertEqual(caget(pulse_PVs['BNC_run']), pulse_values['BNC_STOPPED'])

    def test_timing_btn(self):
        """
        Timing should change BNC mode to normal and make sure that the laser shutter is closed before starting pulses
        :return: 
        """
        self.widget.start_timing_btn.click()
        time.sleep(0.1)
        self.assertEqual(caget(general_PVs['laser_shutter_status']), general_values['laser_shutter_blocking'])
        self.assertEqual(caget(pulse_PVs['BNC_mode']), pulse_values['BNC_NORMAL'])
        self.assertEqual(caget(pulse_PVs['BNC_run']), pulse_values['BNC_RUNNING'])
        self.widget.stop_pulse_btn.click()

    def test_run_with_temperature_only(self):
        file_name = caget(lf_PVs['lf_last_file_name'], as_string=True)
        self.widget.measure_temperature_cb.setChecked(True)
        self.widget.measure_diffraction_cb.setChecked(False)
        self.widget.start_pulse_btn.click()
        self.assertNotEqual(caget(lf_PVs['lf_last_file_name'], as_string=True), file_name)

    def test_run_with_xrd_only(self):
        pass

    def test_run_with_temp_and_xrd(self):
        pass
