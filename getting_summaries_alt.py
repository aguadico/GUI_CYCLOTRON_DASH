import pandas as pd
import numpy as np
import getting_subsystems_data_alt
import columns_names
va = 0
def get_summary_ion_source(self): 
    source_current = self.df_subsystem_source.Arc_I
    source_voltage = self.df_subsystem_source.Arc_V
    gas_flow = self.df_subsystem_source.Gas_flow
    ratio_current = self.df_subsystem_source.Ratio_current
    foil_number = np.average(self.df_subsystem_source.Foil_No)
    ave_source_current,std_source_current,max_source_current,min_source_current = getting_subsystems_data_alt.get_statistic_values(source_current)  
    ave_source_voltage,std_source_voltage,max_source_voltage,min_source_voltage = getting_subsystems_data_alt.get_statistic_values(source_voltage)  
    ave_gas_flow,std_gas_flow,max_gas_flow,min_gas_flow = getting_subsystems_data_alt.get_statistic_values(gas_flow) 
    ave_ratio_current,std_ratio_current,max_ratio_current,min_ratio_current = getting_subsystems_data_alt.get_statistic_values(ratio_current)
    df_source_values = [[np.float(int(self.file_number)),self.date_stamp,self.target_number,foil_number,
    float(max_source_current),float(min_source_current),float(ave_source_current),float(std_source_current),
    float(max_source_voltage),float(min_source_voltage),float(ave_source_voltage),float(std_source_voltage),
    float(max_gas_flow),
    float(max_ratio_current),float(min_ratio_current),float(ave_ratio_current),float(std_ratio_current),float(std_source_current)/float(ave_source_current)*100,0]]
    df_source_i = pd.DataFrame(df_source_values,columns=columns_names.COLUMNS_SOURCE)
    self.df_source = self.df_source.append(df_source_i,ignore_index=True)


def get_summary_vacuum(self):
    vacuum_level = self.df_subsystem_vacuum.Vacuum_P
    gas_flow = self.df_subsystem_source.Gas_flow
    ave_gas_flow,std_gas_flow,max_gas_flow,min_gas_flow = getting_subsystems_data_alt.get_statistic_values(gas_flow) 
    foil_number = np.average((self.df_subsystem_vacuum.Foil_No))
    ave_vacuum,std_vacuum,max_vacuum,min_vacuum = getting_subsystems_data_alt.get_statistic_values(vacuum_level)
    vacuum_values = [[np.float(int(self.file_number)),self.date_stamp,self.target_number,foil_number,float(max_vacuum)*1e5,float(min_vacuum)*1e5,float(ave_vacuum)*1e5,float(std_vacuum)*1e5,
    float(std_vacuum)/float(ave_vacuum),0,float(ave_vacuum)/float(ave_gas_flow)*100,((float(std_vacuum)**2+float(ave_gas_flow)**2))**0.5/float(ave_gas_flow)*100]]
    df_vacuum_i = pd.DataFrame((vacuum_values),columns=columns_names.COLUMNS_VACUUM)
    self.df_vacuum = self.df_vacuum.append(df_vacuum_i,ignore_index=True)

def get_summary_volume(self):
    pressure_initial = np.min(self.df_subsystem_pressure.Target_P.astype(float)[0:np.min(self.df_subsystem_pressure.Target_P[self.df_subsystem_pressure.Target_P.astype(float) > 400].index)])
    pressure_final = self.df_subsystem_pressure.Target_P.astype(float)[np.min(self.df_subsystem_pressure.Target_P[self.df_subsystem_pressure.Target_P.astype(float) > 400].index)]
    pressure_irradiation = self.df_subsystem_pressure_irradiation.Target_P
    foil_number = np.average((self.df_subsystem_vacuum.Foil_No))
    vacuum_level = self.df_subsystem_vacuum.Vacuum_P
    volume = ((pressure_final-pressure_initial)/pressure_final)
    ave_pressure,std_pressure,max_pressure,min_pressure = getting_subsystems_data_alt.get_statistic_values(pressure_irradiation)
    ave_volume,std_volume,max_volume,min_volume = getting_subsystems_data_alt.get_statistic_values(volume)
    volume_values = [[np.float(int(self.file_number)),self.date_stamp,self.target_number,foil_number,pressure_initial,pressure_final,
    float(max_pressure),float(min_pressure),float(ave_pressure),float(std_pressure),
    float(max_volume)*1e5,float(min_volume)*1e5,float(ave_volume)*1e5,float(std_volume)*1e5]]
    df_volume_i = pd.DataFrame((volume_values),columns=columns_names.COLUMNS_VOLUME)
    self.df_volume = self.df_volume.append(df_volume_i,ignore_index=True)

def get_summary_magnet(self):
    magnet_current = self.df_subsystem_magnet.Magnet_I
    foil_number = np.average((self.df_subsystem_magnet.Foil_No))
    ave_magnet_current,std_magnet_current,max_magnet_current,min_magnet_current = getting_subsystems_data_alt.get_statistic_values(magnet_current)
    start_isochronism = np.min(self.df_isochronism.Magnet_I)
    end_isochronism = np.max(self.df_isochronism.Magnet_I)
    iso_average = np.average([start_isochronism,end_isochronism])
    print ("ISOCHRONISM")
    print (self.df_isochronism.Magnet_I)
    if len(self.df_isochronism.Magnet_I) == 0:
        selected_value =  (self.df_subsystem_magnet.Magnet_I.iloc[0])
    elif len(self.df_isochronism.Magnet_I) != 0:
        selected_value = self.df_isochronism.Magnet_I.iloc[-1]
    selected_value_rel = 50/(iso_average/selected_value)  
    magnet_current = pd.concat([self.time_all,self.magnet_current_total],axis=1,keys=["Time","Current_I"])
    time_values = magnet_current.drop_duplicates(subset="Current_I").Time.astype(str)
    initial_time = time_values.iloc[0]
    if len(magnet_current.drop_duplicates(subset="Current_I").Time) > 1:  
        final_time = time_values.iloc[1]
        total_time = [initial_time,final_time]   
        initial_time_seconds =  (int(total_time[0].split(":")[0])*3600+int(total_time[0].split(":")[1])*60+int(total_time[0].split(":")[2])) 
        if int(total_time[0].split(":")[0]) > int(total_time[-1].split(":")[0]):
            final_time_seconds = (int(total_time[-1][0])+24)*3600+int(total_time[-1].split(":")[1])*60+int(total_time[-1].split(":")[2])
        elif int(total_time[0].split(":")[0]) <= int(total_time[-1].split(":")[0]):
            final_time_seconds = (int(total_time[-1].split(":")[0])*3600+int(total_time[-1].split(":")[1])*60+int(total_time[-1].split(":")[2]))
        delta_minutes = (final_time_seconds - initial_time_seconds)/60
    elif len(magnet_current.drop_duplicates(subset="Current_I").Time) <= 1:
        delta_minutes = 0
    magnet_values = [[np.float(int(self.file_number)),self.date_stamp,self.target_number,foil_number,float(max_magnet_current),float(min_magnet_current),float(ave_magnet_current),float(std_magnet_current),
    float(start_isochronism),float(end_isochronism),float(selected_value),float(selected_value_rel),0,float(delta_minutes),0]]
    df_magnet_i = pd.DataFrame((magnet_values),columns=columns_names.COLUMNS_MAGNET)
    self.df_magnet = self.df_magnet.append(df_magnet_i,ignore_index=True)
    

def get_summary_rf(self):
    dee1_voltage = self.df_subsystem_rf.Dee_1_kV
    dee2_voltage = self.df_subsystem_rf.Dee_2_kV
    forwarded_power = self.df_subsystem_rf.RF_fwd_W
    reflected_power = self.df_subsystem_rf.RF_refl_W
    phase_load = self.df_subsystem_rf.Phase_load
    flap1_pos = self.df_subsystem_rf.Flap1_pos
    flap2_pos = self.df_subsystem_rf.Flap2_pos
    foil_number = np.average((self.df_subsystem_rf.Foil_No))
    ave_dee1_voltage,std_dee1_voltage,max_dee1_voltage,min_dee1_voltage = getting_subsystems_data_alt.get_statistic_values(dee1_voltage)   
    ave_dee2_voltage,std_dee2_voltage,max_dee2_voltage,min_dee2_voltage = getting_subsystems_data_alt.get_statistic_values(dee2_voltage)
    ave_forwarded_power,std_forwarded_power,max_forwarded_power,min_forwarded_power = getting_subsystems_data_alt.get_statistic_values(forwarded_power)
    ave_reflected_power,std_reflected_power,max_reflected_power,min_reflected_power = getting_subsystems_data_alt.get_statistic_values(reflected_power)
    ave_flap1_pos,std_flap1_pos,max_flap1_pos,min_flap1_pos = getting_subsystems_data_alt.get_statistic_values(flap1_pos)
    ave_flap2_pos,std_flap2_pos,max_flap2_pos,min_flap2_pos = getting_subsystems_data_alt.get_statistic_values(flap2_pos)
    ave_phase_load,std_phase_load,max_phase_load,min_phase_load = getting_subsystems_data_alt.get_statistic_values(phase_load)  
    rf_values = [[np.float(int(self.file_number)),self.date_stamp,self.target_number,foil_number,max_dee1_voltage,min_dee1_voltage,ave_dee1_voltage,std_dee1_voltage,max_dee2_voltage,min_dee2_voltage,ave_dee2_voltage,std_dee2_voltage,
    max_forwarded_power,min_forwarded_power,ave_forwarded_power,std_forwarded_power,max_reflected_power,min_reflected_power,ave_reflected_power,std_reflected_power,max_phase_load,min_phase_load,ave_phase_load,std_phase_load,max_flap1_pos,
    min_flap1_pos,ave_flap1_pos,std_flap1_pos,
    max_flap2_pos,min_flap2_pos,ave_flap2_pos,std_flap2_pos,
    self.sparks_number,self.distance_flap_1,self.average_instant_speed_1,self.max_instant_speed_1,self.std_instant_speed_1,
    self.distance_flap_2,self.average_instant_speed_2,self.max_instant_speed_2,self.std_instant_speed_2,
    ave_reflected_power*100,std_reflected_power*100,std_dee1_voltage/ave_dee1_voltage*100,std_dee2_voltage/ave_dee2_voltage*100,0,0,
    0,0,0,0,0,0,0]]
    df_rf_i = pd.DataFrame((rf_values),columns=columns_names.COLUMNS_RF)      
    self.df_rf = self.df_rf.append(df_rf_i,ignore_index=True)


def get_summary_extraction(self):
    #Aquí es donde tengo que extraer el número de target + numero de target
    carousel_position = self.df_subsystem_extraction.Extr_pos
    balance_position = self.df_subsystem_extraction.Balance
    foil_number = np.average((self.df_subsystem_extraction.Foil_No))
    ave_carousel_position,std_carousel_position, max_carousel_position, min_carousel_position = getting_subsystems_data_alt.get_statistic_values(carousel_position)
    ave_balance_position,std_balance_position, max_balance_position, min_balance_position = getting_subsystems_data_alt.get_statistic_values(balance_position)
    print ("TARGET NUMBER")
    print (self.target_number)
    if float(self.target_number) <= 3:
        carousel_number = 1
    elif float(self.target_number)>3: 
        carousel_number = 4
    if ave_carousel_position/3 <= 10: 
        position = 0
    elif ((ave_carousel_position/3 > 10) & (ave_carousel_position/3 < 20)):
        position = 1
    elif ave_carousel_position/3 > 20:
        position = 2
    phys_number = carousel_number + position
    print (phys_number)
    extraction_values = [[np.float(int(self.file_number)),self.date_stamp,self.name,self.target_number,phys_number,foil_number,max_carousel_position,min_carousel_position,ave_carousel_position,std_carousel_position,max_balance_position,min_balance_position,ave_balance_position,std_balance_position]]
    df_extraction_i = pd.DataFrame((extraction_values),columns=columns_names.COLUMNS_EXTRACTION)      
    self.df_extraction = self.df_extraction.append(df_extraction_i,ignore_index=True)



def get_summary_beam(self):
    target_current = self.df_subsystem_beam.Target_I
    extraction_current = self.df_subsystem_beam.Foil_I 
    collimator_r = self.df_subsystem_beam.Coll_r_I   
    collimator_l = self.df_subsystem_beam.Coll_l_I  
    collimator_r_rel = self.df_subsystem_beam.Coll_r_rel 
    collimator_l_rel = self.df_subsystem_beam.Coll_l_rel
    target_rel = self.df_subsystem_beam.Target_rel
    extraction_losses = self.df_subsystem_beam.Extraction_losses
    foil_number = np.average((self.df_subsystem_beam.Foil_No))
    collimator_total_rel = collimator_r_rel + collimator_l_rel
    ave_extraction_current,std_extraction_current,max_extraction_current,min_extraction_current = getting_subsystems_data_alt.get_statistic_values(extraction_current)
    ave_target_current,std_target_current,max_target_current,min_target_current = getting_subsystems_data_alt.get_statistic_values(target_current)
    ave_collimator_r,std_collimator_r, max_collimator_r, min_collimator_r = getting_subsystems_data_alt.get_statistic_values(collimator_r)
    ave_collimator_l,std_collimator_l, max_collimator_l, min_collimator_l = getting_subsystems_data_alt.get_statistic_values(collimator_l)
    ave_collimator_r_rel,std_collimator_r_rel, max_collimator_r_rel, min_collimator_r_rel = getting_subsystems_data_alt.get_statistic_values(collimator_r_rel)
    ave_collimator_l_rel,std_collimator_l_rel, max_collimator_l_rel, min_collimator_l_rel = getting_subsystems_data_alt.get_statistic_values(collimator_l_rel)
    ave_collimator_total_rel,std_collimator_total_rel, max_collimator_total_rel, min_collimator_total_rel = getting_subsystems_data_alt.get_statistic_values(collimator_total_rel)
    ave_target_rel,std_target_rel,max_target_rel,min_target_rel = getting_subsystems_data_alt.get_statistic_values(target_rel)
    ave_extraction_losses,std_extraction_losses,max_extraction_losses,min_extraction_losses = getting_subsystems_data_alt.get_statistic_values(extraction_losses)
    beam_values = [[np.float(int(self.file_number)),self.date_stamp,self.target_number,foil_number,
    max_collimator_l,min_collimator_l, ave_collimator_l, std_collimator_l,
    max_collimator_r,min_collimator_r, ave_collimator_r, std_collimator_r,
    max_collimator_l_rel,min_collimator_l_rel, ave_collimator_l_rel, std_collimator_l_rel,
    max_collimator_r_rel,min_collimator_r_rel, ave_collimator_r_rel, std_collimator_r_rel,
    max_target_current,min_target_current,ave_target_current,std_target_current,
    max_extraction_current,min_extraction_current,ave_extraction_current,std_extraction_current,
    max_target_rel,min_target_rel,ave_target_rel,std_target_rel,
    max_extraction_losses,min_extraction_losses,ave_extraction_losses,std_extraction_losses, 
    max_collimator_total_rel,min_collimator_total_rel, ave_collimator_total_rel, std_collimator_total_rel,float(std_target_rel)/float(ave_target_rel),0]]
    df_beam_i = pd.DataFrame((beam_values),columns=columns_names.COLUMNS_BEAM )      
    self.df_beam = self.df_beam.append(df_beam_i,ignore_index=True)


def get_filling_volume(self,va):
    #pressure_initial = np.min(self.df_subsystem_pressure.Target_P.astype(float)[0:np.min(self.df_subsystem_pressure.Target_P[self.df_subsystem_pressure.Target_P.astype(float) > 400].index)])
    #pressure_final = self.df_subsystem_pressure.Target_P.astype(float)[np.min(self.df_subsystem_pressure.Target_P[self.df_subsystem_pressure.Target_P.astype(float) > 400].index)]
    pressure_no_current = self.file_df.Target_P.astype(float)[(self.file_df.Target_I.astype(float) < 1)]
    high_pressure = pressure_no_current[pressure_no_current > 400][3:-3]
    low_pressure = pressure_no_current[3:np.min(high_pressure.index)][pressure_no_current < 70]
    high_pressure_ave = np.average(high_pressure)
    high_pressure_std = np.std(high_pressure)
    low_pressure_ave = np.average(low_pressure)
    low_pressure_std = np.std(low_pressure)
    pressure_irradiation_ave = np.average(self.df_subsystem_pressure_irradiation.Target_P)
    pressure_irradiation_std = np.std(self.df_subsystem_pressure_irradiation.Target_P)
    foil_number = np.average((self.df_subsystem_vacuum.Foil_No))
    if float(self.file_df.Target_P[3]) < 100:
        va += 1
        values_filling = self.file_df.Target_P[(self.file_df.Target_P.astype(float) < 100) & (self.file_df.Target_P.astype(float) > 10)] 
        initial_index = self.file_df.Target_P[self.file_df.Target_P.astype(float) > 105].index[0] 
        p_values = self.file_df.Target_P[3:initial_index-1]
        minimal_index = p_values[p_values.astype(float) == np.min(p_values.astype(float))].index[0]
        initial_pressure = float(self.file_df.Target_P[minimal_index])
        final_pressure = float(self.file_df.Target_P[initial_index-1])
        relative_change = (final_pressure-initial_pressure)
        time_list = (va)
        #file = (float(file[:-4]))
    else: 
        relative_change = 0
        time_list = 0
        initial_pressure = self.file_df.Target_P[3] 
        final_pressure = self.file_df.Target_P[3] 
    filling_list = [[np.float(self.file_number),self.date_stamp,self.target_number,relative_change,0,high_pressure_ave,high_pressure_std,low_pressure_ave,low_pressure_std,pressure_irradiation_ave,
    pressure_irradiation_std]]
    df_filling_volume_i = pd.DataFrame(filling_list,columns=columns_names.COLUMNS_FILLING)
    self.df_filling_volume = self.df_filling_volume.append(df_filling_volume_i,ignore_index=True)
