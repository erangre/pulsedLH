# -*- coding: utf8 -*-

import unittest
import os
import gc

import numpy as np

from ...model.WidthDelayModel import WidthDelayModel

unittest_path = os.path.dirname(__file__)
data_path = os.path.join(unittest_path, '../data')


class WidthDelayModelTest(unittest.TestCase):
    def setUp(self):
        self.model = WidthDelayModel()

    def tearDown(self):
        del self.model
        gc.collect()

    def test_calc_ds_delay(self):
        pass

    def test_calc_ds_width(self):
        pass

    def test_calc_us_delay(self):
        pass

    def test_calc_us_width(self):
        pass
