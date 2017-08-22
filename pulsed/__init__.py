# -*- coding: utf8 -*-

from __future__ import absolute_import

import sys

try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO
import traceback
from qtpy import QtWidgets

#
# resources_path = os.path.join(os.path.dirname(__file__), 'resources')
# calibrants_path = os.path.join(resources_path, 'calibrants')
# icons_path = os.path.join(resources_path, 'icons')
# data_path = os.path.join(resources_path, 'data')
# style_path = os.path.join(resources_path, 'style')


def excepthook(exc_type, exc_value, traceback_obj):
    tb_info_file = StringIO()
    traceback.print_tb(traceback_obj, None, tb_info_file)
    tb_info_file.seek(0)
    tb_info = tb_info_file.read()
    errmsg = '%s: \n%s' % (str(exc_type), str(exc_value))
    sections = [errmsg, tb_info]
    msg = '\n'.join(sections)
    print(msg)


def main():
    app = QtWidgets.QApplication([])
    sys.excepthook = excepthook
    from sys import platform as _platform
    from .controller.MainController import MainController

    controller = MainController()
    controller.show_window()
    app.exec_()
    del app
