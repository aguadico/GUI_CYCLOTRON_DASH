import columns_names
import pandas as pd
import numpy as np
import saving_trends_alt
import ion_source_studies
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import additional_functions
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
            #fig.update_xaxes(zeroline=True, zerolinewidth=1, zerolinecolor='#223A38')
            #fig.update_yaxes(zeroline=True, zerolinewidth=1, zerolinecolor='#223A38') 
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
                df_summary_source = self.df_source[self.df_source.TARGET.astype(float) == float(target)]
                df_summary_vacuum = self.df_vacuum[self.df_vacuum.TARGET.astype(float) == float(target)]
                df_summary_beam = self.df_beam[self.df_beam.TARGET.astype(float) == float(target)]
                df_summary_rf = self.df_rf[self.df_rf.TARGET.astype(float) == float(target)]
                df_summary_magnet = self.df_magnet[self.df_magnet.TARGET.astype(float) == float(target)]
                df_summary_transmission = self.df_transmission[self.df_transmission.TARGET.astype(float) == float(target)]
                df_extraction = self.df_extraction[self.df_extraction.TARGET.astype(float) == float(target)]
                physical_target = df_extraction.PHYSICAL_TARGET.iloc[0]
                k += 1  
                volume_information = self.df_filling_volume[self.df_volume.TARGET.astype(float) == float(target)]
                x_values = getattr(df_summary_source,ticker_horizontal)
                if ticker == "SOURCE": 
                    y_values = [[df_summary_source['CURRENT_AVE']],[df_summary_vacuum["PRESSURE_AVE"]],[df_summary_source.HFLOW],
                    [self.source_performance_total],[df_summary_source["CURRENT_STD"].astype(float)/df_summary_source["CURRENT_AVE"].astype(float)*100]]
                    y_values_error = [[df_summary_source['CURRENT_STD']],[df_summary_vacuum["PRESSURE_STD"]],[len(df_summary_source["HFLOW"])*[0]],
                    [self.source_performance_total_error],[df_summary_vacuum["PRESSURE_STD"]],[[0]*len(df_summary_source["CURRENT_STD"])]]
                    units = [[r"I source [mA]"],["Vacuum Pressure [1e-5 mbar]"],["H flow [sccm]"],["Source performance [mA/uA]"],["I source stability [%]"]]
                    reference_value = [[[500,700,850,"Upper limit"]],[[1.8,1.9,2,"Upper limit"]],[[5.5,6,6.5,"Upper limit"],[3.5,3,2.5,"Lower limit"]],[[3.5,4.5,6,"Upper limit"]],[[5,10,15,"Upper limit"]]]
                elif ticker == "BEAM":
                    y_values = [[df_summary_beam['FOIL_CURRENT_AVE']],[df_summary_beam["TARGET_CURRENT_AVE"]],
                    [(df_summary_beam["COLL_CURRENT_L_AVE"].astype(float)+df_summary_beam["COLL_CURRENT_R_AVE"].astype(float))/(df_summary_beam['FOIL_CURRENT_AVE'].astype(float))*100],
                    [df_summary_beam["TARGET_CURRENT_STD"].astype(float)/df_summary_beam["TARGET_CURRENT_AVE"].astype(float)*100],
                    [df_summary_beam['EXTRACTION_LOSSES_AVE']]] 
                    y_values_error =  [[df_summary_beam['FOIL_CURRENT_STD']],[df_summary_beam["TARGET_CURRENT_STD"]],
                    [(df_summary_beam["COLL_CURRENT_L_STD"]**2+df_summary_beam["COLL_CURRENT_R_STD"]**2)**0.5],
                    [[0]*len(df_summary_beam["TARGET_CURRENT_AVE"])],[df_summary_beam['EXTRACTION_LOSSES_STD']]]
                    units = [[r"I foil [uA]"],["I target [\u03bcA]"],["I collimators[%]"],["I target stability [%]"],["Extraction losses [%]"]]
                    reference_value = [[[120,125,130,"Upper limit"]],[[102,105,110,"Upper limit"]],[[20,25,30,"Upper limit"],[7,5,2,"Lower limit"]],[[1.5,2,5,"Upper limit"]],[[1,1.5,3,"Upper limit"],[-1,-1.5,-3,"Lower limit"]]]
                elif ticker == "VACUUM":
                    y_values = [[df_summary_vacuum['PRESSURE_AVE']],[df_summary_transmission["TRANSMISSION_AVE"]],
                    [df_summary_source["CURRENT_AVE"]],
                    [df_summary_vacuum["PRESSURE_STD"].astype(float)/df_summary_vacuum["PRESSURE_AVE"].astype(float)*100],
                    [df_summary_vacuum["PRESSURE_AVE"].astype(float)/df_summary_source.HFLOW.astype(float)]]
                    y_values_error =  [[df_summary_vacuum['PRESSURE_STD']],[df_summary_transmission["TRANSMISSION_STD"]],
                    [df_summary_source["CURRENT_STD"]],
                    [[0]*len(df_summary_vacuum["PRESSURE_STD"])],
                    [[0]*len(df_summary_vacuum["PRESSURE_STD"])]]
                    units = [[r"Vacuum Pressure [1e-5 mbar]"],["Transmission [%]"],["I source [mA]"],["Vacuum stability[%]"],["Vacuum/Gas [1e-5mbar/sccm]"]]
                    reference_value = [[[1.8,1.9,2,"Upper limit"]],[[60,50,40,"Lower limit"]],[[500,700,800,"Upper limit"]],[[2,5,7.5,"Upper limit"]],[[0.35,0.4,0.5,"Upper limit"]]]
                elif ticker == "MAGNET":
                    y_values = [[df_summary_magnet['CURRENT_AVE']],[df_summary_magnet["START_IRRADIATION_REL"]],
                    [df_summary_magnet["DELTA_TIME"]]]
                    y_values_error = [[df_summary_magnet['CURRENT_STD']],[[0]*len(df_summary_magnet["START_IRRADIATION_REL"])],
                    [[0]*len(df_summary_magnet["DELTA_TIME"])]]
                    units = [[r"Current [A]"],["Relative current to center [%]"],["Delta time [min]"]]
                    fig.update_yaxes(range=[15, 25], row=3, col=1)
                    reference_value = [[[np.average(self.df_magnet.CURRENT_AVE)+2.5,np.average(self.df_magnet.CURRENT_AVE)+5,np.average(self.df_magnet.CURRENT_AVE)+10,"Upper limit"],[np.average(self.df_magnet.CURRENT_AVE)-2.5,np.average(self.df_magnet.CURRENT_AVE)-5,np.average(self.df_magnet.CURRENT_AVE)-10,"Lower limmit"]],[[47.5,45,40,"Lower limit"],[52.5,55,60,"Upper limit"]],[[],[]]]
                elif ticker == "RF":
                    y_values = [[df_summary_rf['DEE1_VOLTAGE_AVE'],df_summary_rf['DEE2_VOLTAGE_AVE']],[df_summary_rf["FORWARD_POWER_AVE"]],
                    [df_summary_rf["REFLECTED_POWER_AVE"]*100],
                    [df_summary_rf["FLAP1_AVE"],df_summary_rf["FLAP2_AVE"]],
                    [df_summary_rf['PHASE_LOAD_AVE']]] 
                    y_values_error =  [[df_summary_rf['DEE1_VOLTAGE_STD'],df_summary_rf['DEE2_VOLTAGE_STD']],[df_summary_rf["FORWARD_POWER_STD"]],
                    [df_summary_rf["REFLECTED_POWER_STD"]*100],
                    [df_summary_rf["FLAP1_STD"],df_summary_rf["FLAP2_STD"]],[df_summary_rf['PHASE_LOAD_STD']]]
                    units = [[r"Dee 1","Dee 2"],["Dee 1"],["Dee 2"],["Flap 1","Flap 2"]
                    ,["RF Phase"]]
                    units_ax = [[r"Voltage Dee [kV]","Voltage Dee [kV]"],["Forward power[kW]"],["Reflected power [W]"],["Flap [%]","Flap  [%]"]
                    ,["RF Phase load [o]"]]
                    reference_value = [[[]],[[13.5,14.5,15,"Upper limit"]],[[400,500,600,"Upper limit"]],[[10,8,6,"Lower limit"]],[[5.5,6,6.5,"Upper limit"],[4.5,4,3.5,"Lower limit"]]]
                elif ticker == "RF_STABILITY":
                    y_values = [[df_summary_rf["SPARKS"]],[df_summary_rf['DEE1_VOLTAGE_STD']/df_summary_rf['DEE1_VOLTAGE_AVE']*100,df_summary_rf['DEE2_VOLTAGE_STD']/df_summary_rf['DEE1_VOLTAGE_AVE']*100],
                    [df_summary_rf["DISTANCE_FLAP_1"],df_summary_rf["DISTANCE_FLAP_2"]],
                    [df_summary_rf["MAX_INSTANT_SPEED_1"],df_summary_rf["MAX_INSTANT_SPEED_2"]],[df_summary_rf["AVERAGE_INSTANT_SPEED_1"],
                    df_summary_rf["AVERAGE_INSTANT_SPEED_2"]]]
                    y_values_error = [[[0]*len(df_summary_rf["SPARKS"])],[[0]*len(df_summary_rf['DEE1_VOLTAGE_STD']),[0]*len(df_summary_rf['DEE2_VOLTAGE_STD'])],
                    [[0]*len(df_summary_rf["DISTANCE_FLAP_1"]),[0]*len(df_summary_rf["DISTANCE_FLAP_2"])],
                    [[0]*len(df_summary_rf["DISTANCE_FLAP_1"]),[0]*len(df_summary_rf["DISTANCE_FLAP_2"])],
                    [[0]*len(df_summary_rf["DISTANCE_FLAP_1"]),[0]*len(df_summary_rf["DISTANCE_FLAP_2"])]]
                    units = [["Number of sparks"],["Dee 1","Dee 2"],["Flap 1","Flap 2"]
                    ,["Flap 1","Flap 2"],["Flap 1","Flap 2"]]
                    units_ax = [["Number of sparks"],["Voltage stability [%]","Voltage stability [%]"],["Distance flap [%]","Distance flap [%]"]
                    ,["Max speed flap [%/s]","Max speed flap [%/s]"],["Ave speed irradiation [%/h]","Ave flap speed [%/h]"]]
                    reference_value = [[[]],[[2,2.5,3,"Upper limit"]],[[1,-0.5,-2.5,"Lower limit"]],[[7.5,10,12.5,"Upper limit"]],[[7,10,15,"Upper limit"]]]
                elif ticker == "TARGET":
                    y_values = [[volume_information["RELATIVE_VOLUME"]],[volume_information["LOW_PRESSURE_AVE"]],
                    [volume_information["HIGH_PRESSURE_AVE"]],[volume_information["PRESSURE_IRRADIATION_AVE"]]]
                    y_values_error = [[[0]*len(volume_information["RELATIVE_VOLUME"])],[volume_information["LOW_PRESSURE_STD"]],
                    [volume_information["HIGH_PRESSURE_STD"]],[volume_information["PRESSURE_IRRADIATION_STD"]]]
                    units = [["Delta pressure filling [psi]"],["Low pressure [psi]"],["High pressure [psi]"],["Pressure irradiation [psi]"]]
                    reference_value = [[[20,15,12,"Lower limit"]],[[70,72.5,75,"Upper limit"]],[[445,450,460,"Upper limit"]],[[445,450,460,"Upper limit"]]]
                    fig.update_yaxes(range=[14, 30], row=1, col=1)
                for i in range(len(y_values)): 
                    for j in range(len(y_values[i])):
                        if ((ticker == "RF") or (ticker == "RF_STABILITY")):
                            fig = additional_functions.plotting_simple_name(fig,x_values,y_values[i][j],y_values_error[i][j],units_ax[i][j],i+1,1,COLORS_RF[k][j],COLORS_RF_OUT[k][j],units[i][j] + " T " + str(physical_target),reference_value[i],ticker_layer)
                        else:
                            fig = additional_functions.plotting_simple_name(fig,x_values,y_values[i][j],y_values_error[i][j],units[i][j],i+1,1,COLORS_TRENDS[k],COLORS_TRENDS_OUT[k]," T " + str(physical_target),reference_value[i],ticker_layer)
            fig.add_layout_image(dict(
                        source="https://raw.githubusercontent.com/michaelbabyn/plot_data/master/naphthalene.png",
                        x=0.4,
                        y=0.4,
                        ),
                    row=1,col=1)
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
            fig.update_xaxes(title_text="Date", row=len(y_values), col=1)
        elif ticker_horizontal == "FILE":
            fig.update_xaxes(title_text="File", row=len(y_values), col=1)
        return fig



