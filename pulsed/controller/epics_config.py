PIMAX_OFFLINE = True
PILATUS_OFFLINE = True

pil3_prefix = '13PIL3:cam1:'

pil3_PVs = {
    'trigger_mode': pil3_prefix + 'TriggerMode',
    'exposures_per_image': pil3_prefix + 'NumExposures',
    'exposure_time': pil3_prefix + 'AcquireTime',
    'threshold_apply': pil3_prefix + 'ThresholdApply',
    'status_message': pil3_prefix + 'StatusMessage_RBV',
    'Acquire': pil3_prefix + 'Acquire',
    'file_name': pil3_prefix.replace('cam1', 'TIFF1') + 'FullFileName_RBV',
}

pil3_values = {
    'trigger_external_enable': 1,
    'trigger_internal': 0,
    'status_message_ok': 'OK',
}

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
    'BNC_T4_enable': bnc_prefix + 'P4:State',
    'BNC_burst_count': bnc_prefix + 'BurstCount',
    'BNC_T1_Amplitude': bnc_prefix + 'P1:Amplitude',
    'BNC_T2_Amplitude': bnc_prefix + 'P2:Amplitude',
    'BNC_T4_Amplitude': bnc_prefix + 'P4:Amplitude',
}

pulse_values = {
    'BNC_RUNNING': 1,
    'BNC_STOPPED': 0,
    'BNC_BURST': 2,
    'BNC_NORMAL': 0,
    'BNC_ENABLE': 1,
    'BNC_DISABLE': 0,
    'DETECTOR_GATE_AMPLITUDE': 7.0,
    'LASER_GATE_AMPLITUDE': 10.0,
}

unidig1_prefix = "13IDD:Unidig1"
unidig2_prefix = "13IDD:Unidig2"

general_PVs = {
    'laser_shutter_status': unidig2_prefix + 'Bi4.VAL',
    'laser_shutter_control': unidig2_prefix + 'Bo4',
    'pilatus_gate_control': unidig2_prefix + 'Bo20',
    'laser_glass_slides_status': unidig2_prefix + 'Bi6.VAL',
    'laser_glass_slides_control': unidig2_prefix + 'Bo6',
    'xrd_shutter_control': unidig1_prefix + 'Bo11',
    'xrd_shutter_status': unidig1_prefix + 'Bi11.VAL',
    'ds_light_control': unidig1_prefix + 'Bo22',
    'ds_light_status': unidig1_prefix + 'Bi22.VAL',
    'us_light_control': unidig1_prefix + 'Bo20',
    'us_light_status': unidig1_prefix + 'Bi20.VAL',
    'laser_enable_control': '13IDD:LaserPLC:UserModeEnableRequest',
}

general_values = {
    'laser_shutter_blocking': 0,
    'laser_shutter_clear': 1,
    'pilatus_gate_control_BNC': 1,
    'pilatus_gate_control_XPS': 0,
    'laser_glass_slides_in': 0,
    'laser_glass_slides_out': 1,
    'xrd_shutter_closed': 1,
    'xrd_shutter_open': 0,
    'light_off': 0,
    'light_on': 1,
}

laser1_prefix = '13IDD:Laser1'
laser2_prefix = '13IDD:Laser2'

laser_PVs = {
    'ds_enable_modulation': laser2_prefix + 'EnableModulation.PROC',
    'ds_disable_modulation': laser2_prefix + 'DisableModulation.PROC',
    'ds_modulation_status': laser2_prefix + 'Modulation',
    'us_enable_modulation': laser1_prefix + 'EnableModulation.PROC',
    'us_disable_modulation': laser1_prefix + 'DisableModulation.PROC',
    'us_modulation_status': laser1_prefix + 'Modulation',
    'ds_laser_percent': '13IDD:DAC2_4.VAL',
    'ds_laser_percent_tweak': '13IDD:DAC2_4_tweakVal',
    'us_laser_percent': '13IDD:DAC2_3.VAL',
    'us_laser_percent_tweak': '13IDD:DAC2_3_tweakVal',
    'ds_emission_status': laser2_prefix + 'Emission',
    'us_emission_status': laser1_prefix + 'Emission',
    'ds_laser_power_supply': laser2_prefix + 'PowerSupply',
    'us_laser_power_supply': laser1_prefix + 'PowerSupply',
    'ds_diode_current': laser2_prefix + 'DiodeCurrent',
    'us_diode_current': laser1_prefix + 'DiodeCurrent',
}

laser_values = {
    'modulation_enabled': 1,
    'modulation_disabled': 0,
    'emission_off': 0,
    'emission_on': 1,
    'power_supply_on': 0,
    'power_supply_off': 1,
}

lf_prefix = '13IDDLF1:cam1:'

lf_PVs = {
    'lf_set_experiment': lf_prefix + 'LFExperimentName',
    'lf_get_experiment': lf_prefix + 'LFExperimentName_RBV',
    'lf_set_trigger_mode': lf_prefix + 'TriggerMode',
    'lf_get_trigger_mode': lf_prefix + 'TriggerMode_RBV',
    'lf_detector_state': lf_prefix + 'DetectorState_RBV',
    'lf_last_file_name': lf_prefix + 'LFFileName_RBV',
    'lf_full_file_name': lf_prefix + 'FullFileName_RBV',
    'lf_acquire': lf_prefix + 'Acquire',
    'lf_get_accs': lf_prefix + 'NumAccumulations_RBV',
    'lf_set_accs': lf_prefix + 'NumAccumulations',
    'lf_get_frames': lf_prefix + 'NumImages_RBV',
    'lf_set_frames': lf_prefix + 'NumImages',
    'lf_get_bg_file_name': lf_prefix + 'LFBackgroundFile_RBV',
    'lf_set_bg_file_name':lf_prefix + 'LFBackgroundFile',
    'lf_set_image_mode': lf_prefix + 'ImageMode',
    'lf_get_image_mode': lf_prefix + 'ImageMode_RBV',
    'lf_set_internal_trigger_freq': lf_prefix + 'LFTriggerFrequency',
    'lf_gate_width': lf_prefix + 'LFRepGateWidth',
}

lf_values = {
    'PIMAX_normal': 'PIMAX_temperature',
    'PIMAX_pulsed': 'PIMAX_temperature_pulsed',
    'lf_detector_idle': 'Idle',
    'lf_Done': 0,
    'lf_Acquiring': 1,
    'PIMAX_normal_bg_file_name': 'b_pimax',
    'PIMAX_pulsed_bg_file_name': 'b_pimax_pulsed',
    'PIMAX_trigger_internal': 0,
    'PIMAX_trigger_external': 1,
    'lf_image_mode_normal': 0,
    'lf_image_mode_background': 2,
}

# ignore this so far:
# pilw_prefix = '13PIL3:cam1:'
#
# pilw_PVs = {
#     'trigger_mode': pilw_prefix + 'TriggerMode',
#     'exposures_per_image': pilw_prefix + 'NumExposures',
#     'exposure_time': pilw_prefix + 'AcquireTime',
#     'threshold_apply': pilw_prefix + 'ThresholdApply',
#     'status_message': pilw_prefix + 'StatusMessage_RBV',
#     'Acquire': pilw_prefix + 'Acquire',
#     'file_name': pilw_prefix.replace('cam1', 'TIFF1') + 'FullFileName_RBV',
# }
#
# pilw_values = {
#     'trigger_external_enable': 1,
#     'trigger_internal': 0,
#     'status_message_ok': 'OK',
# }
