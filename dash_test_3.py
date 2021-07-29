import json
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
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
import computing_charge_df
import dash_table as dt
import io
from datetime import date
import managing_files_alt
import computing_charge_df_alt
import source_performance_studies_alt


#df_summary_source = tfs.read("/Users/anagtv/Documents/OneDrive/046 - Medical Devices/Mantenimientos ciclotrones/TCP/ANALYSIS/20210625/table_summary_source.out")
#df_summary_vacuum = tfs.read("/Users/anagtv/Documents/OneDrive/046 - Medical Devices/Mantenimientos ciclotrones/TCP/ANALYSIS/20210625/table_summary_vacuum.out")
#df_summary_beam = tfs.read("/Users/anagtv/Documents/OneDrive/046 - Medical Devices/Mantenimientos ciclotrones/TCP/ANALYSIS/20210625/table_summary_beam.out")
#df_summary_rf = tfs.read("/Users/anagtv/Documents/OneDrive/046 - Medical Devices/Mantenimientos ciclotrones/TCP/ANALYSIS/20210625/table_summary_rf.out")
df_summary_performance = tfs.read("/Users/anagtv/Documents/OneDrive/046 - Medical Devices/Mantenimientos ciclotrones/TCP/ANALYSIS/20210625/source_summary_values.out")
#df = pd.DataFrame(list(zip(df_summary_beam.DATE,df_summary_source.CURRENT_AVE,df_summary_source.CURRENT_STD,df_summary_beam.TARGET_CURRENT_AVE,df_summary_beam.TARGET_CURRENT_STD,df_summary_beam.COLL_CURRENT_L_AVE + df_summary_beam.COLL_CURRENT_R_AVE,3
#	df_summary_beam.COLL_CURRENT_L_STD + df_summary_beam.COLL_CURRENT_R_STD,df_summary_vacuum.PRESSURE_AVE))
#    ,columns=["DATE","SOURCE","SOURCE_STD","TARGET","TARGET_STD","COLLIMATORS","COLLIMATORS_STD","VACUUM"])
#df_target_1 = tfs.read("cumulated_charge_1.out")
#df_target_2 = tfs.read("cumulated_charge_2.out")
columns = ["CHOOSE","SOURCE","VACUUM","RF"]
columns_locations = ["JNS","TCP","DIJ"]
columns_directory = ["CURRENT DIRECTORY"]


class data_to_analyze:
    def __init__(self):
        self.output_path = "/Users/anagtv/Documents/OneDrive/046 - Medical Devices/Mantenimientos ciclotrones/"
        self.fileName_folder = "/Users/anagtv/Documents/OneDrive/046 - Medical Devices/Mantenimientos ciclotrones/"
        self.current_row = 0

cyclotron_data = data_to_analyze()


class cyclotron:
    def __init__(self):
        self.output_path = "/Users/anagtv/Documents/OneDrive/046 - Medical Devices/Mantenimientos ciclotrones/TEST"
        self.target_number = 0
        self.date_stamp = 0
        self.name = 0 
        self.file_number = 0
        self.irradiation_values = 0
        self.file_df = []
        columns_names.initial_df(self)

    def file_output(self):
        #Computing or just displaying trends
        saving_trends_alt.getting_summary_per_file(self)

cyclotron_information = cyclotron()
target_1 = computing_charge_df_alt.target_cumulative_current(computing_charge_df_alt.df_information)
target_2 = computing_charge_df_alt.target_cumulative_current(computing_charge_df_alt.df_information)
target = source_performance_studies_alt.target_parameters()
central_region_summary = source_performance_studies_alt.central_region()
file_summary = source_performance_studies_alt.file_information()

dt1_table = [
    dt.DataTable(
        id = 'dt1', 
        columns =  [{"name": i, "id": i,} for i in (columns_names.COLUMNS_SOURCE)],)]

content_first_row = dbc.Row(
    [
        dbc.Col(
            dbc.Row([dcc.Graph(id='time-series-chart')])
        ),
       dbc.Col(
            dbc.Row([dcc.Graph(id='time-series-chart3')])
        )
    ]
)


app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    dbc.Container([dbc.Row([dcc.Dropdown(
        id="ticker",
        options=[{"label": x, "value": x} 
                 for x in columns],
        value=columns[0],
        clearable=False,
    )]),
    content_first_row,
    dbc.Row([dcc.Graph(id='time-series-chart4')]),
    dcc.Upload(
        id='upload_data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
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
    ),
    html.Div(id='output_data'),
    ])
])


@app.callback(
    Output("time-series-chart4", "figure"), 
    [Input("ticker", "value")],
    )
def display_source_performance(ticker): 
    #df_summary_performance = tfs.read(os.path.join(cyclotron_data.output_path,"source_summary_values.out"))
    if ticker == "SOURCE": 
        df_summary_source = tfs.read(os.path.join(cyclotron_data.output_path,"table_summary_source.out"))
        df_summary_beam = tfs.read(os.path.join(cyclotron_data.output_path,"table_summary_beam.out"))
        df_to_average = df_summary_performance.PERFORMANCE
        text_to_plot = "Source performance [mA/\u03bcA]"
    elif ticker == "VACUUM":
        df_summary_vacuum = tfs.read(os.path.join(cyclotron_data.output_path,"table_summary_vacuum.out"))
        df_to_average = df_summary_vacuum['PRESSURE_AVE']
        text_to_plot = "Vacuum level"
    elif ticker == "RF": 
        df_summary_rf = tfs.read(os.path.join(cyclotron_data.output_path,"table_summary_rf.out"))
        text_to_plot = "RF level"
        df_to_average = df_summary_rf.FORWARD_POWER_AVE
    else:
        df_to_average = [0,0,0]
        text_to_plot = " "
    fig_evolution = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = np.average(df_to_average) ,
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {'text': text_to_plot },
    gauge = {
                'axis': {'range': [None, 5], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "darkblue"},
                'steps' : [
                     {'range': [0, 1.5], 'color': "green"},
                     {'range': [1.5, 3], 'color': "yellow"},
                     {'range': [3, 4.5], 'color': "orange"},
                     {'range': [4.5, 6], 'color': "red"}
                ],
        
                'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 3.5}
            }
))
    fig_evolution.update_layout(paper_bgcolor = "lavender", font = {'color': "darkblue", 'family': "Arial"})
    return fig_evolution


@app.callback(
    Output("time-series-chart3", "figure"), 
    Input("ticker", "value"),
    Input("time-series-chart", "figure"),
    Input('upload_data', 'contents'),
    State('upload_data', 'filename'),
    State('upload_data', 'last_modified')
    )
def display_time_series_2(ticker,chart,list_of_contents,list_of_names, list_of_dates):
    df_target_1 = target_1.df_information_foil
    df_target_2 = target_2.df_information_foil
    fig2 =go.Figure(go.Sunburst(
    labels=["Total", "Target 1", "Target 2", "Foil 1 (1)","Foil 2 (1)", "Foil 3 (1)","Foil 4 (1)","Foil 5 (1)","Foil 6 (1)","Foil 1 (2)","Foil 2 (2)", "Foil 3 (2)","Foil 4 (2)"],
    parents=["","Total","Total","Target 1","Target 1","Target 1","Target 1","Target 1","Target 1","Target 2","Target 2","Target 2","Target 2"],values = 
    [df_target_1.CURRENT_TARGET.sum() + df_target_2.CURRENT_TARGET.sum(),df_target_1.CURRENT_TARGET.sum(),df_target_2.CURRENT_TARGET.sum(),
    df_target_1.CURRENT_FOIL[df_target_1.FOIL == "1"].sum(), df_target_1.CURRENT_FOIL[df_target_1.FOIL == "2"].sum(), df_target_1.CURRENT_FOIL[df_target_1.FOIL == "3"].sum(),
    df_target_1.CURRENT_FOIL[df_target_1.FOIL == "4"].sum(),df_target_1.CURRENT_FOIL[df_target_1.FOIL == "5"].sum(),df_target_1.CURRENT_FOIL[df_target_1.FOIL == "6"].sum(), df_target_2.CURRENT_FOIL[df_target_2.FOIL == "1"].sum(), df_target_2.CURRENT_FOIL[df_target_2.FOIL == "2"].sum(),
    df_target_2.CURRENT_FOIL[df_target_2.FOIL == "3"].sum(), df_target_2.CURRENT_FOIL[df_target_2.FOIL == "4"].sum()]))
    fig2.update_layout(paper_bgcolor = "lavender", font = {'color': "darkblue", 'family': "Arial"})
    return fig2

@app.callback(
    Output("time-series-chart", "figure"), 
    Input("ticker", "value"),
    Input('upload_data', 'contents'),
    State('upload_data', 'filename'),
    State('upload_data', 'last_modified')
    )
def display_time_series(ticker,list_of_contents,list_of_names, list_of_dates):
    fig = make_subplots(rows=3, cols=1,shared_xaxes=True,
                    vertical_spacing=0.02)
    if (ticker == "CHOOSE"):
        x_values = [0]
        y_values = [np.array(0),np.array(0),np.array(0)]
        y_values_error = [np.array(0),np.array(0),np.array(0)]
        names = ["","",""]
        units = ["","",""]
    else:
        if list_of_contents is not None:
            #getting_information(cyclotron_information,list_of_contents, list_of_names, list_of_dates)
            #getting_information_charge(target_1,target_2,list_of_contents, list_of_names, list_of_dates)
            getting_information_source_performance(list_of_contents, list_of_names, list_of_dates)
        df_summary_source = cyclotron_information.df_source
        df_summary_vacuum = cyclotron_information.df_vacuum
        df_summary_beam = cyclotron_information.df_beam
        df_summary_rf = cyclotron_information.df_rf
        df = pd.DataFrame(list(zip(df_summary_beam.DATE,df_summary_source.CURRENT_AVE,df_summary_source.CURRENT_STD,df_summary_beam.TARGET_CURRENT_AVE,df_summary_beam.TARGET_CURRENT_STD,df_summary_beam.COLL_CURRENT_L_AVE + df_summary_beam.COLL_CURRENT_R_AVE,
            df_summary_beam.COLL_CURRENT_L_STD + df_summary_beam.COLL_CURRENT_R_STD,df_summary_vacuum.PRESSURE_AVE))
            ,columns=["DATE","SOURCE","SOURCE_STD","TARGET","TARGET_STD","COLLIMATORS","COLLIMATORS_STD","VACUUM"])    
        if ticker == "SOURCE":
            x_values = df['DATE']
            y_values = [df['SOURCE'],df['TARGET'],df['COLLIMATORS']]
            y_values_error =  [df['SOURCE_STD'],df['TARGET_STD'],df['COLLIMATORS_STD']]
            names = ["I source","I target","I collimators"]
            units = [r"I [mA]","I [\u03bcA]","I [\u03bcA]"]
        elif ticker == "VACUUM":
            x_values = df['DATE']
            y_values = [df['SOURCE'],df_summary_vacuum['PRESSURE_AVE'],df_summary_source['HFLOW'].astype(float)] 
            y_values_error =  [df['SOURCE_STD'],df_summary_vacuum['PRESSURE_STD'],[0]*len(df_summary_source['HFLOW'].astype(float))]
            names = ["Source","Pressure","Gas flow"]
            units = ["I [mA]","10e-5 mbar","sccm"]
        elif ticker == "RF": 
            x_values = df['DATE']
            y_values = [df['SOURCE'],df_summary_rf['DEE1_VOLTAGE_AVE'],df_summary_rf['FORWARD_POWER_AVE']]
            y_values_error =  [df['SOURCE_STD'],df_summary_rf['DEE1_VOLTAGE_STD'],df_summary_rf['FORWARD_POWER_STD']]
            names = ["Source","RF Power", "RF Voltage"]
            units = ["I [mA]","kW","kV"]
    fig.add_trace(go.Scatter(x=x_values, y=y_values[0],mode='markers',                                                         
    marker=go.Marker(color='#3D3C28'),
    	error_y=dict(
            type='data',
            symmetric=True,
            array=y_values_error[0],
            ),name=names[0]),row=1, col=1)
    fig.add_trace(go.Scatter(x=x_values, y=y_values[1],error_y=dict(
            type='data',
            symmetric=True,
            array=y_values_error[1],
            ),name=names[1]),row=2, col=1)
    fig.add_trace(go.Scatter(x=x_values, y=y_values[2],
    	error_y=dict(
            type='data',
            symmetric=True,
            array=y_values_error[2],
            ),name=names[2]),row=3, col=1)
    fig.update_layout(height=900, width=800)
    fig.update_xaxes(title_text="Date", row=3, col=1)
    fig.update_yaxes(title_text=units[0], row=1, col=1)
    fig.update_yaxes(title_text=units[1], row=2, col=1)
    fig.update_yaxes(title_text=units[2], row=3, col=1)
    return fig

@app.callback(Output('output_data', 'children'),
              Input('upload_data', 'contents'),
              State('upload_data', 'filename'),
              State('upload_data', 'last_modified'))
def update_output(list_of_contents,list_of_names, list_of_dates):
    ...

        
def getting_information(cyclotron_information,list_of_contents, list_of_names, list_of_dates):
    for c, n, d in zip(list_of_contents, list_of_names, list_of_dates): 
        #all_names.append(str(n[:-4]))
        parse_contents(cyclotron_information,c, n, d) 
        cyclotron_information.file_output()
    saving_trends_alt.getting_summary_final(cyclotron_information)          

def getting_information_charge(target_1,target_2,list_of_contents, list_of_names, list_of_dates):
    for c, n, d in zip(list_of_contents, list_of_names, list_of_dates): 
        #all_names.append(str(n[:-4]))
        parse_contents(cyclotron_information,c, n, d) 
        computing_charge_df_alt.get_target_division(cyclotron_information,target_1,target_2)
    computing_charge_df_alt.get_summation_per_period(target_1)
    computing_charge_df_alt.get_summation_per_period(target_2)  
    print ("TARGET 1")
    print (target_1.df_information_foil)

def getting_information_source_performance(list_of_contents, list_of_names, list_of_dates):
    j = -1
    for c, n, d in zip(list_of_contents, list_of_names, list_of_dates): 
        #all_names.append(str(n[:-4]))
        parse_contents(cyclotron_information,c, n, d) 
        source_performance_studies_alt.get_data(cyclotron_information,file_summary,target,central_region_summary,j)

def parse_contents(cyclotron_information,contents, filename, date):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
    lines = []
    for i in range(len(df)):
        for line in df.loc[i]:
             parts = line.split()
             lines.append(
                np.array(parts))
    column_names = ["Time","Arc_I","Arc_V","Gas_flow","Dee_1_kV",
    "Dee_2_kV","Magnet_I","Foil_I","Coll_l_I","Target_I","Coll_r_I",
    "Vacuum_P","Target_P","Delta_Dee_kV","Phase_load","Dee_ref_V",
    "Probe_I","He_cool_P","Flap1_pos","Flap2_pos","Step_pos",
    "Extr_pos","Balance","RF_fwd_W","RF_refl_W","Foil_No"]
    column_names_nf = ["Time","Arc_I","Arc_V","Gas_flow","Dee_1_kV",
    "Dee_2_kV","Magnet_I","Foil_I","Coll_l_I","Target_I","Coll_r_I",
    "Vacuum_P","Target_P","Delta_Dee_kV","Phase_load","Dee_ref_V",
    "Probe_I","He_cool_P","Flap1_pos","Flap2_pos","Step_pos",
    "Extr_pos","Balance","RF_fwd_W","RF_refl_W","Foil_No"]
    all_values = []
    for j in range(len(column_names)):
        values = []
        for i in list(range(2,len(np.array(lines)))):
            values.append(np.array(lines[i][j]))
        all_values.append(values)
    cyclotron_information.file_df = pd.DataFrame(list(zip(all_values[0],all_values[1],all_values[2],all_values[3],all_values[4],
        all_values[5],all_values[6],all_values[7],all_values[8],all_values[9],all_values[10],all_values[11],
        all_values[12],all_values[13],all_values[14],all_values[15],all_values[16],all_values[17],all_values[18],
        all_values[19],all_values[20],all_values[21],all_values[22],all_values[23],all_values[24],all_values[25])),columns=column_names_nf)
    cyclotron_information.target_number = (df.columns[0][9:10])
    # el file_number esta dentro
    cyclotron_information.file_number = (df.columns[0][35:40])
    # TODO: dar formato a la fecha
    year = str(df.columns[0][49:53])
    month = str(df.columns[0][54:56])
    day = int(df.columns[0][57:60])
    #cyclotron.target_number = 0
    if day < 10:
        day = "0" + str(day)
    cyclotron_information.date_stamp = str(year) + "-" + str(month) + "-" + str(day)
    cyclotron_information.name = lines[0][2]
    #cyclotron_information.file_df = dataframe_test
    #print (cyclotron_information.file_df)
    return cyclotron_information


app.run_server(debug=True)