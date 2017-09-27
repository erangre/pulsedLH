# -*- coding: utf8 -*-
import os
import time
from sys import platform as _platform
from qtpy import QtWidgets, QtCore
from functools import partial
from threading import Thread

try:
    from epics import caget, caput
except ImportError:
    exit(2)

from ..widgets.MainWidget import MainWidget
from ..model.WidthDelayModel import WidthDelayModel
from .utils import caput_lf, caput_pil3
from .epics_config import pulse_PVs, pulse_values, laser_PVs, laser_values, lf_PVs, lf_values, general_PVs, \
    general_values, pil3_PVs, pil3_values


class PulsedHeatingController(QtCore.QObject):

    pulse_changed = QtCore.Signal()
    pulse_running = QtCore.Signal(bool)

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
        self.bg_collected_for = None
        self.timing_adjusted = False
        self.log_order = ['date_time', 'xrd_file_name', 'xrd_file_path', 't_file_name', 't_file_path', 'xrd_exp_time',
                          't_exp_time_per_frame', 'num_t_frames', 'num_t_accumulations', 'num_pulses', 'ds_percent',
                          'us_percent', 'pulse_width', 'shutter', 'manual_gate_delay']
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

        self.widget.collect_quenched_xrd_btn.clicked.connect(self.collect_quenched_xrd_btn_clicked)
        self.widget.measure_t_background_btn.clicked.connect(self.measure_t_background_btn_clicked)

        self.widget.multi_gate_toggle_btn.clicked.connect(self.multi_gate_toggle_btn_clicked)

        self.widget.multi_gate_widget.run_multi_gate_btn.clicked.connect(self.run_multi_gate_btn_clicked)

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

    def start_pulse_btn_clicked(self, gate_delays=None):
        if gate_delays is None:
            gate_delays = [0]

        if caget(laser_PVs['ds_modulation_status']) == 0 or caget(laser_PVs['us_modulation_status']) == 0:
            msg = QtWidgets.QMessageBox()
            msg.setText("One (or both) of the lasers are in CW mode.\nAre you sure you want to proceed?")
            msg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            retval = msg.exec_()
            if retval == QtWidgets.QMessageBox.No:
                return

        if not self.timing_adjusted:
            msg = QtWidgets.QMessageBox()
            msg.setText("Laser timing was not adjusted to current laser power.\nAre you sure you want to proceed?")
            msg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            retval = msg.exec_()
            if retval == QtWidgets.QMessageBox.No:
                return

        self.log_file = open(self.main_widget.config_widget.log_path_le.text(), 'a')
        if self.first_run:
            self.write_headings()
            self.first_run = False
        caput(general_PVs['laser_shutter_control'], general_values['laser_shutter_clear'], wait=True)
        caput(pulse_PVs['BNC_mode'], pulse_values['BNC_BURST'], wait=True)
        manual_gate_delay = self.widget.gate_manual_delay_sb.value()
        for gate_delay in gate_delays:
            try:
                delay = float(gate_delay)
            except ValueError:
                continue
            self.start_pulses_for_single_gate_delay(delay + manual_gate_delay)

        self.widget.gate_manual_delay_sb.setValue(manual_gate_delay)
        self.log_file.close()

    def start_pulses_for_single_gate_delay(self, gate_delay):
        self.widget.gate_manual_delay_sb.setValue(gate_delay)
        self.collect_info_for_log()
        if self.widget.measure_temperature_cb.isChecked():
            if self.bg_collected_for is None or not caget(lf_PVs['lf_get_accs']) == self.bg_collected_for:
                msg = QtWidgets.QMessageBox()
                msg.setText("No BG collected for current T accumulations.\nAre you sure you want to proceed?")
                msg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                retval = msg.exec_()
                if retval == QtWidgets.QMessageBox.No:
                    return
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
        self.widget.stop_pulse_btn.setStyleSheet("font: bold 16px; color: red;")

        while bnc_run_thread.isAlive():
            QtWidgets.QApplication.processEvents()
            time.sleep(0.1)

        self.widget.stop_pulse_btn.setStyleSheet("font: bold 16px; color: black;")

        self.collect_xrd_and_t_info_for_log(xrd=xrd_toggle, temperature=t_toggle)
        self.write_to_log_file()

    def start_pulses_on_thread(self):
        self.pulse_running.emit(True)
        caput(pulse_PVs['BNC_run'], pulse_values['BNC_RUNNING'], wait=True)
        self.wait_until_pulses_end()
        self.pulse_running.emit(False)

    def stop_pulse_btn_clicked(self):
        caput(pulse_PVs['BNC_run'], pulse_values['BNC_STOPPED'], wait=True)

    def start_timing_btn_clicked(self):
        self.timing_adjusted = True
        old_num_pulses = caget(pulse_PVs['BNC_burst_count'])
        temp_num_pulses = 20.0 / caget(pulse_PVs['BNC_period'])
        caput_lf(pulse_PVs['BNC_burst_count'], temp_num_pulses)
        caput(general_PVs['laser_shutter_control'], general_values['laser_shutter_blocking'], wait=True)
        caput(pulse_PVs['BNC_mode'], pulse_values['BNC_BURST'], wait=True)

        bnc_run_thread = Thread(target=self.start_pulses_on_thread)
        bnc_run_thread.start()
        self.widget.stop_pulse_btn.setStyleSheet("font: bold 16px; color: red;")

        while bnc_run_thread.isAlive():
            QtWidgets.QApplication.processEvents()
            time.sleep(0.1)

        self.widget.stop_pulse_btn.setStyleSheet("font: bold 16px; color: black;")

        caput_lf(pulse_PVs['BNC_burst_count'], old_num_pulses)

    def update_bnc_timings(self):
        self.timing_adjusted = False
        self.toggle_percent_and_timing_btns(False)
        QtWidgets.QApplication.processEvents()
        period = caget(pulse_PVs['BNC_period'])
        if period is not None:
            f = 1.0/period
        else:
            f = 1E4
        w = 1.0  # TODO change this to read from settings the pulse width
        ds_percent = caget(laser_PVs['ds_laser_percent'], as_string=False)
        us_percent = caget(laser_PVs['us_laser_percent'], as_string=False)
        ds_us_manual_delay = self.widget.ds_us_manual_delay_sb.value()
        gate_manual_delay = self.widget.gate_manual_delay_sb.value()
        if us_percent is None:
            us_percent = 10.0
        if ds_percent is None:
            ds_percent = 10.0
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
        if value is not None:
            self.widget.ds_percent_display_le.setText(str(round(value, 2)))

    def us_laser_percent_changed(self, value=None, char_value=None):
        if value is None:
            value = caget(laser_PVs['us_laser_percent'])
        if value is not None:
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
        self.timing_adjusted = True

    def gate_manual_delay_changed(self):
        self.update_bnc_timings()
        self.timing_adjusted = True

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
        self.log_info['total_gate_delay'] = caget(pulse_PVs['BNC_T4_delay'])
        self.log_info['manual_gate_delay'] = self.widget.gate_manual_delay_sb.value()
        self.log_info['ds_width'] = caget(pulse_PVs['BNC_T1_delay'])
        self.log_info['us_width'] = caget(pulse_PVs['BNC_T2_delay'])
        self.log_info['num_t_frames'] = caget(lf_PVs['lf_get_frames'])
        self.log_info['num_t_accumulations'] = caget(lf_PVs['lf_get_accs'])
        self.log_info['t_exp_time_per_frame'] = self.log_info['pulse_width'] * self.log_info['num_t_accumulations']
        self.log_info['shutter'] = caget(general_PVs['laser_shutter_status'])
        self.log_info['xrd_exp_time'] = self.log_info['pulse_width'] * caget(pil3_PVs['exposures_per_image'])

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

    def write_headings(self):
        for item in self.log_order:
            self.log_file.write(item + '\t')
        self.log_file.write('\n')
        self.log_file.flush()

    def wait_until_pulses_end(self):
        while caget(pulse_PVs['BNC_run']) == pulse_values['BNC_RUNNING']:
            time.sleep(0.1)

    def collect_quenched_xrd_btn_clicked(self):
        self.log_file = open(self.main_widget.config_widget.log_path_le.text(), 'a')

        if self.first_run:
            self.write_headings()
            self.first_run = False
        caput(general_PVs['laser_shutter_control'], general_values['laser_shutter_blocking'], wait=True)
        caput(pil3_PVs['Acquire'], 1, wait=False)
        caput(pulse_PVs['BNC_mode'], pulse_values['BNC_BURST'], wait=True)
        self.collect_info_for_log()

        bnc_run_thread = Thread(target=self.start_pulses_on_thread)
        bnc_run_thread.start()

        while bnc_run_thread.isAlive():
            QtWidgets.QApplication.processEvents()
            time.sleep(0.1)

        self.collect_xrd_and_t_info_for_log(xrd=True, temperature=False)
        self.write_to_log_file()
        self.log_file.close()

    def measure_t_background_btn_clicked(self):
        lf_experiment = caget(lf_PVs['lf_get_experiment'], as_string=True)
        if lf_experiment == lf_values['PIMAX_normal']:
            return
        elif lf_experiment == lf_values['PIMAX_pulsed']:
            pass
        else:
            return

        previous_settings = {}
        previous_settings[lf_PVs['lf_set_frames']] = caget(lf_PVs['lf_get_frames'])
        previous_settings[general_PVs['xrd_shutter_control']] = caget(general_PVs['xrd_shutter_status'])
        previous_settings[general_PVs['ds_light_control']] = caget(general_PVs['ds_light_status'])
        previous_settings[general_PVs['us_light_control']] = caget(general_PVs['us_light_status'])

        caput(general_PVs['xrd_shutter_control'], general_values['xrd_shutter_closed'])
        caput(general_PVs['ds_light_control'], general_values['light_off'])
        caput(general_PVs['us_light_control'], general_values['light_off'])

        caput(general_PVs['laser_shutter_control'], general_values['laser_shutter_blocking'], wait=True)
        caput_lf(lf_PVs['lf_set_trigger_mode'], lf_values['PIMAX_trigger_internal'])
        caput_lf(lf_PVs['lf_set_internal_trigger_freq'], 1E4)
        caput_lf(lf_PVs['lf_set_frames'], 1)
        caput_lf(lf_PVs['lf_set_image_mode'], lf_values['lf_image_mode_background'])
        caput_lf(lf_PVs['lf_set_bg_file_name'], lf_values['PIMAX_pulsed_bg_file_name'])
        caput_lf(lf_PVs['lf_acquire'], 1, wait=True)
        caput_lf(lf_PVs['lf_set_trigger_mode'], lf_values['PIMAX_trigger_external'])
        caput_lf(lf_PVs['lf_set_image_mode'], lf_values['lf_image_mode_normal'])
        for item in previous_settings:
            if item in lf_PVs:
                caput_lf(item, previous_settings[item], wait=True)
            elif item in pil3_PVs:
                caput_pil3(item, previous_settings[item], wait=True)
            else:
                caput(item, previous_settings[item], wait=True)
        self.bg_collected_for = caget(lf_PVs['lf_get_accs'])

    def multi_gate_toggle_btn_clicked(self):
        self.widget.multi_gate_widget.setVisible(not(self.widget.multi_gate_widget.isVisible()))

    def run_multi_gate_btn_clicked(self):
        gate_delays = self.widget.multi_gate_widget.multi_gate_values_le.text().replace(' ', '').split(',')
        self.start_pulse_btn_clicked(gate_delays)
