# -*- coding: utf8 -*-
import os
import time
from sys import platform as _platform
from qtpy import QtWidgets, QtCore, QtGui

from epics import caget, caput, PV

from ..widgets.MainWidget import MainWidget
from .ModeSwitchController import ModeSwitchController
from .PulsedHeatingController import PulsedHeatingController
from .epics_config import pulse_PVs, pulse_values, laser_PVs, laser_values, lf_PVs, lf_values, pil3_PVs, pil3_values

MAIN_STATUS_OFF = 'Stopped'
MAIN_STATUS_ON = 'Running'
LASER_STATUS_NORMAL = 'CW'
LASER_STATUS_PULSED = 'Pulsed'
PIMAX_STATUS_NORMAL = 'Normal'
PIMAX_STATUS_PULSED = 'Pulsed'
LASER_EMISSION_OFF = 'Off'
LASER_EMISSION_ON = 'On'
MODE_PULSED = 'Pulsed Mode'
MODE_NORMAL = 'CW Mode'
MODE_MIXED = 'Warning: Mixed Mode!'
PIL3_STATUS_PULSED = 'Pulsed'
PIL3_STATUS_NORMAL = 'Normal'


class MainController(object):

    # pv_changed = QtCore.Signal(dict)

    def __init__(self, use_settings=True, settings_directory='default'):
        # super(MainController, self).__init__()
        self.use_settings = use_settings
        self.callbacks = {}
        self.widget = MainWidget()
        self.num_of_pulsed_status_pvs = 0

        # create data
        if settings_directory == 'default':
            self.settings_directory = os.path.join(os.path.expanduser("~"), '.pulsed')
        else:
            self.settings_directory = settings_directory

        # self.model = pulsed_lh_model()
        self.mode_switch_controller = ModeSwitchController(self.widget)
        self.pulsed_heating_controller = PulsedHeatingController(self.widget)

        self.update_main_status()
        self.update_laser_status()
        self.update_pimax_status()
        self.update_pil3_status()
        self.prepare_connections()
        self.create_monitors()
        self.update_main_mode_status()

        # if use_settings:
        #     self.load_default_settings()

    def show_window(self):
        """
        Displays the main window on the screen and makes it active.
        """
        self.widget.show()

        # if _platform == "darwin":
        #     self.widget.setWindowState(
        #         self.widget.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
        #     self.widget.activateWindow()
        #     self.widget.raise_()

    def prepare_connections(self):
        self.widget.mode_switch_btn.clicked.connect(self.switch_tabs)
        self.widget.pulsed_laser_heating_btn.clicked.connect(self.switch_tabs)
        # self.pv_changed.connect(self.pv_changed_emitted)
        self.callbacks[pulse_PVs['BNC_run']] = self.update_main_status
        self.callbacks[laser_PVs['ds_emission_status']] = self.update_ds_laser_emission_status
        self.callbacks[laser_PVs['us_emission_status']] = self.update_us_laser_emission_status
        self.callbacks[laser_PVs['ds_modulation_status']] = self.update_ds_laser_modulation_status
        self.callbacks[laser_PVs['us_modulation_status']] = self.update_us_laser_modulation_status
        self.callbacks[lf_PVs['lf_get_experiment']] = self.update_pimax_status
        self.callbacks[laser_PVs['ds_laser_percent']] = self.pulsed_heating_controller.ds_laser_percent_changed
        self.callbacks[laser_PVs['us_laser_percent']] = self.pulsed_heating_controller.us_laser_percent_changed
        self.callbacks[pil3_PVs['trigger_mode']] = self.update_pil3_status

    def update_main_status(self, value=None, char_value=None):
        if value is None:
            value = caget(pulse_PVs['BNC_run'], as_string=False)
        if value == pulse_values['BNC_RUNNING']:
            self.widget.main_status.setText(MAIN_STATUS_ON)
            self.widget.main_status.setStyleSheet("font: bold 24px; color: red;")
        else:
            self.widget.main_status.setText(MAIN_STATUS_OFF)
            self.widget.main_status.setStyleSheet("font: bold 24px; color: black;")

    def update_main_mode_status(self):
        count_pulsed = 0
        if self.widget.laser_ds_status.text() == LASER_STATUS_PULSED:
            count_pulsed += 1
        if self.widget.laser_us_status.text() == LASER_STATUS_PULSED:
            count_pulsed += 1
        if self.widget.pimax_status.text() == PIMAX_STATUS_PULSED:
            count_pulsed += 1
        if self.widget.pil3_status.text() == PIL3_STATUS_PULSED:
            count_pulsed += 1

        if count_pulsed == self.num_of_pulsed_status_pvs:
            self.widget.main_mode_status.setText(MODE_PULSED)
            self.widget.main_mode_status.setStyleSheet("font: bold 24px; color: blue;")
        elif count_pulsed == 0:
            self.widget.main_mode_status.setText(MODE_NORMAL)
            self.widget.main_mode_status.setStyleSheet("font: bold 24px; color: black;")
        else:
            self.widget.main_mode_status.setText(MODE_MIXED)
            self.widget.main_mode_status.setStyleSheet("font: bold 24px; color: red;")

    def update_ds_laser_emission_status(self, value=None, char_value=None):
        if value is None:
            value = caget(laser_PVs['ds_emission_status'])
        if value == laser_values['emission_off']:
            self.widget.laser_ds_emission_status.setText(LASER_EMISSION_OFF)
            self.widget.laser_ds_emission_status.setStyleSheet("font: bold 18px; color: black;")
            self.widget.mode_switch_widget.ds_laser_normal_btn.setEnabled(True)
            self.widget.mode_switch_widget.ds_laser_pulsed_btn.setEnabled(True)
        else:
            self.widget.laser_ds_emission_status.setText(LASER_EMISSION_ON)
            self.widget.laser_ds_emission_status.setStyleSheet("font: bold 18px; color: red;")
            self.widget.mode_switch_widget.ds_laser_normal_btn.setEnabled(False)
            self.widget.mode_switch_widget.ds_laser_pulsed_btn.setEnabled(False)

    def update_us_laser_emission_status(self, value=None, char_value=None):
        if value is None:
            value = caget(laser_PVs['us_emission_status'])
        if value == laser_values['emission_off']:
            self.widget.laser_us_emission_status.setText(LASER_EMISSION_OFF)
            self.widget.laser_us_emission_status.setStyleSheet("font: bold 18px; color: black;")
            self.widget.mode_switch_widget.us_laser_normal_btn.setEnabled(True)
            self.widget.mode_switch_widget.us_laser_pulsed_btn.setEnabled(True)
        else:
            self.widget.laser_us_emission_status.setText(LASER_EMISSION_ON)
            self.widget.laser_us_emission_status.setStyleSheet("font: bold 18px; color: red;")
            self.widget.mode_switch_widget.us_laser_normal_btn.setEnabled(False)
            self.widget.mode_switch_widget.us_laser_pulsed_btn.setEnabled(False)

    def update_ds_laser_modulation_status(self, value=None, char_value=None):
        if value is None:
            value = caget(laser_PVs['ds_modulation_status'])
        if value == laser_values['modulation_disabled']:
            self.widget.laser_ds_status.setText(LASER_STATUS_NORMAL)
            self.widget.laser_ds_status.setStyleSheet("font: bold 18px; color: black;")
        else:
            self.widget.laser_ds_status.setText(LASER_STATUS_PULSED)
            self.widget.laser_ds_status.setStyleSheet("font: bold 18px; color: blue;")
        self.update_main_mode_status()

    def update_us_laser_modulation_status(self, value=None, char_value=None):
        if value is None:
            value = caget(laser_PVs['us_modulation_status'])
        if value == laser_values['modulation_disabled']:
            self.widget.laser_us_status.setText(LASER_STATUS_NORMAL)
            self.widget.laser_us_status.setStyleSheet("font: bold 18px; color: black;")
        else:
            self.widget.laser_us_status.setText(LASER_STATUS_PULSED)
            self.widget.laser_us_status.setStyleSheet("font: bold 18px; color: blue;")
        self.update_main_mode_status()

    def update_laser_status(self):
        self.update_ds_laser_emission_status()
        self.update_us_laser_emission_status()
        self.update_ds_laser_modulation_status()
        self.update_us_laser_modulation_status()

    def update_pimax_status(self, value=None, char_value=None):
        if char_value is None:
            char_value = caget(lf_PVs['lf_get_experiment'], as_string=True)
        if char_value == lf_values['PIMAX_pulsed']:
            self.widget.pimax_status.setText(PIMAX_STATUS_PULSED)
            self.widget.pimax_status.setStyleSheet("font: bold 18px; color: blue;")
        else:
            self.widget.pimax_status.setText(PIMAX_STATUS_NORMAL)
            self.widget.pimax_status.setStyleSheet("font: bold 18px; color: black;")
        self.update_main_mode_status()

    def update_pil3_status(self, value=None, char_value=None):
        if value is None:
            value = caget(pil3_PVs['trigger_mode'])
        if char_value == pil3_values['trigger_external_enable']:
            self.widget.pil3_status.setText(PIL3_STATUS_PULSED)
            self.widget.pimax_status.setStyleSheet("font: bold 18px; color: blue;")
        else:
            self.widget.pil3_status.setText(PIL3_STATUS_NORMAL)
            self.widget.pimax_status.setStyleSheet("font: bold 18px; color: black;")
        self.update_main_mode_status()

    def switch_tabs(self):
        if self.widget.pulsed_laser_heating_btn.isChecked():
            self.widget.pulsed_laser_heating_widget.setVisible(True)
            self.widget.mode_switch_widget.setVisible(False)
        elif self.widget.mode_switch_btn.isChecked():
            self.widget.pulsed_laser_heating_widget.setVisible(False)
            self.widget.mode_switch_widget.setVisible(True)
        self.widget.fix_sizes()

    def create_monitors(self):
        self.pv_bnc_running = PV(pulse_PVs['BNC_run'])
        self.pv_bnc_running.add_callback(self.pv_changed_value)

        self.pv_ds_laser_emission = PV(laser_PVs['ds_emission_status'])
        self.pv_ds_laser_emission.add_callback(self.pv_changed_value)
        self.pv_us_laser_emission = PV(laser_PVs['us_emission_status'])
        self.pv_us_laser_emission.add_callback(self.pv_changed_value)

        self.pv_ds_laser_modulation = PV(laser_PVs['ds_modulation_status'])
        self.pv_ds_laser_modulation.add_callback(self.pv_changed_value)
        self.pv_us_laser_modulation = PV(laser_PVs['us_modulation_status'])
        self.pv_us_laser_modulation.add_callback(self.pv_changed_value)

        if self.pv_ds_laser_modulation.connected:
            self.num_of_pulsed_status_pvs += 1
        if self.pv_us_laser_modulation.connected:
            self.num_of_pulsed_status_pvs += 1

        self.pv_pimax_experiment = PV(lf_PVs['lf_get_experiment'])
        self.pv_pimax_experiment.add_callback(self.pv_changed_value)
        if self.pv_pimax_experiment.connected:
            self.num_of_pulsed_status_pvs += 1

        self.pv_pil3_trigger_mode = PV(pil3_PVs['trigger_mode'])
        self.pv_pil3_trigger_mode.add_callback(self.pv_changed_value)
        if self.pv_pil3_trigger_mode.connected:
            self.num_of_pulsed_status_pvs += 1

        self.pv_ds_laser_percent = PV(laser_PVs['ds_laser_percent'])
        self.pv_ds_laser_percent.add_callback(self.pv_changed_value)

        self.pv_us_laser_percent = PV(laser_PVs['us_laser_percent'])
        self.pv_us_laser_percent.add_callback(self.pv_changed_value)

    def pv_changed_value(self, **kwargs):
        current_callback = self.callbacks[kwargs.get('pvname', None)]
        if current_callback:
            current_callback(kwargs.get('value', None), kwargs.get('char_value', None))

    # def pv_changed_emitted(self, kwargs):
    #     print("signal emitted")
    #     current_callback = self.callbacks[kwargs.get('pvname', None)]
    #     if current_callback:
    #         current_callback(kwargs.get('value', None))
    #     print(kwargs['pvname'])
    #     print(kwargs['value'])
    #     print(kwargs['char_value'])
