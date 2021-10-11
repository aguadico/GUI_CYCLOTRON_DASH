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
#import ion_source_studies
import additional_functions
import cyclotron_class
import app_layout
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

app.layout = app_layout.layout


COLUMNS_TO_PLOT = {"FOILS_1":["CUMULATIVE_TARGET_1_FOIL_1","CUMULATIVE_TARGET_1_FOIL_2","CUMULATIVE_TARGET_1_FOIL_3","CUMULATIVE_TARGET_1_FOIL_4","CUMULATIVE_TARGET_1_FOIL_5","CUMULATIVE_TARGET_1_FOIL_6"],
"FOILS_2":["CUMULATIVE_TARGET_2_FOIL_1","CUMULATIVE_TARGET_2_FOIL_2","CUMULATIVE_TARGET_2_FOIL_3","CUMULATIVE_TARGET_2_FOIL_4","CUMULATIVE_TARGET_2_FOIL_5","CUMULATIVE_TARGET_2_FOIL_6"],
"TARGET_COLLIMATORS_1":["CUMULATIVE_TARGET_1","CUMULATIVE_CURRENT_COLL_R_1","CUMULATIVE_CURRENT_COLL_L_1"],
"TARGET_COLLIMATORS_2":["CUMULATIVE_TARGET_2","CUMULATIVE_CURRENT_COLL_R_2","CUMULATIVE_CURRENT_COLL_L_2"],
"SOURCE_TARGETS":["CUMULATIVE_SOURCE","CUMULATIVE_TARGET_1","CUMULATIVE_TARGET_2"],
}

TEXT_TO_PLOT = {"FOILS_1":["Foil 1 [Ah]","Foil 2 [mAh]","Foil 3 [mAh]","Foil 4 [Ah]","Foil 5 [mAh]","Foil 6 [mAh]"],
"FOILS_2":["Foil 1 [Ah]","Foil 2 [mAh]","Foil 3 [mAh]","Foil 4 [Ah]","Foil 5 [mAh]","Foil 6 [mAh]"],
"TARGET_COLLIMATORS_1":["Target [mAh]","Collimator upper [uAh]","Collimator lower [uAh]"],
"TARGET_COLLIMATORS_2":["Target [mAh]","Collimator upper [uAh]","Collimator lower [uAh]"],
"SOURCE_TARGETS":["Source [Ah]","Target Position " + str(cyclotron_information.physical_targets[0]) +  " [mAh]","Target Position "+ str(cyclotron_information.physical_targets[1]) + " [mAh]"],
}



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
    print ("ENTERING HEREEE!!!""")
    fig = cyclotron_information.plotting_statistics(ticker,ticker_horizontal,ticker_layer)
    fig.update_layout(height=1500)
    return fig


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
    titles = ["","Target Position " + str(cyclotron_information.physical_targets[0]),"Target Position " + str(cyclotron_information.physical_targets[1]),
    "Target Position " + str(cyclotron_information.physical_targets[0]),"Target Position " + str(cyclotron_information.physical_targets[1])]
    fig_size = [500,500,500,800,800]
    figs = []
    for dict_value,limit,fig_size_i,title in zip(dict_keys,limits,fig_size,titles):
        print ("DICT KEY")
        print (dict_value)
        print (cyclotron_information.df_summary)
        figs.append(plotting_bars(dict_value,limit,fig_size_i,title))
    #print (adasas)
    return figs[0],figs[1],figs[2],figs[3],figs[4]


def plotting_bars(element,limits,fig_size,title):
    text_to_plot = TEXT_TO_PLOT[element]
    values_to_plot = []
    for value in COLUMNS_TO_PLOT[element]:
        print ("VALUES")
        print (value)
        print (getattr(cyclotron_information.df_summary,value).astype(float))
        values_to_plot.append(np.array(getattr(cyclotron_information.df_summary,value).astype(float))[0])
    values = [text_to_plot,values_to_plot]
    settings = [title,limits,fig_size]
    fig_status = additional_functions.plotting_charge(cyclotron_information,values,settings)
    #fig_status.update_layout(height=fig_size) 
    #fig_status.update_layout(title=settings[0]  ,
    #font=dict(size=16,color="#223A38"),font_family="Arial",margin=dict(t=60)) 
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
        lists = zip(list_of_contents, list_of_names, list_of_dates)
        additional_functions.getting_information(cyclotron_information,target_1,target_2,lists)
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