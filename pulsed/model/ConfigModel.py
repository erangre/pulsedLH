# -*- coding: utf8 -*-
from math import floor


class ConfigModel(object):
    def __init__(self):
        pass

    def calc_frames_and_accs(self, pulses, max_accs, delay_time, max_frames, rate):
        if pulses < max_accs:
            return pulses, 1
        # frames = floor(pulses * delay_time / max_accs)
        frames = floor((pulses/rate)/(max_accs/rate + delay_time))
        if frames == 0:
            frames = 1
        if frames > max_frames:
            return max_accs, max_frames
        return max_accs, frames
