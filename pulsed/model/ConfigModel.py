# -*- coding: utf8 -*-
from math import floor


class ConfigModel(object):
    def __init__(self):
        pass

    def calc_frames_and_accs(self, pulses, max_accs, factor, max_frames):
        if pulses < max_accs:
            return pulses, 1

        frames = floor(pulses * factor / max_accs)
        if frames == 0:
            frames = 1
        if frames > max_frames:
            return max_accs, max_frames
        return max_accs, frames
