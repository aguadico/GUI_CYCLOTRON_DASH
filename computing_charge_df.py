import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os 
import pandas as pd
import getting_subsystems_data
import tfs


COLUMN_NAMES = ["DATE","FILE","FOIL","TARGET","CURRENT_SOURCE","CURRENT_FOIL","CURRENT_COLL_L","CURRENT_TARGET","CURRENT_COLL_R"]
df_information = pd.DataFrame(columns=["DATE","FILE","FOIL","TARGET","CURRENT_SOURCE","CURRENT_FOIL","CURRENT_COLL_L","CURRENT_TARGET","CURRENT_COLL_R"])
TIME_PERIOD = ['2021-03-01','2021-12-31']
LIST_NAMES = ["Arc_I","Foil_I","Coll_l_I","Target_I","Coll_r_I"]
FOIL_LIST_NAME = ["CURRENT_SOURCE","CURRENT_FOIL","CURRENT_COLL_L","CURRENT_TARGET","CURRENT_COLL_R"]

def _parse_args():
    parser = OptionParser()
    parser.add_option("-i", "--input",
                    help="Input measurement path",
                    metavar="INPUT", dest="input_path")
    options, _ = parser.parse_args()
    return options.input_path

class target_cumulative_current:
    def __init__(self,df_information):
        self.df_information = df_information
        self.df_information["DATE"] = []
        self.df_information["FOIL"] = [] 
        self.df_information["TARGET"] = []
        self.df_information["CURRENT_SOURCE"] = [] 
        self.df_information["CURRENT_FOIL"] = []
        self.df_information["CURRENT_COLL_L"] = []
        self.df_information["CURRENT_TARGET"] = []
        self.df_information["CURRENT_COLL_R"] = []
        self.df_information_foil = df_information
    def selecting_data_to_plot_reset(self,file_df,target,date_stamp_i,file_number):
        foil_total = (file_df.Foil_No.iloc[-1])
        target_number_list = (int(target[1]))
        total_list = [date_stamp_i,float(file_number),foil_total,target_number_list]
        if np.average(file_df.Target_I.astype(float)) > 0.0:
            for name in LIST_NAMES:  
                initial_hour_string = file_df.Time[file_df.Target_I.astype(float) > 0.01*np.max(file_df.Target_I.astype(float))].iloc[0]
                final_hour_string = file_df.Time[file_df.Target_I.astype(float) > 0.01*np.max(file_df.Target_I.astype(float))].iloc[-1]
                initial_hour = float(initial_hour_string[0:2])*3600+float(initial_hour_string[3:5])*60+float(initial_hour_string[6:8])
                final_hour = float(final_hour_string[0:2])*3600+float(final_hour_string[3:5])*60+float(final_hour_string[6:8])
                average_current = np.average(getattr(file_df,name)[file_df.Target_I.astype(float) > 0.01*np.max(file_df.Target_I.astype(float))].astype(float))
                length = (final_hour-initial_hour)/3600
                total_list.append(average_current.astype(float)*length)
            df_individual = pd.DataFrame([total_list],columns=COLUMN_NAMES)    
            self.df_information = self.df_information.append(df_individual)   
        else:
            print ("HERRREEEEEE")
            print (file_df)
           
    def selecting_foil(self,file_df):       
        total_foil_list = [np.min(file_df.DATE),len(file_df.FILE),np.min(file_df.FOIL),np.min(file_df.TARGET)]
        for name in FOIL_LIST_NAME:
            total_foil_list.append(getattr(file_df,name).astype(float).sum())
        print ("FOIL DF")
        print (file_df)
        print (FOIL_LIST_NAME)
        #foil_total = (file_df.FOIL.iloc[-1])
        df_individual = pd.DataFrame([total_foil_list],columns=COLUMN_NAMES)
        self.df_information_foil = self.df_information_foil.append(df_individual) 

#selecting folder to analyze

def get_logfiles_from_folder(folder):
    filename_completed = []
    for file in os.listdir(folder):
        filename_completed.append(os.path.join(folder,file))
    return filename_completed 

def get_target_division(file,target_1,target_2):
    [target_number,date_stamp,name,file_number] = getting_subsystems_data.get_headers(file)
    real_values = getting_subsystems_data.get_irradiation_information(file)
    data_df = getting_subsystems_data.get_data(real_values)
    data_df_not_zero = data_df[data_df.Arc_I != "0"]
    if float(target_number[1]) in [1.0,2.0,3.0]: 
        target_1.selecting_data_to_plot_reset(data_df,target_number,date_stamp,file_number)
    else:
        target_2.selecting_data_to_plot_reset(data_df,target_number,date_stamp,file_number)

def get_summation_per_period(target):
    #for i in range(len(TIME_PERIOD)):
    target.df_information = target.df_information[(target.df_information['DATE'] > TIME_PERIOD[0]) & (target.df_information['DATE'] < TIME_PERIOD[1])].sort_values(by="FILE").reset_index(drop=True)
    target.df_information.reset_index(drop=True)    
    foil_list = list(target.df_information.FOIL.drop_duplicates().index)
    foil_list.append(target.df_information.FOIL.index[-1])
    print ("FOIL LIST")
    print (foil_list)
    for i in range(len(foil_list)-1):
        df_information_foil = target.df_information[foil_list[i]:foil_list[i+1]]
        target.selecting_foil(df_information_foil)

def saving_dataframe(target,output_name):
    df_total = pd.DataFrame(list(zip(target.df_information_foil.FILE,target.df_information_foil.FOIL,target.df_information_foil.TARGET,target.df_information_foil.CURRENT_SOURCE,target.df_information_foil.CURRENT_FOIL,target.df_information_foil.CURRENT_COLL_L ,target.df_information_foil.CURRENT_TARGET,target.df_information_foil.CURRENT_COLL_R
)),columns=["FILE","FOIL","TARGET","CURRENT_SOURCE","CURRENT_FOIL","CURRENT_COLL_L" ,"CURRENT_TARGET","CURRENT_COLL_R"])
    print ("DF TOTAL")
    print (df_total.dropna())
    tfs.write(output_name,df_total.dropna())


def main(input_path):
    folder = "/Users/anagtv/Documents/OneDrive/046 - Medical Devices/Mantenimientos ciclotrones/TCP/LOGS/2021/Last_maintenance"
    filename_completed  = get_logfiles_from_folder(input_path)
    target_1 = target_cumulative_current(df_information)
    target_2 = target_cumulative_current(df_information)
    for file in filename_completed:
         get_target_division(file,target_1,target_2)
    get_summation_per_period(target_1)
    print ("TARGET 2")
    get_summation_per_period(target_2)
    print ("TARGET 1")
    saving_dataframe(target_1,"cumulated_charge_1.out")
    print ("TARGET 2")
    saving_dataframe(target_2,"cumulated_charge_2.out")

if __name__ == "__main__":
    _input_path = _parse_args()
    main(_input_path)






