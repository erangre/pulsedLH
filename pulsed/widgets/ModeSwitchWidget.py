# -*- coding: utf8 -*-
from qtpy import QtWidgets, QtGui, QtCore


class ModeSwitchWidget(QtWidgets.QGroupBox):
    def __init__(self, *args, **kwargs):
        super(ModeSwitchWidget, self).__init__(*args, **kwargs)

        self._main_layout = QtWidgets.QVBoxLayout()
        self._grid_layout = QtWidgets.QGridLayout()
        self.caption = QtWidgets.QLabel('Normal/Pulsed Modes')

        self._main_layout.addWidget(self.caption)
        # self._main_layout.addLayout(self._grid_layout)
        #
        # self.ds_laser_lbl = QtWidgets.QLabel('DS Laser Mode:')
        # self.ds_laser_normal_btn = QtWidgets.QPushButton('Normal')
        # self.ds_laser_pulsed_btn = QtWidgets.QPushButton('Pulsed')

        self.setLayout(self._main_layout)
