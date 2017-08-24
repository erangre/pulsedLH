bnc_prefix = '13IDD:BNC1:'

pulse_PVs = {
    'BNC_run': bnc_prefix + 'Run',
    'BNC_mode': bnc_prefix + 'Mode',
    'BNC_period': bnc_prefix + 'Period',
    'BNC_T1_width': bnc_prefix + 'P1:Width',
    'BNC_T2_width': bnc_prefix + 'P2:Width',
    'BNC_T4_width': bnc_prefix + 'P4:Width',
    'BNC_T1_delay': bnc_prefix + 'P1:Delay',
    'BNC_T2_delay': bnc_prefix + 'P2:Delay',
    'BNC_T4_delay': bnc_prefix + 'P4:Delay',
}

pulse_values = {
    'BNC_RUNNING': 1,
    'BNC_STOPPED': 0,
    'BNC_BURST': 2,
    'BNC_NORMAL': 0,
}

general_PVs = {
    'laser_shutter_status': '13IDD:Unidig2Bi4.VAL',
    'laser_shutter_control': '13IDD:Unidig2Bo4.VAL',
}

general_values = {
    'laser_shutter_blocking': 0,
    'laser_shutter_clear': 1,
}

laser_PVs = {
    'ds_enable_modulation': '13IDD:Laser2EnableModulation.PROC',
    'ds_disable_modulation': '13IDD:Laser2DisableModulation.PROC',
    'ds_modulation_status': '13IDD:Laser2Modulation',
    'us_enable_modulation': '13IDD:Laser1EnableModulation.PROC',
    'us_disable_modulation': '13IDD:Laser1DisableModulation.PROC',
    'us_modulation_status': '13IDD:Laser1Modulation',
    'ds_laser_percent': '13IDD:DAC2_4.VAL',
    'ds_laser_percent_tweak': '13IDD:DAC2_4_tweakVal',
    'us_laser_percent': '13IDD:DAC2_3.VAL',
    'us_laser_percent_tweak': '13IDD:DAC2_3_tweakVal',
}

laser_values = {
    'modulation_enabled': 1,
    'modulation_disabled': 0,
}

lf_PVs = {
    'lf_set_experiment': '13IDDLF1:cam1:LFExperimentName',
    'lf_get_experiment': '13IDDLF1:cam1:LFExperimentName_RBV',
    'lf_set_trigger_mode': '13IDDLF1:cam1:TriggerMode',
    'lf_get_trigger_mode': '13IDDLF1:cam1:TriggerMode_RBV',
    'lf_detector_state': '13IDDLF1:cam1:DetectorState_RBV',
    'lf_last_file_name': '13IDDLF1:cam1:LFFileName_RBV',
    'lf_acquire': '13IDDLF1:cam1:Acquire',
}

lf_values = {
    'PIMAX_normal': 'PIMAX_temperature',
    'PIMAX_pulsed': 'PIMAX_temperature_pulsed',
    'lf_detector_idle': 'Idle',
    'lf_Done': 0,
    'lf_Acquiring': 1,
}
