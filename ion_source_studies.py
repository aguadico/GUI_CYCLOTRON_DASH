import getting_subsystems_data_alt 
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from scipy.optimize import curve_fit
import seaborn as sns
import matplotlib.pyplot as plt
def curent(X, a):
     x,y,z = X
     return a*(x+y) 
def current_vaccum(X, a,b):
     x,y,z = X
     return a*(x+y) + b*z

def returning_current(cyclotron_data,funct_fit):	
	data_df = cyclotron_data.file_df
	#VARIABLE TO FIT
	y_value_to_fit = data_df.Arc_I[data_df.Target_I.astype(float) > 0.7*np.max(data_df.Target_I.astype(float))].astype(float)
	#INDEPENDET VARIABLES (VACUUM, TARGET CURRENT AND COLLIMATORS )
	x_value_target = data_df.Target_I[data_df.Target_I.astype(float) > 0.7*np.max(data_df.Target_I.astype(float))].astype(float)
	x_value_vacuum = (data_df.Vacuum_P[data_df.Target_I.astype(float) > 0.7*np.max(data_df.Target_I.astype(float))].astype(float))
	x_value_collimators = data_df.Coll_l_I[data_df.Target_I.astype(float) > 0.7*np.max(data_df.Target_I.astype(float))].astype(float) + data_df.Coll_r_I[data_df.Target_I.astype(float) > 0.7*np.max(data_df.Target_I.astype(float))].astype(float)
	# GETTING FOIL TO COMPUTE THE TRANSMISSION FROM FOIL TO TARGET 
	x_value_foil = data_df.Foil_I[data_df.Target_I.astype(float) > 0.7*np.max(data_df.Target_I.astype(float))].astype(float)
	# GETTING TIME EVOLUTION FOR PLOTTING THE INFORMATION
	#time = data_df.Time[data_df.Target_I.astype(float) > 0.7*np.max(data_df.Target_I.astype(float))]
	#time_dt = pd.to_datetime(time, format='%H:%M:%S')
	# CREATE A DF SUMMARY OF THE PREVIOUS VARIABLES.
	df_summary = pd.DataFrame(list(zip(y_value_to_fit.astype(float),x_value_target.astype(float),x_value_collimators.astype(float),x_value_vacuum.astype(float),x_value_foil.astype(float))),columns=["I_SOURCE","I_TARGET","I_COLLIMATOR","VACUUM","I_FOIL"])
	print ("DF SUMMARY")
	print (data_df)
	print (df_summary)
	# DATAFRAME WITH THE INDEPENDENT VARIABLES
	X = pd.DataFrame(np.c_[df_summary['I_TARGET'].astype(float), df_summary['I_COLLIMATOR'].astype(float),(df_summary['VACUUM'].astype(float)-np.min(df_summary['VACUUM'].astype(float)))*1e5], columns=['I_TARGET','I_COLLIMATOR','VACUUM'])
	# DATAFRAME WITH DEPENDENT VARIABLE, IMPORTANT (HERE THE VACUUM IS RELATIVE TO THE MINIMUN VALUE (WITH BEAM))
	Y = df_summary.I_SOURCE
	#CREATING A SUBSET FOR TRAINNING AND TESTING (FOR LATTER)
	print ("ORIGINAL DATA")
	print (X)
	# CURVE FIT
	if len(X.I_TARGET) > 20:
	   #X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size = 0.2, random_state=9)
	   #print ("DATA")
	   #print (X_train)
	   #print (X_train.I_TARGET)
	   #print ("SIZE")
	   #print (len(X_train.I_TARGET))
	   popt, pcov = curve_fit(funct_fit, (X.I_TARGET,X.I_COLLIMATOR,X.VACUUM),Y)
	   # COMPUTNG THE REAL VALUES FROM FIT
	   # GET PROBE CURRENT AND ISOCHRONISM TO COMPUTE TRANSMISSION
	   probe_current = getattr(data_df,"Probe_I").astype(float)[(data_df.Probe_I.astype(float) > 14) & (data_df.Probe_I.astype(float) < 16)]
	   df_isochronism = getting_subsystems_data_alt.get_isochronism(data_df)
	   T_1 = np.average(np.max(df_isochronism.Foil_I)/probe_current)
	   sigma_T_1 = np.std(np.max(df_isochronism.Foil_I)/probe_current)
	   # transmission 2 (from foil to target) and its associated error
	   T_2 = np.average((df_summary.I_TARGET + df_summary.I_COLLIMATOR)/df_summary.I_FOIL)
	   sigma_T_2 = np.std((df_summary.I_TARGET + df_summary.I_COLLIMATOR)/df_summary.I_FOIL)
	   # COMPUTE SOURCE PERFORMANCE AND ITS ASSOCIATED ERROR
	   a = popt[0]
	   x = a*T_1*T_2
	   sigma_a = (np.diag(pcov)**0.5)[0]
	   sigma_x = ((T_1*T_2*sigma_a)**2+(a*T_2*sigma_T_1)**2+(a*T_1*sigma_T_2))**0.5
	   print ("x")
	   print (x)
	   print (sigma_x)
	   print ("TRANSMISSION")
	   print (T_1)
	else: 
		print ("TOO SHORT")
		a = 0
		sigma_a = 0
		x = 0
		sigma_x = 0
	cyclotron_data.source_performance_total.append(x)
	cyclotron_data.source_performance_total_error.append(sigma_x)
	return x,sigma_x

def plotting():
	f, ax = plt.subplots(figsize =(9, 8))
	sns.heatmap(df_summary.corr(), ax = ax, cmap ="YlGnBu", annot=True, linewidths = 0.1,cbar_kws={"shrink": .5})
	plt.savefig("/Users/anagtv/Documents/OneDrive/046 - Medical Devices/Mantenimientos ciclotrones/TCP/ANALYSIS/PLOTS_2/not_normal_correlation_"+str(int(file_number))+".pdf")
	fig, ax = plt.subplots()
	ax.scatter(X.I_TARGET, Y,label="Measured")
	ax.scatter(X_test.I_TARGET,func_2((X_test.I_TARGET,X_test.I_COLLIMATOR,X_test.VACUUM*1e5),popt[0],popt[1]),label="Estimated")
	plt.legend(loc='best')
	plt.savefig("/Users/anagtv/Documents/OneDrive/046 - Medical Devices/Mantenimientos ciclotrones/TCP/ANALYSIS/PLOTS_2/target_source_evolution_"+str(int(file_number)))
	fig2, ax2 = plt.subplots()
	ax2.scatter(X_test.I_COLLIMATOR,y_test,label="Measured")
	ax2.scatter(X_test.I_COLLIMATOR,func_2((X_test.I_TARGET,X_test.I_COLLIMATOR,X_test.VACUUM*1e5),popt[0],popt[1]),label="Estimated")
	plt.legend(loc='best')
	plt.savefig("/Users/anagtv/Documents/OneDrive/046 - Medical Devices/Mantenimientos ciclotrones/TCP/ANALYSIS/PLOTS_2/collimator_source_evolution_"+str(int(file_number)))
	fig5, ax5 = plt.subplots()
	ax5.scatter(range(len(time_dt)),Y,label="Measured")
	ax5.scatter(range(len(time_dt)),func_2((X.I_TARGET,X.I_COLLIMATOR,X.VACUUM*1e5),popt[0],popt[1]),label="Estimated")
	plt.legend(loc='best')
	plt.savefig("/Users/anagtv/Documents/OneDrive/046 - Medical Devices/Mantenimientos ciclotrones/TCP/ANALYSIS/PLOTS_2/time_source_evolution_"+str(int(file_number)))
	fig3, ax3 = plt.subplots()
	ax3.scatter(X_test.VACUUM,y_test,label="Measured")
	ax3.scatter(X_test.VACUUM,func_2((X_test.I_TARGET,X_test.I_COLLIMATOR,X_test.VACUUM*1e5),popt[0],popt[1]),label="Estimated")
	plt.legend(loc='best')
	plt.savefig("/Users/anagtv/Documents/OneDrive/046 - Medical Devices/Mantenimientos ciclotrones/TCP/ANALYSIS/PLOTS_2/vacuum_source_evolution_"+str(int(file_number)))
