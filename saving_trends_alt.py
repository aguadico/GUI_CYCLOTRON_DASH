import os 
import numpy as np
import managing_files_alt
import tfs
import getting_subsystems_data
import getting_subsystems_dataframes
import getting_summaries_subsystems

def getting_summary_per_file(self):
    file_open(self)
    file_open_summary(self)
 
        
def getting_summary_final(self):
        self.df_rf = self.df_rf.dropna()
        self.df_extraction = self.df_extraction.dropna()
        self.df_source = self.df_source.dropna()
        self.df_vacuum = self.df_vacuum.dropna()
        self.df_magnet = self.df_magnet.dropna()
        self.df_beam = self.df_beam.dropna()
        self.df_rf = self.df_rf.sort_values(by=['FILE'])
        self.df_extraction = self.df_extraction.sort_values(by=['FILE'])
        self.df_source = self.df_source.sort_values(by=['FILE'])
        self.df_vacuum = self.df_vacuum.sort_values(by=['FILE'])
        self.df_magnet = self.df_magnet.sort_values(by=['FILE'])
        self.df_beam = self.df_beam.sort_values(by=['FILE'])
        self.df_transmission = self.df_transmission.sort_values(by=['FILE'])
        self.df_volume = self.df_volume.sort_values(by=['FILE'])
        self.df_filling_volume = self.df_filling_volume.sort_values(by=['FILE'])


def file_open(self):
        [self.target_current,self.max_current] = getting_subsystems_data.get_target_parameters(self.file_df)
        self.low_source_current = getting_subsystems_data.get_source_parameters_limit(self.file_df)
        self.time = getting_subsystems_data.get_time(self.file_df,self.max_current)
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
        getting_summaries_subsystems.get_summary_ion_source(self)
        getting_summaries_subsystems.get_summary_vacuum(self)
        getting_summaries_subsystems.get_summary_magnet(self)
        getting_summaries_subsystems.get_summary_rf(self)
        getting_summaries_subsystems.get_summary_extraction(self)
        getting_summaries_subsystems.get_summary_beam(self)
        getting_summaries_subsystems.get_summary_volume(self)
        getting_summaries_subsystems.get_filling_volume(self,0) 
        getting_subsystems_data.get_transmission(self)
        getting_subsystems_data.get_pressure_fluctuations(self,0)        
        self.voltage_limit = (0.8*(self.df_rf.DEE1_VOLTAGE_AVE))  
        self.voltage_values = ["Dee_1_kV","Dee_2_kV"] 