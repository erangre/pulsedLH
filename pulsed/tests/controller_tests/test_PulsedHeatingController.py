# -*- coding: utf8 -*-

import os, sys
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
    lf_PVs, lf_values, pil3_PVs, pil3_values
from ...controller.utils import caput_lf
from ... import excepthook

data_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '../data'))


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

    def test_timing_labels_update(self):
        self.assertEqual(float(self.widget.ds_width_le.text()), 1)
        self.assertEqual(float(self.widget.ds_delay_le.text()), 0)
        self.assertEqual(float(self.widget.us_width_le.text()), 1)
        self.assertEqual(float(self.widget.us_delay_le.text()), 0)

        self.widget.ten_percent_btn.click()
        self.assertAlmostEqual(float(self.widget.ds_width_le.text()), caget(pulse_PVs['BNC_T1_width'])*1E6, places=2)
        self.assertAlmostEqual(float(self.widget.us_width_le.text()), caget(pulse_PVs['BNC_T2_width'])*1E6, places=2)
        self.assertAlmostEqual(float(self.widget.ds_delay_le.text()), caget(pulse_PVs['BNC_T1_delay'])*1E6, places=2)
        self.assertAlmostEqual(float(self.widget.us_delay_le.text()), caget(pulse_PVs['BNC_T2_delay'])*1E6, places=2)

        self.widget.zero_btn.click()

    def test_laser_percent_change_updates_text(self):
        self.widget.zero_btn.click()
        self.assertAlmostEqual(float(self.widget.ds_percent_display_le.text()), 0.0, places=2)
        step_value = 0.2
        enter_value_into_text_field(self.widget.laser_percent_tweak_le, str(step_value))
        self.widget.both_increase_percent_btn.click()
        self.assertAlmostEqual(float(self.widget.ds_percent_display_le.text()), step_value, places=2)

    def test_disable_and_enable_pulses_for_each_laser(self):
        self.assertEqual(caget(pulse_PVs['BNC_T1_enable']), pulse_values['BNC_ENABLE'])
        self.widget.ds_enable_pulses_cb.setChecked(False)
        time.sleep(0.1)

        self.assertEqual(caget(pulse_PVs['BNC_T1_enable']), pulse_values['BNC_DISABLE'])
        self.widget.ds_enable_pulses_cb.setChecked(True)
        time.sleep(0.1)
        self.assertEqual(caget(pulse_PVs['BNC_T1_enable']), pulse_values['BNC_ENABLE'])

        self.assertEqual(caget(pulse_PVs['BNC_T2_enable']), pulse_values['BNC_ENABLE'])
        self.widget.us_enable_pulses_cb.setChecked(False)
        time.sleep(0.1)
        self.assertEqual(caget(pulse_PVs['BNC_T2_enable']), pulse_values['BNC_DISABLE'])

        self.widget.us_enable_pulses_cb.setChecked(True)
        time.sleep(0.1)
        self.assertEqual(caget(pulse_PVs['BNC_T2_enable']), pulse_values['BNC_ENABLE'])

    def test_manual_delay_between_ds_and_us(self):
        self.assertAlmostEqual(self.widget.ds_us_manual_delay_sb.value(), 0, places=3)
        old_t1_delay = caget(pulse_PVs['BNC_T1_delay']) * 1E6
        self.widget.manual_delay_step_size_1_btn.click()
        self.widget.ds_us_manual_delay_sb.stepUp()
        self.assertAlmostEqual(self.widget.ds_us_manual_delay_sb.value(), 1, places=3)
        self.assertAlmostEqual(float(self.widget.ds_delay_le.text()), old_t1_delay + 1, places=2)
        self.widget.ds_us_manual_delay_sb.stepDown()
        self.assertAlmostEqual(float(self.widget.ds_delay_le.text()), old_t1_delay, places=2)

    def test_manual_gate_delay(self):
        self.assertAlmostEqual(self.widget.gate_manual_delay_sb.value(), 0, places=3)
        old_t4_delay = caget(pulse_PVs['BNC_T4_delay']) * 1E6
        self.widget.manual_delay_step_size_1_btn.click()
        self.widget.gate_manual_delay_sb.stepUp()
        self.assertAlmostEqual(self.widget.gate_manual_delay_sb.value(), 1, places=3)
        self.assertAlmostEqual(caget(pulse_PVs['BNC_T4_delay']) * 1E6, old_t4_delay + 1, places=2)
        self.widget.gate_manual_delay_sb.stepDown()
        self.assertAlmostEqual(caget(pulse_PVs['BNC_T4_delay']) * 1E6, old_t4_delay, places=2)

    def test_manual_delay_step_size(self):
        self.widget.manual_delay_step_size_0p001_btn.click()
        self.assertEqual(self.widget.gate_manual_delay_sb.singleStep(), 0.001)
        self.assertEqual(self.widget.ds_us_manual_delay_sb.singleStep(), 0.001)
        self.widget.manual_delay_step_size_0p01_btn.click()
        self.assertEqual(self.widget.gate_manual_delay_sb.singleStep(), 0.01)
        self.assertEqual(self.widget.ds_us_manual_delay_sb.singleStep(), 0.01)
        self.widget.manual_delay_step_size_0p1_btn.click()
        self.assertEqual(self.widget.gate_manual_delay_sb.singleStep(), 0.1)
        self.assertEqual(self.widget.ds_us_manual_delay_sb.singleStep(), 0.1)
        self.widget.manual_delay_step_size_1_btn.click()
        self.assertEqual(self.widget.gate_manual_delay_sb.singleStep(), 1.0)
        self.assertEqual(self.widget.ds_us_manual_delay_sb.singleStep(), 1.0)

    def test_running_creates_log_file(self):
        # sys.excepthook = excepthook
        log_file = os.path.join(data_path, 'test_log.txt')
        os.remove(log_file)
        self.assertFalse(os.path.isfile(log_file))
        QtWidgets.QFileDialog.getSaveFileName = MagicMock(return_value=log_file)
        self.main_controller.widget.config_widget.choose_log_path_btn.click()
        self.widget.measure_temperature_cb.setChecked(True)
        self.widget.measure_diffraction_cb.setChecked(False)
        self.widget.start_pulse_btn.click()
        self.assertTrue(os.path.isfile(log_file))

    def test_collect_quenched_xrd(self):
        old_t_file = caget(lf_PVs['lf_last_file_name'], as_string=True)
        old_xrd_file = caget(pil3_PVs['file_name'], as_string=True)
        self.main_controller.widget.mode_switch_widget.pil3_to_pulsed_btn.click()
        time.sleep(0.5)
        self.widget.collect_quenched_xrd_btn.click()
        self.assertEqual(caget(pulse_PVs['BNC_run']), pulse_values['BNC_STOPPED'])  # maybe not good here. maybe needs
        # to be running
        self.assertEqual(caget(lf_PVs['lf_last_file_name'], as_string=True), old_t_file)
        self.assertNotEqual(caget(pil3_PVs['file_name'], as_string=True), old_xrd_file)

    def test_measure_t_background(self):
        self.widget.measure_t_background_btn.click()
        self.assertEqual(caget(lf_PVs['lf_last_file_name'], as_string=True), lf_values['PIMAX_pulsed_bg_file_name'])

    def test_changing_t_values_demands_bg_collection(self):
        self.assertIsNone(self.controller.bg_collected_for)
        self.widget.measure_t_background_btn.click()
        bg_num_accs = self.controller.bg_collected_for
        self.assertTrue(bg_num_accs)
        self.main_controller.widget.config_widget.pimax_max_num_accs_sb.setValue(20000)
        self.assertNotEqual(caget(lf_PVs['lf_get_accs']), bg_num_accs)
