from epics import caput, caget
from .epics_config import lf_PVs, lf_values
import time


def caput_lf(pv, value, wait=True):
    t0 = time.time()
    caput(pv, value, wait=wait)

    while time.time() - t0 < 20.0:
        time.sleep(0.02)
        if caget(lf_PVs['lf_detector_state'], as_string=True) == lf_values['lf_detector_idle']:
            return True
    return False
