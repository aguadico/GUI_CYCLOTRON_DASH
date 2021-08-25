import columns_names
import pandas as pd
import numpy as np
import saving_trends_alt
import ion_source_studies
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import additional_functions
import columns_names

COLUMNS_SOURCE = ["CURRENT_AVE"]
COLUMNS_VACUUM = ["PRESSURE_AVE"]
COLORS = ["#223A38","#2E8F88"],["#029386","#069AF3"],["#054907","#15B01A"]

COLORS_TRENDS = ["#A0BBBC","#223A38","#0058AB"]
COLORS_TRENDS_OUT = ['#497873','#497873']
#COLORS_TRENDS = ["#0058AB","#75bbfd"]
COLORS_RF = [["#A0BBBC","#223A38"],["#A0BBBC","#223A38"]]
COLORS_RF_OUT = [['#497873','#497873'],['#497873','#497873']]
#COLORS_RF = [[["#223A38","#497873","#054907",],["#223A38","#497873","#054907"],["#223A38","#497873","#054907"],["#223A38","#497873","#054907"],["#223A38","#497873","#054907"]],
#[["#223A38","#497873","#054907",],["#223A38","#497873","#054907"],["#223A38","#497873","#054907"],["#223A38","#497873","#054907"],["#223A38","#497873","#054907"]]]

COLUMNS_MAGNET = ["FILE","DATE","TARGET","FOIL","CURRENT_MAX","CURRENT_MIN","CURRENT_AVE","CURRENT_STD","START_ISO","END_ISO","START_IRRADIATION"]
# es otro tipo de gráfico or maybe not
COLUMNS_BEAM = ["COLL_CURRENT_L_AVE","COLL_CURRENT_R_AVE","TARGET_CURRENT_AVE","FOIL_CURRENT_AVE","EXTRACTION_LOSSES_AVE"]
COLUMNS_EXTRACTION = ["CAROUSEL_POSITION_AVE","BALANCE_POSITION_AVE"]
COLUMNS_TRANSMISSION = ["TRANSMISSION_AVE"]
COLUMNS_RF =  ["DEE1_VOLTAGE_AVE","DEE2_VOLTAGE_AVE","FORWARD_POWER_AVE","REFLECTED_POWER_AVE","PHASE_LOAD_AVE","PHASE_LOAD_STD",
"FLAP1_AVE","FLAP2_AVE"]
COLUMNS_TOTAL = [COLUMNS_SOURCE,COLUMNS_VACUUM,COLUMNS_MAGNET,COLUMNS_BEAM,COLUMNS_EXTRACTION,COLUMNS_TRANSMISSION,COLUMNS_RF]

COLUMNS_SOURCE_INDICATOR = ["CURRENT_AVE"]
COLUMNS_VACUUM_INDICATOR = ["HFLOW"]
COLUMNS_MAGNET_INDICATOR = ["START_IRRADIATION","START_IRRADIATION_REL"]
# es otro tipo de gráfico or maybe not
COLUMNS_EXTRACTION_INDICATOR = ["CAROUSEL_POSITION_AVE","BALANCE_POSITION_AVE"]
COLUMNS_RF_INDICATOR =  ["SPARKS","DISTANCE_FLAP_1","DISTANCE_FLAP_2"]
COLUMNS_TOTAL_INDICATOR = [COLUMNS_SOURCE_INDICATOR,COLUMNS_VACUUM_INDICATOR,COLUMNS_MAGNET_INDICATOR,COLUMNS_EXTRACTION_INDICATOR,COLUMNS_RF_INDICATOR]
COLUMNS_NAMES = ["CUMULATIVE_TARGET_1","CUMULATIVE_TARGET_2","CUMULATIVE_CURRENT_COLL_L_1","CUMULATIVE_CURRENT_COLL_L_2","CUMULATIVE_CURRENT_COLL_R_1",
        "CUMULATIVE_CURRENT_COLL_R_2","CUMULATIVE_SOURCE"]
COLUMNS_FOIL_CHARGE_1 = ["CUMULATIVE_TARGET_1_FOIL_1","CUMULATIVE_TARGET_1_FOIL_2","CUMULATIVE_TARGET_1_FOIL_3","CUMULATIVE_TARGET_1_FOIL_4","CUMULATIVE_TARGET_1_FOIL_5","CUMULATIVE_TARGET_1_FOIL_6"]
COLUMNS_FOIL_CHARGE_2 = ["CUMULATIVE_TARGET_2_FOIL_1","CUMULATIVE_TARGET_2_FOIL_2","CUMULATIVE_TARGET_2_FOIL_3","CUMULATIVE_TARGET_2_FOIL_4","CUMULATIVE_TARGET_2_FOIL_5","CUMULATIVE_TARGET_2_FOIL_6"]
COLUMNS_TOTAL = COLUMNS_NAMES + COLUMNS_FOIL_CHARGE_1 + COLUMNS_FOIL_CHARGE_2



class cyclotron:
    def __init__(self):
        #self.output_path = "/Users/anagtv/Documents/OneDrive/046 - Medical Devices/Mantenimientos ciclotrones/TEST"
        self.target_number = 0
        self.date_stamp = "0"
        self.name = 0 
        self.file_number = 0
        self.irradiation_values = 0
        self.file_df = []
        self.source_performance_total = []
        self.source_performance_total_error = []
        self.source_performance = 0
        self.target_min = 0
        self.target_max = 0
        self.values_targets = [self.target_min,self.target_max]
        #INIT DATAFRAMES
        columns_names.initial_df(self)
        self.df_summary = pd.DataFrame([[0]*len(COLUMNS_TOTAL)],columns=[COLUMNS_TOTAL])
        self.ion_source_performance = pd.DataFrame(columns=["TARGET","SOURCE_PERFORMANCE","SOURCE_PERFORMANCE_ERROR"])
        self.physical_targets = ["1","2"]

    def file_output(self):
        #Computing or just displaying trends
        saving_trends_alt.getting_summary_per_file(self)
        ion_source_studies.returning_current(self,ion_source_studies.current)

    def get_average_std_summary(self):
        all_dataframes = [self.df_source,self.df_vacuum,self.df_magnet,self.df_beam,self.df_extraction,self.df_transmission,self.df_rf]
        df_summary = pd.DataFrame()
        for j in range(len(COLUMNS_TOTAL)):
            for column in COLUMNS_TOTAL[j]:        
                df_summary[column] = all_dataframes[j].describe(include = include)[column]['mean']
                df_summary[column[:-3]+"STD"] = all_dataframes[j].describe(include = include)[column]['std']
        return df_summary

    def get_average_std_summary_cummulative(self,df_target_1,df_target_2):
        include =['object', 'float', 'int']
        #all_dataframes = [self.df_source,self.df_vacuum,self.df_magnet,self.df_extraction,self.df_rf]
        source_performance = np.array(self.source_performance_total)
        self.source_performance = source_performance[source_performance > 0]
        self.df_summary["CUMULATIVE_TARGET_1"] = df_target_1.CURRENT_TARGET.astype(float).sum()/1000
        self.df_summary["CUMULATIVE_TARGET_2"] = df_target_2.CURRENT_TARGET.astype(float).sum()/1000
        self.df_summary["CUMULATIVE_CURRENT_COLL_L_1"] = df_target_1.CURRENT_COLL_L.sum()
        self.df_summary["CUMULATIVE_CURRENT_COLL_L_2"] = df_target_2.CURRENT_COLL_L.sum()
        self.df_summary["CUMULATIVE_CURRENT_COLL_R_1"] = df_target_1.CURRENT_COLL_R.sum()
        self.df_summary["CUMULATIVE_CURRENT_COLL_R_2"] = df_target_2.CURRENT_COLL_R.sum()
        self.df_summary["CUMULATIVE_SOURCE"] = (df_target_1.CURRENT_SOURCE.sum() + df_target_2.CURRENT_SOURCE.sum())/1000 
        for i in range(len(COLUMNS_FOIL_CHARGE_1)):
            self.df_summary[COLUMNS_FOIL_CHARGE_1[i]] = df_target_1.CURRENT_FOIL[df_target_1.FOIL == str(i+1)].sum()       
        for i in range(len(COLUMNS_FOIL_CHARGE_2)):
            self.df_summary[COLUMNS_FOIL_CHARGE_2[i]] = df_target_2.CURRENT_FOIL[df_target_2.FOIL == str(i+1)].sum() 


    def plotting_statistics(self,ticker,ticker_horizontal,ticker_layer):  
        if ((ticker == "CHOOSE") or (len(self.df_extraction.PHYSICAL_TARGET) == 0)):
            fig = make_subplots(rows=3, cols=1,shared_xaxes=True,
                        vertical_spacing=0.02)
            fig.update_layout(height=1500)
            x_values = [0]
            y_values = [np.array(0),np.array(0),np.array(0)]
            y_values_error = [np.array(0),np.array(0),np.array(0)]
            names = ["","",""]
            units = ["","",""]
            reference_value = [[[0,0,""]],[[0,0,""]],[[0,0,""]]]
            for i in range(3): 
                fig = additional_functions.plotting_simple_name(fig,x_values,y_values[i],y_values_error[i],units[i],i+1,1,COLORS[0],COLORS[1],"",reference_value[i],ticker_layer)
        else:
            k = - 1
            df_summary_source = self.df_source
            self.target_min = np.min(self.df_extraction.TARGET.astype(float))
            self.target_max = np.max(self.df_extraction.TARGET.astype(float))
            self.values_targets = [self.target_min,self.target_max]
            fig = make_subplots(rows=5, cols=1,shared_xaxes=False,
                        vertical_spacing=0.05)
            if ticker == "MAGNET":
                fig = make_subplots(rows=3, cols=1,shared_xaxes=True,
                        vertical_spacing=0.02)
            elif ticker == "TARGET":
                fig = make_subplots(rows=4, cols=1,shared_xaxes=True,
                        vertical_spacing=0.02)
            for target in self.values_targets:
                self.df_summary_source = self.df_source[self.df_source.TARGET.astype(float) == float(target)]
                x_values = getattr(self.df_summary_source,ticker_horizontal)
                self.df_summary_vacuum = self.df_vacuum[self.df_vacuum.TARGET.astype(float) == float(target)]
                self.df_summary_beam = self.df_beam[self.df_beam.TARGET.astype(float) == float(target)]
                #(df_summary_beam["COLL_CURRENT_L_AVE"].astype(float)+df_summary_beam["COLL_CURRENT_R_AVE"].astype(float))/(df_summary_beam['FOIL_CURRENT_AVE'].astype(float))*100
                self.df_summary_rf = self.df_rf[self.df_rf.TARGET.astype(float) == float(target)]
                self.df_summary_magnet = self.df_magnet[self.df_magnet.TARGET.astype(float) == float(target)]
                self.df_summary_transmission = self.df_transmission[self.df_transmission.TARGET.astype(float) == float(target)]
                self.df_extraction_target = self.df_extraction[self.df_extraction.TARGET.astype(float) == float(target)]
                self.df_source_performance = self.ion_source_performance[self.ion_source_performance.TARGET.astype(float) == float(target)]
                print ("EXTRACTION")
                print (self.df_extraction)
                physical_target = self.df_extraction.PHYSICAL_TARGET.iloc[0]
                print ("SOURCE PERFORMANCE")
                print (self.source_performance_total)
                print (df_summary_source["CURRENT_AVE"])
                self.volume_information = self.df_filling_volume[self.df_volume.TARGET.astype(float) == float(target)]
                self.df_summary_source["HFLOW_STD"] = [0]*len(self.df_summary_source["HFLOW"])
                print ("HERREEEE!!")
                print (self.df_summary_source)
                print (self.df_summary_vacuum)
                print (self.df_source_performance)
                k += 1  
                for i in range(len(columns_names.COLUMNS_TO_PLOT[ticker])): 
                    for j in range(len(columns_names.COLUMNS_TO_PLOT[ticker][i])):
                        print ("DATAFRAME")
                        print (columns_names.DATAFRAME_TO_PLOT[ticker][i][j])
                        dataframe_to_plot = getattr(self,columns_names.DATAFRAME_TO_PLOT[ticker][i][j])
                        y_values = getattr(dataframe_to_plot,columns_names.COLUMNS_TO_PLOT[ticker][i][j])
                        print ("Y VALUES")
                        print (y_values)
                        y_values_error = getattr(dataframe_to_plot,columns_names.COLUMNS_TO_PLOT_ERROR[ticker][i][j])
                        print (y_values_error)
                        units = columns_names.Y_LABEL[ticker][i][j]
                        legend = columns_names.LEGEND[ticker][i][j]
                        reference_value = columns_names.REFERENCE_VALUE_DICTIONARY[ticker][i]
                        if ((ticker == "RF") or (ticker == "RF_STABILITY")):
                            fig = additional_functions.plotting_simple_name(fig,x_values,y_values,y_values_error,units,i+1,1,COLORS_RF[k][j],COLORS_RF_OUT[k][j],legend + " T " + str(physical_target),reference_value,ticker_layer)
                        else:
                            fig = additional_functions.plotting_simple_name(fig,x_values,y_values,y_values_error,units,i+1,1,COLORS_TRENDS[k],COLORS_TRENDS_OUT[k],legend + " T " + str(physical_target),reference_value,ticker_layer)
            print ("X VALUES")
            print (x_values)
        #fig.update_layout(title="Statistical values")
        fig.update_layout(showlegend=False)
        fig.update_layout(height=1500)
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='#FFFFFF',font=dict(size=16,color="black"),font_family="Arial",margin=dict(t=5)) 
        fig.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
        fig.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
        #fig.update_layout(title="Statistical evolution") 
        if ticker_horizontal == "DATE":
            fig.update_xaxes(title_text="Date", row=len(columns_names.COLUMNS_TO_PLOT[ticker]), col=1)
        elif ticker_horizontal == "FILE":
            fig.update_xaxes(title_text="File", row=len(columns_names.COLUMNS_TO_PLOT[ticker]), col=1)
        return fig


