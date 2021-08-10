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


columns = ["CHOOSE","SOURCE","MAGNET","BEAM","VACUUM","RF","RF_STABILITY","TARGET"]
columns_horizontal = ["DATE","FILE"]
#columns_directory = ["CURRENT DIRECTORY"]
target_1 = computing_charge_df_alt.target_cumulative_current(computing_charge_df_alt.df_information)
target_2 = computing_charge_df_alt.target_cumulative_current(computing_charge_df_alt.df_information)

#COLORS = ["#047495","#fc5a50","#74a662"]
COLORS = ["#F97306","#EF4026"],["#029386","#069AF3"],["#054907","#15B01A"]
COLORS_TRENDS = [[["#F97306","#EF4026","#054907"],["#F97306","#EF4026","#054907"],["#F97306","#EF4026","#054907"],["#F97306","#029386","#054907"]],[["#029386","#069AF3","#15B01A"],
["#029386","#069AF3","#15B01A"],["#029386","#069AF3","#15B01A"],["#029386","#069AF3","#15B01A"]]]

cyclotron_information = cyclotron_class.cyclotron()


dt1_table = [
    dt.DataTable(
        id = 'dt1', 
        columns =  [{"name": i, "id": i,} for i in (columns_names.COLUMNS_SOURCE)],)]

app = JupyterDash(external_stylesheets=[dbc.themes.SLATE])

layout = {
  "title": "Plot With Background Color", 
  "width": 576, 
  "height": 396, 
  "margin": {
    "b": 49, 
    "l": 72, 
    "r": 57, 
    "t": 47, 
    "pad": 0
  }, 
  "xaxis1": {
    "side": "bottom", 
    "type": "linear", 
    #"range": [-13.473985351971331, 459.5006453519714], 
    "ticks": "inside", 
    "anchor": "y1", 
    "domain": [0.0, 1.0], 
    "mirror": "ticks", 
    "nticks": 7, 
    "showgrid": True, 
    "showline": True, 
    "tickfont": {"size": 10.0}, 
    "zeroline": False
  }, 
  "yaxis1": {
    "side": "left", 
    "type": "linear", 
    #"range": [-0.061127115526122155, 1.0627937821927889], 
    "ticks": "inside", 
    "anchor": "x1", 
    #"domain": [0.0, 1.0], 
    "mirror": "ticks", 
    "nticks": 8, 
    "showgrid": True, 
    "showline": True, 
    "tickfont": {"size": 10.0}, 
    "zeroline": False
  }, 
  "autosize": False, 
  "hovermode": "closest", 
  "titlefont": {
    "size": 12.0, 
    "color": "#262626"
  }, 
  "showlegend": False, 
  "plot_bgcolor": "white"
}
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
        id='upload_data_file',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Individual File'),
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
                ], width=6),
            ], align='center'), 
            html.Br(),
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id='time-series-chart4')
                ], width=12),
            ], align='center'), 
            html.Br(),
            dbc.Row([
                 dbc.Col([
                    dcc.Graph(id='target_collimators_1')
                ], width=6),
                dbc.Col([
                    dcc.Graph(id='target_collimators_2') 
                ], width=6),
            ], align='center'),
            html.Br(),
            dbc.Row([
                 dbc.Col([
                    dcc.Graph(id='foils_1_1_2_3')
                ], width=6),
                dbc.Col([
                    dcc.Graph(id='foils_2_1_2_3') 
                ], width=6),
            ], align='center'),  
             html.Br(),
            dbc.Row([
                 dbc.Col([
                    dcc.Graph(id='foils_1_4_5_6')
                ], width=6),
                dbc.Col([
                    dcc.Graph(id='foils_2_4_5_6') 
                ], width=6),
            ], align='center')   
        ]), color = 'dark'
    )
])


def general_status_plot(fig_status,values_to_plot,range_values,y_position,text_to_plot):
    for i in range(len(values_to_plot)):
        if np.min(range_values[i][2]) <=(values_to_plot[i]) <= np.max(range_values[i][2]):
             print ("RED")
             normalized_colors_internal = "#FE420F"
             normalized_colors_external = "#F97306"
        elif np.min(range_values[i][1]) < (values_to_plot[i]) <= np.max(range_values[i][1]):
             print ("ORANGE")
             normalized_colors_internal = "orange"
             normalized_colors_external = "#FAC205" 
        elif np.min(range_values[i][0]) <= (values_to_plot[i]) <= np.max(range_values[i][0]):
             print ("GREEN")
             normalized_colors_internal = "green"
             normalized_colors_external = "#76FF7B"
        fig_status.add_trace(go.Indicator(
    mode = "number+gauge", value = values_to_plot[i][0],
    domain = {'x': [0.25, 1], 'y': y_position[i]},
    title = {'text' :text_to_plot[i]},
    gauge = {
        'shape': "bullet",
        'axis': {'range': [None, np.max(range_values[i])]},
        'steps': [
            {'range': range_values[i][3], 'color': "red"},
            ],
        'bar': {'color': normalized_colors_internal}
        }))
    return fig_status

@app.callback(
    Output("time_series_chart_volume", "figure"), 
    Input("ticker", "value"),
    Input("time_series_chart", "figure"),
    Input('upload_data_file', 'filename'),
    )
def daily_report(ticker,chart,input_file): 
    fig_volume = go.FigureWidget(make_subplots(rows=3, cols=1,shared_xaxes=True,
                    vertical_spacing=0.02))
    fig_volume.update_layout(title="Individual log")
    fig_volume.update_layout(height=1500)
    if (ticker == "CHOOSE"):
        x_values = [0]
        y_values = [np.array(0),np.array(0),np.array(0)]
        y_values_error = [np.array(0),np.array(0),np.array(0)]
        names = ["","",""]
        units = ["","",""]
        for i in range(3): 
            fig_volume = additional_functions.plotting_simple_no_error(fig_volume,x_values,y_values[i],units[i],i+1,1,COLORS[i][0],"")
    else:
       if ticker == "SOURCE":
          fig_volume = additional_functions.plotting_simple_no_error(fig_volume,cyclotron_information.file_df.Time,cyclotron_information.file_df.Arc_I.astype(float),"Arc I [mA]",1,1,COLORS[2][0],"Source current")
          fig_volume = additional_functions.plotting_simple_no_error(fig_volume,cyclotron_information.file_df.Time,cyclotron_information.file_df.Target_I.astype(float),"Target I [\u03bcA]",2,1,COLORS[2][0],"Target current")
          fig_volume = additional_functions.plotting_simple_no_error(fig_volume,cyclotron_information.file_df.Time,cyclotron_information.file_df.Coll_l_I.astype(float)+cyclotron_information.file_df.Coll_r_I.astype(float),"Collimators [\u03bcA]",3,1,COLORS[2][0],"Collimators current")
          print ("HEEEERERRR")
          scatter = fig_volume.data[0]
          print (scatter)
          fig_volume.layout.hovermode = 'closest'
          scatter.on_click(update_point)
       elif ticker == "VACUUM": 
          fig_volume = additional_functions.plotting_simple_no_error(fig_volume,cyclotron_information.file_df.Time,cyclotron_information.file_df.Arc_I,"Arc I [mA]",1,1,COLORS[2][0],"Source current")
          fig_volume = additional_functions.plotting_simple_no_error(fig_volume,cyclotron_information.file_df.Time,cyclotron_information.file_df.Vacuum_P.astype(float)*1e5,"Vacuum P [1e-5 mbar]",2,1,COLORS[2][0],"Vacuum")
          fig_volume = additional_functions.plotting_simple_no_error(fig_volume,cyclotron_information.file_df.Time,cyclotron_information.file_df.Gas_flow,"Gas flow [sccm]",3,1,COLORS[2][0],"Gas flow")
       elif ticker == "RF": 
          fig_volume = additional_functions.plotting_simple_no_error(fig_volume,cyclotron_information.file_df.Time,cyclotron_information.file_df.Flap1_pos.astype(float),"Flap [%]",1,1,COLORS[2][0],"Flap 1")
          fig_volume = additional_functions.plotting_simple_no_error(fig_volume,cyclotron_information.file_df.Time,cyclotron_information.file_df.Flap2_pos.astype(float),"Flap [%]",1,1,COLORS[2][1],"Flap 2")
          fig_volume = additional_functions.plotting_simple_no_error(fig_volume,cyclotron_information.file_df.Time,cyclotron_information.file_df.Dee_1_kV.astype(float),"RF Voltage 1 [kV]",2,1,COLORS[2][0],"RF Dee 1")
          fig_volume = additional_functions.plotting_simple_no_error(fig_volume,cyclotron_information.file_df.Time,cyclotron_information.file_df.Dee_2_kV.astype(float),"RF Voltage 2 [kV]",2,1,COLORS[2][1],"RF Dee 2")
          fig_volume = additional_functions.plotting_simple_no_error(fig_volume,cyclotron_information.file_df.Time,cyclotron_information.file_df.RF_fwd_W.astype(float),"RF Power (forwarded) [kW]",3,1,COLORS[2][0],"RF Power Fwd")
          fig_volume = additional_functions.plotting_simple_no_error(fig_volume,cyclotron_information.file_df.Time,cyclotron_information.file_df.RF_refl_W.astype(float),"RF Power (reflected) [kW]",3,1,COLORS[2][1], "RF Power Rfl")
       elif ticker == "TARGET":
          fig_volume = additional_functions.plotting_simple_no_error(fig_volume,cyclotron_information.file_df.Time,cyclotron_information.file_df.Target_I.astype(float),"Target I [\u03bcA]",1,1,COLORS[2][0],"Target current")
          fig_volume = additional_functions.plotting_simple_no_error(fig_volume,cyclotron_information.file_df.Time,cyclotron_information.file_df.Target_P.astype(float),"Pressure [psi]",2,1,COLORS[2][0],"Target pressure")
          fig_volume = additional_functions.plotting_simple_no_error(fig_volume,cyclotron_information.file_df.Time,cyclotron_information.file_df.Extr_pos.astype(float),"Extraction position [%]",3,1,COLORS[2][0],"Extraction")
       fig_volume.update_layout(title="Last log")
       fig_volume.update_xaxes(title_text="Date", row=3, col=1)
    return (fig_volume)
   



@app.callback(
    Output("time_series_chart", "figure"), 
    Input("ticker", "value"),
    Input("ticker_horizontal", "value"),
    Input('upload_data', 'contents'),
    State('upload_data', 'filename'),
    State('upload_data', 'last_modified')
    )
def display_time_series(ticker,ticker_horizontal,list_of_contents,list_of_names, list_of_dates):
    fig = cyclotron_information.plotting_stadistics(ticker,ticker_horizontal)
    return fig
 

# CUMULATIVE PLOTS 


@app.callback(
    Output("time-series-chart4", "figure"), 
    Input("ticker", "value"),
    Input("time_series_chart", "figure"),
    )
def display_total_charge(ticker,chart): 
    text_to_plot = ["Total Source [Ah]","Total Target " + str(cyclotron_information.physical_targets[0]) +  " [mAh]","Total Target "+ str(cyclotron_information.physical_targets[1]) + " [mAh]"]
    values_to_plot = [np.array(cyclotron_information.df_summary["CUMULATIVE_SOURCE"].astype(float))[0],np.array(cyclotron_information.df_summary["CUMULATIVE_TARGET_1"].astype(float))[0],
    np.array(cyclotron_information.df_summary["CUMULATIVE_TARGET_2"].astype(float))[0]]
    range_values = [[[-1,50],[50,70],[110,120],[110,120]],[[-1,7000],[7000,11000],[11000,12000],[11000,12000]],[[-1,7000],[7000,11000],[11000,12000],[11000,12000]]]
    y_position = [[0.7, 0.9],[0.4, 0.6],[0.08, 0.25]]     
    fig_status = go.Figure()
    fig_status = general_status_plot(fig_status,values_to_plot,range_values,y_position,text_to_plot)
    fig_status.update_layout(title="Source & Targets")
    return fig_status

def return_fig(text_to_plot,values_to_plot,range_values):
    y_position = [[0.7, 0.9],[0.4, 0.6],[0.08, 0.25]]     
    fig_status = go.Figure()
    fig_status = general_status_plot(fig_status,values_to_plot,range_values,y_position,text_to_plot)
    return fig_status

@app.callback(
    Output("foils_1_1_2_3", "figure"), 
    Input("ticker", "value"),
    Input("time_series_chart", "figure"),
    )
def display_foils_1_1_2_3(ticker,chart): 
    text_to_plot = ["Foil 1 [Ah]","Foil 2 [mAh]","Foil 3 [mAh]"]
    values_to_plot = [np.array(cyclotron_information.df_summary["CUMULATIVE_TARGET_1_FOIL_1"].astype(float))[0],np.array(cyclotron_information.df_summary["CUMULATIVE_TARGET_1_FOIL_2"].astype(float))[0],
    np.array(cyclotron_information.df_summary["CUMULATIVE_TARGET_1_FOIL_3"].astype(float))[0]]
    range_values = [[[-1,1900],[1900,2000],[2000,2700],[2000,2700]],[[-1,1900],[1900,2000],[2000,2700],[2000,2700]],[[-1,1900],[1900,2000],[2000,2700],[2000,2700]]]
    fig_status = return_fig(text_to_plot,values_to_plot,range_values)
    fig_status.update_layout(title="Target " + str(cyclotron_information.physical_targets[0]) + " (Foil 1 & Foil 2 & Foil 3)")
    return fig_status

@app.callback(
    Output("foils_1_4_5_6", "figure"), 
    Input("ticker", "value"),
    Input("time_series_chart", "figure"),
    )
def display_foils_1_4_5_6(ticker,chart): 
    text_to_plot = ["Foil 4 [Ah]","Foil 5 [mAh]","Foil 6 [mAh]"]
    values_to_plot = [np.array(cyclotron_information.df_summary["CUMULATIVE_TARGET_1_FOIL_4"].astype(float))[0],np.array(cyclotron_information.df_summary["CUMULATIVE_TARGET_1_FOIL_5"].astype(float))[0],
    np.array(cyclotron_information.df_summary["CUMULATIVE_TARGET_1_FOIL_6"].astype(float))[0]]
    range_values = [[[-1,1900],[1900,2000],[2000,2700],[2000,2700]],[[-1,1900],[1900,2000],[2000,2700],[2000,2700]],[[-1,1900],[1900,2000],[2000,2700],[2000,2700]]]  
    fig_status = return_fig(text_to_plot,values_to_plot,range_values)
    fig_status.update_layout(title="Target " + str(cyclotron_information.physical_targets[0]) + " (Foil 4 & Foil 5 & Foil 6)")
    return fig_status

@app.callback(
    Output("foils_2_1_2_3", "figure"), 
    Input("ticker", "value"),
    Input("time_series_chart", "figure"),
    )
def display_foils_2_1_2_3(ticker,chart): 
    text_to_plot = ["Foil 1 [Ah]","Foil 2 [mAh]","Foil 3 [mAh]"]
    values_to_plot = [np.array(cyclotron_information.df_summary["CUMULATIVE_TARGET_2_FOIL_1"].astype(float))[0],np.array(cyclotron_information.df_summary["CUMULATIVE_TARGET_2_FOIL_2"].astype(float))[0],
    np.array(cyclotron_information.df_summary["CUMULATIVE_TARGET_2_FOIL_3"].astype(float))[0]]
    range_values = [[[-1,1900],[1900,2000],[2000,2700],[2000,2700]],[[-1,1900],[1900,2000],[2000,2700],[2000,2700]],[[-1,1900],[1900,2000],[2000,2700],[2000,2700]]]    
    fig_status = return_fig(text_to_plot,values_to_plot,range_values)
    fig_status.update_layout(title="Target " + str(cyclotron_information.physical_targets[1])  + " (Foil 1 & Foil 2 & Foil 3)")
    return fig_status

@app.callback(
    Output("foils_2_4_5_6", "figure"), 
    Input("ticker", "value"),
    Input("time_series_chart", "figure"),
    )
def display_foils_2_4_5_6(ticker,chart): 
    text_to_plot = ["Foil 4 [Ah]","Foil 5 [mAh]","Foil 6 [mAh]"]
    values_to_plot = [np.array(cyclotron_information.df_summary["CUMULATIVE_TARGET_2_FOIL_4"].astype(float))[0],np.array(cyclotron_information.df_summary["CUMULATIVE_TARGET_2_FOIL_5"].astype(float))[0],
    np.array(cyclotron_information.df_summary["CUMULATIVE_TARGET_2_FOIL_6"].astype(float))[0]]
    range_values = [[[-1,1900],[1900,2000],[2000,2600],[2000,2600]],[[-1,1900],[1900,2000],[2000,2600],[2000,2600]],[[-1,1900],[1900,2000],[2000,2600],[2000,2600]]]
    fig_status = return_fig(text_to_plot,values_to_plot,range_values)
    fig_status.update_layout(title="Target " + str(cyclotron_information.physical_targets[1])  + " (Foil 4 & Foil 5 & Foil 6)")
    return fig_status

@app.callback(
    Output("target_collimators_1", "figure"), 
    Input("ticker", "value"),
    Input("time_series_chart", "figure"),
    Input('upload_data', 'filename')
    )
def display_target_collimators_1(ticker,chart,list_of_names): 
    text_to_plot = ["Target [mAh]","Collimator upper [mAh]","Collimator lower [mAh]"]
    values_to_plot = [np.array(cyclotron_information.df_summary["CUMULATIVE_TARGET_1"].astype(float))[0],np.array(cyclotron_information.df_summary["CUMULATIVE_CURRENT_COLL_R_1"].astype(float))[0],
    np.array(cyclotron_information.df_summary["CUMULATIVE_CURRENT_COLL_L_1"].astype(float))[0]]
    range_values = [[[-1,7000],[7000,11000],[11000,12000],[11000,12000]],[[-1,100],[100,1500],[1500,2000],[1500,2000]],[[-1,1000],[1000,1500],[1500,2000],[1500,2000]]]
    fig_status = return_fig(text_to_plot,values_to_plot,range_values)
    fig_status.update_layout(title="Target & Collimators " + str(cyclotron_information.physical_targets[0]))
    return fig_status

@app.callback(
    Output("target_collimators_2", "figure"), 
    Input("ticker", "value"),
    Input("time_series_chart", "figure"),
    )
def display_target_collimators_1(ticker,chart): 
    text_to_plot = ["Target [mAh]","Collimator upper [mAh]","Collimator lower [mAh]"]
    values_to_plot = [np.array(cyclotron_information.df_summary["CUMULATIVE_TARGET_2"].astype(float))[0],np.array(cyclotron_information.df_summary["CUMULATIVE_CURRENT_COLL_R_2"].astype(float))[0],
    np.array(cyclotron_information.df_summary["CUMULATIVE_CURRENT_COLL_L_2"].astype(float))[0]]
    range_values = [[[-1,7000],[7000,11000],[11000,12000],[11000,12000]],[[-1,100],[100,1500],[1500,2000],[1500,2000]],[[-1,1000],[1000,1500],[1500,2000],[1500,2000]]]
    fig_status = return_fig(text_to_plot,values_to_plot,range_values)
    fig_status.update_layout(title="Target & Collimators " + str(cyclotron_information.physical_targets[1]))
    return fig_status

  
@app.callback(Output('output_data', 'children'),
              Input('upload_data', 'contents'),
              State('upload_data', 'filename'),
              State('upload_data', 'last_modified'))
def update_output(list_of_contents,list_of_names, list_of_dates):
    #columns_names.initial_df(cyclotron_information)
    cyclotron_information.__init__()
    target_1.__init__(computing_charge_df_alt.df_information)
    target_2.__init__(computing_charge_df_alt.df_information)
    if list_of_contents is not None:
        additional_functions.getting_information(cyclotron_information,target_1,target_2,list_of_contents, list_of_names, list_of_dates)
 

@app.callback(Output('output_data_folder', 'children'),
              Input('upload_data_file', 'contents'),
              State('upload_data_file', 'filename'),
              State('upload_data_file', 'last_modified'))
def update_output(list_of_contents,list_of_names, list_of_dates):
    #cyclotron_information = cyclotron()
    #columns_names.initial_df(cyclotron_information)  
    print (list_of_names)
    print (list_of_dates)
    if list_of_contents is not None:
        additional_functions.parse_contents(cyclotron_information,list_of_contents[0],list_of_names[0], list_of_dates[0])
        print ("CYCLOTRON INFORMATION")
        print (cyclotron_information.file_df)   
    #return (cyclotron_information)
        #target_1.
        #df_information = pd.DataFrame(columns=["DATE","FILE","FOIL","TARGET","CURRENT_SOURCE","CURRENT_FOIL","CURRENT_COLL_L","CURRENT_TARGET","CURRENT_COLL_R"])
        #additional_functions.getting_information(cyclotron_information,target_1,target_2,list_of_contents, list_of_names, list_of_dates)

        
def update_point(trace, points, selector):
    print ("ENTERING HEREEE")
    c = list(scatter.marker.color)
    s = list(scatter.marker.size)
    for i in points.point_inds:
        c[i] = '#bae2be'
        s[i] = 20
        with f.batch_update():
            scatter.marker.color = c
            scatter.marker.size = s


app.run_server(debug=True)