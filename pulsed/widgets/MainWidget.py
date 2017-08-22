# -*- coding: utf8 -*-
from qtpy import QtWidgets, QtGui, QtCore


class MainWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(MainWidget, self).__init__(*args, **kwargs)

        self._outer_layout = QtWidgets.QVBoxLayout()

        self._status_layout = QtWidgets.QVBoxLayout()
        self._component_status_layout = QtWidgets.QHBoxLayout()

        self._main_layout = QtWidgets.QVBoxLayout()

        self.main_status = QtWidgets.QLabel()
