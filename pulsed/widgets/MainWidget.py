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

        self._status_layout.addWidget(self.main_status)
        self._status_layout.addLayout(self._component_status_layout)

        self.setLayout(self._outer_layout)
