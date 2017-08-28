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
    'BNC_T1_enable': bnc_prefix + 'P1:State',
    'BNC_T2_enable': bnc_prefix + 'P2:State',
    'BNC_T$_enable': bnc_prefix + 'P4:State',
    'BNC_burst_count': bnc_prefix + 'BurstCount'
}

pulse_values = {
    'BNC_RUNNING': 1,
    'BNC_STOPPED': 0,
    'BNC_BURST': 2,
    'BNC_NORMAL': 0,
    'BNC_ENABLE': 1,
    'BNC_DISABLE': 0,
}

general_PVs = {
    'laser_shutter_status': '13IDD:Unidig2Bi4.VAL',
    'laser_shutter_control': '13IDD:Unidig2Bo4.VAL',
    'pilatus_gate_control': '13IDD:Unidig2Bo20',
}

general_values = {
    'laser_shutter_blocking': 0,
    'laser_shutter_clear': 1,
    'pilatus_gate_control_BNC': 1,
    'pilatus_gate_control_XPS': 0,
}

# TODO - maybe change to a prefix like for BNC

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
    'ds_emission_status': '13IDD:Laser2Emission',
    'us_emission_status': '13IDD:Laser1Emission',
}

laser_values = {
    'modulation_enabled': 1,
    'modulation_disabled': 0,
    'emission_off': 0,
    'emission_on': 1,
}

lf_PVs = {
    'lf_set_experiment': '13IDDLF1:cam1:LFExperimentName',
    'lf_get_experiment': '13IDDLF1:cam1:LFExperimentName_RBV',
    'lf_set_trigger_mode': '13IDDLF1:cam1:TriggerMode',
    'lf_get_trigger_mode': '13IDDLF1:cam1:TriggerMode_RBV',
    'lf_detector_state': '13IDDLF1:cam1:DetectorState_RBV',
    'lf_last_file_name': '13IDDLF1:cam1:LFFileName_RBV',
    'lf_acquire': '13IDDLF1:cam1:Acquire',
    'lf_get_accs': '13IDDLF1:cam1:NumAccumulations_RBV',
    'lf_set_accs': '13IDDLF1:cam1:NumAccumulations',
    'lf_get_frames': '13IDDLF1:cam1:NumImages_RBV',
    'lf_set_frames': '13IDDLF1:cam1:NumImages',
}

lf_values = {
    'PIMAX_normal': 'PIMAX_temperature',
    'PIMAX_pulsed': 'PIMAX_temperature_pulsed',
    'lf_detector_idle': 'Idle',
    'lf_Done': 0,
    'lf_Acquiring': 1,
}

pil3_prefix = '13PIL3:cam1:'

pil3_PVs = {
    'trigger_mode': pil3_prefix + 'TriggerMode',
    'exposures_per_image': pil3_prefix + 'NumExposures',
    'exposure_time': pil3_prefix + 'AcquireTime',
    'threshold_apply': pil3_prefix + 'ThresholdApply',
    'status_message': pil3_prefix + 'StatusMessage_RBV',
    'Acquire': pil3_prefix + 'Acquire',
}

pil3_values = {
    'trigger_external_enable': 1,
    'trigger_internal': 0,
    'status_message_ok': 'OK',
}
