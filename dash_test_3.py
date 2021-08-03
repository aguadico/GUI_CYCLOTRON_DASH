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


columns = ["CHOOSE","SOURCE","VACUUM","RF","TARGET"]
columns_horizontal = ["DATE","FILE"]
#columns_directory = ["CURRENT DIRECTORY"]
target_1 = computing_charge_df_alt.target_cumulative_current(computing_charge_df_alt.df_information)
target_2 = computing_charge_df_alt.target_cumulative_current(computing_charge_df_alt.df_information)

#COLORS = ["#047495","#fc5a50","#74a662"]
COLORS = [["#029386","#069AF3"],["#F97306","#EF4026"],["#054907","#15B01A"]]

class cyclotron:
    def __init__(self):
        #self.output_path = "/Users/anagtv/Documents/OneDrive/046 - Medical Devices/Mantenimientos ciclotrones/TEST"
        self.target_number = 0
        self.date_stamp = 0
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

    def file_output(self):
        #Computing or just displaying trends
        saving_trends_alt.getting_summary_per_file(self)
        ion_source_studies.returning_current(cyclotron_information,ion_source_studies.current_vaccum)

cyclotron_information = cyclotron()


dt1_table = [
    dt.DataTable(
        id = 'dt1', 
        columns =  [{"name": i, "id": i,} for i in (columns_names.COLUMNS_SOURCE)],)]

app = JupyterDash(external_stylesheets=[dbc.themes.SLATE])

app.layout = html.Div([
    dbc.Card(
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                   dcc.Dropdown(
        id="ticker",
        options=[{"label": x, "value": x} 
                 for x in columns],
        value=columns[0],
        clearable=False,
    )
            ], width=2),
            dbc.Col([
                   dcc.Dropdown(
        id="ticker_horizontal",
        options=[{"label": x, "value": x} 
                 for x in columns_horizontal],
        value=columns_horizontal[0],
        clearable=False,
    )
            ], width=2)
                ,
                dbc.Col([
                    dcc.Upload(
        id='upload_data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files'),
                dbc.Col([
                    html.Div(id='output_data')
                ], width=1),
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    )
                ], width=3),
                dbc.Col([
                    dcc.Upload(
        id='upload_data_folder',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Folder'),
                dbc.Col([
                    html.Div(id='output_data_folder')
                ], width=1),
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    )
                ], width=3)
            ], align='center'),  
            html.Br(),
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id='time_series_chart_volume')
                ], width=5),
                dbc.Col([
                    dcc.Graph(id='time_series_chart') 
                ], width=5),
            ], align='center'), 
            html.Br(),
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id='time-series-chart4')
                ], width=5),
                dbc.Col([
                    dcc.Graph(id='time-series-chart3')
                ], width=6),
            ], align='center'),      
        ]), color = 'dark'
    )
])



@app.callback(
    Output("time_series_chart_volume", "figure"), 
    [Input("ticker", "value")],
    Input("time_series_chart", "figure"),
    )
def daily_report(ticker,chart): 
    fig = make_subplots(rows=3, cols=1,shared_xaxes=True,
                    vertical_spacing=0.02)
    fig.update_layout(height=900, width=800)
    if (ticker == "CHOOSE"):
        x_values = [0]
        y_values = [np.array(0),np.array(0),np.array(0)]
        y_values_error = [np.array(0),np.array(0),np.array(0)]
        names = ["","",""]
        units = ["","",""]
        for i in range(3): 
            fig = additional_functions.plotting_simple(fig,x_values,y_values[i],y_values_error[i],units[i],i+1,1,COLORS[i][0])
    else:
       fig_volume = additional_functions.plotting_simple_no_error(fig,cyclotron_information.file_df.Time,cyclotron_information.file_df.Arc_I,"Arc I [mA]",1,1,COLORS[1][0])
       fig_volume = additional_functions.plotting_simple_no_error(fig,cyclotron_information.file_df.Time,cyclotron_information.file_df.Target_I,"Target I [\u03bcA]",2,1,COLORS[1][0])
       fig_volume = additional_functions.plotting_simple_no_error(fig,cyclotron_information.file_df.Time,cyclotron_information.file_df.Vacuum_P,"Vacuum P [1e-5 mbar]",3,1,COLORS[1][0])
       fig.update_layout(showlegend=False)
       fig.update_xaxes(title_text="Date", row=3, col=1)
    return (fig)
   


@app.callback(
    Output("time-series-chart4", "figure"), 
    Input("ticker", "value"),
    Input("time_series_chart", "figure"),
    )
def display_source_performance(ticker,chart): 
    if ticker == "SOURCE": 
        df_to_average = cyclotron_information.source_performance
        print ("DF SOURCE")
        print (df_to_average)
        text_to_plot = "Source performance [mA/\u03bcA]"
        range_values = [[0,1.5],[1.5,3],[3.0,4.5],[4.5,6.0]]
        value_ob = 3.0
    elif ticker == "VACUUM":
        df_to_average = (cyclotron_information.df_vacuum['PRESSURE_AVE'])
        text_to_plot = "Vacuum level"
        range_values = [[0,1.3],[1.3,1.6],[1.6,1.8],[1.8,2.0]]
        value_ob = 2.0
    elif ticker == "RF": 
        text_to_plot = "RF level"
        df_to_average = cyclotron_information.df_rf.FORWARD_POWER_AVE
        range_values = [[0,11],[11,12],[12,13],[13,14]]
        value_ob = 13.5
    else:
        df_to_average = [0,0,0]
        text_to_plot = " "
        range_values = [[0,1],[1,2],[2,3],[3,4]]
        value_ob = 3.5
    fig_evolution = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = np.average(df_to_average) ,
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {'text': text_to_plot },
    gauge = {
                'axis': {'range': [None, np.max(range_values)], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "darkblue"},
                'steps' : [
                     {'range': range_values[0], 'color': "green"},
                     {'range': range_values[1], 'color': "yellow"},
                     {'range': range_values[2], 'color': "orange"},
                     {'range': range_values[3], 'color': "red"}
                ],
        
                'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': value_ob}
            }
))
    fig_evolution.update_layout(paper_bgcolor = "lavender", font = {'color': "darkblue", 'family': "Arial"})
    return fig_evolution


@app.callback(
    Output("time-series-chart3", "figure"), 
    Input("ticker", "value"),
    Input("time_series_chart", "figure"),
    Input('upload_data', 'contents'),
    State('upload_data', 'filename'),
    State('upload_data', 'last_modified')
    )
def display_time_series_2(ticker,chart,list_of_contents,list_of_names, list_of_dates):
    df_target_1 = target_1.df_information_foil
    df_target_2 = target_2.df_information_foil
    print ("TARGET INFORMATION")
    print (target_1.df_information_foil)
    fig2 =go.Figure(go.Sunburst(
     labels=["Ion Source", "Target 1", "Target 2", "Foil 1 (1)","Foil 2 (1)", "Foil 3 (1)","Foil 4 (1)","Foil 5 (1)","Foil 6 (1)","Foil 1 (2)","Foil 2 (2)", "Foil 3 (2)","Foil 4 (2)"],
     parents=["","Ion Source","Ion Source","Target 1","Target 1","Target 1","Target 1","Target 1","Target 1","Target 2","Target 2","Target 2","Target 2"],values = 
     [(df_target_1.CURRENT_SOURCE.sum() + df_target_2.CURRENT_SOURCE.sum())/1000,df_target_1.CURRENT_TARGET.sum()/1000,df_target_2.CURRENT_TARGET.sum()/1000,
     df_target_1.CURRENT_FOIL[df_target_1.FOIL == "1"].sum(), df_target_1.CURRENT_FOIL[df_target_1.FOIL == "2"].sum(), df_target_1.CURRENT_FOIL[df_target_1.FOIL == "3"].sum(),
     df_target_1.CURRENT_FOIL[df_target_1.FOIL == "4"].sum(),df_target_1.CURRENT_FOIL[df_target_1.FOIL == "5"].sum(),df_target_1.CURRENT_FOIL[df_target_1.FOIL == "6"].sum(), df_target_2.CURRENT_FOIL[df_target_2.FOIL == "1"].sum(), df_target_2.CURRENT_FOIL[df_target_2.FOIL == "2"].sum(),
     df_target_2.CURRENT_FOIL[df_target_2.FOIL == "3"].sum(), df_target_2.CURRENT_FOIL[df_target_2.FOIL == "4"].sum()]))
    fig2.update_layout(paper_bgcolor = "lavender", font = {'color': "darkblue", 'family': "Arial"},margin = dict(t=0, l=0, r=0, b=0))
    return fig2

@app.callback(
    Output("time_series_chart", "figure"), 
    Input("ticker", "value"),
    Input("ticker_horizontal", "value"),
    Input('upload_data', 'contents'),
    State('upload_data', 'filename'),
    State('upload_data', 'last_modified')
    )
def display_time_series(ticker,ticker_horizontal,list_of_contents,list_of_names, list_of_dates):
    fig = make_subplots(rows=3, cols=1,shared_xaxes=True,
                    vertical_spacing=0.02)
    fig.update_layout(height=900, width=800)
    if (ticker == "CHOOSE"):
        x_values = [0]
        y_values = [np.array(0),np.array(0),np.array(0)]
        y_values_error = [np.array(0),np.array(0),np.array(0)]
        names = ["","",""]
        units = ["","",""]
        for i in range(3): 
            fig = additional_functions.plotting_simple(fig,x_values,y_values[i],y_values_error[i],units[i],i+1,1,COLORS[i][0])
    else:
        df_summary_source = cyclotron_information.df_source
        df_summary_vacuum = cyclotron_information.df_vacuum
        df_summary_beam = cyclotron_information.df_beam
        df_summary_rf = cyclotron_information.df_rf
        cyclotron_information.target_min = np.min(df_summary_source.TARGET.astype(float))
        cyclotron_information.target_max = np.max(df_summary_source.TARGET.astype(float))
        cyclotron_information.values_targets = [cyclotron_information.target_min,cyclotron_information.target_max]
        j = - 1
        for target in cyclotron_information.values_targets:
            j += 1  
            df = pd.DataFrame(list(zip(df_summary_beam.DATE,df_summary_source.TARGET,df_summary_source.FILE,df_summary_source.CURRENT_AVE,df_summary_source.CURRENT_STD,df_summary_beam.TARGET_CURRENT_AVE,df_summary_beam.TARGET_CURRENT_STD,df_summary_beam.COLL_CURRENT_L_AVE + df_summary_beam.COLL_CURRENT_R_AVE,
                df_summary_beam.COLL_CURRENT_L_STD + df_summary_beam.COLL_CURRENT_R_STD,df_summary_vacuum.PRESSURE_AVE))
                ,columns=["DATE","TARGET_NUMBER","FILE","SOURCE","SOURCE_STD","TARGET","TARGET_STD","COLLIMATORS","COLLIMATORS_STD","VACUUM"])    
            df = df[df.TARGET_NUMBER.astype(float) == float(target)]
            volume_information = cyclotron_information.df_volume[cyclotron_information.df_volume.TARGET.astype(float) == float(target)]
            x_values = getattr(df,ticker_horizontal)
            if ticker == "SOURCE":
                y_values = [df['SOURCE'],df['TARGET'],df['COLLIMATORS']]
                y_values_error =  [df['SOURCE_STD'],df['TARGET_STD'],df['COLLIMATORS_STD']]
                units = [r"I source[mA]","I target [\u03bcA]","I collimators[\u03bcA]"]
            elif ticker == "VACUUM":
                y_values = [df['SOURCE'],df_summary_vacuum['PRESSURE_AVE'],df_summary_source['HFLOW'].astype(float)] 
                y_values_error =  [df['SOURCE_STD'],df_summary_vacuum['PRESSURE_STD'],[0]*len(df_summary_source['HFLOW'].astype(float))]
                units = ["I [mA]","10e-5 mbar","sccm"]
            elif ticker == "RF": 
                y_values = [df['SOURCE'],df_summary_rf['DEE1_VOLTAGE_AVE'],df_summary_rf['FORWARD_POWER_AVE']]
                y_values_error =  [df['SOURCE_STD'],df_summary_rf['DEE1_VOLTAGE_STD'],df_summary_rf['FORWARD_POWER_STD']]
                units = ["I [mA]","kV","kW"]
            elif ticker == "TARGET":
                print ("TARGET")
                print (volume_information)
                y_values = [df['SOURCE'],volume_information.PRESSURE_FINAL,volume_information.MAX_PRESSURE]
                y_values_error =  [df['SOURCE_STD'],volume_information.STD_PRESSURE,volume_information.STD_PRESSURE]
                units = [r"I source[mA]","Pressure final [psi]","Pressure average [psi]"]
            for i in range(3): 
                fig = additional_functions.plotting_simple(fig,x_values,y_values[i],y_values_error[i],units[i],i+1,1,COLORS[0][j])
    #scatter.on_click(update_point)
    fig.update_layout(showlegend=False)
    fig.update_xaxes(title_text="Date", row=3, col=1)
    return fig
 

@app.callback(Output('output_data', 'children'),
              Input('upload_data', 'contents'),
              State('upload_data', 'filename'),
              State('upload_data', 'last_modified'))
def update_output(list_of_contents,list_of_names, list_of_dates):
    if list_of_contents is not None:
        additional_functions.getting_information(cyclotron_information,target_1,target_2,list_of_contents, list_of_names, list_of_dates)
    
@app.callback(Output('output_data_folder', 'children'),
              Input('upload_data_folder', 'contents'),
              State('upload_data_folder', 'filename'),
              State('upload_data_folder', 'last_modified'))
def update_output(list_of_contents,list_of_names, list_of_dates):
    if list_of_contents is not None:
        print ("HEREEEE")
        #additional_functions.getting_information(cyclotron_information,target_1,target_2,list_of_contents, list_of_names, list_of_dates)

        


app.run_server(debug=True)