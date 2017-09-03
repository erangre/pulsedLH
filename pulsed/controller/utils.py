try:
    from epics import caput, caget
except ImportError:
    exit(2)

from .epics_config import lf_PVs, lf_values, pil3_PVs, pil3_values
import time

def caput_lf(pv, value, wait=True):
    if not caget(lf_PVs['lf_detector_state'], as_string=True) == lf_values['lf_detector_idle']:
        return False
    t0 = time.time()

    caput(pv, value, wait=wait)

    while time.time() - t0 < 20.0:
        time.sleep(0.02)
        if caget(lf_PVs['lf_detector_state'], as_string=True) == lf_values['lf_detector_idle']:
            return True
    return False


def caput_pil3(pv, value, wait=True):
    t0 = time.time()
    caput(pv, value, wait=wait)

    while time.time() - t0 < 20.0:
        time.sleep(0.02)
        if pil3_values['status_message_ok'] in caget(pil3_PVs['status_message'], as_string=True):
            return True
    return False
