import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os 
import pandas as pd
import tfs


COLUMN_NAMES = ["DATE","FILE","FOIL","TARGET","CURRENT_SOURCE","CURRENT_FOIL","CURRENT_COLL_L","CURRENT_TARGET","CURRENT_COLL_R"]
df_information = pd.DataFrame(columns=["DATE","FILE","FOIL","TARGET","CURRENT_SOURCE","CURRENT_FOIL","CURRENT_COLL_L","CURRENT_TARGET","CURRENT_COLL_R"])
TIME_PERIOD = ['2021-03-01','2021-12-31']
LIST_NAMES = ["Arc_I","Foil_I","Coll_l_I","Target_I","Coll_r_I"]
FOIL_LIST_NAME = ["CURRENT_SOURCE","CURRENT_FOIL","CURRENT_COLL_L","CURRENT_TARGET","CURRENT_COLL_R"]

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

    def get_hour_string(self,file_df,location):
        hour_string = file_df.Time[file_df.Target_I.astype(float) > 0.01*np.max(file_df.Target_I.astype(float))].iloc[location]
        return hour_string

    def cumulative_charge_calculation(self,cyclotron_information):
        #file_df_zero = cyclotron_information.file_df
        file_df_source_on = cyclotron_information.file_df[cyclotron_information.file_df.Arc_I != "0"]
        foil_number = (file_df_source_on.Foil_No.iloc[-1])
        target_number_list = (int(cyclotron_information.target_number))
        total_list = [cyclotron_information.date_stamp,float(cyclotron_information.file_number),foil_number,target_number_list]
        if np.average(file_df_source_on.Target_I.astype(float)) > 0.0:
            # TRY TO USE THE OTHER METHOD
            for name in LIST_NAMES:  
                total_charge = np.sum(getattr(file_df_source_on,name).astype(float))*3/3600
                total_list.append(total_charge)
            df_individual = pd.DataFrame([total_list],columns=COLUMN_NAMES)  
            self.df_information = self.df_information.append(df_individual).reset_index(drop=True)  
        #else:
        #    print ("HERRREEEEEE")
        #    print (file_df_source_on)
        #print (adsasfda)
           
    def selecting_foil(self):       
        total_foil_list = [np.min(self.df_information_foil_individual.DATE),len(self.df_information_foil_individual.FILE),np.min(self.df_information_foil_individual.FOIL),np.min(self.df_information_foil_individual.TARGET)]
        for name in FOIL_LIST_NAME:
            total_foil_list.append(getattr(self.df_information_foil_individual,name).astype(float).sum())
        df_individual = pd.DataFrame([total_foil_list],columns=COLUMN_NAMES)
        self.df_information_foil = self.df_information_foil.append(df_individual).reset_index(drop=True)  
        #self.df_information_foil = self.df_information_foil.drop_duplicates(subset=['CURRENT_SOURCE'])

    def get_summation_per_period(self):
        self.df_information = self.df_information.sort_values(by="FILE").reset_index(drop=True) 
        foil_list = [1.0,2.0,3.0,4.0,5.0,6.0]
        for foil in foil_list:
            self.df_information_foil_individual = self.df_information[self.df_information.FOIL.astype(float) == foil].drop_duplicates(subset=['FILE'])
            #self.df_information_foil_individual = self.df_information_foil_individual.drop_duplicates(subset=['FILE'])
            #print (self.df_information_foil_individual)
            if len(self.df_information_foil_individual) > 0:
               #print ("ADDING")
               self.selecting_foil()
               #print (self.df_information_foil)









