#COLUMNS_SOURCE = ["FILE","DATE","TARGET","FOIL","CURRENT_MAX", "CURRENT_MIN","CURRENT_AVE","CURRENT_STD","VOLTAGE_MAX","VOLTAGE_MIN","VOLTAGE_AVE","VOLTAGE_STD","HFLOW",
#    "RATIO_MAX", "RATIO_MIN","RATIO_AVE","RATIO_STD"] 
COLUMNS_SOURCE = ["FILE","DATE","TARGET","FOIL","CURRENT_MAX", "CURRENT_MIN","CURRENT_AVE","CURRENT_STD","VOLTAGE_MAX","VOLTAGE_MIN","VOLTAGE_AVE","VOLTAGE_STD","HFLOW",
    "RATIO_MAX", "RATIO_MIN","RATIO_AVE","RATIO_STD","SOURCE_STABILITY","SOURCE_STABILITY_STD"]
COLUMNS_VACUUM = ["FILE","DATE","TARGET","FOIL","PRESSURE_MAX","PRESSURE_MIN","PRESSURE_AVE","PRESSURE_STD","VACUUM_STABILITY","VACUUM_STABILITY_STD","NORMALIZED_VACUUM","NORMALIZED_VACUUM_STD"]
COLUMNS_MAGNET = ["FILE","DATE","TARGET","FOIL","CURRENT_MAX","CURRENT_MIN","CURRENT_AVE","CURRENT_STD","START_ISO","END_ISO","START_IRRADIATION","START_IRRADIATION_REL","START_IRRADIATION_REL_STD","DELTA_TIME","DELTA_TIME_STD"]
#COLUMNS_RF =  ["FILE","DATE","TARGET","FOIL","DEE1_VOLTAGE_MAX","DEE1_VOLTAGE_MIN","DEE1_VOLTAGE_AVE","DEE1_VOLTAGE_STD","DEE2_VOLTAGE_MAX","DEE2_VOLTAGE_MIN","DEE2_VOLTAGE_AVE","DEE2_VOLTAGE_STD",
#    "FORWARD_POWER_MAX","FORWARD_POWER_MIN","FORWARD_POWER_AVE","FORWARD_POWER_STD","REFLECTED_POWER_MAX","REFLECTED_POWER_MIN","REFLECTED_POWER_AVE","REFLECTED_POWER_STD",
#    "PHASE_LOAD_MAX","PHASE_LOAD_MIN","PHASE_LOAD_AVE","PHASE_LOAD_STD"]
COLUMNS_BEAM = ["FILE","DATE","TARGET","FOIL","COLL_CURRENT_L_MAX","COLL_CURRENT_L_MIN","COLL_CURRENT_L_AVE","COLL_CURRENT_L_STD","COLL_CURRENT_R_MAX","COLL_CURRENT_R_MIN","COLL_CURRENT_R_AVE","COLL_CURRENT_R_STD"
    ,"RELATIVE_COLL_CURRENT_L_MAX","RELATIVE_COLL_CURRENT_L_MIN","RELATIVE_COLL_CURRENT_L_AVE","RELATIVE_COLL_CURRENT_L_STD",
    "RELATIVE_COLL_CURRENT_R_MAX","RELATIVE_COLL_CURRENT_R_MIN","RELATIVE_COLL_CURRENT_R_AVE","RELATIVE_COLL_CURRENT_R_STD",
    "TARGET_CURRENT_MAX","TARGET_CURRENT_MIN","TARGET_CURRENT_AVE","TARGET_CURRENT_STD","FOIL_CURRENT_MAX","FOIL_CURRENT_MIN","FOIL_CURRENT_AVE","FOIL_CURRENT_STD",
    "RELATIVE_TARGET_CURRENT_MAX","RELATIVE_TARGET_CURRENT_MIN","RELATIVE_TARGET_CURRENT_AVE","RELATIVE_TARGET_CURRENT_STD",
    "EXTRACTION_LOSSES_MAX","EXTRACTION_LOSSES_MIN","EXTRACTION_LOSSES_AVE","EXTRACTION_LOSSES_STD",
    "RELATIVE_COLL_CURRENT_MAX","RELATIVE_COLL_CURRENT_MIN","RELATIVE_COLL_CURRENT_AVE","RELATIVE_COLL_CURRENT_STD","TARGET_STABILITY","TARGET_STABILITY_STD"]
COLUMNS_EXTRACTION = ["FILE","DATE","CYCLOTRON","TARGET","PHYSICAL_TARGET","FOIL","CAROUSEL_POSITION_MAX","CAROUSEL_POSITION_MIN","CAROUSEL_POSITION_AVE","CAROUSEL_POSITION_STD"
    ,"BALANCE_POSITION_MAX","BALANCE_POSITION_MIN","BALANCE_POSITION_AVE","BALANCE_POSITION_STD"]
COLUMNS_TRANSMISSION = ["FILE","DATE","TARGET","TRANSMISSION_AVE","TRANSMISSION_STD","FOIL"]
COLUMNS_FILLING = ["FILE","DATE","TARGET","RELATIVE_VOLUME","RELATIVE_VOLUME_STD","HIGH_PRESSURE_AVE","HIGH_PRESSURE_STD","LOW_PRESSURE_AVE","LOW_PRESSURE_STD","PRESSURE_IRRADIATION_AVE","PRESSURE_IRRADIATION_STD"]
COLUMNS_FLUCTUATIONS = ["FILE","TIME_LIST","DATE","TARGET","PRESSURE_FLUCTUATIONS"]

COLUMNS_RF =  ["FILE","DATE","TARGET","FOIL","DEE1_VOLTAGE_MAX","DEE1_VOLTAGE_MIN","DEE1_VOLTAGE_AVE","DEE1_VOLTAGE_STD","DEE2_VOLTAGE_MAX","DEE2_VOLTAGE_MIN","DEE2_VOLTAGE_AVE","DEE2_VOLTAGE_STD",
    "FORWARD_POWER_MAX","FORWARD_POWER_MIN","FORWARD_POWER_AVE","FORWARD_POWER_STD","REFLECTED_POWER_MAX","REFLECTED_POWER_MIN","REFLECTED_POWER_AVE","REFLECTED_POWER_STD",
    "PHASE_LOAD_MAX","PHASE_LOAD_MIN","PHASE_LOAD_AVE","PHASE_LOAD_STD",
    "FLAP1_MAX","FLAP1_MIN","FLAP1_AVE","FLAP1_STD","FLAP2_MAX","FLAP2_MIN","FLAP2_AVE","FLAP2_STD","SPARKS","DISTANCE_FLAP_1","AVERAGE_INSTANT_SPEED_1","MAX_INSTANT_SPEED_1","STD_INSTANT_SPEED_1",
    "DISTANCE_FLAP_2","AVERAGE_INSTANT_SPEED_2","MAX_INSTANT_SPEED_2","STD_INSTANT_SPEED_2",
    "REFLECTED_POWER_AVE_W","REFLECTED_POWER_STD_W","DEE_1_VOLTAGE_STABILITY","DEE_2_VOLTAGE_STABILITY","DEE_1_VOLTAGE_STABILITY_STD","DEE_2_VOLTAGE_STABILITY_STD","DISTANCE_FLAP_1_STD","DISTANCE_FLAP_2_STD","MAX_INSTANT_SPEED_1_STD",
    "MAX_INSTANT_SPEED_2_STD","AVERAGE_INSTANT_SPEED_1_STD","AVERAGE_INSTANT_SPEED_2_STD","SPARKS_STD"]

#
COLUMN_RF = ["DEE1 VOLTAGE [kV]","DEE2 VOLTAGE [kV]","FORWARDED POWER [kW]","REFLECTED POWER [kW]","FLAP1 POSITION [%]","FLAP2 POSITION [%]"]
COLUMNS_RF_AVE =  ["DEE1_VOLTAGE_AVE","DEE2_VOLTAGE_AVE","FORWARD_POWER_AVE","REFLECTED_POWER_AVE","FLAP1_AVE","FLAP2_AVE"]
COLUMNS_RF_STD =  ["DEE1_VOLTAGE_STD","DEE2_VOLTAGE_STD","FORWARD_POWER_STD","REFLECTED_POWER_STD","FLAP1_STD","FLAP2_STD"]
COLUMN_BEAM = ["COLL L [uA]","COLL R [uA]","COLL REL L[%]","COLL REL R[%]","TARGET[uA]","FOIL[uA]"]
COLUMNS_BEAM_AVE = ["COLL_CURRENT_R_AVE","COLL_CURRENT_R_AVE",
            "RELATIVE_COLL_CURRENT_L_AVE",
            "RELATIVE_COLL_CURRENT_R_AVE",
             "TARGET_CURRENT_AVE",
             "FOIL_CURRENT_AVE"]
COLUMNS_BEAM_STD = ["COLL_CURRENT_L_STD","COLL_CURRENT_R_STD","RELATIVE_COLL_CURRENT_L_STD","RELATIVE_COLL_CURRENT_R_STD","TARGET_CURRENT_STD",
         "FOIL_CURRENT_STD"]
COLUMN_EXTRACTION = ["CAROUSSEL [%]","BALANCE [%]"]
COLUMNS_EXTRACTION_AVE = ["CAROUSEL_POSITION_AVE","BALANCE_POSITION_AVE"]
COLUMNS_EXTRACTION_STD = ["CAROUSEL_POSITION_STD","BALANCE_POSITION_STD"]
COLUMN_ION_SOURCE = ["CURRENT [mA]","VOLTAGE [V]","RATIO [mA/uA]"]
COLUMNS_ION_SOURCE_AVE = ["CURRENT_AVE","VOLTAGE_AVE","RATIO_AVE"]
COLUMNS_ION_SOURCE_STD = ["CURRENT_STD","VOLTAGE_STD","RATIO_STD"]
COLUMN_VACUUM = ["PRESSURE [10-5 mbar]"]
COLUMNS_VACUUM_AVE = ["PRESSURE_AVE"]
COLUMNS_VACUUM_STD = ["PRESSURE_STD"]
COLUMN_MAGNET = [str("MAGNET CURRENT [A]")]
COLUMNS_MAGNET_AVE = ["CURRENT_AVE","CURRENT_STD"]
COLUMNS_MAGNET_STD = ["CURRENT_STD"]
COLUMN_LOSSES = ["EXTRACTION LOSSES [%]"]
COLUMNS_LOSSES_AVE = ["EXTRACTION_LOSSES_AVE"]  
COLUMNS_LOSSES_STD = ["EXTRACTION_LOSSES_STD"]
COLUMN_TRANSMISSION = ["TRANSMISSION"]
COLUMNS_TRANSMISSION_AVE = ["TRANSMISSION_AVE"]
COLUMNS_TRANSMISSION_STD = ["TRANSMISSION_STD"]
SUMMARY_FILE_NAMES = ["table_summary_source.out","table_summary_source.out","table_summary_source.out","table_summary_source.out","table_summary_vacuum.out","table_summary_magnet.out",
        "table_summary_rf.out","table_summary_rf.out","table_summary_rf.out","table_summary_extraction.out","table_summary_beam.out","table_summary_beam.out","table_summary_beam.out","table_summary_beam.out","table_summary_beam.out",
        "table_summary_transmission.out"]
LABELS = ["CURRENT_","VOLTAGE_","RATIO_","SOURCE_PERFORMANCE_","PRESSURE_","CURRENT_","RELATIVE_TARGET_CURRENT_","EXTRACTION_LOSSES_","TRANSMISSION_"]
LABELS_1 = ["DEE1_VOLTAGE_","FORWARD_POWER_","FLAP1_","CAROUSEL_POSITION_","COLL_CURRENT_L_","RELATIVE_COLL_CURRENT_L_","TARGET_CURRENT_"]
LABELS_2 = ["DEE2_VOLTAGE_","REFLECTED_POWER_","FLAP2_","BALANCE_POSITION_","COLL_CURRENT_R_","RELATIVE_COLL_CURRENT_R_","FOIL_CURRENT_"]
YLABEL = ["CURRENT [mA]","VOLTAGE [V]",r"RATIO [mA/$\mu A$]",r"RATIO [$\mu A$/mA]",r"PRESSURE [$10^{-5}$mbar]","MAGNET CURRENT [A]",r"RELATIVE CURRENT (FOIL)[%]","LOSSES [%]",r"TRANSMISSION RATE [($\mu A$ Foil/$\mu A$ Probe) %]"]
YLABEL_D = ["AVERAGE VOLTAGE [kV]",r"AVERAGE POWER [kW]",r"AVERAGE POSITION [%]",r"POSITION [%]",r"CURRENT [$\mu A$]",r"RELATIVE CURRENT [%]",r"AVERAGE CURRENT [$\mu$A]"]
FILE_NAME = ["ion_source_evolution.pdf","voltage_evolution.pdf","ratio_evolution.pdf","source_performance.pdf","vacuum_evolution.pdf","magnet_evolution.pdf","relative_currents_foil.pdf","efficiency_target_evolution.pdf","transmission.pdf"]
FILE_NAME_D = ["dee1_dee2_voltage_evolution.pdf","power_evolution.pdf","flap_evolution.pdf","carousel_balance_evolution.pdf","collimator_current_evolution.pdf","absolute_collimator_current_evolution.pdf","target_foil_evolution.pdf"]
LEGEND = ["T","T","T","T","T","T","T","T","T"]
LEGEND_1 = ["DEE1","FORWARDED ","FLAP 1 ","CAROUSEL ","COLLIMATOR  L","COLLIMATOR  L","TARGET ","COLLIMATOR L ","TARGET "]
LEGEND_2 = ["DEE2","REFELECTED ","FLAP 2 ","BALANCE ","COLLIMATOR  R","COLLIMATOR  R","FOIL ","COLLIMATOR R ","FOIL "]
COLUMNS_VOLUME = ["FILE","DATE","TARGET","FOIL","PRESSURE_INITIAL","PRESSURE_FINAL","MAX_PRESSURE","MIN_PRESSURE","AVE_PRESSURE","STD_PRESSURE","MAX_VOLUME","MIN_VOLUME","AVE_VOLUME","STD_VOLUME"]

COLUMNS_TO_PLOT = {"CHOOSE":[["PLOT_1"],["PLOT_2"],["PLOT_3"]],
"SOURCE":[['CURRENT_AVE'],["PRESSURE_AVE"],["HFLOW"],["SOURCE_PERFORMANCE"],["SOURCE_STABILITY"]],
"BEAM":[['FOIL_CURRENT_AVE'],["TARGET_CURRENT_AVE"],["RELATIVE_COLL_CURRENT_AVE"],["TARGET_STABILITY"],['EXTRACTION_LOSSES_AVE']],
"VACUUM":[['PRESSURE_AVE'],["TRANSMISSION_AVE"],["CURRENT_AVE"],["VACUUM_STABILITY"],["NORMALIZED_VACUUM"]],
"RF":[['DEE1_VOLTAGE_AVE','DEE2_VOLTAGE_AVE'],["FORWARD_POWER_AVE"],["REFLECTED_POWER_AVE_W"],["FLAP1_AVE","FLAP2_AVE"],['PHASE_LOAD_AVE']],
"RF_STABILITY":[["SPARKS"],["DEE_1_VOLTAGE_STABILITY","DEE_2_VOLTAGE_STABILITY"],["DISTANCE_FLAP_1","DISTANCE_FLAP_2"],["MAX_INSTANT_SPEED_1","MAX_INSTANT_SPEED_2"],["AVERAGE_INSTANT_SPEED_1","AVERAGE_INSTANT_SPEED_2"]],
"TARGET":[["RELATIVE_VOLUME"],["LOW_PRESSURE_AVE"],["HIGH_PRESSURE_AVE"],["PRESSURE_IRRADIATION_AVE"]],
"MAGNET":[['CURRENT_AVE'],["START_IRRADIATION_REL"],["DELTA_TIME"]]}

COLUMNS_TO_PLOT_ERROR = {"CHOOSE":[["PLOT_1"],["PLOT_2"],["PLOT_3"]],
"SOURCE":[['CURRENT_STD'],["PRESSURE_STD"],["HFLOW_STD"],["SOURCE_PERFORMANCE_ERROR"],["SOURCE_STABILITY_STD"]],
"BEAM":[['FOIL_CURRENT_STD'],["TARGET_CURRENT_STD"],["RELATIVE_COLL_CURRENT_STD"],["TARGET_STABILITY_STD"],['EXTRACTION_LOSSES_STD']],
"VACUUM":[['PRESSURE_STD'],["TRANSMISSION_STD"],["CURRENT_STD"],["VACUUM_STABILITY_STD"],["NORMALIZED_VACUUM_STD"]],
"RF":[['DEE1_VOLTAGE_STD','DEE2_VOLTAGE_STD'],["FORWARD_POWER_STD"],["REFLECTED_POWER_STD_W"],["FLAP1_STD","FLAP2_STD"],['PHASE_LOAD_STD']],
"RF_STABILITY":[["SPARKS_STD"],["DEE_1_VOLTAGE_STABILITY_STD","DEE_2_VOLTAGE_STABILITY_STD"],["DISTANCE_FLAP_1_STD","DISTANCE_FLAP_2_STD"],["MAX_INSTANT_SPEED_1_STD","MAX_INSTANT_SPEED_2_STD"],["AVERAGE_INSTANT_SPEED_1_STD","AVERAGE_INSTANT_SPEED_2_STD"]],
"TARGET":[["RELATIVE_VOLUME_STD"],["LOW_PRESSURE_STD"],["HIGH_PRESSURE_STD"],["PRESSURE_IRRADIATION_STD"]],
"MAGNET":[['CURRENT_STD'],["START_IRRADIATION_REL_STD"],["DELTA_TIME_STD"]]}

DATAFRAME_TO_PLOT = {"CHOOSE":[["df_zero"]]*3,
"SOURCE":[["df_summary_source"],["df_summary_vacuum"],["df_summary_source"],["df_source_performance"],["df_summary_source"]],
"BEAM":[["df_summary_beam"]]*5,
"VACUUM":[["df_summary_vacuum"],["df_summary_transmission"],["df_summary_source"],["df_summary_vacuum"],["df_summary_vacuum"]],
"RF":[["df_summary_rf","df_summary_rf"],["df_summary_rf"],["df_summary_rf"],["df_summary_rf","df_summary_rf"],["df_summary_rf"]],
"RF_STABILITY":[["df_summary_rf"],["df_summary_rf","df_summary_rf"],["df_summary_rf","df_summary_rf"],["df_summary_rf","df_summary_rf"],["df_summary_rf","df_summary_rf"]],
"TARGET":[["volume_information"]]*4,
"MAGNET":[["df_summary_magnet"]]*3}

REFERENCE_VALUE_DICTIONARY = {"CHOOSE":[[[]],[[]]],
"SOURCE":[[[500,700,850,"Upper limit"]],[[1.8,1.9,2,"Upper limit"]],[[5.5,6,6.5,"Upper limit"],[3.5,3,2.5,"Lower limit"]],[[3.5,4.5,6,"Upper limit"]],[[5,10,15,"Upper limit"]]],
"BEAM":[[[600,700,800]],[[110,120,130]],[[20,25,35]],[[95,85,70]],[[-0.5,-1,-2],[0.5,1,2]]],
"VACUUM":[[[1.8,1.9,2,"Upper limit"]],[[60,50,40,"Lower limit"]],[[500,700,800,"Upper limit"]],[[2,5,7.5,"Upper limit"]],[[0.35,0.4,0.5,"Upper limit"]]],
"RF":[[[]],[[13.5,14.5,15,"Upper limit"]],[[400,500,600,"Upper limit"]],[[10,8,6,"Lower limit"]],[[5.5,6,6.5,"Upper limit"],[4.5,4,3.5,"Lower limit"]]],
"RF_STABILITY":[[[]],[[2,2.5,3,"Upper limit"]],[[1,-0.5,-2.5,"Lower limit"]],[[7.5,10,12.5,"Upper limit"]],[[7,10,15,"Upper limit"]]],
"TARGET":[[[20,15,12,"Lower limit"]],[[70,72.5,75,"Upper limit"]],[[445,450,460,"Upper limit"]],[[445,450,460,"Upper limit"]]],
"MAGNET":[[[]],[[]],[[]]]}

Y_LABEL = {"CHOOSE":[[" "]]*3,
"SOURCE":[[r"I source [mA]"],["Vacuum Pressure [1e-5 mbar]"],["H flow [sccm]"],["Source performance [mA/uA]"],["I source stability [%]"]],
"BEAM":[[r"I foil [uA]"],["I target [\u03bcA]"],["I collimators[%]"],["I target stability [%]"],["Extraction losses [%]"]],
"VACUUM":[[r"Vacuum Pressure [1e-5 mbar]"],["Transmission [%]"],["I source [mA]"],["Vacuum stability[%]"],["Vacuum/Gas [1e-5mbar/sccm]"]],
"RF":[[r"Voltage Dee [kV]","Voltage Dee [kV]"],["Forward power[kW]"],["Reflected power [W]"],["Flap [%]","Flap  [%]"],["RF Phase load [o]"]],
"RF_STABILITY":[["Number of sparks"],["Voltage stability [%]","Voltage stability [%]"],["Distance flap [%]","Distance flap [%]"],["Max speed flap [%/s]","Max speed flap [%/s]"],["Ave speed irradiation [%/h]","Ave flap speed [%/h]"]],
"TARGET":[["Delta pressure filling [psi]"],["Low pressure [psi]"],["High pressure [psi]"],["Pressure irradiation [psi]"]],
"MAGNET":[[r"Current [A]"],["Relative current to center [%]"],["Delta time [min]"]]}


LEGEND = {"CHOOSE":[[" "]]*3,
"SOURCE":[[""]]*5,
"BEAM":[[""]]*5,
"VACUUM":[[""]]*5,
"RF":[[r"Dee 1","Dee 2"],["Forward power "],["Reflected power  "],["Flap 1","Flap 2"],["RF Phase load"]],
"RF_STABILITY":[["Number of sparks"],["Dee 1","Dee 2"],["Flap 1","Flap 2"],["Flap 1","Flap 2"],["Flap 1","Flap 2"]],
"TARGET":[[""]]*4,
"MAGNET":[[""]]*3}


import pandas as pd
def flags(self): 
        self.current_row = 0
        self.current_row_folder = 0
        self.current_row_statistics = 0
        self.current_row_analysis = 0 
        self.row_to_plot = 0
        self.current_row_observables = 0
        self.current_row_observables_tab3 = 0      
        self.target_1_value = "0"
        self.target_2_value = "0"
        self.max_min_value = "0"        
        self.week_value = "0"
        self.day_value = "1"
        self.flag_no_gap = "1"

def initial_df(self):               
        self.df_source = pd.DataFrame(columns=COLUMNS_SOURCE)
        self.df_vacuum = pd.DataFrame(columns=COLUMNS_VACUUM)
        self.df_magnet = pd.DataFrame(columns=COLUMNS_MAGNET)
        self.df_beam = pd.DataFrame(columns=COLUMNS_BEAM )
        self.df_rf = pd.DataFrame(columns=COLUMNS_RF)
        self.df_extraction = pd.DataFrame(columns=COLUMNS_EXTRACTION)
        self.df_transmission = pd.DataFrame(columns=COLUMNS_TRANSMISSION)
        self.df_filling_volume = pd.DataFrame(columns=COLUMNS_FILLING)
        self.df_pressure_fluctuations = pd.DataFrame(columns=COLUMNS_FLUCTUATIONS)
        self.df_volume = pd.DataFrame(columns=COLUMNS_VOLUME)


