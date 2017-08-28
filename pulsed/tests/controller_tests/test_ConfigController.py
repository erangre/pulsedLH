# -*- coding: utf8 -*-

import os
import gc
import time
import shutil
import numpy as np
from mock import MagicMock
from epics import caput, caget
from math import floor

from ..utility import QtTest, enter_value_into_text_field

from qtpy import QtCore, QtWidgets
from qtpy.QtTest import QTest

from ...controller.MainController import MainController
from ...controller.ConfigController import DEFAULT_GATE_WIDTH, DEFAULT_MAX_NUM_PIMAX_ACCS, DEFAULT_NUM_PULSES, \
    DEFAULT_PULSE_FREQ, PULSE_FACTOR, PIMAX_FACTOR, DEFAULT_MAX_NUM_PIMAX_FRAMES, DEFAULT_LOG_FILE
from ...controller.MainController import MAIN_STATUS_OFF, MAIN_STATUS_ON, LASER_STATUS_NORMAL, LASER_STATUS_PULSED, \
    PIMAX_STATUS_NORMAL, PIMAX_STATUS_PULSED
from ...controller.epics_config import pulse_PVs, general_PVs, pulse_values, general_values, laser_PVs, laser_values, \
    lf_PVs, lf_values, pil3_PVs, pil3_values
from ...controller.utils import caput_lf

unittest_data_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '../data'))


class PulsedHeatingControllerTest(QtTest):
    def setUp(self):
        self.main_controller = MainController()
        self.controller = self.main_controller.config_controller
        self.widget = self.controller.widget
        self.model = self.controller.model

    def tearDown(self):
        del self.controller
        del self.widget
        del self.main_controller
        gc.collect()

    def test_set_number_of_pulses(self):
        self.assertEqual(self.widget.num_pulses_sb.value(), DEFAULT_NUM_PULSES)
        accs, frames = self.model.calc_frames_and_accs(DEFAULT_NUM_PULSES, DEFAULT_MAX_NUM_PIMAX_ACCS, PIMAX_FACTOR,
                                                       DEFAULT_MAX_NUM_PIMAX_FRAMES)
        self.assertEqual(caget(lf_PVs['lf_get_accs']), accs)
        self.assertEqual(caget(lf_PVs['lf_get_frames']), frames)
        # self.assertEqual(caget(pil3_PVs['exposures_per_image']), DEFAULT_NUM_PULSES)
        old_bnc_burst_count = caget(pulse_PVs['BNC_burst_count'])
        self.assertEqual(old_bnc_burst_count, self.widget.num_pulses_sb.value() * PULSE_FACTOR)

        num_pulses = DEFAULT_NUM_PULSES * 6

        self.widget.num_pulses_sb.setValue(num_pulses)
        time.sleep(0.1)

        self.assertEqual(caget(pulse_PVs['BNC_burst_count']), num_pulses * PULSE_FACTOR)
        # self.assertEqual(caget(pil3_PVs['exposures_per_image']), num_pulses)
        accs, frames = self.model.calc_frames_and_accs(num_pulses, DEFAULT_MAX_NUM_PIMAX_ACCS, PIMAX_FACTOR,
                                                       DEFAULT_MAX_NUM_PIMAX_FRAMES)
        self.assertEqual(caget(lf_PVs['lf_get_accs']), accs)
        self.assertEqual(caget(lf_PVs['lf_get_frames']), frames)
        # TODO - uncomment pilatus parts

    def test_set_max_number_of_pimax_accumulations(self):
        self.widget.num_pulses_sb.setValue(DEFAULT_MAX_NUM_PIMAX_ACCS * 4/PIMAX_FACTOR)
        time.sleep(0.1)
        num_frames = caget(lf_PVs['lf_get_frames'])
        self.widget.pimax_max_num_accs_sb.setValue(DEFAULT_MAX_NUM_PIMAX_ACCS * 2)
        time.sleep(0.1)
        self.assertEqual(caget(lf_PVs['lf_get_frames']), int(num_frames/2))

    def test_set_max_number_of_pimax_frames(self):
        self.widget.num_pulses_sb.setValue(DEFAULT_MAX_NUM_PIMAX_ACCS / PIMAX_FACTOR * DEFAULT_MAX_NUM_PIMAX_FRAMES * 2)
        time.sleep(0.1)
        num_frames = caget(lf_PVs['lf_get_frames'])
        self.widget.pimax_max_num_frames_sb.setValue(DEFAULT_MAX_NUM_PIMAX_ACCS * 3)
        time.sleep(0.1)
        self.assertEqual(caget(lf_PVs['lf_get_frames']), num_frames * 2)

    def test_set_gate_width(self):
        pass

    def test_set_pulse_frequency(self):
        pass

    def test_set_logging_file(self):
        self.assertEqual(self.widget.log_path_le.text(), DEFAULT_LOG_FILE)
        new_path = os.path.join(unittest_data_path, 'log.txt')
        QtWidgets.QFileDialog.getSaveFileName = MagicMock(return_value=new_path)
        self.widget.choose_log_path_btn.click()
        self.assertEqual(self.widget.log_path_le.text(), new_path)
