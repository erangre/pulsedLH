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

        self.pimax_lbl = QtWidgets.QLabel('PIMAX Mode:')
        self.pimax_to_normal_btn = QtWidgets.QPushButton('Normal')
        self.pimax_to_pulsed_btn = QtWidgets.QPushButton('Pulsed')
        self.pimax_btn_group = QtWidgets.QButtonGroup()
        self.pimax_btn_group.addButton(self.pimax_to_normal_btn)
        self.pimax_btn_group.addButton(self.pimax_to_pulsed_btn)

        self.pil3_lbl = QtWidgets.QLabel('Pilatus 3 Mode:')
        self.pil3_to_normal_btn = QtWidgets.QPushButton('Normal')
        self.pil3_to_pulsed_btn = QtWidgets.QPushButton('Pulsed')
        self.pil3_btn_group = QtWidgets.QButtonGroup()
        self.pil3_btn_group.addButton(self.pil3_to_normal_btn)
        self.pil3_btn_group.addButton(self.pil3_to_pulsed_btn)

        self.all_lbl = QtWidgets.QLabel('All Mode:')
        self.all_to_normal_btn = QtWidgets.QPushButton('Normal')
        self.all_to_pulsed_btn = QtWidgets.QPushButton('Pulsed')

        self.all_btn_group = QtWidgets.QButtonGroup()
        self.all_btn_group.addButton(self.all_to_normal_btn)
        self.all_btn_group.addButton(self.all_to_pulsed_btn)

        self._grid_layout.addWidget(self.ds_laser_lbl, 0, 0)
        self._grid_layout.addWidget(self.ds_laser_normal_btn, 0, 1)
        self._grid_layout.addWidget(self.ds_laser_pulsed_btn, 0, 2)
        self._grid_layout.addWidget(self.us_laser_lbl, 1, 0)
        self._grid_layout.addWidget(self.us_laser_normal_btn, 1, 1)
        self._grid_layout.addWidget(self.us_laser_pulsed_btn, 1, 2)
        self._grid_layout.addWidget(self.pimax_lbl, 2, 0)
        self._grid_layout.addWidget(self.pimax_to_normal_btn, 2, 1)
        self._grid_layout.addWidget(self.pimax_to_pulsed_btn, 2, 2)
        self._grid_layout.addWidget(self.pil3_lbl, 3, 0)
        self._grid_layout.addWidget(self.pil3_to_normal_btn, 3, 1)
        self._grid_layout.addWidget(self.pil3_to_pulsed_btn, 3, 2)
        self._grid_layout.addWidget(self.all_lbl, 4, 0)
        self._grid_layout.addWidget(self.all_to_normal_btn, 4, 1)
        self._grid_layout.addWidget(self.all_to_pulsed_btn, 4, 2)

        self.setLayout(self._main_layout)

        self.style_widgets()

    def style_widgets(self):
        self.ds_laser_normal_btn.setCheckable(True)
        self.ds_laser_pulsed_btn.setCheckable(True)
        self.us_laser_normal_btn.setCheckable(True)
        self.us_laser_pulsed_btn.setCheckable(True)
        self.pimax_to_normal_btn.setCheckable(True)
        self.pimax_to_pulsed_btn.setCheckable(True)
        self.pil3_to_normal_btn.setCheckable(True)
        self.pil3_to_pulsed_btn.setCheckable(True)
