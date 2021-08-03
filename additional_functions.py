import numpy as np
import pandas as pd
import base64
import io
import saving_trends_alt
import managing_files_alt
import computing_charge_df_alt
import ion_source_studies
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots
import plotly.graph_objects as go


def plotting_simple(fig,x_values,y_values,y_values_error,units,position_x,position_y,colori):
    fig.add_trace(go.Scatter(x=x_values, y=y_values,mode='markers',                                                         
    marker=go.Marker(color=colori),
        error_y=dict(
            type='data',
            symmetric=True,
            array=y_values_error,
            )),row=position_x, col=position_y)
    fig.update_yaxes(title_text=units, row=position_x, col=position_y)
    return fig

def plotting_simple_no_error(fig,x_values,y_values,units,position_x,position_y,colori):
    fig.add_trace(go.Scatter(x=x_values, y=y_values,mode='markers',                                                         
    marker=go.Marker(color=colori)),row=position_x, col=position_y)
    fig.update_yaxes(title_text=units, row=position_x, col=position_y)
    return fig

#def plotting_three_variables(fig,x_values,y_values,y_values_error,names,units):
#    fig = plotting_simple(fig,x_values,y_values[0],y_values_error[0],names[0],units[0],1,1)
#    fig.add_trace(go.Scatter(x=x_values, y=y_values[1],mode='markers',                                                         
#    marker=go.Marker(color=colori), error_y=dict(
#            type='data',
#            symmetric=True,
#            array=y_values_error[1],
#            ),name=names[1]),row=2, col=1)
#    fig.add_trace(go.Scatter(x=x_values, y=y_values[2],mode='markers',
#        error_y=dict(
#            type='data',
#            symmetric=True,
#            array=y_values_error[2],
#            ),name=names[2]),row=3, col=1)
#    
#    fig.update_yaxes(title_text=units[2], row=3, col=1)
#    return fig

def getting_information(cyclotron_information,target_1,target_2,list_of_contents, list_of_names, list_of_dates):
    for c, n, d in zip(list_of_contents, list_of_names, list_of_dates): 
        #all_names.append(str(n[:-4]))
        parse_contents(cyclotron_information,c, n, d) 
        cyclotron_information.file_output()
        if float(cyclotron_information.target_number) in [1.0,2.0,3.0]: 
           print ("THIS TARGET")
           target_1.selecting_data_to_plot_reset(cyclotron_information)
        else:
           print ("OR THIS ONE")
           target_2.selecting_data_to_plot_reset(cyclotron_information)
    saving_trends_alt.getting_summary_final(cyclotron_information) 
    target_1.get_summation_per_period()
    target_2.get_summation_per_period()  
    cyclotron_information.source_performance = np.average(np.array(cyclotron_information.source_performance_total)[np.array(cyclotron_information.source_performance_total) > 0])         


def current_vaccum(X, a,b):
     x,y,z = X
     return a*(x+y) + b*z

def current(X, a,b):
     x,y,z = X
     return a*(x+y) 


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