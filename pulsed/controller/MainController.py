# -*- coding: utf8 -*-
import os
from sys import platform as _platform
from qtpy import QtWidgets, QtCore

from epics import caget, caput

from ..widgets.MainWidget import MainWidget
from .ModeSwitchController import ModeSwitchController
from .PulsedHeatingController import PulsedHeatingController
from .epics_config import pulse_PVs, pulse_values, laser_PVs, laser_values, lf_PVs, lf_values

MAIN_STATUS_OFF = 'Stopped'
MAIN_STATUS_ON = 'Running'
LASER_STATUS_NORMAL = 'CW'
LASER_STATUS_PULSED = 'Pulsed'
PIMAX_STATUS_NORMAL = 'Normal'
PIMAX_STATUS_PULSED = 'Pulsed'


class MainController(object):
    def __init__(self, use_settings=True, settings_directory='default'):
        self.use_settings = use_settings
        self.widget = MainWidget()

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
        self.prepare_connections()

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

    def update_main_status(self):
        if caget(pulse_PVs['BNC'], as_string=False) == pulse_values['BNC_RUNNING']:
            self.widget.main_status.setText(MAIN_STATUS_ON)
            self.widget.main_status.setStyleSheet("font: bold 24px; color: red;")
        else:
            self.widget.main_status.setText(MAIN_STATUS_OFF)
            self.widget.main_status.setStyleSheet("font: bold 24px; color: black;")

    def update_laser_status(self):
        if caget(laser_PVs['ds_modulation_status']) == laser_values['modulation_disabled']:
            self.widget.laser_ds_status.setText(LASER_STATUS_NORMAL)
            self.widget.laser_ds_status.setStyleSheet("font: bold 18px; color: black;")
        else:
            self.widget.laser_ds_status.setText(LASER_STATUS_PULSED)
            self.widget.laser_ds_status.setStyleSheet("font: bold 18px; color: blue;")

        if caget(laser_PVs['us_modulation_status']) == laser_values['modulation_disabled']:
            self.widget.laser_us_status.setText(LASER_STATUS_NORMAL)
            self.widget.laser_us_status.setStyleSheet("font: bold 18px; color: black;")
        else:
            self.widget.laser_us_status.setText(LASER_STATUS_PULSED)
            self.widget.laser_us_status.setStyleSheet("font: bold 18px; color: blue;")

    def update_pimax_status(self):
        if caget(lf_PVs['lf_get_experiment'], as_string=True) == lf_values['PIMAX_pulsed']:
            self.widget.pimax_status.setText(PIMAX_STATUS_PULSED)
            self.widget.pimax_status.setStyleSheet("font: bold 18px; color: blue;")
        else:
            self.widget.pimax_status.setText(PIMAX_STATUS_NORMAL)
            self.widget.pimax_status.setStyleSheet("font: bold 18px; color: black;")

    def prepare_connections(self):
        self.widget.mode_switch_btn.clicked.connect(self.switch_tabs)
        self.widget.pulsed_laser_heating_btn.clicked.connect(self.switch_tabs)

    def switch_tabs(self):
        if self.widget.pulsed_laser_heating_btn.isChecked():
            self.widget.pulsed_laser_heating_widget.setVisible(True)
            self.widget.mode_switch_widget.setVisible(False)
        elif self.widget.mode_switch_btn.isChecked():
            self.widget.pulsed_laser_heating_widget.setVisible(False)
            self.widget.mode_switch_widget.setVisible(True)
