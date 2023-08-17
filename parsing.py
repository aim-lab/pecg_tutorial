import numpy as np
import pandas as pd
import wfdb
import ast

class PTBParser:

    def __init__(self, DB_path=None, physionet_db_dir=None):
        if DB_path is None:
            DB_path = './data/'
        self.DB_path = DB_path
        self.table = pd.read_csv(DB_path + 'ptbxl_database.csv')
        self.fs = 500 #Hz; parser is set to use the high resolution recordings
        
        # For downloading:
        if physionet_db_dir is None:
            self.physionet_db_dir = 'ptb-xl'
    
    def get_wfdb_path(self, index):
        # Get the wfdb path as given in the database table:
        wfdb_path = self.DB_path + self.table['filename_hr'][int(index)]  # hr = high resolution folder files
        return wfdb_path
    
    def get_label(self, index):
        # A method to decide the label:
        prob_dict = ast.literal_eval(self.table['scp_codes'][int(index)])
        keys = list(prob_dict.keys())
        values = list(prob_dict.values())
        if 'SR' in keys:
            return 0
        elif 'AFIB' in keys:
            return 1
        else:
            return -1
            
    def __getitem__(self, index):
        record = wfdb.rdrecord(self.get_wfdb_path(index))
        signal = record.p_signal
        label = self.get_label(index)
        return signal, label

    def __len__(self):
        return len(self.table)  # database size
    
    def download_recordings(self, indices):
        records = []
        for index in indices:
            records.append(self.table['filename_hr'][int(index)])
        wfdb.dl_database(self.physionet_db_dir, self.DB_path, records)