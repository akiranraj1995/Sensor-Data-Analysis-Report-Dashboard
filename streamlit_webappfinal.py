#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 22:43:35 2023

@author: expert
"""

import streamlit as st
import pandas as pd
import os
import time

def run_app():
    st.header("Sensor Data Analysis Report Dashboard")

    # Define input folder
    input_folder = 'streaming_data'
    
    # Create empty containers to display results
    containers = {
        'Total Number of Records': [st.subheader("1. Total Number of Records"), st.empty()],
        'Sensor ID and Its Count': [st.subheader("2. Sensor ID and Its Count"), st.empty()],
        'Summary Statistics of Sensor ID': [st.subheader("3. Summary Statistics of Sensor ID"), st.empty()]
    }
    
    while True:
        # Check for CSV files in input folder
        csv_files = [f for f in os.listdir(input_folder) if f.endswith('.csv')]
        if csv_files:
            # If CSV files are found, concatenate them into a single dataframe and display number of records
            dfs = [pd.read_csv(os.path.join(input_folder, f)) for f in csv_files]
            df = pd.concat(dfs)
            num_records = df.shape[0]
            containers['Total Number of Records'][1].write(f"Total number of records: **{num_records}**")
            
            # Display unique Sensor IDs and their counts
            sensor_counts = df['Sensor ID'].value_counts()
            sensor_counts_df = pd.DataFrame({'Sensor ID': sensor_counts.index, 'Count': sensor_counts.values})
            containers['Sensor ID and Its Count'][1].write(sensor_counts_df)
            
            # Calculate summary statistics of sensor IDs
            sensor_stats = df.groupby('Sensor ID')['Time Difference (s)'].agg(['mean', 'max', 'min']).reset_index()
            sensor_stats.rename(columns={'mean': 'Mean Interval', 'max': 'Maximum Interval', 'min': 'Minimum Interval'}, inplace=True)
            sensor_stats['Maximum Interval'] = sensor_stats['Maximum Interval'].fillna(0).astype(int)
            sensor_stats['Minimum Interval'] = sensor_stats['Minimum Interval'].fillna(0).astype(int)
            sensor_stats['Mean Interval'] = sensor_stats['Mean Interval'].apply(lambda x: '{:.2f}'.format(x))
            containers['Summary Statistics of Sensor ID'][1].write(sensor_stats)
            
        else:
            # If no CSV files are found, display a message
            containers['Total Number of Records'][1].write(f"No CSV files found in folder: {input_folder}")
            containers['Sensor ID and Its Count'][1].empty()
            containers['Summary Statistics of Sensor ID'][1].empty()
        
        # Sleep for 1 second before checking for new CSV files again
        time.sleep(1)

if __name__ == '__main__':
    run_app()
