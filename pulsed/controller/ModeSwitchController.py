# -*- coding: utf8 -*-
import os
import time
from sys import platform as _platform
from qtpy import QtWidgets, QtCore

from epics import caget, caput

from ..widgets.MainWidget import MainWidget
from .utils import caput_lf
from .epics_config import pulse_PVs, pulse_values, laser_PVs, laser_values, lf_PVs, lf_values


class ModeSwitchController(object):
    def __init__(self, widget):
        """
        :param widget:
        :type widget: MainWidget
        """
        self.widget = widget
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
        self.widget.mode_switch_widget.all_to_pulsed_btn.clicked.connect(self.all_to_pulsed_btn_clicked)
        self.widget.mode_switch_widget.all_to_normal_btn.clicked.connect(self.all_to_normal_btn_clicked)

    def ds_laser_pulsed_btn_clicked(self):
        t0 = time.time()
        caput(laser_PVs['ds_enable_modulation'], 1, wait=True)
        while time.time() - t0 < 5.0:
            if caget(laser_PVs['ds_modulation_status']) == laser_values['modulation_enabled']:
                return
            # TODO Add here error message that DS laser cannot be changed to pulsed

    def ds_laser_normal_btn_clicked(self):
        t0 = time.time()
        caput(laser_PVs['ds_disable_modulation'], 1, wait=True)
        while time.time() - t0 < 5.0:
            if caget(laser_PVs['ds_modulation_status']) == laser_values['modulation_disabled']:
                return
            # TODO Add here error message that DS laser cannot be changed to normal

    def us_laser_pulsed_btn_clicked(self):
        t0 = time.time()
        caput(laser_PVs['us_enable_modulation'], 1, wait=True)
        while time.time() - t0 < 5.0:
            if caget(laser_PVs['us_modulation_status']) == laser_values['modulation_enabled']:
                return
            # TODO Add here error message that DS laser cannot be changed to pulsed

    def us_laser_normal_btn_clicked(self):
        t0 = time.time()
        caput(laser_PVs['us_disable_modulation'], 1, wait=True)
        while time.time() - t0 < 5.0:
            if caget(laser_PVs['us_modulation_status']) == laser_values['modulation_disabled']:
                return
            # TODO Add here error message that DS laser cannot be changed to normal

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

    def pimax_to_normal_btn_clicked(self):
        caput_lf(lf_PVs['lf_set_experiment'], lf_values['PIMAX_normal'], wait=True)

    def update_pimax_btns_state(self):
        if caget(lf_PVs['lf_get_experiment'], as_string=True) == lf_values['PIMAX_normal']:
            self.widget.mode_switch_widget.pimax_to_normal_btn.setChecked(True)
        elif caget(lf_PVs['lf_get_experiment'], as_string=True) == lf_values['PIMAX_pulsed']:
            self.widget.mode_switch_widget.pimax_to_pulsed_btn.setChecked(True)

    def all_to_normal_btn_clicked(self):
        self.ds_laser_normal_btn_clicked()
        self.us_laser_normal_btn_clicked()
        self.pimax_to_normal_btn_clicked()
        self.update_laser_btns_state()
        self.update_pimax_btns_state()

    def all_to_pulsed_btn_clicked(self):
        self.ds_laser_pulsed_btn_clicked()
        self.us_laser_pulsed_btn_clicked()
        self.pimax_to_pulsed_btn_clicked()
        self.update_laser_btns_state()
        self.update_pimax_btns_state()
