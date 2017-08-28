# -*- coding: utf8 -*-
from math import exp


class WidthDelayModel(object):
    def __init__(self):
        pass

    def calc_all_delays_and_widths(self, f=10000, w=1.0, ds_percent=0.0, us_percent=0.0, ds_us_manual_delay =0.0,
                                   gate_manual_delay=0.0):
        timings = {}
        if ds_percent < 10.0:
            ds_delay = 0.0
            timings['width_t1'] = 1E-6
        else:
            ds_delay = self.calc_ds_delay(f, ds_percent)
            timings['width_t1'] = self.calc_ds_width(f, w, ds_percent) * 1E-6

        if us_percent < 10.0:
            us_delay = 0.0
            timings['width_t2'] = 1E-6
        else:
            us_delay = self.calc_us_delay(f, us_percent)
            timings['width_t2'] = self.calc_us_width(f, w, us_percent) * 1E-6

        timings['width_t4'] = w * 1E-6
        if us_delay >= ds_delay - ds_us_manual_delay:
            timings['delay_t1'] = (us_delay - ds_delay + ds_us_manual_delay) * 1E-6
            timings['delay_t2'] = 0.0
            timings['delay_t4'] = (us_delay + gate_manual_delay) * 1E-6
        else:
            timings['delay_t1'] = 0.0
            timings['delay_t2'] = (ds_delay - us_delay - ds_us_manual_delay) * 1E-6
            timings['delay_t4'] = (ds_delay + gate_manual_delay) * 1E-6
        return timings

    # TODO - find out how to better estimate T4 delay
    # TODO - find out how to make it general for f, and not just 2k and 10k

    def calc_ds_delay(self, f=10000, ds_percent=0.0):
        x = ds_percent
        if f == 10000:
            y0 = 5.59921
            a1 = 17.86787
            t1 = 33.86155
            a2 = 51.54521
            t2 = 8.73576
            a3 = 173.82727
            t3 = 3.44445
        elif f == 2000:
            y0 = 8.91502
            a1 = 48.5665
            t1 = 31.0344
            a2 = 5467.15437
            t2 = 1.74255
            a3 = 234.08518
            t3 = 6.54734
        else:
            return None
        dn_d = a1 * exp(-x / t1) + a2 * exp(-x / t2) + a3 * exp(-x / t3) + y0
        return dn_d

    def calc_ds_width(self, f=10000, w=1.0, ds_percent=0.0):
        x = ds_percent
        if f == 10000:
            y0 = 3.46689
            a1 = 46.6149
            t1 = 8.763
            a2 = 565.44972
            t2 = 2.52871
            a3 = 21.36811
            t3 = 33.02238
        elif f == 2000:
            y0 = 7.91923
            a1 = 401.88866
            t1 = 4.39488
            a2 = 802.75706
            t2 = 2.49365
            a3 = 73.42733
            t3 = 23.761
        else:
            return None
        dn_w = a1 * exp(-x / t1) + a2 * exp(-x / t2) + a3 * exp(-x / t3) + y0 + w - 1.0
        return dn_w

    def calc_us_delay(self, f=10000, us_percent=0.0):
        x = us_percent
        if f == 10000:
            y0 = 6.28051
            a1 = 149.00329
            t1 = 3.00296
            a2 = 26.78538
            t2 = 27.31508
            a3 = 92.90255
            t3 = 5.96622
        elif f == 2000:
            y0 = 7.55121
            a1 = 118.18111
            t1 = 10.92433
            a2 = 34.55431
            t2 = 48.507
            a3 = 989.97189
            t3 = 3.14699
        else:
            return None
        up_d = a1 * exp(-x / t1) + a2 * exp(-x / t2) + a3 * exp(-x / t3) + y0
        return up_d

    def calc_us_width(self, f=10000, w=1.0, us_percent=0.0):
        x = us_percent
        if f == 10000:
            y0 = 4.51345
            a1 = 26.85413
            t1 = 26.85433
            a2 = 31.17528
            t2 = 11.09784
            a3 = 882.92817
            t3 = 2.29394
        elif f == 2000:
            y0 = 8.46117
            a1 = 784.37458
            t1 = 2.33123
            a2 = 405.81113
            t2 = 4.84842
            a3 = 76.62549
            t3 = 26.01205
        else:
            return None
        up_w = a1 * exp(-x / t1) + a2 * exp(-x / t2) + a3 * exp(-x / t3) + y0 + w - 1.0
        return up_w
