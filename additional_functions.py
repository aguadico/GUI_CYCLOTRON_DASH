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
import cyclotron_class
import tfs
import getting_subsystems_data_alt

RANGE_VALUES_CHARGE = {"TARGET_COLLIMATORS":[[[0,10],[10,12.5],[12.5,15]],[[0,300],[300,500],[500,700]],[[0,300],[300,500],[500,700]]],
"FOILS": [[[0,2000],[2000,2500],[2500,3000]]] * 6,
"SOURCE_TARGETS":[[[0,100],[100,125],[125,150]],[[0,10],[10,12.5],[12.5,15]],[[0,10],[10,12.5],[12.5,15]]]}
POSITION = {"TARGET_COLLIMATORS":[[0.7, 0.9],[0.4, 0.6],[0.08, 0.25]],"SOURCE_TARGETS":[[0.7, 0.9],[0.4, 0.6],[0.08, 0.25]],
"FOILS":[[0.8,0.9],[0.64,0.74],[0.48,0.58],[0.32, 0.42],[0.16, 0.26],[0.0, 0.1]]}

def general_status_plot(fig_status,values_to_plot,range_values,y_position,text_to_plot):
    for i in range(len(values_to_plot)):
        fig_status.add_trace(go.Indicator(
    mode = "number+gauge", value = values_to_plot[i][0],
    domain = {'x': [0.25, 1], 'y': y_position[i]},
    title = {'text' :text_to_plot[i]},
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

def return_fig(fig_status,text_to_plot,values_to_plot,range_values,range_element):
    y_position = POSITION[range_element]    
    fig_status = general_status_plot(fig_status,values_to_plot,range_values,y_position,text_to_plot)
    fig_status.update_layout(paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='#FFFFFF',font=dict(size=16,color="#223A38"),font_family="Arial",margin=dict(t=35))  
    return fig_status

def plotting_charge(cyclotron_information,text_to_plot,values_to_plot,top_text,range_element):
    range_values = RANGE_VALUES_CHARGE[range_element]
    fig_status = go.Figure()
    fig_status = return_fig(fig_status,text_to_plot,values_to_plot,range_values,range_element)
    fig_status.update_layout(title=top_text  ,
    font=dict(size=16,color="#223A38"),font_family="Arial",margin=dict(t=60)) 
    return fig_status

def plotting_simple_name(fig,x_values,y_values,y_values_error,units,position_x,position_y,colori,markersi,namei,reference_value,ticker_layer):
    fig.add_trace(go.Scatter(x=x_values, y=y_values,name=namei,mode='markers',                                                         
    marker=go.Marker(dict(size=12,color=colori,line=dict(width=2,color=markersi))),
        error_y=dict(
            type='data',
            symmetric=True,
            array=y_values_error
            )),row=position_x, col=position_y)
    print ("TICKER LAYER")
    print (ticker_layer)
    if ticker_layer == ["ADRF"]:
        for i in range(len(reference_value)):
             if len(reference_value[i]) > 0:
                fig.add_hrect(y0=reference_value[i][1], y1=reference_value[i][2], line_width=0, fillcolor="red", opacity=0.05,row=position_x, col=position_y)
                fig.add_hrect(y0=reference_value[i][0], y1=reference_value[i][1], line_width=0, fillcolor="orange", opacity=0.05,row=position_x, col=position_y)
                fig.add_hline(y=reference_value[i][1], line_dash="dot",line_color="red",annotation_text="High risk area",
                     annotation_position="bottom right",row=position_x, col=position_y)
                fig.add_hline(y=reference_value[i][0], line_dash="dot",line_color="orange",annotation_text="Medium risk area",
                     annotation_position="bottom right",row=position_x, col=position_y)

    #fig.add_hline(y=reference_value, line_dash="dot",line_color="green",
    #          annotation_text="Reference value", 
    #          annotation_position="bottom right",row=position_x, col=position_y)
    #fig.add_hline(y=np.average(y_values), line_dash="dot",line_color="blue",
    #          annotation_text="Average", 
    #          annotation_position="bottom right",row=position_x, col=position_y)
    fig.update_yaxes(title_text=units,row=position_x, col=position_y)
    return fig

def plotting_simple_no_error(fig,x_values,y_values,units,position_x,position_y,colori,namei,sizei):
    fig.add_trace(go.Scatter(x=x_values, y=y_values,mode='markers',name=namei,                                                        
    marker=go.Marker(dict(size=sizei,color=colori))),row=position_x, col=position_y)
    fig.update_yaxes(title_text=units, row=position_x, col=position_y)
    return fig


def getting_information(cyclotron_information,target_1,target_2,list_of_contents, list_of_names, list_of_dates):
    #fig_volume.update_layout(paper_bgcolor='rgba(0,0,0,0)',
    #        plot_bgcolor='#F3F6F6',font=dict(size=18,color="#223A38")) 
    #fig_volume.update_layout(title="Individual log " + str(cyclotron_information.file_number) + " Date " + str(cyclotron_information.date_stamp))
    for c, n, d in zip(list_of_contents, list_of_names, list_of_dates): 
        #all_names.append(str(n[:-4]))
        parse_contents(cyclotron_information,c, n, d) 
        target_current = cyclotron_information.file_df.Target_I.astype(float)
        pre_irradiation_len = (len(cyclotron_information.file_df.Target_I[cyclotron_information.file_df['Target_I'].astype(float) == 50.0].astype(float))) + (len(cyclotron_information.file_df.Target_I[cyclotron_information.file_df['Target_I'].astype(float) == 25.0].astype(float))) + (len(cyclotron_information.file_df.Target_I[cyclotron_information.file_df['Target_I'].astype(float) == 0.0].astype(float)))
        pre_irradiation_len_relative = (pre_irradiation_len/len(cyclotron_information.file_df.Target_I.astype(float)))
        max_current = np.max(cyclotron_information.file_df.Target_I.astype(float))    
        #if ((pre_irradiation_len_relative) < 0.3 and float(max_current) > 15):
        if (float(max_current) > 15):
            print ("MAX CURRENT")
            print (cyclotron_information.file_df.Target_I[cyclotron_information.file_df.Target_I.astype(float)> 20])
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
    tfs.write("target_1_charge.out",target_1.df_information)
    tfs.write("target_2_charge.out",target_2.df_information)
    cyclotron_information.source_performance = np.average(np.array(cyclotron_information.source_performance_total)[np.array(cyclotron_information.source_performance_total) > 0])         
    df_target_1 = target_1.df_information_foil
    df_target_2 = target_2.df_information_foil
    cyclotron_information.get_average_std_summary_cummulative(df_target_1,df_target_2)
    cyclotron_information.physical_targets = [np.min(cyclotron_information.df_extraction.PHYSICAL_TARGET),np.max(cyclotron_information.df_extraction.PHYSICAL_TARGET)]


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
    cyclotron_information.file_df["Collimators"] = cyclotron_information.file_df.Coll_l_I.astype(float)+cyclotron_information.file_df.Coll_r_I.astype(float)
    cyclotron_information.file_df["Losses"] = (1-(cyclotron_information.file_df.Target_I.astype(float)+cyclotron_information.file_df.Coll_l_I.astype(float)+cyclotron_information.file_df.Coll_r_I.astype(float))/cyclotron_information.file_df.Foil_I.astype(float))*100
    cyclotron_information.file_df["Relative_target"] = cyclotron_information.file_df.Target_I.astype(float)/cyclotron_information.file_df.Foil_I.astype(float)
    cyclotron_information.file_df["Vacuum_mbar"] = cyclotron_information.file_df.Vacuum_P.astype(float)*1e5
    cyclotron_information.df_isochronism = getting_subsystems_data_alt.get_isochronism(cyclotron_information.file_df)
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