# -*- coding: utf8 -*-
from qtpy import QtWidgets, QtGui, QtCore


class PulsedLaserHeatingWidget(QtWidgets.QGroupBox):
    def __init__(self, *args, **kwargs):
        super(PulsedLaserHeatingWidget, self).__init__(*args, **kwargs)

        self.ten_percent_btn = QtWidgets.QPushButton('10%')
        self.zero_btn = QtWidgets.QPushButton('Zero')
        self.laser_percent_tweak_le = QtWidgets.QLineEdit('0.1')
        self.ds_increase_percent_btn = QtWidgets.QPushButton('\u25b2')
        self.ds_decrease_percent_btn = QtWidgets.QPushButton('\u25bc')
        self.us_increase_percent_btn = QtWidgets.QPushButton('\u25b2')
        self.us_decrease_percent_btn = QtWidgets.QPushButton('\u25bc')
        self.both_increase_percent_btn = QtWidgets.QPushButton('\u25b2')
        self.both_decrease_percent_btn = QtWidgets.QPushButton('\u25bc')

        self.style_widgets()

    def style_widgets(self):
        self.laser_percent_tweak_le.setValidator(QtGui.QDoubleValidator())
