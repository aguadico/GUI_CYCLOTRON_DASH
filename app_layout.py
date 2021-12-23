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
import dash_table as dt
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
import glob
import flask
import base64
from collections import OrderedDict



data = OrderedDict(
    [
        ("Subsystem", ["Ion Source", "Vacuum", "RF", "Magnet", "Beam", "Target"]),
        ("Overall", ["OK", "OK", "Warning", "OK", "Danger", "Danger"]),
        ("Value", [3, -20, 3.512, 4, 10423, -441.2]),
        ("Units", ["mA/uA", r"mbar", "kW", "%", "mA @ foil", "psi"]),
        
    ]
)
#df = pd.DataFrame(data)
values = [["Ion Source","Parameter","OK",0,0,0,0,0,0,"mA/uA"]]
df = pd.DataFrame(values,columns=["Subsystem","Parameter","Overall","Value","Deviation","Max","Min","Reference min","Reference max","Unit"])
columns = ["CHOOSE","SOURCE","MAGNET","BEAM","VACUUM","RF","RF_STABILITY","TARGET"]
columns_logfile = ["CHOOSE","SOURCE","MAGNET","BEAM","VACUUM","RF","TARGET"]
columns_horizontal = ["DATE","FILE"]
columns_layers = ["REMOVE REFERENCE VALUES","ADD REFERENCE VALUES"]

def b64_image(image_filename):
    with open(image_filename, 'rb') as f:
        image = f.read()
    return 'data:image/png;base64,' + base64.b64encode(image).decode('utf-8')


image_directory = '/Users/anagtv/GUI_CYCLOTRON_DASH/'
list_of_images = [os.path.basename(x) for x in glob.glob('{}*.png'.format(image_directory))]
static_image_route = '/static/'

print ("LIST OF IMAGES")
print (list_of_images[0])
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '20px',
    'fontWeight': 'bold',
    'borderRadius': '5px',
    'backgroundColor': '#497873',
    'font-family':"Arial"

}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#223A38',
    'color': 'white',
    'padding': '20px',
    'borderRadius': '5px',
    'font-family':"Arial",
    'fontWeight': 'bold',

}

tabs_styles = {
    'color': '#A0BBBC',   
    "margin-right": "10px",
    "margin-left": "10px",
}

font_styles_subtitles = {
    'color': 'black',
    'padding': '10px',
    'fontSize': '20px',
    'font-family':"Arial",
    'marginTop': '20px',
}

font_styles = {
    'color': 'black',
    'padding': '10px',
    'fontSize': '18px',
    'font-family':"Arial",
    "margin-left": "20px",
}

font_styles_2 = {
    'color': 'black',
    'padding': '30px',
    'fontSize': '18px',
    'font-family':"Arial"
}

font_styles_title = {
    'color': "#223A38",
    'marginTop': '50px',
    "margin-left": "40px",
    #'margin':'30px',
    'fontWeight': 'bold',
    'fontSize': '25px',
    'font-family':"Arial",
}

font_styles_text = {
    'padding': '10px',

}


tab1 = html.Div([
    dbc.Card(
        dbc.CardBody([
        #dbc.Row([html.Label('Cyclotron Analyitics',style=font_styles_title)], align='center'),
        #dbc.Row([]),
        dbc.Row([
                dbc.Col([
                dbc.Row([
                    dbc.Col([html.Img(
                src=b64_image('beta_pharma_logo.png'),
                style={
                'maxWidth': '300px',
                'maxHeight': '100px',
                'marginLeft': 'auto',
                'marginRight': 'auto',
                'margin': '15px',})]
                ,width=3),
                    dbc.Col([dcc.Markdown('''
Welcome to the **Cyclotron Analytics Dashboard!**
''')],style=font_styles_title)]),
                dbc.Row([dcc.Markdown('''
Here you can analyze the cyclotron stability based on detailed log file analysis.

The dashboard contains three tabs: **Statistical Values**, **Individual Logfile** and **Component Lifetime**. 

**Statistical values**: this tab shows the average and standard deviation of the indicators associated with the selected subsystem. 

The cyclotron is divided into the following subsystems: *Ion source*, *Vacuum*, *Magnet*, *RF and RF stability*, *Beam* and *Target*.
''')],style=font_styles),
                ],width=7),
                dbc.Col([
                dbc.Row([
                dbc.Col([html.Label('Cyclotron Inputs',style=font_styles_subtitles)],width=8),
                ]),
                dbc.Row([
                dbc.Col([dcc.Upload(id='upload_data',children=html.Div([html.A('Select data to analyze'),
                dcc.Loading(
                    id="loading-1",
                    color= "#223A38",
                    children=[html.Div([html.Div(id="loading_output_1")])],
                    type="default",style={'padding': '10px'}),]),style={
                    'width': '500px',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'solid',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px',
                    'color': '#223A38',
                    'backgroundColor':'#FFFFFF',
                    'font-family':"Arial",
                    'fontSize': '18px',
                },multiple=True)],width=8.5),
                #dbc.Col([
                #    dcc.Graph(figure={'layout': go.Layout(xaxis =  {'showgrid': False}, yaxis = {'showgrid': False},width=100,height=50)},
        #style={'backgroundColor':'rgba(0,0,0,0)'},
        #id='logo')],width=1),
                html.Br()
                ]),
                #dbc.Col([
                html.Br(),
                dbc.Row([
                html.Br(),
                dbc.Col([html.Label('Select a subsystem',style=font_styles_subtitles)],width=4),
                dbc.Col([html.Label('Select horizontal axis',style=font_styles_subtitles)],width=4),
                dbc.Col([html.Label('Enable/disable limits',style=font_styles_subtitles)],width=4)
                ]),
                dbc.Row([
                dbc.Col([dcc.Dropdown(id="ticker",options=[{"label": x, "value": x}  for x in columns],value=columns[0], clearable=False)],width=4),
                dbc.Col([dcc.Dropdown(id="ticker_horizontal",options=[{"label": x, "value": x}  for x in columns_horizontal],value=columns_horizontal[0],clearable=False)],width=4),
                dbc.Col([dcc.Checklist(options=[{'label': 'Add references ', 'value': 'ADRF'}],
                        value=[],labelStyle={'display':'inline-block','color':"#223A38",'fontSize': '18px','font-family':"Arial"},id='ticker_layer',inputStyle=tabs_styles)],width=4),
                ])
                #], width=12)
        ],style={'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'margin': '10px',
                    'color': '#223A38',
                    'margin': '10px',
                }),
        ],style={'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'margin': '10px',
                    'color': '#223A38',
                    'margin': '10px',
                    'backgroundColor': '#A0BBBC',
                }),  
        dbc.Row([dbc.Col([
        dbc.Row([dcc.Markdown('''
**Statistical values**''')],style=font_styles),
        dcc.Graph(figure={'layout': go.Layout(xaxis =  {'showgrid': False}, yaxis = {'showgrid': False})},
        style={'backgroundColor':'rgba(0,0,0,0)'},
        id='time_series_chart')], width=12)], align='center',style={'borderWidth': '1px',
                    'borderStyle': 'solid',
                    'borderRadius': '5px',
                    'margin': '10px',
                    'color': '#223A38',
                    'margin': '10px',
                }),
        ]), color = '#f8fff4')])


tab2 =  html.Div([
    dbc.Card(
        dbc.CardBody([
        #dbc.Row([html.Label('Cyclotron Analyitics',style=font_styles_title)], align='center'),
        #dbc.Row([]),
        dbc.Row([
                dbc.Col([
                dbc.Row([
                    dbc.Col([html.Img(
                src=b64_image('beta_pharma_logo.png'),
                style={
                'maxWidth': '300px',
                'maxHeight': '100px',
                'marginLeft': 'auto',
                'marginRight': 'auto',
                'margin': '15px',})]
                ,width=3),
                    dbc.Col([dcc.Markdown('''
Welcome to the **Cyclotron Analytics Dashboard!**
''')],style=font_styles_title)]),
                dbc.Row([dcc.Markdown('''
Here you can analyze the cyclotron stability based on detailed log file analysis.

The dashboard contains three tabs: **Statistical Values**, **Individual Logfile** and **Component Lifetime**. 

**Individual Logfile**: this tab shows the time evolution of the values recorded by the different cyclotron subsystems. 

The cyclotron is divided into the following subsystems: *Ion source*, *Vacuum*, *Magnet*, *RF and RF stability*, *Beam* and *Target*.
''')],style=font_styles),
                ],width=7),
                dbc.Col([
                dbc.Row([
                dbc.Col([html.Label('Cyclotron Inputs',style=font_styles_subtitles)],width=8),
                ]),
                dbc.Row([
                dbc.Col([dcc.Upload(id='upload_data_file',children=html.Div([html.A('Select an individual logfile to analyze'),
                dcc.Loading(
                    id="loading-2",
                    color="#223A38", 
                    children=[html.Div([html.Div(id="loading-output-2")])],
                    type="default",style={'padding':'10px'}),]),style={
                    'width': '500px',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'solid',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px',
                    'color': '#223A38',
                    'backgroundColor':'#FFFFFF',
                    'font-family':"Arial",
                    'fontSize': '18px',
                },multiple=True)],width=8.5),
                html.Br()
                ]),
                #dbc.Col([
                html.Br(),
                html.Div(id="loading_message"),
                dbc.Row([
                html.Br(),
                dbc.Col([html.Label('Select a subsystem',style=font_styles_subtitles)],width=4),
                #dbc.Col([html.Label('Select horizontal axis',style=font_styles_subtitles)],width=4),
                dbc.Col([html.Label('Enable/disable limits',style=font_styles_subtitles)],width=4)
                ]),
                dbc.Row([
                dbc.Col([dcc.Dropdown(id="ticker_2",options=[{"label": x, "value": x}  for x in columns_logfile],value=columns_logfile[0], clearable=False)],width=4),
                #dbc.Col([dcc.Dropdown(id="ticker_horizontal_2",options=[{"label": x, "value": x}  for x in columns_horizontal],value=columns_horizontal[0],clearable=False)],width=4),
                dbc.Col([dcc.Checklist(options=[{'label': 'Add references ', 'value': 'ADRF'}],
                        value=[],labelStyle={'display':'inline-block','color':"#223A38",'fontSize': '18px','font-family':"Arial"},id='ticker_layer_file',inputStyle=tabs_styles)],width=4)
                ])
                #], width=12)
        ],style={'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'margin': '10px',
                    'color': '#223A38',
                    'margin': '10px',
                }),
        ],style={'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'margin': '10px',
                    'color': '#223A38',
                    'margin': '10px',
                    'backgroundColor': '#A0BBBC',
                }),  
        dbc.Row([dbc.Col([
        dbc.Row([dcc.Markdown('''
**Individual log analysis**''')],style=font_styles),
        dcc.Graph(figure={'layout': go.Layout(xaxis =  {'showgrid': False}, yaxis = {'showgrid': False})},
        style={'backgroundColor':'rgba(0,0,0,0)'},
        id='time_series_chart_volume')], width=12)], align='center',style={'borderWidth': '1px',
                    'borderStyle': 'solid',
                    'borderRadius': '5px',
                    'margin': '10px',
                    'color': '#223A38',
                    'margin': '10px',
                }),
        ]), color = '#f8fff6')])

tab3 =  html.Div([
    dbc.Card(
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                dbc.Row([
                    dbc.Col([html.Img(
                src=b64_image('beta_pharma_logo.png'),
                style={
                'maxWidth': '300px',
                'maxHeight': '100px',
                'marginLeft': 'auto',
                'marginRight': 'auto',
                'margin': '15px',})]
                ,width=3),
                    dbc.Col([dcc.Markdown('''
Welcome to the **Cyclotron Analytics Dashboard!**.
''')],style=font_styles_title)]),
                dbc.Row([dcc.Markdown('''
Here you can analyze the cyclotron stability based on detailed log file analysis.

The dashboard contains three tabs: **Statistical Values**, **Individual Logfile** and **Component Lifetime**. 

**Component Lifetime**: this tab shows cumulative charge @ different locations. 

Locations: *Ion source*, *Targets*, *Collimators* and *Foils*.
''')],style=font_styles),
                ],width=7),
                dbc.Col([
                html.Br(),
                html.Br(),
                dbc.Row([
                dbc.Col([html.Label('Cyclotron Inputs',style=font_styles_subtitles)],width=8),
                ]),
                dbc.Row([
                dbc.Col([html.Label('Select the data in the "Statistic values" tab. Once the logfiles have been analyzed, cumulative charge will be displayed here')],width=8.5,style=font_styles),
                html.Br()
                ]),
                #dbc.Col([
                html.Br(),
                #], width=12)
        ],style={'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'margin': '10px',
                    'color': '#223A38',
                    'margin': '10px',
                }),
        ],style={'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'margin': '10px',
                    'color': '#223A38',
                    'margin': '10px',
                    'backgroundColor': '#A0BBBC',
                }),  
            html.Br(),
            dbc.Row([
                dbc.Row([dcc.Markdown('''
**General cyclotron status**''')],style=font_styles_2),
                dbc.Col([
                    dt.DataTable(
    id='table_status',
    columns=[
        {'id': c, 'name': c}
        for c in df.columns
    ],
    style_as_list_view=True,
    data=df.to_dict('records'),
    filter_action="native",
    sort_action="native",
    style_cell={'textAlign': 'center','margin': '10px'},

    style_data =  {'fontSize': '25px',
            'font-family':"Arial",
            },
    style_header={'backgroundColor': '#223A38','fontSize': '25px',
            'font-family':"Arial"},
    style_data_conditional=[
        {
            'if': {
                'column_id': 'Region',
            },
            'backgroundColor': 'dodgerblue',
            'color': 'white'
        },
        {
            'if': {
                'filter_query': '{Overall} = "Danger"',
                'column_id': 'Overall'
            },
            'backgroundColor': 'tomato',
            'color': 'white',

        },
        {
            'if': {
                'filter_query': '{Overall} = "OK"',
                'column_id': 'Overall'
            },
            'backgroundColor': 'green',
            'color': 'white'
        },
        {
            'if': {
                'filter_query': '{Overall} = "Warning"',
                'column_id': 'Overall'
            },
            'backgroundColor': 'orange',
            'color': 'white'
        }],
    style_header_conditional=[{
        'if': {'column_editable': False},
        'backgroundColor': '#A0BBBC',
        'color': 'white'
    }],
    )
                ], width=12),
            ], align='center',style={'borderWidth': '1px',
                    'borderStyle': 'solid',
                    'borderRadius': '5px',
                    'margin': '10px',
                    'color': '#223A38',
                    'margin': '10px',
                }),
            html.Br(),
            dbc.Row([
                dbc.Row([dcc.Markdown('''
**Source & Target**''')],style=font_styles_2),
                dbc.Col([
                    dcc.Graph(id='time-series-chart4')
                ], width=12),
            ], align='center',style={'borderWidth': '1px',
                    'borderStyle': 'solid',
                    'borderRadius': '5px',
                    'margin': '10px',
                    'color': '#223A38',
                    'margin': '10px',
                }), 
            html.Br(), 
            html.Br(),
            dbc.Col([
                dbc.Row([dcc.Markdown('''
**Target & Collimators**''')],style=font_styles),
                dbc.Row([dbc.Col([
                    dcc.Graph(id='target_collimators_1')
                ], width=6),
                dbc.Col([
                    dcc.Graph(id='target_collimators_2') 
                ], width=6)]
            )], align='center',style={'borderWidth': '1px',
                    'borderStyle': 'solid',
                    'borderRadius': '5px',
                    'margin': '10px',
                    'color': '#223A38',
                    'margin': '10px',
                }),
            html.Br(),  
             html.Br(),
            dbc.Col([dbc.Row([dcc.Markdown('''
**Foils**''')],style=font_styles),
                dbc.Row([dbc.Col([
                    dcc.Graph(id='foils_1_4_5_6')
                ], width=6,style={"height": "120vh"}),
                dbc.Col([
                    dcc.Graph(id='foils_2_4_5_6') 
                ], width=6,style={"height": "120vh"})])
            ], align='center',style={'borderWidth': '1px',
                    'borderStyle': 'solid',
                    'borderRadius': '5px',
                    'margin': '10px',
                    'color': '#223A38',
                    'margin': '10px',
                })   
        ]), color = '#f8fff6'
    )
])



layout = dcc.Tabs([
        dcc.Tab(label='Statistical values', children=[tab1],style=tab_style, selected_style=tab_selected_style,id="tab_1"),
        dcc.Tab(label='Individual file', children=[tab2],style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Component lifetime', children=[tab3],style=tab_style, selected_style=tab_selected_style),
        ],id="tabs-with-classes", style=tabs_styles)

