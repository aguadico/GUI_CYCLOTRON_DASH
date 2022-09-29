
# for referral, see: https://plotly.com/python/

# required extensions: (copy command in terminal)
#   pip install dash      
#   pip install dash-extensions
#   pip install dash-bootstrap-components
#   pip install jupyter-dash
#   pip install pandas
#   pip install tfs-pandas
#   pip install matplotlib

# for external programs: (needed to run this one too)
#   pip install scipy
#   pip install ipywidgets

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
sys.path.append("/Users/anagtv/GUI_CYCLOTRON_BOTH_TARGETS")         # cambiable?
import saving_trends_alt
import columns_names
import dash_table as dt
import io
from datetime import date
import managing_files_alt
import computing_charge_class
#import ion_source_studies
import additional_functions
import cyclotron_class
import app_layout
import getting_subsystems_data
import time
import plotting_logs

columns = ["CHOOSE","SOURCE","MAGNET","BEAM","VACUUM","RF","RF_STABILITY","TARGET"]
columns_horizontal = ["DATE","FILE"]
#columns_directory = ["CURRENT DIRECTORY"]


cyclotron_information = cyclotron_class.cyclotron()
target_1 = computing_charge_class.target_cumulative_current(computing_charge_class.df_information)
target_2 = computing_charge_class.target_cumulative_current(computing_charge_class.df_information)


####### DOCUMENTATION
#
# Esta parte del código define las funciones que se llaman  al presionar los botones de la GUI. 
#
# daily report: plots de la evolución diaría de un logfile
# display_time_series
# display_foils_2_4_5_6
# plotting_bars
# update_output
# update_output
#
#
#



app = JupyterDash(external_stylesheets=[dbc.themes.SLATE])
app.title = "Cyclotron Analytics"
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app.layout = app_layout.layout

# aqui´ iban columns to plot y text to plot


@app.callback(
    Output("time_series_chart_volume", "figure"), 
    Input("ticker_2", "value"),
    Input("ticker_layer_file", "value"),
    Input('tabs-with-classes', 'value'),
    Input('upload_data_file', 'filename'),
    )
def daily_report(ticker,ticker_layer,tabs,input_file): 
    tickers = [ticker,ticker_layer]
    fig_logfile = plotting_logs.daily_report(tickers,tabs,input_file,cyclotron_information)
    return (fig_logfile)
   

@app.callback(
    Output("time_series_chart", "figure"), 
    Input("ticker", "value"),
    Input("ticker_horizontal", "value"),
    Input("ticker_layer", "value"),
    Input('upload_data', 'contents'),
    Input('tabs-with-classes', 'value')
    )
def display_time_series(ticker,ticker_horizontal,ticker_layer,list_of_contents,tabs):
    #fig = make_subplots(rows=3, cols=1,shared_xaxes=True,
    #                    vertical_spacing=0.02)
    fig = cyclotron_information.plotting_statistics(ticker,ticker_horizontal,ticker_layer)
    fig.update_layout(height=1500)
    return fig


COLUMNS_TO_PLOT = {"FOILS_1":["CUMULATIVE_TARGET_1_FOIL_1","CUMULATIVE_TARGET_1_FOIL_2","CUMULATIVE_TARGET_1_FOIL_3","CUMULATIVE_TARGET_1_FOIL_4","CUMULATIVE_TARGET_1_FOIL_5","CUMULATIVE_TARGET_1_FOIL_6"],
"FOILS_2":["CUMULATIVE_TARGET_2_FOIL_1","CUMULATIVE_TARGET_2_FOIL_2","CUMULATIVE_TARGET_2_FOIL_3","CUMULATIVE_TARGET_2_FOIL_4","CUMULATIVE_TARGET_2_FOIL_5","CUMULATIVE_TARGET_2_FOIL_6"],
"TARGET_COLLIMATORS_1":["CUMULATIVE_TARGET_1","CUMULATIVE_CURRENT_COLL_R_1","CUMULATIVE_CURRENT_COLL_L_1"],
"TARGET_COLLIMATORS_2":["CUMULATIVE_TARGET_2","CUMULATIVE_CURRENT_COLL_R_2","CUMULATIVE_CURRENT_COLL_L_2"],
"SOURCE_TARGETS":["CUMULATIVE_SOURCE","CUMULATIVE_TARGET_1","CUMULATIVE_TARGET_2"],
}

TEXT_TO_PLOT = {"FOILS_1":["Foil 1 [\u03bcAh]","Foil 2 [\u03bcAh]","Foil 3 [\u03bcAh]","Foil 4 [\u03bcAh]","Foil 5 [\u03bcAh]","Foil 6 [\u03bcAh]"],
"FOILS_2":["Foil 1 [\u03bcAh]","Foil 2 [\u03bcAh]","Foil 3 [\u03bcAh]","Foil 4 [\u03bcAh]","Foil 5 [\u03bcAh]","Foil 6 [\u03bcAh]"],
"TARGET_COLLIMATORS_1":["Target [mAh]","Collimator upper [\u03bcAh]","Collimator lower [\u03bcAh]"],
"TARGET_COLLIMATORS_2":["Target [mAh]","Collimator upper [\u03bcAh]","Collimator lower [\u03bcAh]"],
"SOURCE_TARGETS":["Source [Ah]","Target Position " + str(cyclotron_information.values_targets[0]) +  " [mAh]","Target Position "+ str(cyclotron_information.values_targets[1]) + " [mAh]"],
}


@app.callback(
    Output("time-series-chart4", "figure"),
    Output("target_collimators_1", "figure"),
    Output("target_collimators_2", "figure"),
    Output("foils_1_4_5_6", "figure"),
    Output("foils_2_4_5_6", "figure"), 
    Input('loading_output_1', 'children'), 
    Input('tabs-with-classes', 'value'), 
    )
def display_foils_2_4_5_6(loading,tabs): 
    dict_keys = ["SOURCE_TARGETS","TARGET_COLLIMATORS_1","TARGET_COLLIMATORS_2","FOILS_1","FOILS_2"]
    limits = ["SOURCE_TARGETS","TARGET_COLLIMATORS","TARGET_COLLIMATORS","FOILS","FOILS"]
    titles = ["","Target Position " + str(cyclotron_information.values_targets[0]),"Target Position " + str(cyclotron_information.values_targets[1]),
    "Target Position " + str(cyclotron_information.values_targets[0]),"Target Position " + str(cyclotron_information.values_targets[1])]
    fig_size = [500,500,500,800,800]
    figs = []
    for dict_value,limit,fig_size_i,title in zip(dict_keys,limits,fig_size,titles):
        figs.append(plotting_bars(dict_value,limit,fig_size_i,title))
    df_status_cyclotron = computing_reference_values("REFLECTED_POWER_W_AVE")
    print ("STATUS CYCLOTRON")
    print (df_status_cyclotron)
    return figs[0],figs[1],figs[2],figs[3],figs[4]


@app.callback(Output('table_status','style_data_conditional'),
    Input('upload_data_file', 'filename'))
def update_styles(loading):
    return [
            {
                'if': {
                    'filter_query': '{Overall} eq "Danger"'
                },
                'color': 'red'
            },
            {
                'if': {
                    'filter_query': '{Overall} eq "OK"'
                },
                'color': 'green'
            },
            {
                'if': {
                    'filter_query': '{Overall} eq  "Warning"'
                },
                'color': 'orange'
            },
            {
                'if': {
                    'filter_query': '{Overall} eq  "--"'
                },
                'backgroundColor': 'white'
            }
        ]

#@app.callback(
#    Output("table_status", "data"),
#    Input('upload_data', 'filename')
#)
#def updateTable(n_clicks):
#    df = computing_reference_values("REFLECTED_POWER_W_AVE")
#    print ("HEREEEE!!!!")
#    print (df)
#    data_1 = df.to_dict("rows")
#    return data_1
#    


def setting_status(name,limits):
    if abs(float(name)) < limits[0]:
        status = "OK"
    elif abs(float(name)) > limits[1]:
        status = "Danger"
    else:
        status = "Warning"
    return status

def setting_status_inverse(name,limits):
    if abs(float(name)) < limits[0]:
        status = "Danger"
    elif abs(float(name)) > limits[1]:
        status = "OK"
    else:
        status = "Warning"
    return status

#       COMPROBATIONS OF VALUES "COMPONENT LIFETIME" FOR WARNINGS & DANGERS

def getting_statistics_values(name,df,limits,flag):
    average_value = str(round(np.average(getattr(df,name).astype(float)),1))
    std_value = str(round(np.std(getattr(df,name).astype(float)),1))
    max_value = str(round(np.max(getattr(df,name).astype(float)),1))
    min_value = str(round(np.min(getattr(df,name).astype(float)),1))
    if flag == 0:
        verification = setting_status(average_value,limits)
    elif flag == 1:
        verification = setting_status_inverse(average_value,limits)
    elif flag == 2:
        verification = "--"
    elif flag == 3: 
        verification_up = setting_status(average_value,limits[1])
        verification_down = setting_status_inverse(average_value,limits[0])
        if verification_up == "OK" and verification_down == "OK":
           verification = "OK"
        elif verification_up == "OK" and verification_down == "Warning":
           verification = "Warning"
        elif verification_up == "Warning" and verification_down == "OK":  
           verification = "Warning"
        else:
            verification = "Danger"
    elif flag == 4:
        verification = setting_status(std_value,limits)
    elif flag == 5:
        verification = setting_status(max_value,limits)
    elif flag == 6:
        average_value = str(round(np.average(getattr(df,name)[getattr(df,name)>0].astype(float)),1))
        std_value = str(round(np.std(getattr(df,name)[getattr(df,name)>0].astype(float)),1))
        max_value = str(round(np.max(getattr(df,name)[getattr(df,name)>0].astype(float)),1))
        min_value = str(round(np.min(getattr(df,name)[getattr(df,name)>0].astype(float)),1))
        verification = setting_status(average_value,limits)
    statistics = [average_value,std_value,max_value,min_value,verification]
    return statistics

def computing_reference_values(name):
    #       reference values for warnings, and flags (defined just above)
    reflected_power = getting_statistics_values("REFLECTED_POWER_W_AVE",cyclotron_information.df_rf,[300,500],0)
    forwarded_power = getting_statistics_values("FORWARD_POWER_AVE",cyclotron_information.df_rf,[13,14],0)
    transmission = getting_statistics_values("TRANSMISSION_AVE",cyclotron_information.df_transmission,[55,65],1)
    start_position_magnet = getting_statistics_values("START_IRRADIATION_REL_AVE",cyclotron_information.df_magnet,[49,51],1)  
    ratio_source  = getting_statistics_values("SOURCE_PERFORMANCE_AVE",cyclotron_information.ion_source_performance,[3,5],0) 
    current_source = getting_statistics_values("CURRENT_MAX",cyclotron_information.df_source,[550,700],0) 
    vacuum_pressure  = getting_statistics_values("PRESSURE_AVE",cyclotron_information.df_vacuum,[1.6,1.9],0) 
    hflow = getting_statistics_values('HFLOW_AVE',cyclotron_information.df_source,[0.5,1],4)
    magnet_current = getting_statistics_values("CURRENT_AVE",cyclotron_information.df_magnet,[0],2)
    target_current = getting_statistics_values("TARGET_CURRENT_MAX",cyclotron_information.df_beam,[105,110],5)
    foil_current = getting_statistics_values("FOIL_CURRENT_MAX",cyclotron_information.df_beam,[120,125],0)
    extraction_losses = getting_statistics_values("EXTRACTION_LOSSES_AVE",cyclotron_information.df_beam,[2,5],0)
    relative_coll = getting_statistics_values("RELATIVE_COLL_CURRENT_AVE",cyclotron_information.df_beam,[[5,10],[20,25]],3)
    pressure_irradiation = getting_statistics_values("PRESSURE_IRRADIATION_AVE",cyclotron_information.df_filling_volume,[[410.5,425],[450,465]],3)
    dee1_voltage = getting_statistics_values("DEE1_VOLTAGE_AVE",cyclotron_information.df_rf,[0],2)
    dee2_voltage = getting_statistics_values("DEE2_VOLTAGE_MAX",cyclotron_information.df_rf,[0],2)
    flap1 = getting_statistics_values("FLAP1_AVE",cyclotron_information.df_rf,[5,10],1)
    flap2 = getting_statistics_values("FLAP2_AVE",cyclotron_information.df_rf,[5,10],1)
    sparks = getting_statistics_values("SPARKS_AVE",cyclotron_information.df_rf,[1,2],0)
    volume_filling = getting_statistics_values('RELATIVE_VOLUME_AVE',cyclotron_information.df_filling_volume,[30,35],6)     # ana: [18,20] de limites
    probe = getting_statistics_values("PROBE_AVE",cyclotron_information.df_beam,[1,3],0)
    source_performance_ave = ratio_source[0]

    #       values shown inside the table
    values = [["Ion Source","Ion Source performance (probe)",ratio_source[-1],ratio_source[0],(ratio_source[1]),(ratio_source[2]),(ratio_source[3]),0,3,"mA/uA"],
    ["Ion Source","Ion Source current",current_source[-1],current_source[0],current_source[1],current_source[2],current_source[3],0,450,"mA"],
    ["Ion Source", "H flow", hflow[-1],hflow[0],hflow[1],hflow[2],hflow[3],"0","0.2 (deviation)","sccm"],
    ["Vacuum","Pressure",vacuum_pressure[-1],vacuum_pressure[0],vacuum_pressure[1],vacuum_pressure[2],vacuum_pressure[3],0,1.65,"10e-5 mbar"],
    ["Vacuum ","Transmission",transmission[-1],transmission[0],transmission[1],transmission[2],transmission[3],65,100,"%"],
    ["Beam", "I foil", foil_current[-1],foil_current[0],foil_current[1],foil_current[2],foil_current[3],"0","10 (deviation)","uA"],
    ["Beam","I target", target_current[-1],target_current[0],target_current[1],target_current[2],target_current[3],"0","10 (deviation)","uA"],
    ["Beam","I collimators", relative_coll[-1],relative_coll[0],relative_coll[1],relative_coll[2],relative_coll[3],8,20,"%"],
    ["Beam", "Extraction losses",extraction_losses[-1],extraction_losses[0],extraction_losses[1],extraction_losses[2],extraction_losses[3],0,0.5,"%"],
    ["Beam","Probe current", probe[-1],probe[0],probe[1],probe[2],probe[3],0,0.5,"uA"],
    ["RF", "Reflected power",reflected_power[-1],reflected_power[0],reflected_power[1],reflected_power[2],reflected_power[3],0,300 ,"W"],
    ["RF","Forwarded power",forwarded_power[-1],forwarded_power[0],forwarded_power[1],forwarded_power[2],forwarded_power[3],0,14 ,"kW"],
    ["RF", "Sparks",sparks[-1],sparks[0],sparks[1],sparks[2],sparks[3],0,0,"-"],  
    ["RF", "Flap 1",flap1[-1],flap1[0],flap1[1],flap1[2],flap1[3],5,100,"%"],
    ["RF", "Flap 2",flap2[-1],flap2[0],flap2[1],flap2[2],flap2[3],5,100,"%"],
    ["Target","Pressure irradiation",pressure_irradiation[-1],pressure_irradiation[0],pressure_irradiation[1],pressure_irradiation[2],pressure_irradiation[3], 425,450,"Psi"],
    ["Target","Relative volume filling",volume_filling[-1],volume_filling[0],volume_filling[1],volume_filling[2],volume_filling[3],15,35,"Psi"]]
    dff = pd.DataFrame(values,columns=["Subsystem","Parameter","Overall","Value","Deviation","Max","Min","Reference min","Reference max","Unit"])
    print ("DF CYCLOTRON")
    print (dff)
    return dff
    
    

def plotting_bars(element,limits,fig_size,title):
    text_to_plot = TEXT_TO_PLOT[element]
    values_to_plot = []
    for value in COLUMNS_TO_PLOT[element]:
        #print ("VALUES")
        #print (value)
        #print (getattr(cyclotron_information.df_summary,value).astype(float))
        values_to_plot.append(np.array(getattr(cyclotron_information.df_summary,value).astype(float))[0])
    values = [text_to_plot,values_to_plot]
    settings = [title,limits,fig_size]
    fig_status = additional_functions.plotting_charge(cyclotron_information,values,settings)
    #fig_status.update_layout(height=fig_size) 
    #fig_status.update_layout(title=settings[0]  ,
    #font=dict(size=16,color="#223A38"),font_family="Arial",margin=dict(t=60)) 
    return fig_status



@app.callback(Output('loading_output_1', 'children'),
              Output("table_status", "data"),
              Input('upload_data', 'contents'),
              State('upload_data', 'filename'),
              State('upload_data', 'last_modified'))
def update_output(list_of_contents,list_of_names, list_of_dates):
    cyclotron_information.__init__()
    target_1.__init__(computing_charge_class.df_information)
    target_2.__init__(computing_charge_class.df_information)
    if list_of_contents is not None:
        lists = zip(list_of_contents, list_of_names, list_of_dates)
        cyclotron_information.getting_information(target_1,target_2,lists)
    if (list_of_names) is None:
        message_to_show = "No data to display"
    else:
        message_to_show = "Click on Select a subsystem to display the time-evolution"
    df = computing_reference_values("REFLECTED_POWER_W_AVE")
    print ("HEREEEE!!!!")
    print (df)
    data_1 = df.to_dict("rows")
    return message_to_show,data_1
 


@app.callback(Output('loading-output-2', 'children'),
              Input('upload_data_file', 'contents'),
              State('upload_data_file', 'filename'),
              State('upload_data_file', 'last_modified'))
def update_output_logfile(list_of_contents,list_of_names, list_of_dates): 
    if list_of_contents is not None:
        additional_functions.parse_contents(cyclotron_information,list_of_contents[0],list_of_names[0], list_of_dates[0])  
    if (list_of_names) is None:
        message_to_show = "Select logfile to display"
    else:
        message_to_show = "Click on Select a subsystem to display the time-evolution"
    return message_to_show


app.run_server(debug=True)