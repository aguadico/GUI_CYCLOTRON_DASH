import numpy as np
import pandas as pd
import base64
import io
import saving_trends_alt
import managing_files_alt
import computing_charge_df_alt
#simport ion_source_studies
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import cyclotron_class
import tfs
import getting_subsystems_data_alt


RANGE_VALUES_CHARGE = {"TARGET_COLLIMATORS":[[[0,10],[10,12.5],[12.5,15]],[[0,300],[300,500],[500,700]],[[0,300],[300,500],[500,700]]],
"FOILS": [[[0,2000],[2000,2500],[2500,3000]]] * 6,
"SOURCE_TARGETS":[[[0,100],[100,125],[125,150]],[[0,10],[10,12.5],[12.5,15]],[[0,10],[10,12.5],[12.5,15]]]}
POSITION = {"TARGET_COLLIMATORS":[[0.7, 0.9],[0.4, 0.6],[0.08, 0.25]],"SOURCE_TARGETS":[[0.7, 0.9],[0.4, 0.6],[0.08, 0.25]],
"FOILS":[[0.8,0.9],[0.64,0.74],[0.48,0.58],[0.32, 0.42],[0.16, 0.26],[0.0, 0.1]]}


COLUMN_NAMES = ["Time","Arc_I","Arc_V","Gas_flow","Dee_1_kV",
    "Dee_2_kV","Magnet_I","Foil_I","Coll_l_I","Target_I","Coll_r_I",
    "Vacuum_P","Target_P","Delta_Dee_kV","Phase_load","Dee_ref_V",
    "Probe_I","He_cool_P","Flap1_pos","Flap2_pos","Step_pos",
    "Extr_pos","Balance","RF_fwd_W","RF_refl_W","Foil_No"]


def general_status_plot(fig_status,values,range_values,y_position):
    for i in range(len(values[1])):
        fig_status.add_trace(go.Indicator(
    mode = "number+gauge", value = values[1][i][0],
    domain = {'x': [0.25, 1], 'y': y_position[i]},
    title = {'text' :values[0][i]},
    gauge = {
        'shape': "bullet",
        'axis': {'range': [None, np.max(range_values[i])]},
        'steps': [
            {'range': range_values[i][2], 'color': "red"},
            {'range': range_values[i][0], 'color': "green"},
            {'range': range_values[i][1], 'color': "orange"},
            ],
        'bar': {'color': "#223A38"}
        }))
    return fig_status

def return_fig(fig_status,values,range_values,range_element):
    y_position = POSITION[range_element]    
    fig_status = general_status_plot(fig_status,values,range_values,y_position)
    #fig_status.update_layout(paper_bgcolor='rgba(0,0,0,0)',
    #        plot_bgcolor='#FFFFFF',font=dict(size=16,color="#223A38"),font_family="Arial",margin=dict(t=35))  
    return fig_status

def plotting_charge(cyclotron_information,values,settings):
    range_values = RANGE_VALUES_CHARGE[settings[1]]
    fig_status = go.Figure()
    fig_status = return_fig(fig_status,values,range_values,settings[1])
    fig_status.update_layout(height=settings[2]) 
    fig_status.update_layout(title=settings[0]  ,
    font=dict(size=16,color="#223A38"),font_family="Arial",margin=dict(t=100)) 
    return fig_status

def updating_figures(fig,values,settings):
    fig.update_yaxes(title_text=values, row=settings[0], col=settings[1])
    return fig 

def adding_limits(fig,settings):
    fill_colors = ["orange","red"]
    annotation_text = ["Medium risk area","High risk area"]
    for i in range(len(settings[5])):
        if len(settings[5][i]) > 0:
            for j in range(len(fill_colors)):
                fig.add_hrect(y0=settings[5][i][j], y1=settings[5][i][j+1], line_width=0, fillcolor=fill_colors[j], opacity=0.05,row=settings[0], col=settings[1])
                fig.add_hline(y=settings[5][i][j], line_dash="dot",line_color=fill_colors[j],annotation_text=annotation_text[j],
                        annotation_position="bottom right",row=settings[0], col=settings[1])

def plotting_simple_name(fig,values,settings):
    fig.add_trace(go.Scatter(x=values[0], y=values[1],name=settings[4],mode='markers',                                                         
    marker=go.Marker(dict(size=12,color=settings[2],line=dict(width=2,color=settings[3]))),
        error_y=dict(type='data',symmetric=True,array=values[2])),
    row=settings[0], col=settings[1])
    if settings[-1] == ["ADRF"]:
        fig = adding_limits(fig,settings)
    fig = updating_figures(fig,values[3],settings)
    return fig

def plotting_simple_no_error(fig,values,settings):
    fig.add_trace(go.Scatter(x=values[0], y=values[1],mode='markers',name=settings[3],                                                        
    marker=go.Marker(dict(size=settings[4],color=settings[2]))),row=settings[0], col=settings[1])
    fig = updating_figures(fig,values[2],settings)
    return fig

def get_summary_target(target_1,target_2):
    target_1.get_summation_per_period()
    target_2.get_summation_per_period()  
    df_target_1 = target_1.df_information_foil
    df_target_2 = target_2.df_information_foil
    return df_target_1,df_target_2

def complete_cyclotron_information(cyclotron_information,df_target_1,df_target_2):
    cyclotron_information.source_performance = np.average(np.array(cyclotron_information.source_performance_total)[np.array(cyclotron_information.source_performance_total) > 0])          
    cyclotron_information.get_average_std_summary_cummulative(df_target_1,df_target_2)
    cyclotron_information.physical_targets = [np.min(cyclotron_information.df_extraction.PHYSICAL_TARGET),np.max(cyclotron_information.df_extraction.PHYSICAL_TARGET)]

def getting_information(cyclotron_information,target_1,target_2,lists):
    for c, n, d in lists: 
        parse_contents(cyclotron_information,c, n, d) 
        max_current = np.max(cyclotron_information.file_df.Target_I.astype(float))    
        if (float(max_current) > 15):
            # STARTING GETTING SUBSYSTEMS PER FILE
            cyclotron_information.file_output()
            # SELECTING TARGET
            if float(cyclotron_information.target_number) in [1.0,2.0,3.0]: 
               target_1.selecting_data_to_plot_reset(cyclotron_information)
            else:
               target_2.selecting_data_to_plot_reset(cyclotron_information)
    # COMPUTING SUMMARY PER FILE
    df_target_1,df_target_2 = get_summary_target(target_1,target_2)
    saving_summaries(cyclotron_information,df_target_1,df_target_2)

def saving_summaries(cyclotron_information,df_target_1,df_target_2):
    saving_trends_alt.getting_summary_final(cyclotron_information) 
    complete_cyclotron_information(cyclotron_information,df_target_1,df_target_2)
    

def getting_lines(df):
    lines = []
    for i in range(len(df)):
        for line in df.loc[i]:
             parts = line.split()
             lines.append(
                np.array(parts))
    return lines

def getting_values(lines):
    all_values = []
    for j in range(len(COLUMN_NAMES)):
        values = []
        for i in list(range(2,len(np.array(lines)))):
            values.append(np.array(lines[i][j]))
        all_values.append(values)
    return all_values

def creating_df(cyclotron_information,all_values):
    cyclotron_information.file_df = pd.DataFrame(list(zip(all_values[0],all_values[1],all_values[2],all_values[3],all_values[4],
        all_values[5],all_values[6],all_values[7],all_values[8],all_values[9],all_values[10],all_values[11],
        all_values[12],all_values[13],all_values[14],all_values[15],all_values[16],all_values[17],all_values[18],
        all_values[19],all_values[20],all_values[21],all_values[22],all_values[23],all_values[24],all_values[25])),columns=COLUMN_NAMES)
    cyclotron_information.file_df["Collimators"] = cyclotron_information.file_df.Coll_l_I.astype(float)+cyclotron_information.file_df.Coll_r_I.astype(float)
    cyclotron_information.file_df["Losses"] = (1-(cyclotron_information.file_df.Target_I.astype(float)+cyclotron_information.file_df.Coll_l_I.astype(float)+cyclotron_information.file_df.Coll_r_I.astype(float))/cyclotron_information.file_df.Foil_I.astype(float))*100
    cyclotron_information.file_df["Relative_target"] = cyclotron_information.file_df.Target_I.astype(float)/cyclotron_information.file_df.Foil_I.astype(float)*100
    cyclotron_information.file_df["Vacuum_mbar"] = cyclotron_information.file_df.Vacuum_P.astype(float)*1e5

def filling_cyclotron_information(cyclotron_information,date,df,lines):
    cyclotron_information.date_stamp = str(date[0]) + "-" + str(date[1]) + "-" + str(date[2])
    cyclotron_information.name = lines[0][2]
    cyclotron_information.df_isochronism = getting_subsystems_data_alt.get_isochronism(cyclotron_information.file_df)
    cyclotron_information.target_number = (df.columns[0][9:10])
    cyclotron_information.file_number = (df.columns[0]).split()[6]

def get_value(df,position,leng):
    value = str((df.columns[0]).split()[position][leng[0]:leng[1]])
    return value 

def get_year_month_day(df,position,leng):
    date = []
    for i in range(3):
        date.append(get_value(df,position[i],leng[i]) )
    #year = 
    #month = str((df.columns[0]).split()[position[1]][leng[1][0]:leng[1][1]])
    #day = int((df.columns[0]).split()[position[2]][leng[2][0]:leng[2][1]])
    return date

def parse_contents(cyclotron_information,contents, filename, date):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
    lines = getting_lines(df)
    all_values = getting_values(lines)
    creating_df(cyclotron_information,all_values)
    try: 
       day = int((df.columns[0]).split()[-1][8:10])
       position = [-1,-1,-1]
       leng = [[0,4],[5,7],[8,10]]
    except: 
       position = [-2,-2,-1]
       leng = [[0,4],[5,7],[0,5]]
    date = get_year_month_day(df,position,leng)
    if int(date[2]) < 10:
        date[2] = "0" + str(date[2])
    #date = [year,month,day]
    filling_cyclotron_information(cyclotron_information,date,df,lines)


    return cyclotron_information