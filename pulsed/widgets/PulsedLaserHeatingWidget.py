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
        self.start_pulse_btn = QtWidgets.QPushButton('Start')
        self.stop_pulse_btn = QtWidgets.QPushButton('Stop')
        self.start_timing_btn = QtWidgets.QPushButton('Start Timing')
        self.measure_temperature_cb = QtWidgets.QCheckBox('measure T?')
        self.measure_diffraction_cb = QtWidgets.QCheckBox('measure XRD?')
        self.ds_lbl = QtWidgets.QLabel('down-stream')
        self.us_lbl = QtWidgets.QLabel('up-stream')

        self._layout = QtWidgets.QVBoxLayout()
        self._grid_layout = QtWidgets.QGridLayout()
        self.caption = QtWidgets.QLabel('Pulsed Laser Heating')
        self._layout.addWidget(self.caption)
        self._layout.addLayout(self._grid_layout)

        self._grid_layout.addWidget(self.start_timing_btn, 0, 0, 1, 1)
        self._grid_layout.addWidget(self.stop_pulse_btn, 0, 2, 1, 3)
        self._grid_layout.addWidget(self.start_pulse_btn, 0, 6, 1, 1)
        self._grid_layout.addWidget(self.ten_percent_btn, 2, 0)
        self._grid_layout.addWidget(self.both_increase_percent_btn, 2, 3)
        self._grid_layout.addWidget(self.zero_btn, 2, 6)
        self._grid_layout.addWidget(self.ds_lbl, 3, 0, 1, 2)
        self._grid_layout.addWidget(self.laser_percent_tweak_le, 3, 2, 1, 3)
        self._grid_layout.addWidget(self.us_lbl, 3, 5, 1, 2)
        self._grid_layout.addWidget(self.ds_decrease_percent_btn, 4, 0)
        self._grid_layout.addWidget(self.ds_increase_percent_btn, 4, 1)
        self._grid_layout.addWidget(self.both_decrease_percent_btn, 4, 3)
        self._grid_layout.addWidget(self.us_decrease_percent_btn, 4, 5)
        self._grid_layout.addWidget(self.us_increase_percent_btn, 4, 6)

        self.setLayout(self._layout)

        self.style_widgets()

    def style_widgets(self):
        self.laser_percent_tweak_le.setValidator(QtGui.QDoubleValidator())
        self.ds_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.us_lbl.setAlignment(QtCore.Qt.AlignCenter)