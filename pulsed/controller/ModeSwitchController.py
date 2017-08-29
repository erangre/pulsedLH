# -*- coding: utf8 -*-
import os
import time
from sys import platform as _platform
from qtpy import QtWidgets, QtCore

from epics import caget, caput

from ..widgets.MainWidget import MainWidget
from .utils import caput_lf, caput_pil3
from .epics_config import pulse_PVs, pulse_values, laser_PVs, laser_values, lf_PVs, lf_values, pil3_PVs, pil3_values, \
    general_PVs, general_values


class ModeSwitchController(object):
    def __init__(self, widget):
        """
        :param widget:
        :type widget: MainWidget
        """
        self.widget = widget
        self.old_settings = {}
        self.prepare_connections()
        self.update_laser_btns_state()
        self.update_pimax_btns_state()

    def prepare_connections(self):
        self.widget.mode_switch_widget.ds_laser_pulsed_btn.clicked.connect(self.ds_laser_pulsed_btn_clicked)
        self.widget.mode_switch_widget.ds_laser_normal_btn.clicked.connect(self.ds_laser_normal_btn_clicked)
        self.widget.mode_switch_widget.us_laser_pulsed_btn.clicked.connect(self.us_laser_pulsed_btn_clicked)
        self.widget.mode_switch_widget.us_laser_normal_btn.clicked.connect(self.us_laser_normal_btn_clicked)
        self.widget.mode_switch_widget.pimax_to_pulsed_btn.clicked.connect(self.pimax_to_pulsed_btn_clicked)
        self.widget.mode_switch_widget.pimax_to_normal_btn.clicked.connect(self.pimax_to_normal_btn_clicked)
        self.widget.mode_switch_widget.pil3_to_pulsed_btn.clicked.connect(self.pil3_to_pulsed_btn_clicked)
        self.widget.mode_switch_widget.pil3_to_normal_btn.clicked.connect(self.pil3_to_normal_btn_clicked)
        self.widget.mode_switch_widget.all_to_pulsed_btn.clicked.connect(self.all_to_pulsed_btn_clicked)
        self.widget.mode_switch_widget.all_to_normal_btn.clicked.connect(self.all_to_normal_btn_clicked)

    def ds_laser_pulsed_btn_clicked(self):
        t0 = time.time()
        caput(laser_PVs['ds_enable_modulation'], 1, wait=True)
        while time.time() - t0 < 5.0:
            if caget(laser_PVs['ds_modulation_status']) == laser_values['modulation_enabled']:
                return
        msg = QtWidgets.QMessageBox()
        msg.setText("Cannot switch DS laser to pulsed mode. Make sure emission is off.")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.exec_()

    def ds_laser_normal_btn_clicked(self):
        t0 = time.time()
        caput(laser_PVs['ds_disable_modulation'], 1, wait=True)
        while time.time() - t0 < 5.0:
            if caget(laser_PVs['ds_modulation_status']) == laser_values['modulation_disabled']:
                return

        msg = QtWidgets.QMessageBox()
        msg.setText("Cannot switch DS laser to normal mode. Make sure emission is off.")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.exec_()

    def us_laser_pulsed_btn_clicked(self):
        t0 = time.time()
        caput(laser_PVs['us_enable_modulation'], 1, wait=True)
        while time.time() - t0 < 5.0:
            if caget(laser_PVs['us_modulation_status']) == laser_values['modulation_enabled']:
                return

        msg = QtWidgets.QMessageBox()
        msg.setText("Cannot switch US laser to pulsed mode. Make sure emission is off.")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.exec_()

    def us_laser_normal_btn_clicked(self):
        t0 = time.time()
        caput(laser_PVs['us_disable_modulation'], 1, wait=True)
        while time.time() - t0 < 5.0:
            if caget(laser_PVs['us_modulation_status']) == laser_values['modulation_disabled']:
                return
        msg = QtWidgets.QMessageBox()
        msg.setText("Cannot switch US laser to normal mode. Make sure emission is off.")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.exec_()

    def update_laser_btns_state(self):
        if caget(laser_PVs['ds_modulation_status']) == laser_values['modulation_enabled']:
            self.widget.mode_switch_widget.ds_laser_pulsed_btn.setChecked(True)
        else:
            self.widget.mode_switch_widget.ds_laser_normal_btn.setChecked(True)

        if caget(laser_PVs['us_modulation_status']) == laser_values['modulation_enabled']:
            self.widget.mode_switch_widget.us_laser_pulsed_btn.setChecked(True)
        else:
            self.widget.mode_switch_widget.us_laser_normal_btn.setChecked(True)

    def pimax_to_pulsed_btn_clicked(self):
        caput_lf(lf_PVs['lf_set_experiment'], lf_values['PIMAX_pulsed'], wait=True)
        caput_lf(lf_PVs['lf_set_experiment'], lf_values['PIMAX_pulsed'], wait=True)

    def pimax_to_normal_btn_clicked(self):
        caput_lf(lf_PVs['lf_set_experiment'], lf_values['PIMAX_normal'], wait=True)
        caput_lf(lf_PVs['lf_set_experiment'], lf_values['PIMAX_normal'], wait=True)

    def update_pimax_btns_state(self):
        if caget(lf_PVs['lf_get_experiment'], as_string=True) == lf_values['PIMAX_normal']:
            self.widget.mode_switch_widget.pimax_to_normal_btn.setChecked(True)
        elif caget(lf_PVs['lf_get_experiment'], as_string=True) == lf_values['PIMAX_pulsed']:
            self.widget.mode_switch_widget.pimax_to_pulsed_btn.setChecked(True)

    def pil3_to_pulsed_btn_clicked(self):
        self.old_settings['pilatus_exposure_time'] = caget(pil3_PVs['exposure_time'])
        caput_pil3(pil3_PVs['trigger_mode'], pil3_values['trigger_external_enable'])
        num_pulses = self.widget.config_widget.num_pulses_sb.value()
        caput_pil3(pil3_PVs['exposures_per_image'], num_pulses)
        caput_pil3(pil3_PVs['exposure_time'], 1E-6)  # TODO - read this from config tab
        caput_pil3(pil3_PVs['threshold_apply'], 1)
        caput_pil3(pil3_PVs['threshold_apply'], 1)
        caput_pil3(pil3_PVs['threshold_apply'], 1)
        caput_pil3(general_PVs['pilatus_gate_control'], general_values['pilatus_gate_control_BNC'])

    def pil3_to_normal_btn_clicked(self):
        caput_pil3(pil3_PVs['trigger_mode'], pil3_values['trigger_internal'])
        caput_pil3(pil3_PVs['exposures_per_image'], 1)
        caput_pil3(pil3_PVs['exposure_time'], self.old_settings.get('pilatus_exposure_time', 1.0))
        caput_pil3(pil3_PVs['threshold_apply'], 1)
        caput_pil3(pil3_PVs['threshold_apply'], 1)
        caput_pil3(pil3_PVs['threshold_apply'], 1)
        caput_pil3(general_PVs['pilatus_gate_control'], general_values['pilatus_gate_control_XPS'])

    def update_pil3_btns_state(self):
        if caget(pil3_PVs['trigger_mode']) == pil3_values['trigger_internal']:
            self.widget.mode_switch_widget.pimax_to_normal_btn.setChecked(True)
        elif caget(pil3_PVs['trigger_mode']) == pil3_values['trigger_external_enable']:
            self.widget.mode_switch_widget.pimax_to_pulsed_btn.setChecked(True)

    def all_to_normal_btn_clicked(self):
        self.ds_laser_normal_btn_clicked()
        self.us_laser_normal_btn_clicked()
        self.pimax_to_normal_btn_clicked()
        # self.pil3_to_normal_btn_clicked()
        self.update_laser_btns_state()
        self.update_pimax_btns_state()
        self.update_pil3_btns_state()
        # TODO - uncomment pilatus

    def all_to_pulsed_btn_clicked(self):
        self.ds_laser_pulsed_btn_clicked()
        self.us_laser_pulsed_btn_clicked()
        self.pimax_to_pulsed_btn_clicked()
        # self.pil3_to_pulsed_btn_clicked()
        self.update_laser_btns_state()
        self.update_pimax_btns_state()
        self.update_pil3_btns_state()
        # TODO - uncomment pilatus
