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
from scipy.optimize import curve_fit
import getting_subsystems_data_alt 
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
        self.physical_targets = ["1","2"]
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
        self.df_summary_source = pd.DataFrame(columns=[columns_names.COLUMNS_SOURCE])
        self.df_summary_vacuum = pd.DataFrame(columns=[columns_names.COLUMNS_VACUUM])
        self.df_summary_beam = pd.DataFrame(columns=[columns_names.COLUMNS_BEAM])
        self.df_summary_transmission = pd.DataFrame(columns=[columns_names.COLUMNS_TRANSMISSION])
        self.df_extraction_target = pd.DataFrame(columns=[columns_names.COLUMNS_EXTRACTION])
        self.df_source_performance = pd.DataFrame(columns=["FILE","TARGET","SOURCE_PERFORMANCE","SOURCE_PERFORMANCE_ERROR","TRANSMISSION"])
        self.volume_information  = pd.DataFrame(columns=[columns_names.COLUMNS_VOLUME])
        #INIT DATAFRAMES
        columns_names.initial_df(self)
        self.df_summary = pd.DataFrame([[0]*len(COLUMNS_TOTAL)],columns=[COLUMNS_TOTAL])
        self.ion_source_performance = pd.DataFrame(columns=["FILE","TARGET","SOURCE_PERFORMANCE","SOURCE_PERFORMANCE_ERROR","TRANSMISSION"])
        
    def current(self,X, a):
         x,y = X
         return a*(x+y) 
    def current_vaccum(X, a,b):
         x,y,z = X
         return a*(x+y) + b*z

    def returning_current(self,funct_fit):    
        data_df = self.file_df
        #VARIABLE TO FIT
        y_value_to_fit = data_df.Arc_I[data_df.Target_I.astype(float) > 0.7*np.max(data_df.Target_I.astype(float))].astype(float)
        #INDEPENDET VARIABLES (VACUUM, TARGET CURRENT AND COLLIMATORS )
        x_value_target = data_df.Target_I[data_df.Target_I.astype(float) > 0.7*np.max(data_df.Target_I.astype(float))].astype(float)
        x_value_vacuum = (data_df.Vacuum_P[data_df.Target_I.astype(float) > 0.7*np.max(data_df.Target_I.astype(float))].astype(float))
        x_value_collimators = data_df.Coll_l_I[data_df.Target_I.astype(float) > 0.7*np.max(data_df.Target_I.astype(float))].astype(float) + data_df.Coll_r_I[data_df.Target_I.astype(float) > 0.7*np.max(data_df.Target_I.astype(float))].astype(float)
        x_value_foil = data_df.Foil_I[data_df.Target_I.astype(float) > 0.7*np.max(data_df.Target_I.astype(float))].astype(float)
        df_summary = pd.DataFrame(list(zip(y_value_to_fit.astype(float),x_value_target.astype(float),x_value_collimators.astype(float),x_value_vacuum.astype(float),x_value_foil.astype(float))),columns=["I_SOURCE","I_TARGET","I_COLLIMATOR","VACUUM","I_FOIL"])
        # DATAFRAME WITH THE INDEPENDENT VARIABLES
        X = pd.DataFrame(np.c_[df_summary['I_TARGET'].astype(float), df_summary['I_COLLIMATOR'].astype(float),(df_summary['VACUUM'].astype(float)-np.min(df_summary['VACUUM'].astype(float)))*1e5], columns=['I_TARGET','I_COLLIMATOR','VACUUM'])
        # DATAFRAME WITH DEPENDENT VARIABLE, IMPORTANT (HERE THE VACUUM IS RELATIVE TO THE MINIMUN VALUE (WITH BEAM))
        Y = df_summary.I_SOURCE
        #CREATING A SUBSET FOR TRAINNING AND TESTING (FOR LATTER)
        # CURVE FIT
        print ("VALUES")
        print (X.I_TARGET)
        print ((np.array(X.I_TARGET),np.array(X.I_COLLIMATOR),np.array(X.VACUUM)))
        T_1 = 0
        if len(X.I_TARGET) > 20:
           print ("FUNC FIT")
           popt, pcov = curve_fit(funct_fit, (np.array(X.I_TARGET),np.array(X.I_COLLIMATOR)),Y)
           # COMPUTNG THE REAL VALUES FROM FIT
           # GET PROBE CURRENT AND ISOCHRONISM TO COMPUTE TRANSMISSION
           probe_current = getattr(data_df,"Probe_I").astype(float)[(data_df.Probe_I.astype(float) > 14) & (data_df.Probe_I.astype(float) < 16)]
           df_isochronism = getting_subsystems_data_alt.get_isochronism(data_df)
           T_1 = np.average(np.max(df_isochronism.Foil_I[:-1].astype(float))/probe_current)
           sigma_T_1 = np.std(np.max(df_isochronism.Foil_I)/probe_current)
           # transmission 2 (from foil to target) and its associated error
           T_2 = np.average((df_summary.I_TARGET + df_summary.I_COLLIMATOR)/df_summary.I_FOIL)
           sigma_T_2 = np.std((df_summary.I_TARGET + df_summary.I_COLLIMATOR)/df_summary.I_FOIL)
           # COMPUTE SOURCE PERFORMANCE AND ITS ASSOCIATED ERROR
           a = popt[0]
           x = a*T_1*T_2
           sigma_a = (np.diag(pcov)**0.5)[0]
           sigma_x = ((T_1*T_2*sigma_a)**2+(a*T_2*sigma_T_1)**2+(a*T_1*sigma_T_2))**0.5
           print ("x")
           print (x)
           print (sigma_x)
           print ("TRANSMISSION")
           print (T_1)
        else: 
            print ("TOO SHORT")
            a = 0
            sigma_a = 0
            x = 0
            sigma_x = 0
        print ("ION SOURCE PERFORMANCE")
        print (x)
        print (sigma_x)
        print ("TRANSMISSION")
        #print (T_1*T_2)
        self.ion_source_performance = self.ion_source_performance.append({"FILE":self.file_number,'TARGET':self.target_number,'SOURCE_PERFORMANCE':x,'SOURCE_PERFORMANCE_ERROR':sigma_x,"TRANSMISSION":T_1}, ignore_index=True)
        #cyclotron_data.ion_source_performance = cyclotron_data.ion_source_performance.append({'SOURCE_PERFORMANCE':x}, ignore_index=True)
        #cyclotron_data.ion_source_performance = cyclotron_data.ion_source_performance.append({'SOURCE_PERFORMANCE_ERROR':sigma_x}, ignore_index=True)
        #print (cyclotron_data.ion_source_performance)
        self.source_performance_total.append(x)
        self.source_performance_total_error.append(sigma_x)
        print ("ION SOURCE PERFORMANCE DF")
        print (self.ion_source_performance)


    def file_output(self):
        #Computing or just displaying trends
        saving_trends_alt.getting_summary_per_file(self)
        #ion_source_studies.returning_current(self,ion_source_studies.current)
        self.returning_current(self.current)

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
    
    def getting_sub_dataframe(self,data,target):
        filtered_data = data[data.TARGET.astype(float) == float(target)]
        return (filtered_data)

    def plotting_statistics(self,ticker,ticker_horizontal,ticker_layer):  
        k = - 1
        #df_summary_source = self.df_source
        self.target_min = np.min(self.df_extraction.TARGET.astype(float))
        self.target_max = np.max(self.df_extraction.TARGET.astype(float))
        self.values_targets = [self.target_min,self.target_max]
        #fig = make_subplots(rows=5, cols=1,shared_xaxes=False)
        #fig.update_layout(height=1500)
        print ("ENTERING HEREEEEEEE!")
        fig = go.FigureWidget(make_subplots(rows=len(columns_names.COLUMNS_TO_PLOT[ticker]), cols=1,shared_xaxes=False,
                vertical_spacing=0.05))
        #fig.update_layout(height=1500)
        print ("ENTERING HEREEEEEEEE!")
        if ticker == "MAGNET":
            fig = make_subplots(rows=3, cols=1,shared_xaxes=True,
                    vertical_spacing=0.02)
        elif ticker == "TARGET":
            fig = make_subplots(rows=4, cols=1,shared_xaxes=True,
                    vertical_spacing=0.02)
        for target in self.values_targets:
            self.df_summary_source = self.getting_sub_dataframe(self.df_source,target)
            self.df_summary_vacuum = self.getting_sub_dataframe(self.df_vacuum,target)
            self.df_summary_beam = self.getting_sub_dataframe(self.df_beam,target)
            self.df_summary_transmission = self.getting_sub_dataframe(self.df_transmission,target)
            self.df_extraction_target = self.getting_sub_dataframe(self.df_extraction,target)
            self.df_source_performance = self.getting_sub_dataframe(self.ion_source_performance,target)
            self.volume_information = self.getting_sub_dataframe(self.df_volume,target)
            self.df_summary_magnet = self.df_magnet[self.df_magnet.TARGET.astype(float) == float(target)]
            x_values = getattr(self.df_summary_source,ticker_horizontal) 
            self.df_summary_source["HFLOW_STD"] = [0]*len(self.df_summary_source["HFLOW"])
            k += 1  
            for i in range(len(columns_names.COLUMNS_TO_PLOT[ticker])): 
                for j in range(len(columns_names.COLUMNS_TO_PLOT[ticker][i])):
                    dataframe_to_plot = getattr(self,columns_names.DATAFRAME_TO_PLOT[ticker][i][j])
                    y_values = getattr(dataframe_to_plot,columns_names.COLUMNS_TO_PLOT[ticker][i][j])
                    y_values_error = getattr(dataframe_to_plot,columns_names.COLUMNS_TO_PLOT_ERROR[ticker][i][j])
                    units = columns_names.Y_LABEL[ticker][i][j]
                    legend = columns_names.LEGEND[ticker][i][j]
                    reference_value = columns_names.REFERENCE_VALUE_DICTIONARY[ticker][i]
                    values = [x_values,y_values,y_values_error,units]
                    if ((ticker == "RF") or (ticker == "RF_STABILITY")):
                        settings = [i+1,1,COLORS_RF[k][j],COLORS_RF_OUT[k][j],legend + " T " + str(target),reference_value,ticker_layer]
                        fig = additional_functions.plotting_simple_name(fig,values,settings)
                    else:
                        settings = [i+1,1,COLORS_TRENDS[k],COLORS_TRENDS_OUT[k],legend + " T " + str(target),reference_value,ticker_layer]
                        fig = additional_functions.plotting_simple_name(fig,values,settings)
        #fig.update_layout(title="Statistical values")
        fig.update_layout(showlegend=False)
        fig.update_layout(height=1500)
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='#FFFFFF',font=dict(size=16,color="black"),font_family="Arial",margin=dict(t=5)) 
        fig.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
        fig.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
        if ticker_horizontal == "DATE":
            fig.update_xaxes(title_text="Date", row=len(columns_names.COLUMNS_TO_PLOT[ticker]), col=1)
        elif ticker_horizontal == "FILE":
            fig.update_xaxes(title_text="File", row=len(columns_names.COLUMNS_TO_PLOT[ticker]), col=1)
        return fig



