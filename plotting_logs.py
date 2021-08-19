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

COLORS = ["#A0BBBC","#223A38","#497873"]
def daily_report(ticker,ticker_layer,tabs,input_file,cyclotron_information):     
    fig_logfile = go.FigureWidget(make_subplots(rows=3, cols=1,shared_xaxes=False,
                    vertical_spacing=0.1))
    fig_logfile.update_layout(height=1500)
    fig_logfile.update_layout(showlegend=False)
    fig_logfile.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
    fig_logfile.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
    if (ticker == "CHOOSE"):
        x_values = [0]
        y_values = [np.array(0),np.array(0),np.array(0)]
        y_values_error = [np.array(0),np.array(0),np.array(0)]
        names = ["","",""]
        units = ["","",""]
        for i in range(3): 
            fig_logfile = additional_functions.plotting_simple_no_error(fig_logfile,x_values,y_values[i],units[i],i+1,1,COLORS[0],"",10)
    else:
       if ticker == "SOURCE":
          fig_logfile = additional_functions.plotting_simple_no_error(fig_logfile,cyclotron_information.file_df.Time,cyclotron_information.file_df.Arc_I.astype(float),"Arc I [mA]",1,1,COLORS[0],"Source current",10)
          fig_logfile = additional_functions.plotting_simple_no_error(fig_logfile,cyclotron_information.file_df.Time,cyclotron_information.file_df.Target_I.astype(float),"Target I [\u03bcA]",2,1,COLORS[0],"Target current",10)
          fig_logfile = additional_functions.plotting_simple_no_error(fig_logfile,cyclotron_information.file_df.Time,cyclotron_information.file_df.Coll_l_I.astype(float)+cyclotron_information.file_df.Coll_r_I.astype(float),"Collimators [\u03bcA]",3,1,COLORS[0],"Collimators current",10)
          row_number = 3
          reference_value = [[[600,700,800]],[[120,130,140]],[[20,25,35]]]
       if ticker == "BEAM":
          fig_logfile = go.FigureWidget(make_subplots(rows=5, cols=1,shared_xaxes=False,
                    vertical_spacing=0.1))
          fig_logfile = additional_functions.plotting_simple_no_error(fig_logfile,cyclotron_information.file_df.Time,cyclotron_information.file_df.Arc_I.astype(float),"Arc I [mA]",1,1,COLORS[0],"Source current",10)
          fig_logfile = additional_functions.plotting_simple_no_error(fig_logfile,cyclotron_information.file_df.Time,cyclotron_information.file_df.Target_I.astype(float),"Target I [\u03bcA]",2,1,COLORS[0],"Target current",10)
          fig_logfile = additional_functions.plotting_simple_no_error(fig_logfile,cyclotron_information.file_df.Time,cyclotron_information.file_df.Coll_l_I.astype(float)+cyclotron_information.file_df.Coll_r_I.astype(float),"Collimators [\u03bcA]",3,1,COLORS[0],"Collimators current",10)
          fig_logfile = additional_functions.plotting_simple_no_error(fig_logfile,cyclotron_information.file_df.Time,cyclotron_information.file_df.Target_I.astype(float)/cyclotron_information.file_df.Foil_I.astype(float)*100,"I target/I foil [%]",4,1,COLORS[0],"I target/I foil [%]",10)
          losses = (cyclotron_information.file_df.Target_I.astype(float)+cyclotron_information.file_df.Coll_l_I.astype(float)+cyclotron_information.file_df.Coll_r_I.astype(float))/cyclotron_information.file_df.Foil_I.astype(float)
          fig_logfile = additional_functions.plotting_simple_no_error(fig_logfile,cyclotron_information.file_df.Time,(1-losses)*100,"Extraction losses [%]",5,1,COLORS[0],"Extraction losses [%]",10)
          row_number = 5
          reference_value = [[[600,700,800]],[[110,120,130]],[[20,25,35]],[[95,85,70]],[[-0.5,-1,-2],[0.5,1,2]]]
       elif ticker == "VACUUM": 
          fig_logfile = additional_functions.plotting_simple_no_error(fig_logfile,cyclotron_information.file_df.Time,cyclotron_information.file_df.Arc_I.astype(float),"Arc I [mA]",1,1,COLORS[0],"Source current",10)
          fig_logfile = additional_functions.plotting_simple_no_error(fig_logfile,cyclotron_information.file_df.Time,cyclotron_information.file_df.Vacuum_P.astype(float)*1e5,"Vacuum Pressure [1e-5 mbar]",2,1,COLORS[0],"Vacuum",10)
          fig_logfile = additional_functions.plotting_simple_no_error(fig_logfile,cyclotron_information.file_df.Time,cyclotron_information.file_df.Gas_flow.astype(float),"Gas flow [sccm]",3,1,COLORS[0],"Gas flow",10)
          row_number = 5
          reference_value = [[[600,700,800]],[[1.6,1.7,1.8]],[]]
       elif ((ticker == "RF") or (ticker == "RF_STABILITY")): 
          fig_logfile = additional_functions.plotting_simple_no_error(fig_logfile,cyclotron_information.file_df.Time,cyclotron_information.file_df.Dee_1_kV.astype(float),"RF Voltage [kV]",1,1,COLORS[0],"Dee 1",10)
          fig_logfile = additional_functions.plotting_simple_no_error(fig_logfile,cyclotron_information.file_df.Time,cyclotron_information.file_df.Dee_2_kV.astype(float),"RF Voltage [kV]",1,1,COLORS[1],"Dee 2",10)
          fig_logfile = additional_functions.plotting_simple_no_error(fig_logfile,cyclotron_information.file_df.Time,cyclotron_information.file_df.Flap1_pos.astype(float),"Flap [%]",2,1,COLORS[0],"Flap 1",10)
          fig_logfile = additional_functions.plotting_simple_no_error(fig_logfile,cyclotron_information.file_df.Time,cyclotron_information.file_df.Flap2_pos.astype(float),"Flap [%]",2,1,COLORS[1],"Flap 2",10)
          fig_logfile = additional_functions.plotting_simple_no_error(fig_logfile,cyclotron_information.file_df.Time,cyclotron_information.file_df.RF_fwd_W.astype(float),"RF Power [kW]",3,1,COLORS[0],"Fwd",10)
          fig_logfile = additional_functions.plotting_simple_no_error(fig_logfile,cyclotron_information.file_df.Time,cyclotron_information.file_df.RF_refl_W.astype(float),"RF Power [kW]",3,1,COLORS[1], "Rfl",10)
          row_number = 3
          reference_value = [[[]],[[10,5,0]],[[13,14,15],[0.5,0.6,0.7]]]
       elif ticker == "TARGET":
          fig_logfile = additional_functions.plotting_simple_no_error(fig_logfile,cyclotron_information.file_df.Time,cyclotron_information.file_df.Target_I.astype(float),"Target I [\u03bcA]",1,1,COLORS[0],"Target current",10)
          fig_logfile = additional_functions.plotting_simple_no_error(fig_logfile,cyclotron_information.file_df.Time,cyclotron_information.file_df.Target_P.astype(float),"Pressure [psi]",2,1,COLORS[0],"Target pressure",10)
          fig_logfile = additional_functions.plotting_simple_no_error(fig_logfile,cyclotron_information.file_df.Time,cyclotron_information.file_df.Extr_pos.astype(float),"Extraction position [%]",3,1,COLORS[0],"Extraction",10)
          row_number = 3
          reference_value = [[[110,120,130]],[[450,460,480]],[]]
       elif ticker == "MAGNET":
           fig_logfile = go.FigureWidget(make_subplots(rows=2, cols=1,shared_xaxes=False,
                    vertical_spacing=0.1))
           fig_logfile.update_layout(height=1500)
           fig_logfile.update_xaxes(title_text="Magnet I [A]", row=2, col=1)
           cyclotron_information.df_isochronism = getting_subsystems_data_alt.get_isochronism(cyclotron_information.file_df)
           fig_logfile = additional_functions.plotting_simple_no_error(fig_logfile,cyclotron_information.file_df.Time,cyclotron_information.file_df.Magnet_I.astype(float),"Magnet I [A]",1,1,COLORS[0],"Magnet current",10)
           fig_logfile = additional_functions.plotting_simple_no_error(fig_logfile,cyclotron_information.df_isochronism.Magnet_I.iloc[:-1],cyclotron_information.df_isochronism.Foil_I.iloc[:-1],"I [\u03bcA]",2,1,COLORS[0],"Foil current",12)
           fig_logfile = additional_functions.plotting_simple_no_error(fig_logfile,cyclotron_information.df_isochronism.Magnet_I.iloc[:-1],cyclotron_information.df_isochronism.Target_I.iloc[:-1],"I [\u03bcA]",2,1,COLORS[1],"Target current",12)
           fig_logfile = additional_functions.plotting_simple_no_error(fig_logfile,cyclotron_information.df_isochronism.Magnet_I.iloc[:-1],cyclotron_information.df_isochronism.Coll_l_I.iloc[:-1]+cyclotron_information.df_isochronism.Coll_r_I.iloc[:-1],"I [\u03bcA]",2,1,COLORS[2],"Collimators current",12)
           row_number = 1
           fig_logfile.add_vline(x=cyclotron_information.df_isochronism.Magnet_I.iloc[-1],line_width=4, line_dash="dot",line_color="green",annotation_text="Isochronism"
            ,row=2, col=1)
           reference_value = [[[]],[[]]]
       fig_logfile.update_xaxes(title_text="Time [HH:MM:SS]", row=row_number, col=1)
       fig_logfile.update_layout(showlegend=False)  
       fig_logfile.update_layout(title="Log number " + str(cyclotron_information.file_number) + " Date " + str(cyclotron_information.date_stamp),
        font=dict(size=16,color="#223A38"),font_family="Arial",margin=dict(t=60)) 
       if ticker_layer == ["ADRF"]:
           for i in range(len(reference_value)):
                for j in range(len(reference_value[i])):
                    if len(reference_value[i][j]) > 0:
                        fig_logfile.add_hrect(y0=reference_value[i][j][1], y1=reference_value[i][j][2], line_width=0, fillcolor="red", opacity=0.05,row=i+1, col=1)
                        fig_logfile.add_hrect(y0=reference_value[i][j][0], y1=reference_value[i][j][1], line_width=0, fillcolor="orange", opacity=0.05,row=i+1, col=1)
                        fig_logfile.add_hline(y=reference_value[i][j][1], line_dash="dot",line_color="red",annotation_text="High risk area",
                             annotation_position="bottom right",row=i+1, col=1)
                        fig_logfile.add_hline(y=reference_value[i][j][0], line_dash="dot",line_color="orange",annotation_text="Medium risk area",
                             annotation_position="bottom right",row=i+1, col=1)
    fig_logfile.update_layout(paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='#FFFFFF',font=dict(size=16,color="black"),font_family="Arial",margin=dict(t=35))  
    fig_logfile.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
    fig_logfile.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
    return (fig_logfile)
   