# -*- coding: utf8 -*-


class WidthDelayModel(object):
    def __init__(self):
        self._ds_width = 1E-6
        self._ds_delay = 0.0
        self._us_width = 1E-6
        self._us_delay = 0.0

        self.ds_percent = 0.0
        self.us_percent = 0.0

    @property
    def ds_delay(self):
        return self._ds_delay

    @ds_delay.setter
    def ds_delay(self, value):
        self._ds_delay = value

    @property
    def ds_width(self):
        pass

    @property
    def us_delay(self):
        pass

    @property
    def us_width(self):
        pass
