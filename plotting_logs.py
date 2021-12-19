import json
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from jupyter_dash import JupyterDash
from dash.dependencies import Input, Output,State
import plotly.express as px
import pandas as pd
import tfs
import base64
import datetime
import dash_table
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import os
import sys
sys.path.append("/Users/anagtv/GUI_CYCLOTRON_BOTH_TARGETS")
import saving_trends_alt
import columns_names
import dash_table as dt
import io
from datetime import date
import managing_files_alt
#import computing_charge_df_alt
#import ion_source_studies
import additional_functions
import cyclotron_class
import app_layout
import getting_subsystems_data
import time

COLORS = ["#A0BBBC","#223A38","#497873"]
REFERENCE_VALUE_DICTIONARY = {"CHOOSE":[[[]],[[]]],
"SOURCE":[[[600,700,800]],[[120,130,140]],[[20,25,35]]],
"BEAM":[[[600,700,800]],[[110,120,130]],[[20,25,35]],[[85,75,70]],[[0.5,10,100]]],
"VACUUM":[[[600,700,800]],[[1.6,1.7,1.8]],[]],
"RF":[[[]],[[10,5,0]],[[13,14,15],[0.5,1.5,3]]],
"TARGET":[[[110,120,130]],[[450,460,480]],[]],
"MAGNET":[[[]],[[]]]}


ROW_NUMBER = {"CHOOSE":4,"SOURCE":4,"BEAM":5,"VACUUM":5,"RF":3,"TARGET":3,"MAGNET":1}

COLUMNS_TO_PLOT = {"CHOOSE":[["PLOT_1"],["PLOT_2"],["PLOT_3"]],
"SOURCE":[["Arc_I"],["Target_I"],["Collimators"],["Vacuum_mbar"]],
"BEAM":[["Arc_I"],["Target_I"],["Collimators"],["Relative_target"],["Losses"]],
"VACUUM":[["Arc_I"],["Vacuum_mbar"],["Gas_flow"]],
"RF":[["Dee_1_kV","Dee_2_kV"],["Flap1_pos","Flap2_pos"],["RF_fwd_W","RF_refl_W"]],
"TARGET":[["Target_I"],["Target_P"],["Extr_pos"]],
"MAGNET":[["Magnet_I"],["Foil_I","Target_I","Coll_l_I"]]}

HORIZONTAL_VALUES = {"CHOOSE":[["PLOT_1"],["PLOT_2"],["PLOT_3"]],
"SOURCE":[["Time"]]*4,
"BEAM":[["Time"]]*5,"VACUUM":[["Time"]]*3,"RF":[["Time"]*3]*3,"TARGET":[["Time"]]*3,"MAGNET":[["Time"],["Magnet_I","Magnet_I","Magnet_I"]]}

DATAFRAME_TO_PLOT = {"CHOOSE":[["df_zero_individual"]]*3,
"SOURCE":[["file_df"]]*4,
"BEAM":[["file_df"]]*5,"VACUUM":[["file_df"]]*3,"RF":[["file_df"]*3]*3,"TARGET":[["file_df"]]*3,"MAGNET":[["file_df"],["df_isochronism","df_isochronism","df_isochronism"]]}

Y_LABEL = {"CHOOSE":[[" "]]*3,
"SOURCE":[["Arc I [mA]"],["Target I [\u03bcA]"],["I Collimators [\u03bcA]"],["Vacuum Pressure [1e-5 mbar]"]],
"BEAM":[["Arc I [mA]"],["Target I [\u03bcA]"],["Collimators [\u03bcA]"],["I target/I foil [%]"],["Extraction losses [%]"]],
"VACUUM":[["Arc I [mA]"],["Vacuum Pressure [1e-5 mbar]"],["Gas flow [sccm]"]],
"RF":[["RF Voltage [kV]","RF Voltage [kV]"],["Flap [%]","Flap [%]"],["RF Power [kW]","RF Power [kW]"]],
"TARGET":[["Target I [\u03bcA]"],["Pressure [psi]"],["Extraction position [%]"]],
"MAGNET":[["Magnet I [A]"],["I [\u03bcA]","I [\u03bcA]","I [\u03bcA]"]]}

LEGEND = {"CHOOSE":[[" "]]*3,
"SOURCE":[["Source current"],["Target current"],["Collimators current"],["Vacuum"]],
"BEAM":[["Source"],["Target"],["Collimators"],["Relative Target"],["Extraction losses"]],
"VACUUM":[["Source current"],["Vacuum"],["Gas flow"]],
"RF":[["Dee 1","Dee 2"],["Flap 1","Flap 2"],["Fwd","Rfl"]],
"TARGET":[["Target current"],["Target pressure"],["Extraction"]],
"MAGNET":[["Magnet current"],["Foil current","Target current","Collimators current"]]}

def fig_setting_layout(fig):
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='#FFFFFF',font=dict(size=16,color="black"),font_family="Arial",margin=dict(t=35))  
    return fig

def fig_setting(row_number,cyclotron_information,ticker):
    fig_logfile = go.FigureWidget(make_subplots(rows=len(COLUMNS_TO_PLOT[ticker]), cols=1,shared_xaxes=False,
                vertical_spacing=0.1))
    fig_logfile.update_xaxes(title_text="Time [HH:MM:SS]", row=row_number, col=1)  
    fig_logfile.update_layout(title="Log number " + str(cyclotron_information.file_number) + " Date " + str(cyclotron_information.date_stamp),
    font=dict(size=16,color="#223A38"),font_family="Arial",margin=dict(t=60)) 
    fig_logfile.update_layout(height=1500,showlegend=False)
    fig_logfile.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
    fig_logfile.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
    fig_logfile = fig_setting_layout(fig_logfile)
    return fig_logfile

def adding_reference(fig_logfile,ticker):
    reference_value = REFERENCE_VALUE_DICTIONARY[ticker] 
    colors = ["orange","red"]
    text = ["Medium risk area","High risk area"]
    for i in range(len(reference_value)):
        for j in range(len(reference_value[i])):
            if len(reference_value[i][j]) > 0:
                for k in range(2):
                    fig_logfile.add_hrect(y0=reference_value[i][j][k], y1=reference_value[i][j][k+1], line_width=0, fillcolor=colors[k], opacity=0.05,row=i+1, col=1)
                    fig_logfile.add_hline(y=reference_value[i][j][k], line_dash="dot",line_color=colors[k],annotation_text=text[k],
                         annotation_position="bottom right",row=i+1, col=1)
    return fig_logfile


#def get_values_and_settings(horizontal_values,position,y_label,legend,j):#
#   
#    
#    return (values,settings)

def plotting_functions(cyclotron_information,parameters,fig_logfile,position,j):
    for column,df,horizontal_value,y_label,legend in parameters:
        dataframe_to_plot = getattr(cyclotron_information,df)
        y_values = getattr(dataframe_to_plot,column).astype(float)
        x_values = getattr(dataframe_to_plot,horizontal_value)
        values = [x_values,y_values,y_label]
        settings = [position,1,COLORS[j],legend,10]
        #values,settings = get_values_and_settings(dataframe_to_plot,column,horizontal_value,position,y_label,legend,j)
        j = j+1
        if df == "df_isochronism":
            fig_logfile = plotting_isochronism(cyclotron_information,dataframe_to_plot,fig_logfile)      
        fig_logfile = additional_functions.plotting_simple_no_error(fig_logfile,values,settings)
    return fig_logfile

def initializing_df(cyclotron_information):
    cyclotron_information.df_zero_individual["PLOT_1"] = 0
    cyclotron_information.df_zero_individual["PLOT_2"] = 0
    cyclotron_information.df_zero_individual["PLOT_3"] = 0    
    cyclotron_information.df_zero_individual["PLOT_1"] = 0
    cyclotron_information.df_zero_individual["PLOT_2"] = 0
    cyclotron_information.df_zero_individual["PLOT_3"] = 0  

def plotting_isochronism(cyclotron_information,dataframe_to_plot,fig_logfile):
    dataframe_to_plot = dataframe_to_plot.iloc[:-1]
    fig_logfile.add_vline(x=cyclotron_information.df_isochronism.Magnet_I.iloc[-1],line_width=4, line_dash="dot",line_color="green",annotation_text="Isochronism"
            ,row=2, col=1)
    fig_logfile.update_xaxes(title_text="Time [HH:MM:SS]", row=1, col=1)
    fig_logfile.update_xaxes(title_text="Current [A]", row=2, col=1)
    return fig_logfile

def daily_report(tickers,tabs,input_file,cyclotron_information):     
    row_number = ROW_NUMBER[tickers[0]]
    cyclotron_information.df_zero_individual = pd.DataFrame(columns=["Time","PLOT_1","PLOT_2","PLOT_3"])
    initializing_df(cyclotron_information)
    fig_logfile = fig_setting(row_number,cyclotron_information,tickers[0])
    positions = list(np.array(list(range(len(COLUMNS_TO_PLOT[tickers[0]]))))+1)
    for set_of_columns,dataframes,horizontal_values,y_labels,legends,position in zip(COLUMNS_TO_PLOT[tickers[0]],DATAFRAME_TO_PLOT[tickers[0]],HORIZONTAL_VALUES[tickers[0]],Y_LABEL[tickers[0]],LEGEND[tickers[0]],positions):
      j = 0
      parameters = zip(set_of_columns,dataframes,horizontal_values,y_labels,legends)
      fig_logfile = plotting_functions(cyclotron_information,parameters,fig_logfile,position,j)
    if tickers[1] == ["ADRF"]:
        fig_logfile = adding_reference(fig_logfile,tickers[0])
    return (fig_logfile)
   