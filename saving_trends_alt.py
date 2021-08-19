import os 
import numpy as np
import managing_files_alt
import tfs

def getting_summary_per_file(self):
    managing_files_alt.file_open(self)
    managing_files_alt.file_open_summary(self)
 
        
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
        self.df_filling_volume = self.df_filling_volume.sort_values(by=['FILE'])
        print ("FILLING VOLUME")
        print (self.df_filling_volume)

