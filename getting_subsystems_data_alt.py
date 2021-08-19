import pandas
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from optparse import OptionParser
import os
from tkinter import *
from pandas import ExcelWriter
plt.rcParams.update({'font.size': 16})
plt.rcParams["figure.figsize"] = (15,10)
import sys
sys.path.append("/Users/anagtv/Desktop/Cyclotron_python")
sys.path.append("/Users/anagtv/Documents/Beta-Beat.src-master")
#from tfs_files import tfs_pandas
#from mpl_interaction import figure_pz
import matplotlib.pyplot as plt
import tfs
import datetime
from datetime import timedelta
import matplotlib.dates as md
from matplotlib.widgets import CheckButtons
import columns_names
va = 0
COLORS = ['#1E90FF','#FF4500','#32CD32',"#6A5ACD","#20B2AA","#00008B","#A52A2A","#228B22"]


def get_data_tuple(path_file):
    all_parts = []
    logfile = open(path_file,"r")
    for line in logfile:
         parts = line.split()
         all_parts.append(
            parts)
    target_number = (np.array(all_parts[0])[1])
    date_stamp = (np.array(all_parts[0])[8])
    site_name = (np.array(all_parts[1])[2])
    if len(np.array(all_parts[0])) == 10: 
        date_stamp = (np.array(all_parts[0])[8] + "0" + np.array(all_parts[0])[9] )
    real_values = all_parts[4:]
    return real_values,target_number,date_stamp,site_name

def get_logfile_lines(path_file):
    lines = []
    logfile = open(path_file,"r")
    for line in logfile:
         parts = line.split()
         lines.append(
            parts)
    return lines

def get_headers(path_file):
    headers_lines = get_logfile_lines(path_file)
    target_number = (np.array(headers_lines[0])[1])
    date_stamp = (np.array(headers_lines[0])[8])
    site_name = (np.array(headers_lines[1])[2])
    file_number = (np.array(headers_lines[0])[6])
    if len(np.array(headers_lines[0])) == 10: 
        date_stamp = (np.array(headers_lines[0])[8] + "0" + np.array(headers_lines[0])[9] )
    return target_number,date_stamp,site_name,file_number

def get_irradiation_information(path_file):
    irradiation_information = get_logfile_lines(path_file)    
    irradiation_information = irradiation_information[4:]
    return irradiation_information  

def get_data(real_values):
    data_df = pd.DataFrame.from_records(real_values)
    column_names = ["Time","Arc_I","Arc_V","Gas_flow","Dee_1_kV","Dee_2_kV","Magnet_I","Foil_I","Coll_l_I","Target_I","Coll_r_I","Vacuum_P","Target_P","Delta_Dee_kV","Phase_load","Dee_ref_V","Probe_I","He_cool_P","Flap1_pos","Flap2_pos","Step_pos","Extr_pos","Balance","RF_fwd_W","RF_refl_W","Foil_No"]
    column_names_nf = ["Time","Arc_I","Arc_V","Gas_flow","Dee_1_kV","Dee_2_kV","Magnet_I","Foil_I","Coll_l_I","Target_I","Coll_r_I","Vacuum_P","Target_P","Delta_Dee_kV","Phase_load","Dee_ref_V","Probe_I","He_cool_P","Flap1_pos","Flap2_pos","Step_pos","Extr_pos","Balance","RF_fwd_W","RF_refl_W"]
    try:
       data_df = data_df.drop([0,1,2], axis=0)
    except:
       data_df = data_df.drop([0],axis=0)
    try: 
       data_df.columns = column_names
    except:
       data_df.columns = column_names_nf 
    return data_df

def get_time(excel_data_df,current):
    time = excel_data_df.Time[excel_data_df['Target_I'].astype(float) > float(current)]
    return time


def get_transmission(self):
    foil_current_max_isochronism = np.average(np.max(self.df_isochronism.Foil_I[:-1].astype(float))/(self.probe_current.astype(float)))
    transmission = foil_current_max_isochronism*100
    transmission_std = np.std(np.max(self.df_isochronism.Foil_I)/(self.probe_current.astype(float)))
    foil_number = np.average(self.df_subsystem_source.Foil_No)
    transmission_list = [[np.float(int(self.file_number)),self.date_stamp,self.target_number,transmission,transmission_std,foil_number]] 
    df_transmission_i = pd.DataFrame((transmission_list),columns=columns_names.COLUMNS_TRANSMISSION)      
    self.df_transmission = self.df_transmission.append(df_transmission_i,ignore_index=True)

 
def get_isochronism(data_df):
    maximum_value = float(max(data_df.Magnet_I))
    minimum_value = float(min(data_df.Magnet_I))
    maximum_value_str = str(maximum_value)
    minimum_value_str = str(minimum_value)
    intial_values = data_df.Magnet_I[data_df.Magnet_I == minimum_value_str]
    final_values = data_df.Magnet_I[data_df.Magnet_I == maximum_value_str]
    if len(final_values) == 0: 
        maximum_value = int(max(data_df.Magnet_I))
        maximum_value_str = str(maximum_value)     
    if len(intial_values) == 0:
        minimum_value = int(max(data_df.Magnet_I))
        minimum_value_str = str(minimum_value)
    final_index = data_df.Magnet_I[data_df.Magnet_I == maximum_value_str].index[0]
    intial_index = data_df.Magnet_I[data_df.Magnet_I == minimum_value_str].index[0]
    magnet_current = data_df.Magnet_I.loc[intial_index:final_index+1].astype(float)
    coll_current_l = data_df.Coll_l_I.loc[intial_index:final_index+1].astype(float)
    coll_current_r = data_df.Coll_r_I.loc[intial_index:final_index+1].astype(float)
    target_current = data_df.Target_I.loc[intial_index:final_index+1].astype(float)
    foil_current = data_df.Foil_I.loc[intial_index:final_index+1].astype(float)
    time = data_df.Time.loc[intial_index:final_index+1].astype(str)
    df_column_isochronism = ["Time","Magnet_I","Foil_I","Coll_l_I","Target_I","Coll_r_I"]
    df_subsystem_values_beam = [time,magnet_current,foil_current,coll_current_l,target_current,coll_current_r]
    df_isochronism = pd.concat(df_subsystem_values_beam,axis=1,keys=df_column_isochronism)
    print ("ISOCHRONISM!!!!")
    print (df_isochronism)
    return df_isochronism

def get_probe_current(excel_data_df):
    probe_current = getattr(excel_data_df,"Probe_I").astype(float)[(excel_data_df.Probe_I.astype(float) > 14) & (excel_data_df.Probe_I.astype(float) < 16)]
    return probe_current

def get_foil_number(excel_data_df,current):
    foil_number = excel_data_df.Foil_No[excel_data_df['Target_I'].astype(float) > float(current)].astype(int)
    return foil_number

def get_collimator_parameters(excel_data_df,current):
    collimator_r = excel_data_df.Coll_r_I[excel_data_df['Target_I'].astype(float) > float(current)].astype(float)
    collimator_l = excel_data_df.Coll_l_I[excel_data_df['Target_I'].astype(float) > float(current)].astype(float)
    return collimator_r,collimator_l

def get_source_parameters(excel_data_df,current):
    source_voltage = excel_data_df.Arc_V[excel_data_df['Target_I'].astype(float) > float(current)].astype(float)
    gas_flow = excel_data_df.Gas_flow[excel_data_df['Target_I'].astype(float) > float(current)].astype(float)
    source_current = excel_data_df.Arc_I[excel_data_df['Target_I'].astype(float) > float(current)].astype(float)
    return source_voltage,source_current,gas_flow

def get_rf_parameters(excel_data_df,current):
    dee2_voltage = excel_data_df.Dee_2_kV[excel_data_df['Target_I'].astype(float) > float(current)].astype(float)
    dee1_voltage = excel_data_df.Dee_1_kV[excel_data_df['Target_I'].astype(float) > float(current)].astype(float)
    return dee1_voltage,dee2_voltage

def get_rf_parameters_power(excel_data_df,current):
    forwarded_power = excel_data_df.RF_fwd_W[excel_data_df['Target_I'].astype(float) > float(current)].astype(float)
    reflected_power = excel_data_df.RF_refl_W[excel_data_df['Target_I'].astype(float) > float(current)].astype(float)
    phase_load = excel_data_df.Phase_load[excel_data_df['Target_I'].astype(float) > float(current)].astype(float)
    return forwarded_power,reflected_power,phase_load

def get_rf_parameters_sparks(excel_data_df):
    dee2_voltage = excel_data_df.Dee_2_kV[excel_data_df['Arc_I'].astype(float)].astype(float)
    dee1_voltage = excel_data_df.Dee_1_kV[excel_data_df['Arc_I'].astype(float)].astype(float)
    return dee1_voltage,dee2_voltage

def get_rf_parameters_power_sparks(excel_data_df):
    forwarded_power = excel_data_df.RF_fwd_W[excel_data_df['Arc_I'].astype(float)].astype(float)
    reflected_power = excel_data_df.RF_refl_W[excel_data_df['Arc_I'].astype(float)].astype(float)
    phase_load = excel_data_df.Phase_load[excel_data_df['Arc_I'].astype(float)].astype(float)
    return forwarded_power,reflected_power,phase_load

def get_rf_parameters_flaps_sparks(excel_data_df):
    Flap1_pos = excel_data_df.Flap1_pos[excel_data_df['Arc_I'].astype(float)].astype(float)
    Flap2_pos = excel_data_df.Flap2_pos[excel_data_df['Arc_I'].astype(float)].astype(float)
    return Flap1_pos,Flap2_pos

def get_rf_parameters_flaps(excel_data_df,current):
    Flap1_pos = excel_data_df.Flap1_pos[excel_data_df['Target_I'].astype(float) > float(current)].astype(float)
    Flap2_pos = excel_data_df.Flap2_pos[excel_data_df['Target_I'].astype(float) > float(current)].astype(float)
    return Flap1_pos,Flap2_pos

def get_magnet_parameters(excel_data_df,current):
    magnet_current = excel_data_df.Magnet_I[excel_data_df['Target_I'].astype(float) > float(current)].astype(float)
    return magnet_current

def get_target_pressure(excel_data_df,current):
    target_pressure = excel_data_df.Target_P.astype(float)
    return target_pressure

def get_target_pressure_irradiation(excel_data_df,current):
    max_current = 0.85*(np.max(excel_data_df['Target_I'].astype(float)))
    target_pressure = excel_data_df.Target_P[excel_data_df['Target_I'].astype(float) > float(max_current)].astype(float)
    return target_pressure

def get_target_parameters(excel_data_df):
    max_current = 0.85*(np.max(excel_data_df['Target_I'].astype(float)))
    target_current = excel_data_df.Target_I[excel_data_df['Target_I'].astype(float) > float(max_current)].astype(float)
    return target_current,max_current

def get_source_parameters_limit(excel_data_df):
    max_source_current = -0.05*(np.max(excel_data_df['Arc_I'].astype(float)))
    return max_source_current

def get_extraction_parameters(excel_data_df,current):
    extraction_current = excel_data_df.Foil_I[excel_data_df['Target_I'].astype(float) > float(current)].astype(float)
    return extraction_current

def get_extraction_parameters_position(excel_data_df,current):
    carousel_position = excel_data_df.Extr_pos[excel_data_df['Target_I'].astype(float) > float(current)].astype(float)
    balance_position = excel_data_df.Balance[excel_data_df['Target_I'].astype(float) > float(current)].astype(float)
    return carousel_position,balance_position

def get_vacuum_parameters(excel_data_df,current):
    vacuum_level = excel_data_df.Vacuum_P[excel_data_df['Target_I'].astype(float) > float(current)].astype(float)
    return vacuum_level

def get_pressure_fluctuations(self,va):
    if float(self.file_df.Target_P[3]) < 100:
         va += 1
         values_filling = self.file_df.Target_P[self.file_df.Target_P.astype(float) < 100] 
         initial_index = self.file_df.Target_P[self.file_df.Target_P.astype(float) > 100].index[0] 
         p_values = self.file_df.Target_P[3:initial_index-1]
         minimal_index = p_values[p_values.astype(float) == np.min(p_values.astype(float))].index[0]
         initial_pressure = float(self.file_df.Target_P[minimal_index])
         final_pressure = float(self.file_df.Target_P[initial_index-1])
         relative_change = (final_pressure-initial_pressure)/final_pressure
         time_list = va
         initial_pressure_fluctuations = ((float(initial_pressure) - float(self.file_df.Target_P[3]))*100/float(self.file_df.Target_P[3]))
    else: 
         initial_pressure_fluctuations = 0
         time_list = 0
    pressure_fluctuations = [[np.float(self.file_number),time_list,self.date_stamp,self.target_number,initial_pressure_fluctuations]]
    df_pressure_fluctuations_i = pd.DataFrame(pressure_fluctuations,columns=columns_names.COLUMNS_FLUCTUATIONS)
    self.df_pressure_fluctuations = self.df_pressure_fluctuations.append(df_pressure_fluctuations_i,ignore_index=True)

  

def get_statistic_values(value):
    average_value = (np.mean(value))
    std_value = (np.std(value))
    try:
       max_value = (np.max(value))
       min_value = (np.min(value))
    except:
       max_value = 0
       min_value = 0
    return average_value,std_value,max_value,min_value

def main(input_path,output_path,target_current):
    ...
if __name__ == "__main__":
    main()
