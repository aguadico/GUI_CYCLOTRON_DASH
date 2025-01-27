#Functions: open the files and get key parameters and summaries 
import getting_subsystems_data
import getting_subsystems_dataframes
import getting_summaries_subsystems
import pandas as pd
import numpy as np


#def getting_sparks(self,voltage_value):
#        voltage_dee = self.df_subsystem_rf_sparks.Dee_1_kV[getattr(self.df_subsystem_rf_sparks,voltage_value) < float(self.voltage_limit.iloc[self.current_row])]
#        return (voltage_dee)

def get_sparks_numbers(self,dee_number):    
        dee_voltage = getattr(self.df_subsystem_rf,dee_number)
        self.df_subsystem_rf_source = self.df_subsystem_rf_sparks[getattr(self.df_subsystem_rf_sparks,"Arc_I").astype(float) > 0.2*np.max(getattr(self.df_subsystem_rf_sparks,"Arc_I").astype(float))]
        sparks = self.df_subsystem_rf_source.Dee_1_kV[getattr(self.df_subsystem_rf_source,"Dee_1_kV").astype(float) < np.max(dee_voltage.astype(float))*0.75]
        return sparks       

def get_flap_postion(self,flap_number,indexes):
    position =  np.average(np.array(getattr(self.df_subsystem_rf_sparks[self.df_subsystem_rf_sparks.Arc_I>0],flap_number).astype(float))[indexes[0]:indexes[1]])
    return position

def get_instant_and_average_speed(self,flap_number):
    final_average_position = getting_subsystems_data.get_flap_postion(self,flap_number,[-10,-1]) 
    initial_average_position = getting_subsystems_data.get_flap_postion(self,flap_number,[0,20])
    average_speed = (final_average_position-initial_average_position)/(3*len(getattr(self.df_subsystem_rf_sparks[self.df_subsystem_rf_sparks.Arc_I>0],flap_number).astype(float)))*3600
    instant_speed = ((np.array(getattr(self.df_subsystem_rf_sparks[self.df_subsystem_rf_sparks.Arc_I>0],flap_number).astype(float))[:-1]-np.array(getattr(self.df_subsystem_rf_sparks[self.df_subsystem_rf_sparks.Arc_I>0],flap_number).astype(float))[1:])/3)
    average_instant_speed = np.average(average_speed)
    max_instant_speed     = np.max(instant_speed)
    std_instant_speed     = np.std(instant_speed)
    return (average_instant_speed,max_instant_speed,std_instant_speed)

def get_resonance_speed(self,flap_number,dee_number):  
    initial_flap = getattr(self.df_subsystem_rf_sparks,flap_number).iloc[1]
    flap_range = getattr(self.df_subsystem_rf_sparks,flap_number)[getattr(self.df_subsystem_rf_sparks,dee_number) > 0]
    resonance_flap = flap_range.iloc[1]
    distance_flap = resonance_flap - initial_flap
    index_starting_flap = flap_range.index[1]
    starting_resonance_time  =  (index_starting_flap)*3
    return (initial_flap,resonance_flap,distance_flap)

def file_open(self):
        [self.target_current,self.max_current] = getting_subsystems_data.get_target_parameters(self.file_df)
        self.low_source_current   = getting_subsystems_data.get_source_parameters_limit(self.file_df)
        self.time                 = getting_subsystems_data.get_time(self.file_df,self.max_current)
        self.time_smaller_current = getting_subsystems_data.get_time(self.file_df,15)
        self.foil_number = getting_subsystems_data.get_foil_number(self.file_df,self.max_current) 
        self.probe_current = getting_subsystems_data.get_probe_current(self.file_df)
        self.df_subsystem_source = getting_subsystems_dataframes.get_subsystems_dataframe_source(self)
        self.df_subsystem_vacuum = getting_subsystems_dataframes.get_subsystems_dataframe_vacuum(self)
        self.df_subsystem_magnet = getting_subsystems_dataframes.get_subsystems_dataframe_magnet(self)
        self.df_subsystem_rf = getting_subsystems_dataframes.get_subsystems_dataframe_rf(self)
        self.df_subsystem_rf_sparks = getting_subsystems_dataframes.get_subsystems_dataframe_rf_sparks(self)
        self.df_subsystem_extraction = getting_subsystems_dataframes.get_subsystems_dataframe_extraction(self)
        self.df_subsystem_beam = getting_subsystems_dataframes.get_subsystems_dataframe_beam(self)
        self.df_subsystem_pressure = getting_subsystems_dataframes.get_subsystems_dataframe_pressure(self) 
        self.df_subsystem_pressure_irradiation = getting_subsystems_dataframes.get_subsystems_dataframe_pressure_irradiation(self) 
        #
        self.sparks_dee_1 = getting_subsystems_data.get_sparks_numbers(self,"Dee_1_kV")
        self.sparks_dee_2 = getting_subsystems_data.get_sparks_numbers(self,"Dee_2_kV")
        self.sparks_number = len(self.sparks_dee_1) + len(self.sparks_dee_2)
        self.initial_flap_1,self.resonance_flap_1,self.distance_flap_1 = getting_subsystems_data.get_resonance_speed(self,"Flap1_pos","Dee_1_kV")
        self.initial_flap_2,self.resonance_flap_2,self.distance_flap_2 = getting_subsystems_data.get_resonance_speed(self,"Flap2_pos","Dee_2_kV")
        self.average_instant_speed_1, self.max_instant_speed_1, self.std_instant_speed_1 = getting_subsystems_data.get_instant_and_average_speed(self,"Flap1_pos")
        self.average_instant_speed_2, self.max_instant_speed_2, self.std_instant_speed_2 = getting_subsystems_data.get_instant_and_average_speed(self,"Flap2_pos")
        
def file_open_summary(self):
        getting_summaries_alt.get_summary_ion_source(self)
        getting_summaries_alt.get_summary_vacuum(self)
        getting_summaries_alt.get_summary_magnet(self)
        getting_summaries_alt.get_summary_rf(self)
        getting_summaries_alt.get_summary_extraction(self)
        getting_summaries_alt.get_summary_beam(self)
        getting_summaries_alt.get_summary_volume(self)
        getting_summaries_alt.get_filling_volume(self,0) 
        getting_subsystems_data.get_transmission(self)
        getting_subsystems_data.get_pressure_fluctuations(self,0)        
        self.voltage_limit = (0.8*(self.df_rf.DEE1_VOLTAGE_AVE))  
        self.voltage_values = ["Dee_1_kV","Dee_2_kV"] 

