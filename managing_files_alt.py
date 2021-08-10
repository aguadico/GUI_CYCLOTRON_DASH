#Functions: open the files and get key parameters and summaries 
import getting_subsystems_data_alt
import getting_subsystems_alt
import getting_summaries_alt
import pandas as pd
import numpy as np
def file_open(self):
        [self.target_current,self.max_current] = getting_subsystems_data_alt.get_target_parameters(self.file_df)
        # sets a lower ion source limit for finding RF sparks 
        self.low_source_current = getting_subsystems_data_alt.get_source_parameters_limit(self.file_df)
        # get irradiation hours
        self.time = getting_subsystems_data_alt.get_time(self.file_df,self.max_current)
        self.time_all = getting_subsystems_data_alt.get_time(self.file_df,15)
        self.foil_number = getting_subsystems_data_alt.get_foil_number(self.file_df,self.max_current) 
        self.probe_current = getting_subsystems_data_alt.get_probe_current(self.file_df)
        # creating dataframes for all the different susbystems with time evolution 
        self.df_subsystem_source = getting_subsystems_alt.get_subsystems_dataframe_source(self)
        self.df_subsystem_vacuum = getting_subsystems_alt.get_subsystems_dataframe_vacuum(self)
        self.df_subsystem_magnet = getting_subsystems_alt.get_subsystems_dataframe_magnet(self)
        self.df_subsystem_rf = getting_subsystems_alt.get_subsystems_dataframe_rf(self)
        self.df_subsystem_rf_sparks = getting_subsystems_alt.get_subsystems_dataframe_rf_sparks(self)
        dee1_voltage = self.df_subsystem_rf.Dee_1_kV
        dee2_voltage = self.df_subsystem_rf.Dee_2_kV
        flap1_pos = self.df_subsystem_rf_sparks.Flap1_pos
        flap2_pos = self.df_subsystem_rf_sparks.Flap2_pos
        self.df_subsystem_rf_source = self.df_subsystem_rf_sparks[getattr(self.df_subsystem_rf_sparks,"Arc_I").astype(float) > 0.2*np.max(getattr(self.df_subsystem_rf_sparks,"Arc_I").astype(float))]
        sparks_dee_1 = self.df_subsystem_rf_source.Dee_1_kV[getattr(self.df_subsystem_rf_source,"Dee_1_kV").astype(float) < np.max(dee1_voltage.astype(float))*0.75]
        sparks_dee_2 = self.df_subsystem_rf_source.Dee_2_kV[getattr(self.df_subsystem_rf_source,"Dee_2_kV").astype(float) < np.max(dee2_voltage.astype(float))*0.75]
        self.sparks_number = len(sparks_dee_1) + len(sparks_dee_2)
        # distance to find resonance
        print ("RESONANCE")
        self.initial_flap_1 = self.df_subsystem_rf_sparks.Flap1_pos.iloc[1]
        self.resonance_flap_1 = (self.df_subsystem_rf_sparks.Flap1_pos[self.df_subsystem_rf_sparks.Dee_1_kV > 0].iloc[1])
        self.distance_flap_1 = self.resonance_flap_1-self.initial_flap_1
        # 
        self.initial_flap_2 = self.df_subsystem_rf_sparks.Flap2_pos.iloc[0]
        self.resonance_flap_2 = (self.df_subsystem_rf_sparks.Flap2_pos[self.df_subsystem_rf_sparks.Dee_2_kV > 0].iloc[1])
        self.distance_flap_2 = self.resonance_flap_2-self.initial_flap_2
        # computing the time needed for finding resonance and speed
        # computing the time needed for finding resonance and speed (NOT SURE)
        #before_starting_resonance_flap_1 = (self.df_subsystem_rf_sparks.Flap1_pos[self.df_subsystem_rf_sparks.Dee_1_kV == 0].index[0])
        print ("INDEXES")
        index_starting_flap_1 = (self.df_subsystem_rf_sparks.Flap1_pos[self.df_subsystem_rf_sparks.Dee_1_kV > 0].index[1])
        starting_resonance_1 = (index_starting_flap_1)*3
        self.resonance_speed_1 = (float(self.resonance_flap_1)-float(self.initial_flap_1))/starting_resonance_1
        #
        #before_starting_resonance_flap_2 = (self.df_subsystem_rf_sparks.Flap2_pos[self.df_subsystem_rf_sparks.Dee_2_kV == 0].index[-1])
        index_starting_flap_2 = (self.df_subsystem_rf_sparks.Flap2_pos[self.df_subsystem_rf_sparks.Dee_2_kV > 0].index[1])
        starting_resonance_2 = (index_starting_flap_2)*3
        self.resonance_speed_2 = (float(self.resonance_flap_2)-float(self.initial_flap_2))/starting_resonance_2
        # computing instant speed 
        instant_speed_1 = ((np.array(self.df_subsystem_rf.Flap1_pos.astype(float))[-1]-np.array(self.df_subsystem_rf.Flap1_pos.astype(float))[0])/(3*len(self.df_subsystem_rf.Flap1_pos.astype(float)))*3600)
        print ("INSTANT SPEED")
        print (instant_speed_1)
        self.average_instant_speed_1 = np.average(instant_speed_1)
        self.max_instant_speed_1 = np.max(instant_speed_1)
        self.std_instant_speed_1 = np.std(instant_speed_1)
        #
        instant_speed_2 = ((np.array(self.df_subsystem_rf.Flap2_pos.astype(float))[-1]-np.array(self.df_subsystem_rf.Flap2_pos.astype(float))[0])/(3*len(self.df_subsystem_rf.Flap2_pos.astype(float)))*3600)
        self.average_instant_speed_2 = np.average(instant_speed_2)
        self.max_instant_speed_2 = np.max(instant_speed_2)
        self.std_instant_speed_2 = np.std(instant_speed_2)
        #index_ending_flap = (self.df_subsystem_rf_sparks.Flap1_pos[self.df_subsystem_rf_sparks.Dee_1_kV > 0].index[-1])
        foil_number = np.average((self.df_subsystem_rf.Foil_No))
        self.df_subsystem_extraction = getting_subsystems_alt.get_subsystems_dataframe_extraction(self)
        self.df_subsystem_beam = getting_subsystems_alt.get_subsystems_dataframe_beam(self)
        self.df_subsystem_pressure = getting_subsystems_alt.get_subsystems_dataframe_pressure(self) 
        self.df_subsystem_pressure_irradiation = getting_subsystems_alt.get_subsystems_dataframe_pressure_irradiation(self) 
        self.df_isochronism = getting_subsystems_data_alt.get_isochronism(self.file_df)
        #[self.probe_current,self.ion_source_current,self.source_performance,self.source_performance_std] = getting_subsystems_data_alt.get_ion_source_performance(self.file_df) #  
        # Adds dataframe to previous dataframes in case it has been already oppened,

def file_open_summary(self):
        getting_summaries_alt.get_summary_ion_source(self)
        getting_summaries_alt.get_summary_vacuum(self)
        getting_summaries_alt.get_summary_magnet(self)
        getting_summaries_alt.get_summary_rf(self)
        getting_summaries_alt.get_summary_extraction(self)
        getting_summaries_alt.get_summary_beam(self)
        getting_summaries_alt.get_summary_volume(self)
        getting_subsystems_data_alt.get_transmission(self)
        getting_subsystems_data_alt.get_pressure_fluctuations(self,0)
        getting_subsystems_data_alt.get_filling_volume(self,0) 
        self.voltage_limit = (0.8*(self.df_rf.DEE1_VOLTAGE_AVE))  
        self.voltage_values = ["Dee_1_kV","Dee_2_kV"] 
        print ("SUMMARY RF!!!!!!")
        print (self.df_rf)    
        #self.voltage_dee_1 = getting_sparks(self,self.voltage_values[0])
        #self.voltage_dee_2 = getting_sparks(self,self.voltage_values[1])

def getting_sparks(self,voltage_value):
        voltage_dee = self.df_subsystem_rf_sparks.Dee_1_kV[getattr(self.df_subsystem_rf_sparks,voltage_value) < float(self.voltage_limit.iloc[self.current_row])]
        return (voltage_dee)