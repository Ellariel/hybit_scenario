'''
This file contains the parameters for wind-turbines and PV-Systems (all located in the area around the steel-plant).

'''

MODEL_SETUPS = {
            # Forschungs WEA Bremen GmbH
        'WT1': {'module_type': 'RE34_104_3400kw', 'max_power': 3.4},
            # WP Powerwind Anlage 1
        'WT2': {'module_type': 'PW90_2500kw', 'max_power': 2.5},  # Replacement power curve
            # WP Industriehäfen
        'WT3': {'module_type': 'E82_E2_2300kw', 'max_power': 2.3},
        'WT4': {'module_type': 'E82_E2_2300kw', 'max_power': 2.3},
            # WP swb Weserwind
        'WT5': {'module_type': 'ANBONUS_2000kw', 'max_power': 2},  # type-data from: https://www.wpd.de/projekte/referenzliste/#
        'WT6': {'module_type': 'ANBONUS_2000kw', 'max_power': 2},  # wasn't stated in Marktstammdatenregister
        'WT7': {'module_type': 'ANBONUS_2000kw', 'max_power': 2},
        'WT8': {'module_type': 'ANBONUS_2000kw', 'max_power': 2},
        'WT9': {'module_type': 'ANBONUS_2000kw', 'max_power': 2},
        'WT10': {'module_type': 'ANBONUS_2000kw', 'max_power': 2},
            # WP Stahlwerk Bremen
        'WT11': {'module_type': 'E82_2000kw', 'max_power': 2},
        'WT12': {'module_type': 'E82_2000kw', 'max_power': 2},
        'WT13': {'module_type': 'ANBONUS_2300kw', 'max_power': 2.3},
        'WT14': {'module_type': 'ANBONUS_2300kw', 'max_power': 2.3},
        'WT15': {'module_type': 'ANBONUS_2300kw', 'max_power': 2.3},
        'WT16': {'module_type': 'ANBONUS_2300kw', 'max_power': 2.3},
            # WP Mittelsbüren
        'WT17': {'module_type': 'E82_2000kw', 'max_power': 2},
        'WT18': {'module_type': 'E82_2000kw', 'max_power': 2},
            # Ölhafen
        'WT19': {'module_type': 'E82_E2_2300kw', 'max_power': 2.3},
            # WP Weserufer WEA 1
        'WT20': {'module_type': 'Senvion34_3400kw', 'max_power': 3.4},
            # WP Hüttenstraße
        'WT21': {'module_type': 'V90_2000kw', 'max_power': 2},
            #PV-panels
        'PV01': {'module_type': 'PV_385Wp', 'no_modules': 257,},
        'PV02': {'module_type': 'PV_375Wp', 'no_modules': 266,},
        'PV03': {'module_type': 'PV_245Wp', 'no_modules': 120,},
        'PV04': {'module_type': 'PV_325Wp', 'no_modules': 34,},
        'PV05': {'module_type': 'PV_345Wp', 'no_modules': 64,},
        'PV06': {'module_type': 'PV_345Wp', 'no_modules': 288,},
        'PV07': {'module_type': 'PV_240Wp', 'no_modules': 1421,},
        'PV08': {'module_type': 'PV_205Wp', 'no_modules': 195,},
        'PV09': {'module_type': 'PV_330Wp', 'no_modules': 228,},
        'PV10': {'module_type': 'PV_235Wp', 'no_modules': 1757,},
        'PV11': {'module_type': 'PV_285Wp', 'no_modules': 34,},
        'PV12': {'module_type': 'PV_285Wp', 'no_modules': 34,},
        'PV13': {'module_type': 'PV_275Wp', 'no_modules': 36,},
        'PV14': {'module_type': 'PV_260Wp', 'no_modules': 30,},
        'PV15': {'module_type': 'PV_95Wp', 'no_modules': 132,},
        'PV16': {'module_type': 'PV_115Wp', 'no_modules': 299,},
        'PV17': {'module_type': 'PV_270Wp', 'no_modules': 108,},
        'PV18': {'module_type': 'PV_275Wp', 'no_modules': 36,},
        'PV19': {'module_type': 'PV_255Wp', 'no_modules': 117,},
        'PV20': {'module_type': 'PV_77_5Wp', 'no_modules': 756,},
        'PV21': {'module_type': 'PV_310Wp', 'no_modules': 164,},
    }

WT_MODULES = {'E82_2000kw': 'powerCurve_E-82_2000kW.txt', # data source: https://www.reuthwind.de/enercon/enercon_e82.pdf [last access: 29.08.2024]
                  'E82_E2_2300kw': 'powerCurve_E-82E2_2300kW.txt', # data source: https://www.wind-turbine-models.com/turbines/550-enercon-e-82-e2-2.300#powercurve [last access: 29.08.2024]
                  'ANBONUS_2000kw': 'powerCurve_AN-BONUS_2000kW-76.txt', # data source: https://www.thewindpower.net/turbine_de_229_bonus_b76-2000.php [last access: 29.08.2024]
                  'ANBONUS_2300kw': 'powerCurve_AN-BONUS_2300kW-82.txt', # data source: https://www.wind-turbine-models.com/turbines/699-bonus-b82-2300#powercurve [last access: 29.08.2024]
                  'RE34_104_3400kw': 'powerCurve_REpower_3400kW-104.txt', # data source: https://www.thewindpower.net/turbine_de_553_senvion_3.4m104.php [last access: 29.08.2024]
                  'V90_2000kw': 'powerCurve_Vestas-V90.txt', # data source: https://www.wind-turbine-models.com/turbines/16-vestas-v90#powercurve [last access: 29.08.2024]
                  'Senvion34_3400kw': 'powerCurve_Senvion-3400kW.txt', # data source: https://en.wind-turbine-models.com/turbines/1003-senvion-3.4m114 [last access: 29.08.2024]
                  'PW90_2500kw': 'powerCurve_FL2500kw-90.txt',} # no power curve for PW90 available, therefore used data of a similar turbine: https://www.thewindpower.net/turbine_de_153_fuhrlander_fl-2500-90.php [last access: 29.08.2024]

PV_MODULES = {
        'PV_77_5Wp': {'module_length': 1200, 'module_width': 600, 'module_p_peak_kw': 0.0775, 'eta': 0.108}, # eta self-calculated; source: https://www.pvxchange.com/mediafiles/pvxchange/attachments/FS%20Series%202%20Datasheet%20-%20German.pdf
        'PV_95Wp': {'module_length': 1070, 'module_width': 536, 'module_p_peak_kw': 0.095, 'eta': 0.166}, # eta self-calculated: source: https://www.amumot-shop.de/dateien/solarswiss/solarmodul-rahmen-kvm5-95-140-datenblatt.pdf
        'PV_115Wp': {'module_length': 1200, 'module_width': 505, 'module_p_peak_kw': 0.115, 'eta': 0.19}, # source: https://www.esomatic.de/media/pdf/57/54/11/Datenblatt-FDS115-12M10-115Wp.pdf
        #'PV_175Wp': {'module_length': 1482, 'module_width': 676, 'module_p_peak_kw': 0.175, 'eta': 0.175}, # source: https://cdn.enfsolar.com/z/pp/xay60e3c78bd9c1c/5d1e9c90385fe.pdf [last access: 17.09.2024]
        #'PV_185Wp': {'module_length': 1482, 'module_width': 676, 'module_p_peak_kw': 0.185, 'eta': 0.185}, # source: https://cdn.enfsolar.com/z/pp/jddl58oj31/5efbfcf578167.pdf [last access: 17.09.2024]
        'PV_205Wp': {'module_length': 1586, 'module_width': 806, 'module_p_peak_kw': 0.205, 'eta': 0.1614}, # source: https://www.solarswiss.de/unsere-produkte/pv-solarmodule/solarmodul-kvm-205w-24v/ [last access: 17.09.2024]
        'PV_210Wp': {'module_length': 1586, 'module_width': 806, 'module_p_peak_kw': 0.21, 'eta': 0.1643}, # source: https://www.solarswiss.de/unsere-produkte/pv-solarmodule/solarmodul-210-watt-kvm-210-w-24v/ [last access: 17.09.2024]
        #'PV_225Wp': {'module_length': 1650, 'module_width': 992, 'module_p_peak_kw': 0.225, 'eta': 0.137},  # source: https://solarstrom.turbo.at/file.axd?file=/Photovoltaikmodule/TrinaSolar%20TSM-PC05.pdf [last access: 17.ß9.2024]
        'PV_235Wp': {'module_length': 1650, 'module_width': 992, 'module_p_peak_kw': 0.235, 'eta': 0.144},  # source: https://solarstrom.turbo.at/file.axd?file=/Photovoltaikmodule/TrinaSolar%20TSM-PC05.pdf [last access: 17.ß9.2024]
        'PV_240Wp': {'module_length': 1640, 'module_width': 990, 'module_p_peak_kw': 0.240, 'eta': 0.148}, # source: https://www.photovoltaik4all.de/media/e9/15/a1/1694533548/yin03214_ds_yge60cell-29b_series_2_eu_de_201410_v03-hr-1.pdf [last access: 17.09.2024]
        'PV_245Wp': {'module_length': 1640, 'module_width': 990, 'module_p_peak_kw': 0.245, 'eta': 0.151}, # source: https://www.photovoltaik4all.de/media/e9/15/a1/1694533548/yin03214_ds_yge60cell-29b_series_2_eu_de_201410_v03-hr-1.pdf [last access: 17.09.2024]
        'PV_255Wp': {'module_length': 1640, 'module_width': 990, 'module_p_peak_kw': 0.255, 'eta': 0.157}, # source: https://www.photovoltaik4all.de/media/e9/15/a1/1694533548/yin03214_ds_yge60cell-29b_series_2_eu_de_201410_v03-hr-1.pdf [last access: 17.09.2024]
        'PV_260Wp': {'module_length': 1640, 'module_width': 992, 'module_p_peak_kw': 0.260, 'eta': 0.160}, # source: https://www.photovoltaik4all.de/media/e9/15/a1/1694533548/yin03214_ds_yge60cell-29b_series_2_eu_de_201410_v03-hr-1.pdf [last access: 17.09.2024]
        'PV_270Wp': {'module_length': 1678, 'module_width': 991, 'module_p_peak_kw': 0.270, 'eta': 0.162}, # source: https://echtsolar.de/wp-content/uploads/2021/07/JA-Solar-JAP60S03-270-290-SC_Datenblatt.pdf [last access: 17.09.2024]
        'PV_275Wp': {'module_length': 1678, 'module_width': 991, 'module_p_peak_kw': 0.275, 'eta': 0.165}, # source: https://echtsolar.de/wp-content/uploads/2021/07/JA-Solar-JAP60S03-270-290-SC_Datenblatt.pdf [last access: 17.09.2024]
        #'PV_280Wp': {'module_length': 1678, 'module_width': 991, 'module_p_peak_kw': 0.280, 'eta': 0.168}, # source: https://echtsolar.de/wp-content/uploads/2021/07/JA-Solar-JAP60S03-270-290-SC_Datenblatt.pdf [last access: 17.09.2024]
        'PV_285Wp': {'module_length': 1678, 'module_width': 991, 'module_p_peak_kw': 0.285, 'eta': 0.171}, # source: https://echtsolar.de/wp-content/uploads/2021/07/JA-Solar-JAP60S03-270-290-SC_Datenblatt.pdf [last access: 17.09.2024]
        #'PV_290Wp': {'module_length': 1678, 'module_width': 991, 'module_p_peak_kw': 0.290, 'eta': 0.174}, # source: https://echtsolar.de/wp-content/uploads/2021/07/JA-Solar-JAP60S03-270-290-SC_Datenblatt.pdf [last access: 17.09.2024]
        'PV_310Wp': {'module_length': 1680, 'module_width': 990, 'module_p_peak_kw': 0.310, 'eta': 0.188}, # source: https://echtsolar.de/wp-content/uploads/2022/06/Solarwatt-Vision-60M-Datenblatt-DE.pdf[last access: 17.09.2024]
        #'PV_320Wp': {'module_length': 1680, 'module_width': 990, 'module_p_peak_kw': 0.320, 'eta': 0.194}, # source: https://echtsolar.de/wp-content/uploads/2022/06/Solarwatt-Vision-60M-Datenblatt-DE.pdf[last access: 17.09.2024]
        'PV_325Wp': {'module_length': 1670, 'module_width': 1006, 'module_p_peak_kw': 0.325, 'eta': 0.194}, # source: https://echtsolar.de/wp-content/uploads/2022/06/Heckert-Solar-Nemo-2.0-60-M-Black-Datenblatt-DE.pdf [last access: 17.09.2024]
        'PV_330Wp': {'module_length': 1700, 'module_width': 1000, 'module_p_peak_kw': 0.330, 'eta': 0.194}, # source: https://echtsolar.de/wp-content/uploads/2021/07/Sonnenstromfabrik-EXCELLENT_320-325-330_M60-Datenblatt.pdf [last access: 17.09.2024]
        'PV_335Wp': {'module_length': 1670, 'module_width': 1006, 'module_p_peak_kw': 0.335, 'eta': 0.199}, # source: https://echtsolar.de/wp-content/uploads/2022/06/Heckert-Solar-Nemo-2.0-60-M-Datenblatt-DE-2022.pdf [last access: 17.09.2024]
        'PV_345Wp': {'module_length': 1716, 'module_width': 1023, 'module_p_peak_kw': 0.345, 'eta': 0.197}, # source: https://echtsolar.de/wp-content/uploads/2022/06/Aleo-Solar-X63-Premium-2022-Datenblatt-DE.pdf [last access: 17.09.2024]
        'PV_375Wp': {'module_length': 1780, 'module_width': 1052, 'module_p_peak_kw': 0.375, 'eta': 0.202}, # source: https://echtsolar.de/wp-content/uploads/2022/06/Solarwatt-vision-H-3.0-pure-Datenblatt-DE.pdf
        'PV_385Wp': {'module_length': 1767, 'module_width': 1041, 'module_p_peak_kw': 0.385, 'eta': 0.209}, # source: https://echtsolar.de/wp-content/uploads/2022/06/Meyer-Burger-Black-Datenblatt-DE.pdf
    }

def pv_model_params(module_type, no_modules, **kwargs):
    a_m2 = no_modules * PV_MODULES[module_type]['module_length'] * PV_MODULES[module_type]['module_width'] * 0.0001 # overall area of PV modules / Gesamtfläche der PV-Anlage (in m^2)
    p_peak_kw = no_modules * PV_MODULES[module_type]['module_p_peak_kw']  # peak power of PV plant / Nennleistung der PV-Anlage (in kw): x Wp pro Modul bei insgesamt y Modulen
    eta = PV_MODULES[module_type]['eta']  # efficiency of pv plant / Effizienz der PV-Anlage
    cos_phi = 0.95  # Leistungsfaktor (Phasenwinkel)
    t_module_deg_celsius = 15  # initial temperature of PV module / Anfangstemperatur der Module (in °C)
    return {
        # https://midas-mosaik.gitlab.io/pysimmods/base-models/pv.html
        "params" : {
            "pv": {
                "a_m2": a_m2,
                "eta_percent": eta * 100.0,
            },
            "inverter": {
                "sn_kva": p_peak_kw / cos_phi,
                "q_control": "prioritize_p",
                "cos_phi": cos_phi,
                "inverter_mode": "capacitive",
            },
            "sign_convention": "active",
        },
        "inits" : {
            "pv": {
                "t_module_deg_celsius": t_module_deg_celsius,
            },
            "inverter": None,
        },
    }

# battery source: https://info.fluenceenergy.com/hubfs/Fluence%20Gridstack%20Pro_Global_US%20EN.pdf?hsCtaTracking=bfb2018d-bed9-460b-a7f2-40ce77239eed%7Cc929f4f5-0a71-4de0-828e-439063d844b8
batcount = 10  # Anzahl der Batteriespeicher (es werden mehrere der Speicher benötigt, um einen Gesamtspeicher in der passenden Größenordnung zu erhalten)
c_rate = 0.5
cap_per_bat = 5644
cap_kwh = batcount * cap_per_bat  # capacity of battery / Kapazität der Batterie (in kWh)
p_charge_max_kw = batcount * cap_per_bat * c_rate  # maximum charging power / maximale Ladeleistung (in kW)
p_discharge_max_kw = batcount * cap_per_bat * c_rate  # maximum discharging power / maximale Entladeleistung (in kW)
soc_min_percent = 15  # optional parameter - defines a threshold for the state of charge; state of charge may not fall below that value / Mindest-Ladezustand (in %)
soc_percent = 30  # defines the state of charge of the battery in the beginning / Anfangsladezustand (in %)
soc_min_mwh = soc_min_percent / 100 * cap_kwh * 0.001  # *0.001 for kw to mw
BT_PARAMS = {
    # https://midas-mosaik.gitlab.io/pysimmods/base-models/battery.html
    "params" : {
        "cap_kwh": cap_kwh,
        "p_charge_max_kw": p_charge_max_kw,
        "p_discharge_max_kw": p_discharge_max_kw,
        "soc_min_percent": soc_min_percent,
        #"eta_pc", #optional paramter - coefficients of the polynom to model the efficiency of the battery, represented as list of three values
    },
    "inits": {
        "soc_percent": soc_percent,
    },
    # Das Batterie-Modell hat zwei weitere Zustandsvariablen *p_kw* und *eta_percent*.
    # Sie zeigen die aktuelle Leistung und die Effizienz der Batterie an.
}


