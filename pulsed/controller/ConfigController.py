# -*- coding: utf8 -*-
import os
import time
from sys import platform as _platform
from qtpy import QtWidgets, QtCore

try:
    from epics import caget, caput
except ImportError:
    exit(2)

from ..widgets.MainWidget import MainWidget
from .utils import caput_lf, caput_pil3
from .epics_config import pulse_PVs, pulse_values, laser_PVs, laser_values, lf_PVs, lf_values, pil3_PVs, pil3_values, \
    general_PVs, general_values
from ..model.ConfigModel import ConfigModel

DEFAULT_NUM_PULSES = 100000
PULSE_FACTOR = 1.02
DEFAULT_MAX_NUM_PIMAX_ACCS = 10000
PIMAX_FACTOR = 0.8
DEFAULT_MAX_NUM_PIMAX_FRAMES = 40
DEFAULT_GATE_WIDTH = 1
DEFAULT_PULSE_FREQ = 10000
DEFAULT_LOG_FILE = os.path.normpath(os.path.join(os.path.dirname(__file__), time.strftime("..\..\log_%Y_%m_%d.txt")))


class ConfigController(object):
    def __init__(self, widget):
        """
        :param widget:
        :type widget: MainWidget
        """
        self.main_widget = widget
        self.widget = widget.config_widget
        self.model = ConfigModel()
        self.old_settings = {}
        self.set_startup_values()
        self.prepare_connections()

    def prepare_connections(self):
        self.widget.num_pulses_sb.valueChanged.connect(self.num_pulses_sb_changed)
        self.widget.pimax_max_num_accs_sb.valueChanged.connect(self.pimax_max_num_accs_sb_changed)
        self.widget.pimax_max_num_frames_sb.valueChanged.connect(self.pimax_max_num_frames_sb_changed)
        self.widget.choose_log_path_btn.clicked.connect(self.choose_log_path_btn_clicked)
        self.widget.pulse_width_le.editingFinished.connect(self.pulse_width_le_changed)

    def set_startup_values(self):
        self.widget.log_path_le.setText(DEFAULT_LOG_FILE)
        self.widget.num_pulses_sb.setValue(DEFAULT_NUM_PULSES)
        self.widget.pimax_max_num_accs_sb.setValue(DEFAULT_MAX_NUM_PIMAX_ACCS)
        self.widget.pimax_max_num_frames_sb.setValue(DEFAULT_MAX_NUM_PIMAX_FRAMES)
        caput(pulse_PVs['BNC_burst_count'], DEFAULT_NUM_PULSES * PULSE_FACTOR)
        accs, frames = self.model.calc_frames_and_accs(DEFAULT_NUM_PULSES, DEFAULT_MAX_NUM_PIMAX_ACCS, PIMAX_FACTOR,
                                                       DEFAULT_MAX_NUM_PIMAX_FRAMES)
        # if self.main_widget.pimax_status.text() == PIMAX_STATUS_PULSED:
        #     caput_lf(lf_PVs['lf_set_accs'], accs)
        #     caput_lf(lf_PVs['lf_set_frames'], frames)
        # if self.main_widget.pil3_status.text() == PIL3_STATUS_PULSED:
        #     caput(pil3_PVs['exposures_per_image'], DEFAULT_NUM_PULSES)
        self.main_widget.pulsed_laser_heating_widget.num_pulses_le.setText(str(DEFAULT_NUM_PULSES))

    def num_pulses_sb_changed(self):
        num_pulses = self.widget.num_pulses_sb.value()
        caput(pulse_PVs['BNC_burst_count'], num_pulses * PULSE_FACTOR)
        self.update_lf_settings(num_pulses)
        caput_pil3(pil3_PVs['exposures_per_image'], num_pulses)
        self.main_widget.pulsed_laser_heating_widget.num_pulses_le.setText(str(num_pulses))

    def pimax_max_num_accs_sb_changed(self):
        num_pulses = self.widget.num_pulses_sb.value()
        self.update_lf_settings(num_pulses)

    def pimax_max_num_frames_sb_changed(self):
        num_pulses = self.widget.num_pulses_sb.value()
        self.update_lf_settings(num_pulses)

    def update_lf_settings(self, num_pulses=None):
        if num_pulses is None:
            num_pulses = self.widget.num_pulses_sb.value()
        # self.toggle_config_btns(False)
        # QtWidgets.QApplication.processEvents()
        # problem with disabling widgets - currently edited spinbox loses focus.
        max_accs = self.widget.pimax_max_num_accs_sb.value()
        max_frames = self.widget.pimax_max_num_frames_sb.value()
        accs, frames = self.model.calc_frames_and_accs(num_pulses, max_accs, PIMAX_FACTOR, max_frames)
        caput_lf(lf_PVs['lf_set_accs'], accs)
        caput_lf(lf_PVs['lf_set_frames'], frames)
        # self.toggle_config_btns(True)

    def choose_log_path_btn_clicked(self):
        CH_FILE_TEXT = 'Choose file for saving pulsed heating log'
        choose_file = QtWidgets.QFileDialog.getSaveFileName(parent=None, caption=CH_FILE_TEXT,
                                                            directory=os.path.dirname(DEFAULT_LOG_FILE), filter='.txt')
        if isinstance(choose_file, tuple):
            choose_file = choose_file[0] + choose_file[1]
        self.widget.log_path_le.setText(choose_file)

    def toggle_config_btns(self, toggle):
        self.widget.num_pulses_sb.setEnabled(toggle)
        self.widget.pimax_max_num_accs_sb.setEnabled(toggle)
        self.widget.pimax_max_num_frames_sb.setEnabled(toggle)
        self.widget.log_path_le.setEnabled(toggle)
        self.widget.choose_log_path_btn.setEnabled(toggle)
        QtWidgets.QApplication.processEvents()

    def pulse_width_le_changed(self):
        pulse_width = float(self.widget.pulse_width_le.text())*1E-6
        caput(pulse_PVs['BNC_T4_width'], pulse_width)
        caput_lf(lf_PVs['lf_gate_width'], pulse_width)
