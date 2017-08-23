# -*- coding: utf8 -*-
from qtpy import QtWidgets, QtGui, QtCore


class MainWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(MainWidget, self).__init__(*args, **kwargs)

        self._outer_layout = QtWidgets.QVBoxLayout()

        self._status_layout = QtWidgets.QVBoxLayout()
        self._component_status_layout = QtWidgets.QHBoxLayout()

        self._main_layout = QtWidgets.QVBoxLayout()

        self._outer_layout.addLayout(self._status_layout)
        self._outer_layout.addSpacerItem(QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum,
                                                               QtWidgets.QSizePolicy.Expanding))
        self._outer_layout.addLayout(self._main_layout)

        self.main_status = QtWidgets.QLabel()
        self.laser_ds_status_lbl = QtWidgets.QLabel('DS Laser Mode:')
        self.laser_ds_status = QtWidgets.QLabel()
        self.laser_us_status_lbl = QtWidgets.QLabel('US Laser Mode:')
        self.laser_us_status = QtWidgets.QLabel()
        self.pimax_status_lbl = QtWidgets.QLabel('Pimax Mode:')
        self.pimax_status = QtWidgets.QLabel()

        self._component_status_layout.addWidget(self.laser_ds_status_lbl)
        self._component_status_layout.addWidget(self.laser_ds_status)
        self._component_status_layout.addWidget(self.laser_us_status_lbl)
        self._component_status_layout.addWidget(self.laser_us_status)
        self._component_status_layout.addWidget(self.pimax_status_lbl)
        self._component_status_layout.addWidget(self.pimax_status)

        self._status_layout.addWidget(self.main_status)
        self._status_layout.addLayout(self._component_status_layout)

        self.setLayout(self._outer_layout)
        self.style_widgets()

    def style_widgets(self):
        self.laser_ds_status_lbl.setStyleSheet("font: 18px; color: black;")
        self.laser_us_status_lbl.setStyleSheet("font: 18px; color: black;")
        self.pimax_status_lbl.setStyleSheet("font: 18px; color: black;")
