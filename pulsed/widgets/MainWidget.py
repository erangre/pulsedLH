# -*- coding: utf8 -*-
from qtpy import QtWidgets, QtGui, QtCore
from .PulsedLaserHeatingWidget import PulsedLaserHeatingWidget
from  .ModeSwitchWidget import ModeSwitchWidget


class MainWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(MainWidget, self).__init__(*args, **kwargs)

        self._outer_layout = QtWidgets.QVBoxLayout()

        self._status_layout = QtWidgets.QVBoxLayout()
        self._component_status_layout = QtWidgets.QGridLayout()
        self._tab_button_group = QtWidgets.QButtonGroup()
        self._tab_layout = QtWidgets.QHBoxLayout()

        self._main_layout = QtWidgets.QVBoxLayout()
        self._outer_layout.addLayout(self._status_layout)
        self._outer_layout.addSpacerItem(QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum,
                                                               QtWidgets.QSizePolicy.Minimum))
        self._outer_layout.addLayout(self._tab_layout)

        self._outer_layout.addLayout(self._main_layout)

        self.main_status = QtWidgets.QLabel()
        self.laser_ds_status_lbl = QtWidgets.QLabel('DS Laser Mode:')
        self.laser_ds_status = QtWidgets.QLabel()
        self.laser_us_status_lbl = QtWidgets.QLabel('US Laser Mode:')
        self.laser_us_status = QtWidgets.QLabel()
        self.laser_ds_emission_status_lbl = QtWidgets.QLabel('DS Emission:')
        self.laser_ds_emission_status = QtWidgets.QLabel()
        self.laser_us_emission_status_lbl = QtWidgets.QLabel('US Emission:')
        self.laser_us_emission_status = QtWidgets.QLabel()
        self.pimax_status_lbl = QtWidgets.QLabel('Pimax Mode:')
        self.pimax_status = QtWidgets.QLabel()

        self._component_status_layout.addWidget(self.laser_ds_emission_status_lbl, 0, 0)
        self._component_status_layout.addWidget(self.laser_ds_emission_status, 0, 1)
        self._component_status_layout.addWidget(self.laser_us_emission_status_lbl, 0, 2)
        self._component_status_layout.addWidget(self.laser_us_emission_status, 0, 3)
        self._component_status_layout.addWidget(self.laser_ds_status_lbl, 1, 0)
        self._component_status_layout.addWidget(self.laser_ds_status, 1, 1)
        self._component_status_layout.addWidget(self.laser_us_status_lbl, 1, 2)
        self._component_status_layout.addWidget(self.laser_us_status, 1, 3)
        self._component_status_layout.addWidget(self.pimax_status_lbl, 2, 0)
        self._component_status_layout.addWidget(self.pimax_status, 2, 1)

        self._status_layout.addWidget(self.main_status)
        self._status_layout.addLayout(self._component_status_layout)
        self._outer_layout.addStretch(1)

        self.pulsed_laser_heating_btn = QtWidgets.QPushButton('Control Laser Heating')
        self.mode_switch_btn = QtWidgets.QPushButton('Switch Modes')
        self.configuration_btn = QtWidgets.QPushButton('Configure')

        self._tab_button_group.addButton(self.pulsed_laser_heating_btn)
        self._tab_button_group.addButton(self.mode_switch_btn)
        self._tab_button_group.addButton(self.configuration_btn)
        self._tab_layout.addWidget(self.pulsed_laser_heating_btn)
        self._tab_layout.addWidget(self.mode_switch_btn)
        self._tab_layout.addWidget(self.configuration_btn)

        self.pulsed_laser_heating_widget = PulsedLaserHeatingWidget()
        self.mode_switch_widget = ModeSwitchWidget()
        self._main_layout.addWidget(self.pulsed_laser_heating_widget)
        self._main_layout.addWidget(self.mode_switch_widget)

        self.mode_switch_widget.setVisible(False)

        self.setLayout(self._outer_layout)
        self.style_widgets()

    def style_widgets(self):
        self.laser_ds_emission_status_lbl.setStyleSheet("font: 18px; color: black;")
        self.laser_us_emission_status_lbl.setStyleSheet("font: 18px; color: black;")
        self.laser_ds_status_lbl.setStyleSheet("font: 18px; color: black;")
        self.laser_us_status_lbl.setStyleSheet("font: 18px; color: black;")
        self.pimax_status_lbl.setStyleSheet("font: 18px; color: black;")
        self.pulsed_laser_heating_btn.setCheckable(True)
        self.mode_switch_btn.setCheckable(True)
        self.configuration_btn.setCheckable(True)
        self.pulsed_laser_heating_btn.setChecked(True)
        self.mode_switch_btn.setChecked(False)
        self.configuration_btn.setChecked(False)
        self.fix_sizes()

    def fix_sizes(self):
        tab_rect = QtCore.QRect(11, 139, 477, 23)
        main_rect = QtCore.QRect(11, 159, 477, 120)
        outer_rect = QtCore.QRect(0, 0, 499, 316)
        # widget_rect = QtCore.QRect(640, 340, 499, 442)
        self._tab_layout.setGeometry(tab_rect)
        self._main_layout.setGeometry(main_rect)
        self._outer_layout.setGeometry(outer_rect)
        self.setMaximumHeight(450)
        self.setMinimumHeight(450)
