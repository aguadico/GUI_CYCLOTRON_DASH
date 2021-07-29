import pandas as pd
import numpy as np
import os
from datetime import datetime
import tfs
from scipy.optimize import curve_fit
import saving_files_summary_list_20200420
import computing_charge_df

def _parse_args():
    parser = OptionParser()
    parser.add_option("-i", "--input",
                    help="Input measurement path",
                    metavar="INPUT", dest="input_path")
    options, _ = parser.parse_args()
    return options.input_path

class cumulative_charge:
    def __init__(self):
        self.target_current = 0
        self.foil_individual_1 = 0
        self.foil_individual_2 = 0
        self.foil_individual_3 = 0
        self.foil_individual_4 = 0
        self.foil_individual_5 = 0
        self.foil_individual_6 = 0
    def cumluative_charge_calculation(self,previous_value,generic):
        print ("HEREEEE")
        generic = previous_value

class file_information:
    def __init__(self):
       self.file_number = []
       self.week = []
       self.date_stamp = []
    def selecting_file_summary(self,file):
        [target_number,date_stamp,name,file_number] = saving_files_summary_list_20200420.get_headers(file)
        self.file_number.append(file_number)
        date_stamp_format = datetime.strptime(date_stamp, '%Y-%m-%d')
        self.week.append(date_stamp_format.isocalendar()[1])
        self.date_stamp.append(date_stamp)

class central_region:
    def __init__(self):
       self.gas_flow = []
       self.vacuum = []  
       self.vacuum_ave = []
       self.vacuum_std = [] 
       self.vacuum_probe = []
       self.probe_current_transmission = []
       self.probe_current_transmission_std = []
       self.probe_vacuum_transmission = []
       self.source_current_estable = []
       self.source_current = []
       self.transmission_option_a = []
       self.transmission_option_b = []
       self.transmission_option_c = []
    def selecting_central_region_data(self,file_df,max_current,max_current_isochronism):
       vacuum = getting_estable_values(file_df,max_current,"Vacuum_P")*1e5
       source_current_estable = getting_estable_values(file_df,max_current,"Arc_I")
       probe_current = getting_initial_probe_values(file_df,max_current,"Probe_I") 
       vacuum_probe = getting_initial_probe_values(file_df,max_current,"Vacuum_P")*1e5   
       gas_flow = getting_estable_values(file_df,max_current,"Arc_I")
       self.source_current.append(file_df.Arc_I.astype(float).sum())      
       self.probe_current_transmission.append(np.average(probe_current))
       self.probe_vacuum_transmission.append(np.average((vacuum_probe)))
       self.vacuum_ave.append(np.average(vacuum.astype(float)))
       self.probe_current_transmission_std.append(np.std(probe_current))
       self.vacuum_std.append(np.std(vacuum.astype(float)))
       self.source_current_estable.append(np.average(source_current_estable)) 
       self.transmission_option_a.append(max_current_isochronism/np.average(probe_current))
       self.transmission_option_b.append(max_current_isochronism/np.max(probe_current))
       self.transmission_option_c.append(np.average(max_current_isochronism/(probe_current))) 
       self.gas_flow.append(np.max(gas_flow))

class rf_values: 
    def __init__(self):
        self.rf = []
        self.rf_power = []
    def selecting_central_region_data(self,file_df):
        rf_voltage = getting_estable_values(file_df,max_current,"Dee_1_kV")
        rf_power = getting_estable_values(file_df,max_current,"RF_fwd_W")
        self.rf.append(np.max(rf_voltage))
        self.rf_power.append(np.max(rf_power))
      
  
class target_parameters:
    def __init__(self):        
        self.vacuum = []
        self.target_number_list = []
        self.target_current = []
        self.foil_current = []
        self.target_volume = []
        self.pressure_initial_all = []
        self.pressure_final_all = []
        self.probe_current_estimated = []
        self.target_to_foil_ratio = []
    def selecting_data(self,file_df,max_current,transmission):
        target_current = getting_estable_values(file_df,max_current,"Target_I")
        foil_current = getting_estable_values(file_df,max_current,"Foil_I")
        self.target_current.append(np.average(target_current))
        self.foil_current.append(np.average(foil_current))
        self.target_to_foil_ratio.append(np.average(target_current/foil_current))
        self.probe_current_estimated.append(np.average(foil_current/transmission))
        pressure_initial = np.min(file_df.Target_P.astype(float)[0:np.min(file_df.Target_P[file_df.Target_P.astype(float) > 400].index)])
        pressure_final = file_df.Target_P.astype(float)[np.min(file_df.Target_P[file_df.Target_P.astype(float) > 400].index)]
        self.pressure_initial_all.append(pressure_initial)
        self.pressure_final_all.append(pressure_final)
        self.target_volume.append((pressure_final-pressure_initial)/pressure_final)

def getting_estable_values(file_df,max_current,attribute):
    return getattr(file_df,attribute)[file_df.Target_I.astype(float) > 0.7*(max_current)].astype(float)

def getting_initial_probe_values(file_df,max_current,attribute):
    return getattr(file_df,attribute).astype(float)[(file_df.Probe_I.astype(float) > 14) & (file_df.Probe_I.astype(float) < 16)] 


def main():
    #folder = "/Users/anagtv/Documents/OneDrive/046 - Medical Devices/Mantenimientos ciclotrones/MRS/LOGS/2018"
    folder = "/Users/anagtv/Documents/OneDrive/046 - Medical Devices/Mantenimientos ciclotrones/TCP/LOGS/2021"
    filename_completed = []
    for file in os.listdir(folder):
         filename_completed.append(os.path.join(folder,file))
    target = target_parameters()
    central_region_summary = central_region()
    file_summary = file_information()
    week_list = []
    filename_completed_current = []
    transmission_all = []
    vacuum_transmission = []
    probe_current_all = []
    probe_current_std_all = []
    j = -1
    for file in filename_completed:
        real_values = saving_files_summary_list_20200420.get_irradiation_information(file)
        data_df = saving_files_summary_list_20200420.get_data(real_values)
        target_max_current = np.max(data_df.Target_I.astype(float))
        target_average_current = np.average(data_df.Target_I.astype(float))
        if target_average_current > 10.0:
            j += 1
            file_summary.selecting_file_summary(file)
            df_isochronism = saving_files_summary_list_20200420.get_isochronism(data_df)
            central_region_summary.selecting_central_region_data(data_df,target_max_current,np.max(df_isochronism.Foil_I))
            target.selecting_data(data_df,target_max_current,central_region_summary.transmission_option_a[j])
    df_source = pd.DataFrame(list(zip(file_summary.date_stamp,file_summary.file_number,central_region_summary.source_current_estable,central_region_summary.source_current,target.probe_current_estimated,target.target_current)),columns=["DATE","FILE","SOURCE_CURRENT_AVE","SOURCE_CURRENT_CUMULATIVE","PROBE","TARGET"])
    df_source_sort = df_source.sort_values(by="FILE",ignore_index=True)
    cummulative_source = []
    for i in range(len(df_source_sort.PROBE)):
        cummulative_source.append(df_source_sort.SOURCE_CURRENT_CUMULATIVE[0:i].sum()*3/3600)
    df_source_sort["CUMULATIVE_SOURCE_CURRENT"] = cummulative_source
    print (df_source_sort)
    tfs.write("source_performance_values.out",df_source_sort)
       
    

if __name__ == "__main__":
    _input_path = _parse_args()
    main(_input_path)
