import getting_subsystems_data_alt
import pandas as pd
import numpy as np


def get_subsystems_dataframe_source(self):
    df_column_names_source = ["Time","Foil_No","Arc_I","Arc_V","Gas_flow","Ratio_current"]
    source_voltage,source_current,gas_flow = getting_subsystems_data_alt.get_source_parameters(self.file_df,self.max_current)
    ratio_current = source_current/(self.target_current)
    df_subsystem_values_source = [self.time,self.foil_number,source_current,source_voltage,gas_flow,ratio_current]  
    df_subsystem_source = pd.concat(df_subsystem_values_source, axis=1, keys=df_column_names_source)
    return df_subsystem_source

def get_subsystems_dataframe_vacuum(self):
    df_column_names_vacuum = ["Time","Foil_No","Vacuum_P"]
    vacuum_level = getting_subsystems_data_alt.get_vacuum_parameters(self.file_df,self.max_current)
    magnet_current = getting_subsystems_data_alt.get_magnet_parameters(self.file_df,self.max_current)
    df_subsystem_values_vacuum = [self.time,self.foil_number,vacuum_level]
    df_subsystem_vacuum = pd.concat(df_subsystem_values_vacuum,axis=1,keys=df_column_names_vacuum)
    return df_subsystem_vacuum



def get_subsystems_dataframe_magnet(self):    
    df_column_names_magnet = ["Time","Foil_No","Magnet_I"]
    self.magnet_current = getting_subsystems_data_alt.get_magnet_parameters(self.file_df,self.max_current)
    df_subsystem_valuesmagnet = [self.time,self.foil_number,self.magnet_current]
    df_subsystem_magnet = pd.concat(df_subsystem_valuesmagnet,axis=1,keys=df_column_names_magnet)
    return df_subsystem_magnet

def get_subsystems_dataframe_rf(self):
    df_column_names_rf = ["Time","Foil_No","Dee_1_kV","Dee_2_kV","RF_fwd_W","RF_refl_W","Phase_load","Flap1_pos","Flap2_pos"]
    dee1_voltage,dee2_voltage = getting_subsystems_data_alt.get_rf_parameters(self.file_df,self.max_current) 
    forwarded_power,reflected_power,phase_load = getting_subsystems_data_alt.get_rf_parameters_power(self.file_df,self.max_current)
    flap1_pos,flap2_pos = getting_subsystems_data_alt.get_rf_parameters_flaps(self.file_df,self.max_current)
    df_subsystem_values_rf = [self.time,self.foil_number,dee1_voltage,dee2_voltage,forwarded_power,reflected_power,phase_load,flap1_pos,flap2_pos]
    df_subsystem_rf = pd.concat(df_subsystem_values_rf,axis=1,keys=df_column_names_rf)
    return df_subsystem_rf

def get_subsystems_dataframe_rf_sparks(self):
    df_column_names_rf = ["Dee_1_kV","Dee_2_kV","RF_fwd_W","RF_refl_W","Phase_load","Flap1_pos","Flap2_pos"]
    dee1_voltage,dee2_voltage = getting_subsystems_data_alt.get_rf_parameters_sparks(self.file_df,self.max_current) 
    forwarded_power,reflected_power,phase_load = getting_subsystems_data_alt.get_rf_parameters_power_sparks(self.file_df,self.max_current)
    flap1_pos,flap2_pos = getting_subsystems_data_alt.get_rf_parameters_flaps_sparks(self.file_df,self.max_current)
    df_subsystem_values_rf = [dee1_voltage,dee2_voltage,forwarded_power,reflected_power,phase_load,flap1_pos,flap2_pos]
    df_subsystem_rf = pd.concat(df_subsystem_values_rf,axis=1,keys=df_column_names_rf)
    return df_subsystem_rf

def get_subsystems_dataframe_extraction(self):
    df_column_names_extraction = ["Time","Foil_No","Extr_pos","Balance"]
    carousel_position,balance_position = getting_subsystems_data_alt.get_extraction_parameters_position(self.file_df,self.max_current)
    df_subsystem_values_extraction = [self.time,self.foil_number,carousel_position,balance_position]
    df_subsystem_extraction = pd.concat(df_subsystem_values_extraction,axis=1,keys=df_column_names_extraction)
    return df_subsystem_extraction

def get_subsystems_dataframe_beam(self):
    df_column_names_beam = ["Time","Foil_No","Foil_I","Coll_l_I","Target_I","Coll_r_I","Coll_l_rel","Coll_r_rel","Target_rel","Extraction_losses"]
    collimator_r,collimator_l = getting_subsystems_data_alt.get_collimator_parameters(self.file_df,self.max_current) 
    extraction_current = getting_subsystems_data_alt.get_extraction_parameters(self.file_df,self.max_current)
    collimator_r_rel = collimator_r/extraction_current*100
    collimator_l_rel = collimator_l/extraction_current*100
    target_rel = (self.target_current)/extraction_current*100
    extraction_losses = (1-(self.target_current+collimator_l+collimator_r)/extraction_current)*100
    df_subsystem_values_beam = [self.time,self.foil_number,extraction_current,collimator_l,self.target_current,collimator_r,collimator_l_rel,collimator_r_rel,target_rel,extraction_losses]
    df_subsystem_beam = pd.concat(df_subsystem_values_beam,axis=1,keys=df_column_names_beam)
    return df_subsystem_beam

def get_subsystems_dataframe_pressure(self):
    df_column_names_pressure = ["Time","Foil_No","Target_P"]
    target_pressure = getting_subsystems_data_alt.get_target_pressure(self.file_df,self.max_current)
    df_subsystem_values_pressure = [self.time,self.foil_number,target_pressure]
    df_subsystem_pressure = pd.concat(df_subsystem_values_pressure,axis=1,keys=df_column_names_pressure)
    return df_subsystem_pressure

def get_subsystems_dataframe_pressure_irradiation(self):
    df_column_names_pressure = ["Time","Foil_No","Target_P"]
    target_pressure = getting_subsystems_data_alt.get_target_pressure_irradiation(self.file_df,self.max_current)
    df_subsystem_values_pressure = [self.time,self.foil_number,target_pressure]
    df_subsystem_pressure_irradiation = pd.concat(df_subsystem_values_pressure,axis=1,keys=df_column_names_pressure)
    return df_subsystem_pressure_irradiation
