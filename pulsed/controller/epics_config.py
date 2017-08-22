pulse_PVs = {
    'BNC': '13IDD:BNC1:Run',
}

pulse_values = {
    'BNC_RUNNING': 1,
    'BNC_STOPPED': 0,
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
}

laser_values = {
    'modulation_enabled': 1,
    'modulation_disabled': 0,
}
