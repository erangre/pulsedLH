# -*- coding: utf8 -*-
from qtpy import QtWidgets, QtGui, QtCore


class ModeSwitchWidget(QtWidgets.QGroupBox):
    def __init__(self, *args, **kwargs):
        super(ModeSwitchWidget, self).__init__(*args, **kwargs)

        self._main_layout = QtWidgets.QVBoxLayout()
        self._grid_layout = QtWidgets.QGridLayout()
        self.caption = QtWidgets.QLabel('Normal/Pulsed Modes')

        self._main_layout.addWidget(self.caption)
        self._main_layout.addLayout(self._grid_layout)
        self.ds_laser_lbl = QtWidgets.QLabel('DS Laser Mode:')
        self.ds_laser_normal_btn = QtWidgets.QPushButton('Normal')
        self.ds_laser_pulsed_btn = QtWidgets.QPushButton('Pulsed')

        self.ds_laser_btn_group = QtWidgets.QButtonGroup()
        self.ds_laser_btn_group.addButton(self.ds_laser_pulsed_btn)
        self.ds_laser_btn_group.addButton(self.ds_laser_normal_btn)

        self.us_laser_lbl = QtWidgets.QLabel('DS Laser Mode:')
        self.us_laser_normal_btn = QtWidgets.QPushButton('Normal')
        self.us_laser_pulsed_btn = QtWidgets.QPushButton('Pulsed')

        self.us_laser_btn_group = QtWidgets.QButtonGroup()
        self.us_laser_btn_group.addButton(self.us_laser_pulsed_btn)
        self.us_laser_btn_group.addButton(self.us_laser_normal_btn)

        self._grid_layout.addWidget(self.ds_laser_lbl, 0, 0)
        self._grid_layout.addWidget(self.ds_laser_normal_btn, 0, 1)
        self._grid_layout.addWidget(self.ds_laser_pulsed_btn, 0, 2)
        self._grid_layout.addWidget(self.us_laser_lbl, 1, 0)
        self._grid_layout.addWidget(self.us_laser_normal_btn, 1, 1)
        self._grid_layout.addWidget(self.us_laser_pulsed_btn, 1, 2)

        self.setLayout(self._main_layout)

        self.style_widgets()

    def style_widgets(self):
        self.ds_laser_normal_btn.setCheckable(True)
        self.ds_laser_pulsed_btn.setCheckable(True)
        self.us_laser_normal_btn.setCheckable(True)
        self.us_laser_pulsed_btn.setCheckable(True)
