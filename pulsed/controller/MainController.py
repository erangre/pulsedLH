# -*- coding: utf8 -*-
import os
from sys import platform as _platform
from qtpy import QtWidgets, QtCore

from epics import caget, caput

from ..widgets.MainWidget import MainWidget
from .epics_config import pulse_PVs, pulse_values

MAIN_STATUS_OFF = 'Stopped'
MAIN_STATUS_ON = 'Running'
LASER_STATUS_NORMAL = 'CW'
LASER_STATUS_PULSED = 'Pulsed'


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

        self.update_main_status()
        self.update_laser_status()

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
        self.widget.laser_ds_status.setText(LASER_STATUS_NORMAL)
        self.widget.laser_us_status.setText(LASER_STATUS_NORMAL)
