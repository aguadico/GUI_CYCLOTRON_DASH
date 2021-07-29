import os 
import numpy as np
import managing_files_alt
import tfs

def getting_summary_per_file(self):
    target_current = self.file_df.Target_I.astype(float)
    pre_irradiation_len = (len(self.file_df.Target_I[self.file_df['Target_I'].astype(float) == 50.0].astype(float))) + (len(self.file_df.Target_I[self.file_df['Target_I'].astype(float) == 25.0].astype(float))) + (len(self.file_df.Target_I[self.file_df['Target_I'].astype(float) == 0.0].astype(float)))
    pre_irradiation_len_relative = (pre_irradiation_len/len(self.file_df.Target_I.astype(float)))
    print ("PRE_IRRADIATION")
    print (pre_irradiation_len_relative)
    if (pre_irradiation_len_relative) < 0.3:
        managing_files_alt.file_open(self)
        managing_files_alt.file_open_summary(self)
            # GETTING STADISTIC NUMBERS
            # summary voltage 
        
def getting_summary_final(self):
        self.df_rf = self.df_rf.dropna()
        self.df_extraction = self.df_extraction.dropna()
        self.df_source = self.df_source.dropna()
        self.df_vacuum = self.df_vacuum.dropna()
        self.df_magnet = self.df_magnet.dropna()
        self.df_beam = self.df_beam.dropna()

        self.df_rf = self.df_rf.sort_values(by=['FILE'])
        self.df_extraction = self.df_extraction.sort_values(by=['FILE'])
        self.df_source = self.df_source.sort_values(by=['FILE'])
        self.df_vacuum = self.df_vacuum.sort_values(by=['FILE'])
        self.df_magnet = self.df_magnet.sort_values(by=['FILE'])
        self.df_beam = self.df_beam.sort_values(by=['FILE'])
        self.df_transmission = self.df_transmission.sort_values(by=['FILE'])
        self.df_volume = self.df_volume.sort_values(by=['FILE'])

        self.tfs_output_source = os.path.join(self.output_path,"table_summary_source.out")
        self.tfs_output_vacuum = os.path.join(self.output_path,"table_summary_vacuum.out")
        self.tfs_output_magnet = os.path.join(self.output_path,"table_summary_magnet.out")
        self.tfs_output_beam = os.path.join(self.output_path,"table_summary_beam.out")
        self.tfs_output_volume = os.path.join(self.output_path,"table_summary_volume.out")
        self.tfs_output_extraction = os.path.join(self.output_path,"table_summary_extraction.out")
        self.tfs_output_rf = os.path.join(self.output_path,"table_summary_rf.out")
        self.tfs_output_trans = os.path.join(self.output_path,"table_summary_transmission.out")
        self.tfs_output_pressure_fluctuations = os.path.join(self.output_path,"table_summary_pressure_fluctuations.out")
        self.tfs_output_filling_volume = os.path.join(self.output_path,"table_summary_filling_volume.out")

        tfs.write(self.tfs_output_source, self.df_source)
        tfs.write(self.tfs_output_vacuum, self.df_vacuum)
        tfs.write(self.tfs_output_magnet, self.df_magnet)
        tfs.write(self.tfs_output_beam, self.df_beam)
        tfs.write(self.tfs_output_extraction, self.df_extraction)
        tfs.write(self.tfs_output_rf, self.df_rf)
        print ("DF VOLUME")
        print (self.df_volume)
        print (self.df_volume.dropna())
        tfs.write(self.tfs_output_volume, self.df_volume)
        tfs.write(self.tfs_output_trans,self.df_transmission)
