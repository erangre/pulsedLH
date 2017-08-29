# -*- coding: utf8 -*-
import os
import time
from sys import platform as _platform
from qtpy import QtWidgets, QtCore
from functools import partial
from threading import Thread

from epics import caget, caput

from ..widgets.MainWidget import MainWidget
from ..model.WidthDelayModel import WidthDelayModel
from .utils import caput_lf
from .epics_config import pulse_PVs, pulse_values, laser_PVs, laser_values, lf_PVs, lf_values, general_PVs, \
    general_values, pil3_PVs, pil3_values


class PulsedHeatingController(QtCore.QObject):

    pulse_changed = QtCore.Signal()

    def __init__(self, widget):
        """
        :param widget:
        :type widget MainWidget
        """
        super(PulsedHeatingController, self).__init__()
        self.widget = widget.pulsed_laser_heating_widget
        self.main_widget = widget
        self.model = WidthDelayModel()
        self.prepare_connections()
        self.laser_percent_tweak_le_editing_finished()
        self.ds_laser_percent_changed()
        self.us_laser_percent_changed()
        self.manual_delay = 1.0
        self.update_bnc_timings()
        self.log_info = {}
        self.log_order = ['date_time', 'xrd_file_name', 'xrd_file_path', 't_file_name', 't_file_path', 'xrd_exp_time',
                          't_exp_time_per_frame', 'num_t_frames', 'num_t_accumulations', 'num_pulses', 'ds_percent',
                          'us_percent', 'pulse_width']
        self.first_run = True

    def prepare_connections(self):
        self.widget.ten_percent_btn.clicked.connect(self.ten_percent_btn_clicked)
        self.widget.zero_btn.clicked.connect(self.zero_btn_clicked)
        self.widget.ds_enable_pulses_cb.stateChanged.connect(self.ds_enable_pulses_cb_changed)
        self.widget.us_enable_pulses_cb.stateChanged.connect(self.us_enable_pulses_cb_changed)
        self.widget.laser_percent_tweak_le.editingFinished.connect(self.laser_percent_tweak_le_editing_finished)
        self.widget.ds_increase_percent_btn.clicked.connect(self.ds_increase_percent_btn_clicked)
        self.widget.ds_decrease_percent_btn.clicked.connect(self.ds_decrease_percent_btn_clicked)
        self.widget.us_increase_percent_btn.clicked.connect(self.us_increase_percent_btn_clicked)
        self.widget.us_decrease_percent_btn.clicked.connect(self.us_decrease_percent_btn_clicked)
        self.widget.both_increase_percent_btn.clicked.connect(self.both_increase_percent_btn_clicked)
        self.widget.both_decrease_percent_btn.clicked.connect(self.both_decrease_percent_btn_clicked)
        self.widget.start_pulse_btn.clicked.connect(self.start_pulse_btn_clicked)
        self.widget.stop_pulse_btn.clicked.connect(self.stop_pulse_btn_clicked)
        self.widget.start_timing_btn.clicked.connect(self.start_timing_btn_clicked)
        self.widget.ds_us_manual_delay_sb.valueChanged.connect(self.ds_us_manual_delay_changed)
        self.widget.gate_manual_delay_sb.valueChanged.connect(self.gate_manual_delay_changed)
        for manual_delay_step_btn in self.widget.manual_delay_step_btns:
            manual_delay_step_btn.clicked.connect(partial(self.manual_delay_step_btn_clicked, manual_delay_step_btn))

        self.pulse_changed.connect(self.update_bnc_timings)

    def ten_percent_btn_clicked(self):
        caput(laser_PVs['ds_laser_percent'], 10.0, wait=True)
        caput(laser_PVs['us_laser_percent'], 10.0, wait=True)
        self.pulse_changed.emit()

    def zero_btn_clicked(self):
        caput(laser_PVs['ds_laser_percent'], 0.0, wait=True)
        caput(laser_PVs['us_laser_percent'], 0.0, wait=True)
        self.pulse_changed.emit()

    def ds_enable_pulses_cb_changed(self):
        if self.widget.ds_enable_pulses_cb.isChecked():
            caput(pulse_PVs['BNC_T1_enable'], pulse_values['BNC_ENABLE'])
        else:
            caput(pulse_PVs['BNC_T1_enable'], pulse_values['BNC_DISABLE'])

    def us_enable_pulses_cb_changed(self):
        if self.widget.us_enable_pulses_cb.isChecked():
            caput(pulse_PVs['BNC_T2_enable'], pulse_values['BNC_ENABLE'])
        else:
            caput(pulse_PVs['BNC_T2_enable'], pulse_values['BNC_DISABLE'])

    def laser_percent_tweak_le_editing_finished(self):
        caput(laser_PVs['ds_laser_percent_tweak'], float(self.widget.laser_percent_tweak_le.text()), wait=True)
        caput(laser_PVs['us_laser_percent_tweak'], float(self.widget.laser_percent_tweak_le.text()), wait=True)

    def ds_increase_percent_btn_clicked(self):
        inc_pv = laser_PVs['ds_laser_percent_tweak'].replace('Val', '.B')
        caput(inc_pv, 1, wait=True)
        self.pulse_changed.emit()

    def ds_decrease_percent_btn_clicked(self):
        dec_pv = laser_PVs['ds_laser_percent_tweak'].replace('Val', '.A')
        caput(dec_pv, 1, wait=True)
        self.pulse_changed.emit()

    def us_increase_percent_btn_clicked(self):
        inc_pv = laser_PVs['us_laser_percent_tweak'].replace('Val', '.B')
        caput(inc_pv, 1, wait=True)
        self.pulse_changed.emit()

    def us_decrease_percent_btn_clicked(self):
        dec_pv = laser_PVs['us_laser_percent_tweak'].replace('Val', '.A')
        caput(dec_pv, 1, wait=True)
        self.pulse_changed.emit()

    def both_increase_percent_btn_clicked(self):
        inc_pv = laser_PVs['us_laser_percent_tweak'].replace('Val', '.B')
        caput(inc_pv, 1, wait=True)
        inc_pv = laser_PVs['ds_laser_percent_tweak'].replace('Val', '.B')
        caput(inc_pv, 1, wait=True)
        self.pulse_changed.emit()

    def both_decrease_percent_btn_clicked(self):
        dec_pv = laser_PVs['us_laser_percent_tweak'].replace('Val', '.A')
        caput(dec_pv, 1, wait=True)
        dec_pv = laser_PVs['ds_laser_percent_tweak'].replace('Val', '.A')
        caput(dec_pv, 1, wait=True)
        self.pulse_changed.emit()

    def start_pulse_btn_clicked(self):
        self.log_file = open(self.main_widget.config_widget.log_path_le.text(), 'a')
        if self.first_run:
            self.write_headings()
            self.first_run = False
        caput(general_PVs['laser_shutter_control'], general_values['laser_shutter_clear'], wait=True)
        caput(pulse_PVs['BNC_mode'], pulse_values['BNC_BURST'], wait=True)
        self.collect_info_for_log()
        if self.widget.measure_temperature_cb.isChecked():
            caput(lf_PVs['lf_acquire'], 1, wait=False)
            t_toggle = True
        else:
            t_toggle = False
        if self.widget.measure_diffraction_cb.isChecked():
            caput(pil3_PVs['Acquire'], 1, wait=False)
            xrd_toggle = True
        else:
            xrd_toggle = False

        bnc_run_thread = Thread(target=self.start_pulses_on_thread)
        bnc_run_thread.start()

        while bnc_run_thread.isAlive():
            QtWidgets.QApplication.processEvents()
            time.sleep(0.1)

        self.collect_xrd_and_t_info_for_log(xrd=xrd_toggle, temperature=t_toggle)
        self.write_to_log_file()

    def start_pulses_on_thread(self):
        caput(pulse_PVs['BNC_run'], pulse_values['BNC_RUNNING'], wait=True)
        self.wait_until_pulses_end()

    def stop_pulse_btn_clicked(self):
        caput(pulse_PVs['BNC_run'], pulse_values['BNC_STOPPED'], wait=True)

    def start_timing_btn_clicked(self):
        # TODO read the current num of pulses, change to X seconds for alignment, then change back to original num
        caput(general_PVs['laser_shutter_control'], general_values['laser_shutter_blocking'], wait=True)
        caput(pulse_PVs['BNC_mode'], pulse_values['BNC_BURST'], wait=True)
        caput(pulse_PVs['BNC_run'], pulse_values['BNC_RUNNING'], wait=True)

    def update_bnc_timings(self):
        self.toggle_percent_and_timing_btns(False)
        QtWidgets.QApplication.processEvents()
        f = 1.0/caget(pulse_PVs['BNC_period'])
        w = 1.0  # TODO change this to read from settings the pulse width
        ds_percent = caget(laser_PVs['ds_laser_percent'], as_string=False)
        us_percent = caget(laser_PVs['us_laser_percent'], as_string=False)
        ds_us_manual_delay = self.widget.ds_us_manual_delay_sb.value()
        gate_manual_delay = self.widget.gate_manual_delay_sb.value()
        timings = self.model.calc_all_delays_and_widths(f, w, ds_percent, us_percent, ds_us_manual_delay,
                                                        gate_manual_delay)
        caput(pulse_PVs['BNC_T1_delay'], timings['delay_t1'], wait=True)
        caput(pulse_PVs['BNC_T2_delay'], timings['delay_t2'], wait=True)
        caput(pulse_PVs['BNC_T4_delay'], timings['delay_t4'], wait=True)
        caput(pulse_PVs['BNC_T1_width'], timings['width_t1'], wait=True)
        caput(pulse_PVs['BNC_T2_width'], timings['width_t2'], wait=True)
        caput(pulse_PVs['BNC_T4_width'], timings['width_t4'], wait=True)
        self.widget.update_timing_labels(timings)
        self.toggle_percent_and_timing_btns(True)

    def ds_laser_percent_changed(self, value=None, char_value=None):
        if value is None:
            value = caget(laser_PVs['ds_laser_percent'])
        self.widget.ds_percent_display_le.setText(str(round(value, 2)))

    def us_laser_percent_changed(self, value=None, char_value=None):
        if value is None:
            value = caget(laser_PVs['us_laser_percent'])
        self.widget.us_percent_display_le.setText(str(round(value, 2)))

    def toggle_percent_and_timing_btns(self, toggle):
        self.widget.both_increase_percent_btn.setEnabled(toggle)
        self.widget.both_decrease_percent_btn.setEnabled(toggle)
        self.widget.ds_increase_percent_btn.setEnabled(toggle)
        self.widget.ds_decrease_percent_btn.setEnabled(toggle)
        self.widget.us_increase_percent_btn.setEnabled(toggle)
        self.widget.us_decrease_percent_btn.setEnabled(toggle)
        self.widget.ds_us_manual_delay_sb.setEnabled(toggle)
        self.widget.gate_manual_delay_sb.setEnabled(toggle)

    def ds_us_manual_delay_changed(self):
        self.update_bnc_timings()

    def gate_manual_delay_changed(self):
        self.update_bnc_timings()

    def manual_delay_step_btn_clicked(self, manual_delay_step_btn):
        """
        :param manual_delay_step_btn:
        :type manual_delay_step_btn QtWidgets.QPushButton
        :return: 
        """
        manual_delay_step_btn.setChecked(True)
        self.widget.ds_us_manual_delay_sb.setSingleStep(float(manual_delay_step_btn.text()))
        self.widget.gate_manual_delay_sb.setSingleStep(float(manual_delay_step_btn.text()))

    def collect_info_for_log(self):
        self.log_info['date_time'] = time.asctime().replace(' ', '_')
        self.log_info['ds_percent'] = caget(laser_PVs['ds_laser_percent'])
        self.log_info['us_percent'] = caget(laser_PVs['us_laser_percent'])
        self.log_info['num_pulses'] = self.main_widget.config_widget.num_pulses_sb.value()
        self.log_info['pulse_width'] = caget(pulse_PVs['BNC_T4_width'])
        self.log_info['ds_delay'] = caget(pulse_PVs['BNC_T1_delay'])
        self.log_info['us_delay'] = caget(pulse_PVs['BNC_T2_delay'])
        self.log_info['gate_delay'] = caget(pulse_PVs['BNC_T4_delay'])
        self.log_info['ds_width'] = caget(pulse_PVs['BNC_T1_delay'])
        self.log_info['us_width'] = caget(pulse_PVs['BNC_T2_delay'])
        self.log_info['num_t_frames'] = caget(lf_PVs['lf_get_frames'])
        self.log_info['num_t_accumulations'] = caget(lf_PVs['lf_get_accs'])
        self.log_info['t_exp_time_per_frame'] = self.log_info['pulse_width'] * self.log_info['num_t_accumulations']
        # self.log_info['xrd_exp_time'] = self.log_info['pulse_width'] * caget(pil3_PVs['exposures_per_image'])

        # TODO - uncomment pilatus parts

    def collect_xrd_and_t_info_for_log(self, xrd=False, temperature=False):
        if not xrd:
            self.log_info['xrd_exp_time'] = 'N/A'
            self.log_info['xrd_file_name'] = 'N/A'
            self.log_info['xrd_file_path'] = 'N/A'
        else:
            (xrd_path, xrd_file) = os.path.split(caget(pil3_PVs['file_name'], as_string=True))
            self.log_info['xrd_file_name'] = xrd_file
            self.log_info['xrd_file_path'] = xrd_path

        if not temperature:
            self.log_info['num_t_frames'] = 'N/A'
            self.log_info['num_t_accumulations'] = 'N/A'
            self.log_info['t_exp_time_per_frame'] = 'N/A'
            self.log_info['t_file_name'] = 'N/A'
            self.log_info['t_file_path'] = 'N/A'
        else:
            (t_path, t_file) = os.path.split(caget(lf_PVs['lf_full_file_name'], as_string=True))
            self.log_info['t_file_name'] = t_file
            self.log_info['t_file_path'] = t_path

    def write_to_log_file(self):
        for item in self.log_order:
            self.log_file.write(str(self.log_info[item]) + '\t')
        self.log_file.write('\n')
        self.log_file.flush()
        self.log_file.close()

    def write_headings(self):
        for item in self.log_order:
            self.log_file.write(item + '\t')
        self.log_file.write('\n')
        self.log_file.flush()

    def wait_until_pulses_end(self):
        while caget(pulse_PVs['BNC_run']) == pulse_values['BNC_RUNNING']:
            time.sleep(0.1)
