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
import computing_charge_df_alt
import ion_source_studies
import additional_functions
import cyclotron_class
import app_layout_1
import getting_subsystems_data_alt
import time
import plotting_logs

columns = ["CHOOSE","SOURCE","MAGNET","BEAM","VACUUM","RF","RF_STABILITY","TARGET"]
columns_horizontal = ["DATE","FILE"]
#columns_directory = ["CURRENT DIRECTORY"]
target_1 = computing_charge_df_alt.target_cumulative_current(computing_charge_df_alt.df_information)
target_2 = computing_charge_df_alt.target_cumulative_current(computing_charge_df_alt.df_information)



cyclotron_information = cyclotron_class.cyclotron()


app = JupyterDash(external_stylesheets=[dbc.themes.SLATE])
app.title = "Cyclotron Analytics"
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


app.layout = app_layout_1.layout





@app.callback(
    Output("time_series_chart_volume", "figure"), 
    Input("ticker_2", "value"),
    Input("ticker_layer_file", "value"),
    Input('tabs-with-classes', 'value'),
    Input('upload_data_file', 'filename'),
    )
def daily_report(ticker,ticker_layer,tabs,input_file): 
    fig_logfile = plotting_logs.daily_report(ticker,ticker_layer,tabs,input_file,cyclotron_information)
    return (fig_logfile)
   

@app.callback(
    Output("time_series_chart", "figure"), 
    Input("ticker", "value"),
    Input("ticker_horizontal", "value"),
    Input("ticker_layer", "value"),
    Input('tabs-with-classes', 'value'),
    Input('upload_data', 'contents'),
    State('upload_data', 'filename'),
    State('upload_data', 'last_modified')
    )
def display_time_series(ticker,ticker_horizontal,ticker_layer,tabs,list_of_contents,list_of_names, list_of_dates):
    fig = make_subplots(rows=3, cols=1,shared_xaxes=True,
                        vertical_spacing=0.02)
    fig.update_layout(height=1500)
    fig = cyclotron_information.plotting_statistics(ticker,ticker_horizontal,ticker_layer)
    return fig


@app.callback(
    Output("time-series-chart4", "figure"), 
    Input('loading_output_1', 'children'), 
    )
def display_total_charge(loading): 
    text_to_plot = ["Source [Ah]","Target Position " + str(cyclotron_information.physical_targets[0]) +  " [mAh]","Target Position "+ str(cyclotron_information.physical_targets[1]) + " [mAh]"]
    values_to_plot = [np.array(cyclotron_information.df_summary["CUMULATIVE_SOURCE"].astype(float))[0],np.array(cyclotron_information.df_summary["CUMULATIVE_TARGET_1"].astype(float))[0]/1000,
    np.array(cyclotron_information.df_summary["CUMULATIVE_TARGET_2"].astype(float))[0]/1000]    
    fig_status = additional_functions.plotting_charge(cyclotron_information,text_to_plot,values_to_plot," ","charge_source_target")
    return fig_status


@app.callback(
    Output("foils_1_4_5_6", "figure"), 
    Input('loading_output_1', 'children'), 
    )
def display_foils_1_4_5_6(loading): 
    text_to_plot = ["Foil 1 [Ah]","Foil 2 [mAh]","Foil 3 [mAh]","Foil 4 [Ah]","Foil 5 [mAh]","Foil 6 [mAh]"]
    values_to_plot = [np.array(cyclotron_information.df_summary["CUMULATIVE_TARGET_1_FOIL_1"].astype(float))[0],np.array(cyclotron_information.df_summary["CUMULATIVE_TARGET_1_FOIL_2"].astype(float))[0],
    np.array(cyclotron_information.df_summary["CUMULATIVE_TARGET_1_FOIL_3"].astype(float))[0],np.array(cyclotron_information.df_summary["CUMULATIVE_TARGET_1_FOIL_4"].astype(float))[0],np.array(cyclotron_information.df_summary["CUMULATIVE_TARGET_1_FOIL_5"].astype(float))[0],
    np.array(cyclotron_information.df_summary["CUMULATIVE_TARGET_1_FOIL_6"].astype(float))[0]]
    fig_status = additional_functions.plotting_charge(cyclotron_information,text_to_plot,values_to_plot,"Target Position " + str(cyclotron_information.physical_targets[0]) ,"charge_foils")
    fig_status.update_layout(height=800)  
    return fig_status

@app.callback(
    Output("foils_2_4_5_6", "figure"), 
    Input('loading_output_1', 'children'),  
    )
def display_foils_2_4_5_6(loading): 
    text_to_plot = ["Foil 1 [Ah]","Foil 2 [mAh]","Foil 3 [mAh]","Foil 4 [Ah]","Foil 5 [mAh]","Foil 6 [mAh]"]
    values_to_plot = [np.array(cyclotron_information.df_summary["CUMULATIVE_TARGET_2_FOIL_1"].astype(float))[0],np.array(cyclotron_information.df_summary["CUMULATIVE_TARGET_2_FOIL_2"].astype(float))[0],
    np.array(cyclotron_information.df_summary["CUMULATIVE_TARGET_2_FOIL_3"].astype(float))[0],np.array(cyclotron_information.df_summary["CUMULATIVE_TARGET_2_FOIL_4"].astype(float))[0],np.array(cyclotron_information.df_summary["CUMULATIVE_TARGET_2_FOIL_5"].astype(float))[0],
    np.array(cyclotron_information.df_summary["CUMULATIVE_TARGET_2_FOIL_6"].astype(float))[0]]
    fig_status = additional_functions.plotting_charge(cyclotron_information,text_to_plot,values_to_plot,"Target Position " + str(cyclotron_information.physical_targets[1]) ,"charge_foils")
    fig_status.update_layout(height=800) 
    return fig_status

@app.callback(
    Output("target_collimators_1", "figure"),
    Input('loading_output_1', 'children')
        )
def display_target_collimators_1(fig): 
    text_to_plot = ["Target [mAh]","Collimator upper [uAh]","Collimator lower [uAh]"]
    values_to_plot = [np.array(cyclotron_information.df_summary["CUMULATIVE_TARGET_1"].astype(float)/1000)[0],np.array(cyclotron_information.df_summary["CUMULATIVE_CURRENT_COLL_R_1"].astype(float))[0],
    np.array(cyclotron_information.df_summary["CUMULATIVE_CURRENT_COLL_L_1"].astype(float))[0]]   
    fig_status = additional_functions.plotting_charge(cyclotron_information,text_to_plot,values_to_plot,"Position " + str(cyclotron_information.physical_targets[0]) ,"charge_collimators_target")
    return fig_status

@app.callback(
    Output("target_collimators_2", "figure"),
    Input('loading_output_1', 'children'), 
    )
def display_target_collimators_2(fig): 
    text_to_plot = ["Target [mAh]","Collimator upper [uAh]","Collimator lower [uAh]"]
    values_to_plot = [np.array(cyclotron_information.df_summary["CUMULATIVE_TARGET_2"].astype(float)/1000)[0],np.array(cyclotron_information.df_summary["CUMULATIVE_CURRENT_COLL_R_2"].astype(float))[0],
    np.array(cyclotron_information.df_summary["CUMULATIVE_CURRENT_COLL_L_2"].astype(float))[0]]
    fig_status = additional_functions.plotting_charge(cyclotron_information,text_to_plot,values_to_plot,"Position " + str(cyclotron_information.physical_targets[1]),"charge_collimators_target")
    return fig_status


@app.callback(Output('loading_output_1', 'children'),
              Input('upload_data', 'contents'),
              State('upload_data', 'filename'),
              State('upload_data', 'last_modified'))
def update_output(list_of_contents,list_of_names, list_of_dates):
    cyclotron_information.__init__()
    target_1.__init__(computing_charge_df_alt.df_information)
    target_2.__init__(computing_charge_df_alt.df_information)
    if list_of_contents is not None:
        additional_functions.getting_information(cyclotron_information,target_1,target_2,list_of_contents, list_of_names, list_of_dates)
    if (list_of_names) is None:
        message_to_show = "No data to display"
    else:
        message_to_show = "Click on Select a subsystem to display the time-evolution"
    return message_to_show
 




@app.callback(Output('loading-output-2', 'children'),
              Input('upload_data_file', 'contents'),
              State('upload_data_file', 'filename'),
              State('upload_data_file', 'last_modified'))
def update_output(list_of_contents,list_of_names, list_of_dates): 
    if list_of_contents is not None:
        additional_functions.parse_contents(cyclotron_information,list_of_contents[0],list_of_names[0], list_of_dates[0])  
    if (list_of_names) is None:
        message_to_show = "Select logfile to display"
    else:
        message_to_show = "Click on Select a subsystem to display the time-evolution"
    return message_to_show


app.run_server(debug=True)