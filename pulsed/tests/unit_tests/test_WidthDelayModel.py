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

    def test_calc_delay(self):
        ds_delay = self.model.calc_ds_delay(f=10000, ds_percent=10.0)
        us_delay = self.model.calc_us_delay(f=10000, us_percent=10.0)
        self.assertAlmostEqual(us_delay - ds_delay, 2.73, places=2)
        self.fail()

    def test_calc_ds_width(self):
        ds_width = self.model.calc_ds_width(f=10000, w=1.0, ds_percent=10.0)
        us_width = self.model.calc_us_width(f=10000, w=1.0, us_percent=10.0)
        self.assertAlmostEqual(ds_width, 44.98, places=2)
        self.assertAlmostEqual(us_width, 46.97, places=2)

    def test_calc_final_delays(self):
        timings = self.model.calc_all_delays_and_widths(f=10000, w=1.0, ds_percent=10.0, us_percent=10.0)
        self.assertAlmostEqual(timings['delay_t1'], 2.73E-6, places=9)
        self.assertAlmostEqual(timings['delay_t4'], 47.57E-6, places=9)
