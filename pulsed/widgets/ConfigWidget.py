# -*- coding: utf8 -*-
from qtpy import QtWidgets, QtGui, QtCore


class ConfigWidget(QtWidgets.QGroupBox):
    def __init__(self, *args, **kwargs):
        super(ConfigWidget, self).__init__(*args, **kwargs)

        self._main_layout = QtWidgets.QVBoxLayout()
        self._grid_layout = QtWidgets.QGridLayout()
        self.caption = QtWidgets.QLabel('Configuration')

        self.num_pulses_lbl = QtWidgets.QLabel('# of Pulses:')
        self.num_pulses_sb = QtWidgets.QSpinBox()
        self.pulse_width_lbl = QtWidgets.QLabel('Pulse width (us):')
        self.pulse_width_le = QtWidgets.QLineEdit('1')
        self.pimax_gate_width_lbl = QtWidgets.QLabel('PIMAX gate (us)')
        self.pimax_gate_width_le = QtWidgets.QLineEdit('1')
        self.pimax_max_num_accs_lbl = QtWidgets.QLabel('Max # of PIMAX Accumulations:')
        self.pimax_max_num_accs_sb = QtWidgets.QSpinBox()
        self.pimax_max_num_frames_lbl = QtWidgets.QLabel('Max # of PIMAX Frames:')
        self.pimax_max_num_frames_sb = QtWidgets.QSpinBox()
        self.pimax_num_frames_lbl = QtWidgets.QLabel('# of PIMAX Frames')
        self.pimax_num_frames_le = QtWidgets.QLineEdit('8')

        self.log_path_lbl = QtWidgets.QLabel('Pulsed Heating Log:')
        self.log_path_le = QtWidgets.QLineEdit()
        self.choose_log_path_btn = QtWidgets.QPushButton('Choose File')

        self._grid_layout.addWidget(self.num_pulses_lbl, 0, 0, 1, 1)
        self._grid_layout.addWidget(self.num_pulses_sb, 0, 1, 1, 1)
        self._grid_layout.addWidget(self.pulse_width_lbl, 0, 2, 1, 1)
        self._grid_layout.addWidget(self.pulse_width_le, 0, 3, 1, 1)
        self._grid_layout.addWidget(self.pimax_gate_width_lbl, 0, 4, 1, 1)
        self._grid_layout.addWidget(self.pimax_gate_width_le, 0, 5, 1, 1)
        self._grid_layout.addWidget(self.pimax_max_num_accs_lbl, 1, 0, 1, 1)
        self._grid_layout.addWidget(self.pimax_max_num_accs_sb, 1, 1, 1, 1)
        self._grid_layout.addWidget(self.pimax_max_num_frames_lbl, 1, 2, 1, 1)
        self._grid_layout.addWidget(self.pimax_max_num_frames_sb, 1, 3, 1, 1)
        self._grid_layout.addWidget(self.pimax_num_frames_lbl, 1, 4, 1, 1)
        self._grid_layout.addWidget(self.pimax_num_frames_le, 1, 5, 1, 1)
        self._grid_layout.addWidget(self.log_path_lbl, 2, 0, 1, 1)
        self._grid_layout.addWidget(self.log_path_le, 2, 1, 1, 3)
        self._grid_layout.addWidget(self.choose_log_path_btn, 2, 4, 1, 1)

        self._main_layout.addWidget(self.caption)
        self._main_layout.addLayout(self._grid_layout)

        self.setLayout(self._main_layout)

        self.style_widgets()

    def style_widgets(self):
        self.num_pulses_sb.setRange(1, 100000000)
        self.pimax_max_num_accs_sb.setRange(1, 1000000)
        self.pimax_max_num_frames_sb.setRange(1, 200)
        self.pimax_num_frames_le.setEnabled(False)
